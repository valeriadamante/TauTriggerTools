import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()
import pymc3 as pm
from gp_monotonic import gp_monotonic

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

class FitResults:
    def __init__(self, eff, x_pred):
        N = eff.x.shape[0]
        eff = copy.deepcopy(eff)
        new_y = np.cumsum(res.x)
        delta = eff.y - new_y
        eff.y_error_low = np.sqrt(eff.y_error_low ** 2 + delta ** 2)
        eff.y_error_high = np.sqrt(eff.y_error_high ** 2 + delta ** 2)
        eff.y = new_y
        yerr = np.maximum(eff.y_error_low, eff.y_error_high)
        with pm.Model() as gp_model:
            l_ = pm.HalfCauchy('l_',20)
            eta_ = pm.HalfCauchy('eta_',1)
            s_n = pm.HalfNormal('s_n',1)
            kernel = (eta_**2)*pm.gp.cov.Matern32(1,l_)
            gp_default = pm.gp.Marginal(cov_func=kernel)
            gp_default.marginal_likelihood('lik',data_x.reshape(-1,1),data_y,noise=s_n)
            trace = pm.sample(2000,tune=2000,cores=2)
        map_estimate = pm.find_MAP(model=gp_model)
        gp_mon = gp_monotonic(gp_model,gp_default,yerr,map_estimate,eff.x,eff.y)
        self.y_pred,y_cov = gp_mon.predict(x_pred,return_cov=True)
        sigma_orig = np.zeros(N)
        for n in range(N):
            idx = np.argmin(abs(x_pred - eff.x[n]))
            sigma_orig[n] = y_cov[idx]
