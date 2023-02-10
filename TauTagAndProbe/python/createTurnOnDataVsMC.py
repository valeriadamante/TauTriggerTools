#!/usr/bin/env python3

import ROOT
import argparse
import sys
import re
import numpy as np
from array import array
#import py_plot as plt
import math
import os


parser = argparse.ArgumentParser(description='Create turnon curves.')
parser.add_argument('--input_data', required=True, type=str,nargs='+', help="the input")
parser.add_argument('--input_mc', required=True, type=str,nargs='+', help="the input")
parser.add_argument('--channel', required=True, type=str, help="all,ditau,mutau")
parser.add_argument('--selection', required=True, type=str, help="Tau selection")
parser.add_argument('--output', required=True, type=str, help="output file")
parser.add_argument('--vars', required=True, type=str, help="variable to draw")
parser.add_argument('--pu', required=True, type=str, help="variable to draw")

args = parser.parse_args()

path_prefix = '' if 'TauTriggerTools' in os.getcwd() else 'TauTriggerTools/'
sys.path.insert(0, path_prefix + 'Common/python')

from AnalysisTypes import *
from AnalysisTools import *
import RootPlotting
import TriggerConfig
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()
ROOT.gInterpreter.Declare('#include "{}TauTagAndProbe/interface/PyInterface.h"'.format(path_prefix))
RootPlotting.ApplyDefaultGlobalStyle()


def CreateBins(var_name):
    if var_name in [ 'tau_pt' ]:
        bins = np.arange(20, 40, step=4)
        #bins = np.append(bins, np.arange(40, 120, step=4))
        high_pt_bins = [ 40,50, 70, 150]
        bins = np.append(bins,high_pt_bins)
        return bins,False,False
    elif var_name in [ 'jet_pt']:
        bins = np.arange(20, 70, step=4)
        #bins = np.append(bins, np.arange(40, 120, step=4))
        high_pt_bins = [ 70,80,100,120, 150]
        bins = np.append(bins,high_pt_bins)
        return bins,False,False
    elif var_name in [ 'tau_eta', 'tau_gen_vis_eta' ]:
        return np.linspace(-2.3, 2.3, 7), False, False
    elif var_name in [ 'npu', 'npv' ]:
        return np.linspace(20, 70, 5), False, False
    raise RuntimeError("Can't find binning for \"{}\"".format(var_name))

def CreateDataHistograms(input_file, selection_id, hlt_paths, var, hist_model, output_file,ch):
    df = ROOT.RDataFrame('events',input_file)
    eta_th = {"ditau":35,"mutau":30,"etau":30}
    
    if ch == "VBFditau_lo":
        df = df.Filter('(tau_sel & {}) != 0  && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 5 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    elif ch == "etau":
        df = df.Filter('(tau_sel & {}) != 0  && l1Tau_pt >= 26 && l1Tau_hwIso > 0 && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 20 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
   
    else:
        df = df.Filter('(tau_sel & {}) != 0  && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 20 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    
    if var == 'tau_eta' or var == 'npv':
        df = df.Filter('tau_pt > {}'.format(eta_th[ch]))
    # elif var == 'npu':
    #     df = df.Filter('tau_pt > 0')
    # else:
    #     return 0

    df = df.Filter('(byDeepTau2017v2p1VSmu & (1 << 5)) != 0 && (byDeepTau2017v2p1VSjet & (1 << 4)) != 0')
    
    match_mask = 0
    for path_name, path_index in hlt_paths.items():
        match_mask = match_mask | (1 << path_index)

    hist_total = df.Histo1D(hist_model,var)
    hist_pass  = df.Filter('(hlt_acceptAndMatch & {}) != 0'.format(match_mask)) \
                    .Histo1D(hist_model, var)
    # if "Fcopy" in input_file:
    #     hist_pass  = df.Filter('(hlt_acceptAndMatch & {}) != 0 && l1Tau_pt >= 34'.format(match_mask)) \
    #                 .Histo1D(hist_model, var)
    eff = ROOT.TEfficiency(hist_pass.GetPtr(), hist_total.GetPtr())
    print(hist_total.GetPtr().GetEntries())
    return hist_pass,hist_total,eff
        
def CreateMCHistograms(input_file, selection_id, hlt_paths, var, hist_model, output_file,ch,pu):
    
    
    eta_th = {"ditau":35,"mutau":35,"etau":35}
    
    df = ROOT.RDataFrame('events',input_file)
    if ch == "VBFditau_lo":
        df = df.Filter('(tau_sel & {}) != 0  && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 5 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    elif ch == "etau":
        df = df.Filter('(tau_sel & {}) != 0  && l1Tau_pt >= 26 && l1Tau_hwIso > 0 && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 20 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
   
    else:
        df = df.Filter('(tau_sel & {}) != 0  && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 20 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    
    if var == 'tau_eta':
        df = df.Filter('tau_pt > {}'.format(eta_th[ch]))
    
    df = df.Filter('(byDeepTau2017v2p1VSmu & (1 << 5)) != 0 && (byDeepTau2017v2p1VSjet & (1 << 4)) != 0')
    df = df.Filter('tau_charge + muon_charge == 0 && tau_gen_match == 5')
    df = df.Define('weight', "PileUpWeightProvider::GetDefault().GetWeight(npu) * genEventWeight")
    match_mask = 0
    for path_name, path_index in hlt_paths.items():
        match_mask = match_mask | (1 << path_index)
        
    
    hist_total = df.Histo1D(hist_model,var,"weight")
    hist_pass  = df.Filter('(hlt_acceptAndMatch & {}) != 0'.format(match_mask)) \
                    .Histo1D(hist_model, var,"weight")
    # if "Fcopy" in input_file:
    #     hist_pass  = df.Filter('(hlt_acceptAndMatch & {}) != 0 && l1Tau_pt >= 34'.format(match_mask)) \
    #                 .Histo1D(hist_model, var)
    eff = ROOT.TEfficiency(hist_pass.GetPtr(), hist_total.GetPtr())
    print(hist_total.GetPtr().GetEntries())
    return hist_pass,hist_total,eff



trigger_pattern = {"ditau":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v","mutau":"HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1","etau":"HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1","ditaujet":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1_v","VBFditau_hi":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_L2NN_eta2p1_CrossL1_v","VBFditau_lo":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1_v"}
selection_id = ParseEnum(TauSelection, args.selection)
print('Tau selection: {}'.format(selection_id))

n_d_inputs = len(args.input_data)
n_m_inputs = len(args.input_mc) 

n_inputs = n_d_inputs + n_m_inputs
var = args.vars

if args.channel == 'all':
    pass
else:
    trigger_dict = [None] * n_inputs
    hlt_paths = [None] * n_inputs
    for input_id in range(n_d_inputs):
        trigger_dict[input_id] = TriggerConfig.LoadTriggerDictionary(args.input_data[input_id])
        hlt_paths[input_id] = TriggerConfig.GetMatchedTriggers(trigger_dict[input_id][0],trigger_pattern[args.channel])
        #ReportHLTPaths(hlt_paths[input_id], labels[input_id])



    for input_id in range(n_d_inputs,n_inputs):
        print(input_id)
        trigger_dict[input_id] = TriggerConfig.LoadTriggerDictionary(args.input_mc[input_id-n_d_inputs])
        hlt_paths[input_id] = TriggerConfig.GetMatchedTriggers(trigger_dict[input_id][0],trigger_pattern[args.channel])

    output_file = ROOT.TFile(args.output + '.root', 'RECREATE')


    bins, x_scales, divide_by_bw = CreateBins(var)
    hist_models = ROOT.RDF.TH1DModel(var, var, len(bins) - 1, array('d', bins))


    hist_passed = [None] * n_inputs
    hist_total = [None] * n_inputs
    eff = [None] * n_inputs

    for input_id in range(n_d_inputs):
        hist_passed[input_id], hist_total[input_id], eff[input_id] = CreateDataHistograms(args.input_data[input_id], selection_id, hlt_paths[input_id],var, hist_models,output_file,args.channel)


    for input_id in range(n_d_inputs,n_m_inputs+n_d_inputs):
        data_pu_file = ROOT.TFile(args.pu, 'READ')
        data_pu = data_pu_file.Get('pileup')
        df_all = ROOT.RDataFrame('all_events',args.input_mc[input_id-n_d_inputs])
        mc_pu = df_all.Histo1D(ROOT.RDF.TH1DModel(data_pu), 'npu')
        ROOT.PileUpWeightProvider.Initialize(data_pu, mc_pu.GetPtr())
        if args.vars == 'npv':
            hist_passed[input_id], hist_total[input_id], eff[input_id] = CreateMCHistograms(args.input_mc[input_id-n_d_inputs], selection_id, hlt_paths[input_id],'npu', hist_models,output_file,args.channel,args.pu)
        else:
            hist_passed[input_id], hist_total[input_id], eff[input_id] = CreateMCHistograms(args.input_mc[input_id-n_d_inputs], selection_id, hlt_paths[input_id],var, hist_models,output_file,args.channel,args.pu)
    
   

 



    ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)
    c.SetTickx();c.SetTicky();c.SetGridx();c.SetGridy()
    label = ROOT.TLatex(); label.SetNDC(True)
    # use multiplotter for multiple graphs
    mg = ROOT.TMultiGraph("mg", "")
    # legend
    leg = ROOT.TLegend(0.56015,0.331852,0.865915,0.565926)
    leg.SetTextSize(0.025)


    graphs = {}
    icolor = 2
    imaker = 24
    legnames = ["Data","MC"]#["355862_357900","359022_360331","360390_362104","362433_362760","Simulation"]
    for input_id in range(n_m_inputs+n_d_inputs):
        graphs[input_id] =  ROOT.TGraphAsymmErrors(hist_passed[input_id].GetPtr(),hist_total[input_id].GetPtr(), "n")
        graphs[input_id].SetLineColor(icolor)
        graphs[input_id].SetMarkerStyle(imaker)
        graphs[input_id].SetLineWidth(3)
        graphs[input_id].SetMarkerSize(1.5)
        icolor = icolor + 1
        imaker = imaker + 1
        legname = legnames[input_id]
        leg.AddEntry(graphs[input_id],legname)
        print('Drawing {}'.format(legname))
        mg.Add(graphs[input_id])

    mg.GetYaxis().SetRangeUser(0,1)
    mg.GetYaxis().SetNdivisions(5)
    mg.Draw("AP")
    if(args.vars == "tau_pt"):
        label.DrawLatex(0.8, 0.03, "#tau_{pT}")
    elif(args.vars== "npu" or args.vars == "npv"):
        label.DrawLatex(0.8, 0.03, "No. Vertices")
    else:
        label.DrawLatex(0.8, 0.03, "#eta_{#tau}")
    label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS Run3 Data}")
    label.SetTextSize(0.030); label.DrawLatex(0.697995, 0.918519, "#sqrt{s} = 13.6 TeV, 41 fb^{-1}")



    if args.vars == "tau_eta" or args.vars == 'npv':
        label.DrawLatex(0.33, 0.218, "Medium tauID, #tau_{pT} > 30 GeV")
    else:
        label.DrawLatex(0.33, 0.318, "Medium tauID")
    leg.Draw()


    plot_name = args.output+'_'+args.channel+'_'+args.vars+'.pdf'
    cfg_name  = args.output+'_'+args.channel+'_'+args.vars+'.C'
    c.SaveAs('./{}'.format(plot_name))
    c.SaveAs('./{}'.format(cfg_name))

    print('TurnOn is created')
    
