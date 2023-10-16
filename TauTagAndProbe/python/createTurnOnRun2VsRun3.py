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
from tdrstyle import *

parser = argparse.ArgumentParser(description='Create turnon curves.')
parser.add_argument('--input', required=True, type=str, nargs='+', help="the input")
parser.add_argument('--channel', required=True, type=str, help="all,ditau,mutau")
parser.add_argument('--selection', required=True, type=str, help="Tau selection")
parser.add_argument('--output', required=True, type=str, help="output file")
parser.add_argument('--vars', required=True, type=str, help="variable to draw")

args = parser.parse_args()


sys.path.insert(0, 'Common/python')
from AnalysisTypes import *
from AnalysisTools import *
import RootPlotting
import TriggerConfig
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()
RootPlotting.ApplyDefaultGlobalStyle()

# ccp_methods = '''
# int FindBestMatchedHLTObject(float tau_eta, float tau_phi, ULong64_t match_mask, float deltaRThr,
#                              const ROOT::VecOps::RVec<float>& hltObj_eta, const ROOT::VecOps::RVec<float>& hltObj_phi,
#                              const ROOT::VecOps::RVec<ULong64_t>& hltObj_hasPathName,
#                              const ROOT::VecOps::RVec<ULong64_t>& hltObj_hasFilters_2)
# {
#     int best_match_index = -1;
#     float best_deltaR2 = std::pow(deltaRThr, 2);
#     for(size_t n = 0; n < hltObj_eta.size(); ++n) {
#         //if((match_mask & hltObj_hasPathName.at(n) & hltObj_hasFilters_2.at(n)) == 0) continue;
#         if((match_mask & hltObj_hasPathName.at(n)) == 0) continue;
#         const float deta = tau_eta - hltObj_eta.at(n);
#         const float dphi = ROOT::Math::VectorUtil::Phi_mpi_pi(tau_phi - hltObj_phi.at(n));
#         const float deltaR2 = std::pow(deta, 2) + std::pow(dphi, 2);
#         if(deltaR2 >= best_deltaR2) continue;
#         best_match_index = static_cast<int>(n);
#         best_deltaR2 = deltaR2;
#     }
#     return best_match_index;
# }
# '''
# ROOT.gInterpreter.Declare(ccp_methods)

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
        return np.linspace(0, 80, 20), False, False
    raise RuntimeError("Can't find binning for \"{}\"".format(var_name))

def CreateHistograms(input_file, selection_id, hlt_paths, var, hist_model, output_file,ch):
    df = ROOT.RDataFrame('events',input_file)
    if ch == "VBFditau_lo":
        df = df.Filter('(tau_sel & {}) != 0  && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 5 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    elif ch == "etau":
        df = df.Filter('(tau_sel & {}) != 0  && l1Tau_pt >= 26 && l1Tau_hwIso > 0 && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 20 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    # elif ch == "ditau":
    #     df = df.Filter('(tau_sel & {}) != 0  && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 20 && l1Tau_pt > 32 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    else:
        df = df.Filter('(tau_sel & {}) != 0  && muon_pt > 27 && muon_iso < 0.1 && muon_mt < 30 && tau_decayMode != 5 && tau_decayMode != 6 && abs(tau_eta) < 2.3 && tau_pt > 20 && vis_mass > 40 && vis_mass < 80'.format(selection_id))
    
    df = df.Filter('(byDeepTau2017v2p1VSmu & (1 << 5)) != 0 && (byDeepTau2017v2p1VSjet & (1 << 4)) != 0')
    match_mask = 0
    for path_name, path_index in hlt_paths.items():
        match_mask = match_mask | (1 << path_index)
    
    hist_total = df.Histo1D(hist_model,var)
    hist_pass  = df.Filter('(hlt_acceptAndMatch & {}) != 0'.format(match_mask)) \
                    .Histo1D(hist_model, var)
    if "Fcopy" in input_file:
        hist_pass  = df.Filter('(hlt_acceptAndMatch & {}) != 0 && l1Tau_pt >= 34'.format(match_mask)) \
                    .Histo1D(hist_model, var)
    eff = ROOT.TEfficiency(hist_pass.GetPtr(), hist_total.GetPtr())
    print(hist_total.GetPtr().GetEntries())
    return hist_pass,hist_total,eff
        

trigger_pattern = {"ditau":["HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v","HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v","HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v","HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1_v"],"mutau":["HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v"],"etau":["HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v"],"ditaujet":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1_v","VBFditau_hi":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_L2NN_eta2p1_CrossL1_v","VBFditau_lo":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1_v"}
selection_id = ParseEnum(TauSelection, args.selection)
print('Tau selection: {}'.format(args.selection))

n_inputs = len(args.input)
var = args.vars

trigger_dict = [None] * n_inputs
hlt_paths = [None] * n_inputs
itrig = 0
for input_id in range(n_inputs):
    trigger_dict[input_id] = TriggerConfig.LoadTriggerDictionary(args.input[input_id])
    hlt_paths[input_id] = TriggerConfig.GetMatchedTriggers(trigger_dict[input_id][0],trigger_pattern[args.channel][itrig])
    itrig = itrig+1
    #ReportHLTPaths(hlt_paths[input_id], labels[input_id])

output_file = ROOT.TFile(args.output + '.root', 'RECREATE')


bins, x_scales, divide_by_bw = CreateBins(var)
hist_models = ROOT.RDF.TH1DModel(var, var, len(bins) - 1, array('d', bins))


hist_passed = [None] * n_inputs
hist_total = [None] * n_inputs
eff = [None] * n_inputs


for input_id in range(n_inputs):
    hist_passed[input_id], hist_total[input_id], eff[input_id] = \
        CreateHistograms(args.input[input_id], selection_id, hlt_paths[input_id],var, hist_models,output_file,args.channel)




ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)
c.SetGridx();c.SetGridy()
setTDRStyle()
label = ROOT.TLatex(); label.SetNDC(True)
ylabel = ROOT.TLatex(); ylabel.SetNDC(True)
label = ROOT.TLatex(); label.SetNDC(True)

# use multiplotter for multiple graphs
mg = ROOT.TMultiGraph("mg", "")
# legend
leg = ROOT.TLegend(0.60, 0.15, 0.90, 0.30)
leg.SetTextSize(0.025)
leg.SetTextSize(0.025)
leg.SetShadowColor(0)
leg.SetBorderSize(0)


graphs = {}
icolor = 4
imaker = 24
ileg = 0
for input_id in range(n_inputs):
    graphs[input_id] =  ROOT.TGraphAsymmErrors(hist_passed[input_id].GetPtr(),hist_total[input_id].GetPtr(), "n")
    graphs[input_id].SetLineColor(icolor)
    graphs[input_id].SetMarkerStyle(imaker)
    graphs[input_id].SetLineWidth(3)
    graphs[input_id].SetMarkerSize(1.5)
    icolor = icolor - 1
    imaker = imaker + 1
    # legname = args.input[input_id].split(".root")
    # legname = legname[0].split("Muon2022")
    # eraname = "2022"+legname[1]
    # if legname[1] == "F":
    #     eraname = "nominal"
    # elif legname[1] == "Fcopy":
    #     eraname = "L1 #tau_{pT} > 34"
    legname = ["2023C (13.6 TeV)","2022E  (13.6 TeV)","2022F  (13.6 TeV)","2018D  (13 TeV)"]
    leg.AddEntry(graphs[input_id],legname[ileg])
    print('Drawing {}'.format(legname[ileg]))
    mg.Add(graphs[input_id])
    ileg = ileg+1

mg.Draw("AP")
if(args.vars == "tau_pt"):
    label.DrawLatex(0.8, 0.03, "#tau_{pT}")
else:
    label.DrawLatex(0.8, 0.03, "#eta_{#tau}")
label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS Preliminary}")
label.SetTextSize(0.030); label.DrawLatex(0.630, 0.920, "#sqrt{s} = 13.6 TeV and 13 TeV")


leg.Draw()


plot_name = args.output+'_'+args.channel+'_'+args.vars+'.pdf'
cfg_name = args.output+'_'+args.channel+'_'+args.vars+'.C'
c.SaveAs('./{}'.format(plot_name))
c.SaveAs('./{}'.format(cfg_name))

print('TurnOn is created')
    
