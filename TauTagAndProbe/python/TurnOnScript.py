#!/usr/bin/env python3

import ROOT
import argparse
import sys
import re
import numpy as np
from array import array

import math
import os
from tdrstyle import *

from Plothelper import CreateBins,CreateHistograms,CreateMCHistograms
parser = argparse.ArgumentParser(description='Create turnon curves.')
parser.add_argument('--input_run2022', required=True, type=str, nargs='+', help="run2022 data")
parser.add_argument('--input_run2023', required=True, type=str, nargs='+', help="run2023 data")
parser.add_argument('--input_mc', required=True, type=str, nargs='+', help="input mc")
parser.add_argument('--pu', required=True, type=str, help="variable to draw")

parser.add_argument('--channel', required=True, type=str, help="ditau,mutau,etau,VBFditau_hi,VBFditau_lo,ditaujet")
parser.add_argument('--selection', required=False, type=str,default="DeepTau", help="Tau selection")

parser.add_argument('--output', required=True, type=str, help="output file")
parser.add_argument('--vars', required=True,nargs='+', type=str, help="variable to draw")

args = parser.parse_args()

print(args.vars)

sys.path.insert(0, 'Common/python')
from AnalysisTypes import *
from AnalysisTools import *
import RootPlotting
import TriggerConfig
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()
RootPlotting.ApplyDefaultGlobalStyle()

trigger_pattern = {"ditau":["HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v","HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v","HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v","HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1_v"],"mutau":["HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v"],"etau":["HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v","HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v"],"ditaujet":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1_v","VBFditau_hi":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_L2NN_eta2p1_CrossL1_v","VBFditau_lo":"HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1_v","single_tau":["HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS180_eta2p1_v","HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS180_eta2p1_v","HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS180_eta2p1_v"]}
selection_id = ParseEnum(TauSelection, "DeepTau")

n_input1 =len(args.input_run2022) #2
n_input2 =len(args.input_run2023) #3
n_input3 =len(args.input_mc)      #4



n_inputs = n_input1+n_input2+n_input3 #9
output_file = ROOT.TFile(args.output + '.root', 'RECREATE')


trigger_dict = [None] * n_inputs
hlt_paths = [None] * n_inputs
itrig = 0

hist_passed = [None] * n_inputs
hist_total = [None] * n_inputs
eff = [None] * n_inputs

for input_id in range(n_input1): #0-2
    trigger_dict[input_id] = TriggerConfig.LoadTriggerDictionary(args.input_run2022[input_id])
    hlt_paths[input_id] = TriggerConfig.GetMatchedTriggers(trigger_dict[input_id][0],trigger_pattern[args.channel][itrig])
    hist_passed[input_id], hist_total[input_id], eff[input_id] = CreateHistograms(args.input_run2022[input_id], selection_id, hlt_paths[input_id],args.vars,output_file,args.channel)
    itrig = itrig+1


for input_id in range(n_input1,n_inputs-n_input3): #2-5
    trigger_dict[input_id] = TriggerConfig.LoadTriggerDictionary(args.input_run2023[input_id-n_input1])
    hlt_paths[input_id] = TriggerConfig.GetMatchedTriggers(trigger_dict[input_id][0],trigger_pattern[args.channel][itrig])
    hist_passed[input_id], hist_total[input_id], eff[input_id] = CreateHistograms(args.input_run2023[input_id-n_input1], selection_id, hlt_paths[input_id],args.vars,output_file,args.channel)
    itrig = itrig+1

for input_id in range(n_inputs-n_input3,n_inputs): #5-9
    data_pu_file = ROOT.TFile(args.pu, 'READ')
    data_pu = data_pu_file.Get('pileup')
    df_all = ROOT.RDataFrame('all_events',args.input_mc[input_id-n_inputs+n_input3])
    mc_pu = df_all.Histo1D(ROOT.RDF.TH1DModel(data_pu), 'npu')
    ROOT.PileUpWeightProvider.Initialize(data_pu, mc_pu.GetPtr())
    trigger_dict[input_id] = TriggerConfig.LoadTriggerDictionary(args.input_mc[input_id-n_inputs+n_input3])
    hlt_paths[input_id] = TriggerConfig.GetMatchedTriggers(trigger_dict[input_id][0],trigger_pattern[args.channel][itrig])
    hist_passed[input_id], hist_total[input_id], eff[input_id] = CreateMCHistograms(args.input_mc[input_id-n_inputs+n_input3], selection_id, hlt_paths[input_id],args.vars,output_file,args.channel,args.pu)
    itrig = itrig+1

# #for var in args.vars:
# for input_id in range(n_input1): #0-2
#     # bins, x_scales, divide_by_bw = CreateBins(var)
#     # hist_models = ROOT.RDF.TH1DModel(var, var, len(bins) - 1, array('d', bins))
    
# for input_id in range(n_input1,n_inputs-n_input3): #2-5
#     # bins, x_scales, divide_by_bw = CreateBins(var)
#     # hist_models = ROOT.RDF.TH1DModel(var, var, len(bins) - 1, array('d', bins))
    

# for input_id in range(n_inputs-n_input3,n_inputs): #5-9
#     # bins, x_scales, divide_by_bw = CreateBins(var)
#     # hist_models = ROOT.RDF.TH1DModel(var, var, len(bins) - 1, array('d', bins))
    

ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)
c.SetGridx();c.SetGridy()
setTDRStyle()
label = ROOT.TLatex(); label.SetNDC(True)
ylabel = ROOT.TLatex(); ylabel.SetNDC(True)
label = ROOT.TLatex(); label.SetNDC(True)



#var = 'tau_eta'
for var in args.vars:
    # use multiplotter for multiple graphs
    mg = ROOT.TMultiGraph("mg", "")
    # legend
    leg = ROOT.TLegend(0.582707, 0.247312, 0.883459, 0.397849)
    leg.SetTextSize(0.025)
    leg.SetTextSize(0.025)
    leg.SetShadowColor(0)
    leg.SetBorderSize(0)
    
    
    
    
    
    #for var in args.vars:
    graphs = {}
    icolor = [1,4,2]
    ic = 0
    imaker = 9
    ileg = 0
    for input_id in range(n_inputs):
        graphs[input_id] =  ROOT.TGraphAsymmErrors(hist_passed[input_id][var].GetPtr(),hist_total[input_id][var].GetPtr(), "n")
        graphs[input_id].SetLineColor(icolor[ic])
        graphs[input_id].SetMarkerStyle(imaker)
        graphs[input_id].SetLineWidth(3)
        graphs[input_id].SetMarkerSize(1.5)
        ic = ic + 1
        #imaker = imaker + 1
    
        legname = ["Run 2022","Run 2023","Simulation"]
        leg.AddEntry(graphs[input_id],legname[ileg])
        print('Drawing {}'.format(legname[ileg]))
        mg.Add(graphs[input_id])
        ileg = ileg+1

        
    mg.GetYaxis().SetRangeUser(0,1)
    mg.GetYaxis().SetNdivisions(5)
    mg.GetXaxis().SetLabelSize(0.04)
    mg.GetYaxis().SetLabelSize(0.04)
    #mg.GetYaxis().SetTitle("L1 + HLT Efficiency")
    if args.channel == "single_tau" and var == "tau_pt":
        mg.GetXaxis().SetRangeUser(50,500)
    mg.Draw("AP")
    ylabel.SetTextAngle(90);ylabel.SetTextSize(0.0414815);ylabel.DrawLatex(0.035,0.422222, "L1 + HLT Efficiency")
    if args.channel == "VBFditau_lo":
        ylabel.SetTextAngle(90);ylabel.SetTextSize(0.0414815);ylabel.DrawLatex(0.035,0.422222, "HLT Efficiency")
    if(var == "tau_pt"):
        label.SetTextSize(0.0414815);label.DrawLatex(0.67,0.0192593, "Offline p_{T}^{#tau} [GeV]")
        label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS} #it{Preliminary}")
        
    elif(var== "npu" or var == "npv"):
        label.SetTextSize(0.0414815);label.DrawLatex(0.197995,0.0122888, "number of offline reconstructed primary vertices")
        label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS} #it{Preliminary}")
    else:
        label.SetTextSize(0.0414815);label.DrawLatex(0.67,0.0192593, "Offline #eta^{#tau}")
        label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS} #it{Preliminary}")
        #label.SetTextSize(0.030); label.DrawLatex(0.63, 0.912593, "34.3 fb^{-1} (13.6 TeV, 2022)")
        
    if args.channel == 'ditau':
        label.DrawLatex(0.358396,0.434074, "#bf{Double-#tau_{h} trigger performance}")
    elif args.channel == 'mutau':
        label.DrawLatex(0.358396,0.434074, "#bf{#mu#tau_{h} trigger performance}")
    elif args.channel == 'etau':
        label.DrawLatex(0.358396,0.434074, "#bf{e#tau_{h} trigger performance}")
    elif args.channel == 'single_tau':
        label.DrawLatex(0.358396,0.434074, "#bf{Single-#tau_{h} trigger performance}")
    elif args.channel == "VBFditau_hi" or args.channel == "VBFditau_lo":
        label.DrawLatex(0.358396,0.434074, "#bf{VBF di-#tau_{h} trigger performance}")
    else:
        label.DrawLatex(0.358396,0.434074, "#bf{di-#tau_{h} +jets trigger performance}")
    if var == "tau_eta":
        #print("Medium tauID, #tau_ > {} GeV".format(eta_th[args.channel]))
        label.DrawLatex(0.305764,0.183704, "Offline tauID applied at Medium WP")
    elif var == "npv":
        label.DrawLatex(0.305764,0.183704,"Offline tauID applied at Medium WP" )
    else:
        label.DrawLatex(0.305764,0.183704, "Offline tauID applied at Medium WP")
    leg.Draw()
    plot_pdf_name = args.output+'_'+args.channel+'_'+var+'.pdf'
    plot_png_name = args.output+'_'+args.channel+'_'+var+'.png'
    cfg_name = args.output+'_'+args.channel+'_'+var+'.C'
    c.SaveAs('./DPplots/{}'.format(plot_pdf_name))
    c.SaveAs('./DPplots/{}'.format(plot_png_name))
    c.SaveAs('./DPplots/{}'.format(cfg_name))
    
    print('TurnOn is created')
    
