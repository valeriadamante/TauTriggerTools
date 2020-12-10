import argparse
import os
import sys
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy
import copy
from scipy import interpolate

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()
import numpy as np
from gp_monotonic2 import gp_monotonic
from sklearn.gaussian_process import GaussianProcessRegressor,GaussianProcessClassifier
from sklearn.gaussian_process.kernels import Matern, ConstantKernel,RBF

path_prefix = '' if 'TauTriggerTools' in os.getcwd() else 'TauTriggerTools/'
sys.path.insert(0, path_prefix + 'Common/python')
from RootObjects import Histogram, Graph

parser = argparse.ArgumentParser(description='Fit turn-on curves.')
parser.add_argument('--input', required=True, type=str, help="ROOT file with turn-on curves")
parser.add_argument('--output', required=True, type=str, help="output file prefix")
parser.add_argument('--channels', required=False, type=str, default='etau,mutau,ditau', help="channels to process")
parser.add_argument('--decay-modes', required=False, type=str, default='all,0,1,10,11', help="decay modes to process")
parser.add_argument('--working-points', required=False, type=str,
                    default='VVVLoose,VVLoose,VLoose,Loose,Medium,Tight,VTight,VVTight',
                    help="working points to process")
args = parser.parse_args()

def add_fakepoint(eff,pos):
    eff_x = np.insert(eff.x,len(eff.x),pos)
    eff_y = np.insert(eff.y,len(eff.y),eff.y[-1])
    y_err = np.maximum(eff.y_error_low, eff.y_error_high)
    y_err = np.insert(y_err,len(y_err),y_err[-1])
    return eff_x,eff_y,y_err

def MinTarget(dy, eff):
    y = np.cumsum(dy)
    return np.sum(((eff.y - y) / (eff.y_error_high + eff.y_error_low)) ** 2)
class FitResults:
    def __init__(self, eff, x_pred):
        N = eff.x.shape[0]
        res = scipy.optimize.minimize(MinTarget, np.zeros(N), args=(eff,), bounds = [ [0, 1] ] * N,
                                      options={"maxfun": int(1e6)})
        if not res.success:
            print(res)
            raise RuntimeError("Unable to prefit")

            
        eff = copy.deepcopy(eff)
        new_y = np.cumsum(res.x)
        delta = eff.y - new_y
        eff.y_error_low = np.sqrt(eff.y_error_low ** 2 + delta ** 2)
        eff.y_error_high = np.sqrt(eff.y_error_high ** 2 + delta ** 2)
        #eff.y = new_y
        yerr = np.maximum(eff.y_error_low, eff.y_error_high)
        kernel_default = Matern(length_scale=10.0, length_scale_bounds=(10, 100.0), nu=1)
        eff.x,eff.y,yerr = add_fakepoint(eff,200)
        gp_default = GaussianProcessRegressor(kernel=kernel_default,alpha = yerr**2, n_restarts_optimizer=10)
        gp_default.fit(np.atleast_2d(eff.x).T,eff.y)
        gp_mon = gp_monotonic(gp_default,yerr,eff.x,eff.y)
        self.y_pred,y_cov = gp_mon.predict(x_pred,return_cov=True)
        self.sigma_pred = np.diag(y_cov)
        
channels = args.channels.split(',')
decay_modes = args.decay_modes.split(',')
working_points = args.working_points.split(',')
ch_validity_thrs = { 'etau': 35, 'mutau': 32, 'ditau': 40 }
file = ROOT.TFile(args.input, 'READ')
output_file = ROOT.TFile('{}.root'.format(args.output), 'RECREATE', '', ROOT.RCompressionSetting.EDefaults.kUseSmallest)

for channel in channels:
    with PdfPages('{}_{}.pdf'.format(args.output, channel)) as pdf:
        for wp in working_points:
            for dm in decay_modes:
                print('Processing {} {} WP DM = {}'.format(channel, wp, dm))
                dm_label = '_dm{}'.format(dm) if dm != 'all' else ''
                name_pattern = '{{}}_{}_{}{}_fit_eff'.format(channel, wp, dm_label)
                dm_label = '_dm'+ dm if len(dm) > 0 else ''
                eff_data_root = file.Get(name_pattern.format('data'))
                eff_mc_root = file.Get(name_pattern.format('mc'))
                eff_data = Graph(root_graph=eff_data_root)
                eff_mc = Graph(root_graph=eff_mc_root)
                pred_step = 0.1
                #x_low = min(eff_data.x[0] - eff_data.x_error_low[0], eff_mc.x[0] - eff_mc.x_error_low[0])
                #x_high = max(eff_data.x[-1] + eff_data.x_error_high[-1], eff_mc.x[-1] + eff_mc.x_error_high[-1])
                x_low, x_high = 20, 1000
                x_pred = np.arange(x_low, x_high + pred_step / 2, pred_step)

                eff_data_fitted = FitResults(eff_data, x_pred)
                eff_mc_fitted = FitResults(eff_mc, x_pred)

                sf = eff_data_fitted.y_pred / eff_mc_fitted.y_pred
                sf_sigma = np.sqrt( (eff_data_fitted.sigma_pred / eff_mc_fitted.y_pred) ** 2 \
                         + (eff_data_fitted.y_pred / (eff_mc_fitted.y_pred ** 2) * eff_mc_fitted.sigma_pred ) ** 2 )

                fig, (ax, ax_ratio) = plt.subplots(2, 1, figsize=(7, 7), sharex=True,
                                                           gridspec_kw = {'height_ratios':[2, 1]})
                mc_color = 'g'
                data_color = 'k'
                trans = 0.3

                plt_data = ax.errorbar(eff_data.x, eff_data.y, xerr=(eff_data.x_error_low, eff_data.x_error_high),
                                       yerr=(eff_data.y_error_low, eff_data.y_error_high), fmt=data_color+'.',
                                       markersize=5)
                plt_mc = ax.errorbar(eff_mc.x, eff_mc.y, xerr=(eff_mc.x_error_low, eff_mc.x_error_high),
                                     yerr=(eff_mc.y_error_low, eff_mc.y_error_high), fmt=mc_color+'.', markersize=5)

                plt_data_fitted = ax.plot(x_pred, eff_data_fitted.y_pred, data_color+'--')
                ax.fill(np.concatenate([x_pred, x_pred[::-1]]),
                        np.concatenate([eff_data_fitted.y_pred - eff_data_fitted.sigma_pred,
                                       (eff_data_fitted.y_pred + eff_data_fitted.sigma_pred)[::-1]]),
                        alpha=trans, fc=data_color, ec='None')

                plt_mc_fitted = ax.plot(x_pred, eff_mc_fitted.y_pred, mc_color+'--')
                ax.fill(np.concatenate([x_pred, x_pred[::-1]]),
                        np.concatenate([eff_mc_fitted.y_pred - eff_mc_fitted.sigma_pred,
                                       (eff_mc_fitted.y_pred + eff_mc_fitted.sigma_pred)[::-1]]),
                        alpha=trans, fc=mc_color, ec='None')

                ax_ratio.plot(x_pred, sf, 'b--')
                ax_ratio.fill(np.concatenate([x_pred, x_pred[::-1]]),
                              np.concatenate([sf - sf_sigma, (sf + sf_sigma)[::-1]]),
                              alpha=trans, fc='b', ec='None')

                title = "Turn-ons for {} trigger with {} DeepTau VSjet".format(channel, wp)
                if dm != 'all':
                    title += " for DM={}".format(dm)
                else:
                    title += " for all DMs"
                ax.set_title(title, fontsize=16)
                ax.set_ylabel("Efficiency", fontsize=12)
                ax.set_ylim([ 0., 1.1 ])
                ax.set_xlim([ 20, min(200, plt.xlim()[1]) ])

                ax_ratio.set_xlabel("$p_T$ (GeV)", fontsize=12)
                ax_ratio.set_ylabel("Data/MC SF", fontsize=12)
                ax_ratio.set_ylim([0.5, 1.49])

                validity_plt = ax.plot( [ ch_validity_thrs[channel] ] * 2, ax.get_ylim(), 'r--' )
                ax_ratio.plot( [ ch_validity_thrs[channel] ] * 2, ax_ratio.get_ylim(), 'r--' )

                ax.legend([ plt_data, plt_mc, plt_data_fitted[0], plt_mc_fitted[0], validity_plt[0] ],
                          [ "Data", "MC", "Data fitted", "MC fitted", "Validity range"], fontsize=12, loc='lower right')


                plt.subplots_adjust(hspace=0)
                pdf.savefig(bbox_inches='tight')
                plt.close()

                out_name_pattern = '{{}}_{}_{}{}_{{}}'.format(channel, wp, dm_label)
                output_file.WriteTObject(eff_data_root, out_name_pattern.format('data', 'eff'), 'Overwrite')
                output_file.WriteTObject(eff_mc_root, out_name_pattern.format('mc', 'eff'), 'Overwrite')
                eff_data_fitted_hist = Histogram.CreateTH1(eff_data_fitted.y_pred, [x_low, x_high],
                                                           eff_data_fitted.sigma_pred, fixed_step=True)
                eff_mc_fitted_hist = Histogram.CreateTH1(eff_mc_fitted.y_pred, [x_low, x_high],
                                                         eff_mc_fitted.sigma_pred, fixed_step=True)
                sf_fitted_hist = eff_data_fitted_hist.Clone()
                sf_fitted_hist.Divide(eff_mc_fitted_hist)
                output_file.WriteTObject(eff_data_fitted_hist, out_name_pattern.format('data', 'fitted'), 'Overwrite')
                output_file.WriteTObject(eff_mc_fitted_hist, out_name_pattern.format('mc', 'fitted'), 'Overwrite')
                output_file.WriteTObject(sf_fitted_hist, out_name_pattern.format('sf', 'fitted'), 'Overwrite')

output_file.Close()
print('All done.')

        
        
