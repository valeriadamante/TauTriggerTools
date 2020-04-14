#!/usr/bin/env python

import ROOT
import argparse
import sys
import re
import numpy as np
from array import array
import py_plot as plt
import math


parser = argparse.ArgumentParser(description='Copmare two turnon curves.')
parser.add_argument('--input-a', required=True, type=str, help="the first input")
parser.add_argument('--input-b', required=True, type=str, help="the second input")
parser.add_argument('--labels', required=True, type=str, help="labels for both inputs")
parser.add_argument('--pattern', required=True, type=str, help="trigger name pattern")
parser.add_argument('--selection', required=True, type=str, help="Tau selection")
parser.add_argument('--output', required=True, type=str, help="output file")
parser.add_argument('--var-a', required=True, type=str, help="pt variable to draw")
parser.add_argument('--var-b', required=True, type=str, help="eta variable to draw")
parser.add_argument('--pTT', required=True, type=float, help="Threshold pT")
parser.add_argument('--ch', required=True, type=str, help="tt,et,mt")
parser.add_argument('--ext', required=True, type=bool, help="True for hight pT")
args = parser.parse_args()

sys.path.insert(0, 'Common/python')
from AnalysisTypes import *
ROOT.gROOT.SetBatch(True)
chs=['tt','mt','et']
if(args.ch not in chs):
    print("please choose the ch within {tt,et,mt}")
def KatzLog(passed, total):
    """Returns 1-sigma confidence interval for a ratio of proportions using Katz-log method."""
    if np.count_nonzero(total) != len(total):
        raise RuntimeError("Total can't be zero")
    if np.count_nonzero(passed < 0) != 0 or np.count_nonzero(total < 0) != 0:
        raise RuntimeError("Yields can't be negative")
    if np.count_nonzero(passed > total) != 0:
        raise RuntimeError("Passed can't be bigger than total")
    if passed[0] == total[0] and passed[1] == total[1]:
        y1 = total[0] - 0.5
        y2 = total[1] - 1
    else:
        y1 = passed[0] if passed[0] != 0 else 0.5
        y2 = passed[1] if passed[1] != 0 else 0.5
    n1 = total[0]
    n2 = total[1]
    pi1 = y1 / n1
    pi2 = y2 / n2
    theta = pi1 / pi2
    sigma2 = (1 - pi1) / (pi1 * n1) + (1 - pi2) / (pi2 * n2)
    if sigma2<0:
        sigma2=-1*sigma2
    sigma = math.sqrt(sigma2)
    return (theta * math.exp(-sigma), theta * math.exp(sigma))


def LoadTriggerDictionary(file):
    df_support = ROOT.RDataFrame('summary', file)
    summary = df_support.AsNumpy()
    trigger_index = np.array(summary['trigger_index'][0])
    trigger_pattern = np.array(summary['trigger_pattern'][0])
    trigger_dict = {}
    for n in range(len(trigger_pattern)):
        trigger_dict[trigger_pattern[n]] = trigger_index[n]
    return trigger_dict

def GetMatchedTriggers(trigger_dict, pattern):
    reg_ex = re.compile(pattern)
    matched = {}
    for name, pos in trigger_dict.items():
        if reg_ex.match(name) is not None:
            matched[name] = pos
    return matched

def ReportHLTPaths(hlt_paths, label):
    if len(hlt_paths) == 0:
        raise RuntimeError("No HLT path match the pattern for {}".format(label))
    line = 'HLT path for {}:'.format(label)
    for name in hlt_paths:
        line += ' {}'.format(name)
    print(line)

def CreatePtHistograms(input_file, selection_id, hlt_paths, label, var, hist_model, output_file):
    df = ROOT.RDataFrame('events;2', input_file)
    df = df.Filter('(tau_sel & {}) != 0 && abs(tau_gen_vis_eta) < 2.1 && tau_gen_vis_pt > 0'.format(selection_id))
    if(args.ch == 'et'):
        df = df.Filter('(tau_sel & {}) != 0 && abs(tau_gen_vis_eta) < 2.1 && tau_gen_vis_pt > 0 && l1Tau_pt > 26'.format(selection_id))
    match_mask = 0
    for path_name, path_index in hlt_paths.items():
        match_mask = match_mask | (1 << path_index)
    hist_total = df.Histo1D(hist_model, var,'puweight')
    hist_passed = df.Filter('(hlt_acceptAndMatch & {}) != 0'.format(match_mask)) \
                    .Histo1D(hist_model, var,'puweight')
    eff = ROOT.TEfficiency(hist_passed.GetPtr(), hist_total.GetPtr())
    #eff = ROOT.TGraphAsymmErrors(hist_passed.GetPtr(), hist_total.GetPtr())
    output_file.WriteTObject(hist_total.GetPtr(), label + '_pt_total', 'Overwrite')
    output_file.WriteTObject(hist_passed.GetPtr(), label + '_pt_passed', 'Overwrite')
    output_file.WriteTObject(eff, label + '_pt_eff', 'Overwrite')
    return eff,hist_total,hist_passed


def CreateNVtxHistograms(input_file, selection_id,pt_cut, hlt_paths, label, var, hist_model, output_file):
    df = ROOT.RDataFrame('events', input_file)
    df = df.Filter('(tau_sel & {}) != 0 && abs(tau_gen_vis_pt) > {}'.format(selection_id,pt_cut))
    if(args.ch == 'et'):
        df = df.Filter('(tau_sel & {}) != 0 && abs(tau_gen_vis_pt) > {} && l1Tau_pt >26'.format(selection_id,pt_cut))
    match_mask = 0
    for path_name, path_index in hlt_paths.items():
        match_mask = match_mask | (1 << path_index)
    hist_total = df.Histo1D(hist_model, var)
    hist_passed = df.Filter('(hlt_acceptAndMatch & {}) != 0'.format(match_mask)) \
                    .Histo1D(hist_model, var)
    eff = ROOT.TEfficiency(hist_passed.GetPtr(), hist_total.GetPtr())
    #eff = ROOT.TGraphAsymmErrors(hist_passed.GetPtr(), hist_total.GetPtr())
    output_file.WriteTObject(hist_total.GetPtr(), label + '_npv_total', 'Overwrite')
    output_file.WriteTObject(hist_passed.GetPtr(), label + '_npv_passed', 'Overwrite')
    output_file.WriteTObject(eff, label + '_npv_eff', 'Overwrite')
    return eff,hist_total,hist_passed



def CreateEtaHistograms(input_file, selection_id,pt_cut, hlt_paths, label, var, hist_model, output_file):
    df = ROOT.RDataFrame('events', input_file)
    df = df.Filter('(tau_sel & {}) != 0 && tau_gen_vis_pt > {}'.format(selection_id,pt_cut))
    if(args.ch == 'et'):
        df = df.Filter('(tau_sel & {}) != 0 && abs(tau_gen_vis_pt) > {} && l1Tau_pt >26'.format(selection_id,pt_cut))
    match_mask = 0
    for path_name, path_index in hlt_paths.items():
        match_mask = match_mask | (1 << path_index)
    hist_total = df.Histo1D(hist_model, var,'puweight')
    hist_passed = df.Filter('(hlt_acceptAndMatch & {}) != 0'.format(match_mask)) \
                    .Histo1D(hist_model, var,'puweight')
    eff = ROOT.TEfficiency(hist_passed.GetPtr(), hist_total.GetPtr())
    #eff = hist_passed.GetPtr().Divide(hist_total.GetPtr())
    output_file.WriteTObject(hist_total.GetPtr(), label + '_eta_total', 'Overwrite')
    output_file.WriteTObject(hist_passed.GetPtr(), label + '_eta_passed', 'Overwrite')
    output_file.WriteTObject(eff, label + '_eta_eff', 'Overwrite')
    return eff,hist_total,hist_passed

def CreateL1PtHistograms(input_file, selection_id,label, var, hist_model, output_file):
    df = ROOT.RDataFrame('events;2', input_file)
    df = df.Filter('(tau_sel & {}) != 0 && abs(tau_gen_vis_eta) < 2.1 && tau_gen_vis_pt > 0'.format(selection_id))
    if(args.ch == 'et'):
        df = df.Filter('(tau_sel & {}) != 0 && abs(tau_gen_vis_eta) < 2.1 && tau_gen_vis_pt > 0 && l1Tau_pt > 26'.format(selection_id))
    hist_total = df.Histo1D(hist_model, var,'puweight')
    hist_passed = df.Filter('l1Tau_hwIso > 0') \
                    .Histo1D(hist_model, var,'puweight')
    eff = ROOT.TEfficiency(hist_passed.GetPtr(), hist_total.GetPtr())
    #eff = ROOT.TGraphAsymmErrors(hist_passed.GetPtr(), hist_total.GetPtr())
    output_file.WriteTObject(hist_total.GetPtr(), label + '_pt_total', 'Overwrite')
    output_file.WriteTObject(hist_passed.GetPtr(), label + '_pt_passed', 'Overwrite')
    output_file.WriteTObject(eff, label + '_pt_eff', 'Overwrite')
    return eff,hist_total,hist_passed

selection_id = ParseEnum(TauSelection, args.selection)
print('Tau selection: {}'.format(args.selection))

labels = args.labels.split(',')

trigger_dict_a = LoadTriggerDictionary(args.input_a)
trigger_dict_b = LoadTriggerDictionary(args.input_b)

hlt_paths_a = GetMatchedTriggers(trigger_dict_a, args.pattern)
ReportHLTPaths(hlt_paths_a, labels[0])

hlt_paths_b = GetMatchedTriggers(trigger_dict_b, args.pattern)
ReportHLTPaths(hlt_paths_b, labels[1])

output_file = ROOT.TFile(args.output, 'RECREATE')

ext = args.ext
ext_bins = np.arange(0, 70, step=10)
ext_bins = np.append(ext_bins, [80, 100,150, 200, 300, 500, 1000])
bins = np.arange(0, 100, step=10)
bins = np.append(bins, [100, 150, 200])
if(ext==True):
    bins = ext_bins
eta_bins = np.arange(-2.5,3,step=0.5)
hist_model = ROOT.RDF.TH1DModel('tau_pt', '', len(bins)-1, array('d', bins))
hist_model_npv = ROOT.RDF.TH1DModel('npv', '', len(bins)-1, array('d', bins))
hist_model_eta = ROOT.RDF.TH1DModel('tau_eta', '', len(eta_bins)-1, array('d',eta_bins))
pt_eff_a,pt_total_a,pt_passed_a = CreatePtHistograms(args.input_a, selection_id, hlt_paths_a, labels[0], args.var_a, hist_model, output_file)
pt_eff_b,pt_total_b,pt_passed_b = CreatePtHistograms(args.input_b, selection_id, hlt_paths_b, labels[1], args.var_a, hist_model, output_file)
L1pt_eff_a,L1pt_total_a,L1pt_passed_a = CreateL1PtHistograms(args.input_a, selection_id, labels[0], args.var_a, hist_model, output_file)
L1pt_eff_b,L1pt_total_b,L1pt_passed_b = CreateL1PtHistograms(args.input_b, selection_id, labels[1], args.var_a, hist_model, output_file)
eta_eff_a,eta_total_a,eta_passed_a = CreateEtaHistograms(args.input_a, selection_id,args.pTT, hlt_paths_a, labels[0], args.var_b, hist_model_eta, output_file)
eta_eff_b,eta_total_b,eta_passed_b = CreateEtaHistograms(args.input_b, selection_id,args.pTT, hlt_paths_b, labels[1], args.var_b, hist_model_eta, output_file)
npv_eff_a,npv_total_a,npv_passed_a = CreateNVtxHistograms(args.input_a, selection_id,args.pTT, hlt_paths_a, labels[0], args.var_a, hist_model_npv, output_file)
npv_eff_b,npv_total_b,npv_passed_b = CreateNVtxHistograms(args.input_b, selection_id,args.pTT, hlt_paths_b, labels[1], args.var_a, hist_model_npv, output_file)

pt_ratio_1 = hist_model.GetHistogram().Clone('pt_ratio_1')
L1pt_ratio_1 = hist_model.GetHistogram().Clone('L1pt_ratio_1')
eta_ratio_1 = hist_model_eta.GetHistogram().Clone('eta_ratio_1')
npv_ratio_1 = hist_model_npv.GetHistogram().Clone('npv_ratio_1')

#-------------------------- Pt Ratio Plot --------------------------------------------
yErLow,yErHigh=[],[]
xErLow,xErHigh=[],[]
yval,xval=[],[]
for n in range(1,pt_ratio_1.GetNbinsX()+1):
    if pt_eff_b.GetEfficiency(n) != 0 and n!=0:
        norm = pt_eff_a.GetEfficiency(n)/pt_eff_b.GetEfficiency(n)
        if(norm!=0):
            yval.append(norm)
            xval.append(pt_ratio_1.GetBinCenter(n))
            ylow,yhigh = KatzLog(np.array([pt_passed_a.GetBinContent(n),pt_passed_b.GetBinContent(n)]),np.array([pt_total_a.GetBinContent(n),pt_total_b.GetBinContent(n)]))
            yErLow.append(norm-ylow)
            yErHigh.append(yhigh-norm)
            xErLow.append(pt_ratio_1.GetBinWidth(n)/2)
            xErHigh.append(pt_ratio_1.GetBinWidth(n)/2)
            #yval.append(pt_eff_a.Eval(n)/pt_eff_b.Eval(n))

xval_ = array('f',xval)
yval_ = array('f',yval)
exl = array('f',xErLow)
exh = array('f',xErHigh)
eyl = array('f',yErLow)
eyh = array('f',yErHigh)

#--------------------------L1 Pt Ratio Plot --------------------------------------------
l1yErLow,l1yErHigh=[],[]
l1xErLow,l1xErHigh=[],[]
l1yval,l1xval=[],[]
for n in range(1,L1pt_ratio_1.GetNbinsX()+1):
    if L1pt_eff_b.GetEfficiency(n) != 0 and n!=0:
        norm = L1pt_eff_a.GetEfficiency(n)/L1pt_eff_b.GetEfficiency(n)
        if(norm!=0):
            l1yval.append(norm)
            l1xval.append(L1pt_ratio_1.GetBinCenter(n))
            ylow,yhigh = KatzLog(np.array([L1pt_passed_a.GetBinContent(n),L1pt_passed_b.GetBinContent(n)]),np.array([L1pt_total_a.GetBinContent(n),L1pt_total_b.GetBinContent(n)]))
            l1yErLow.append(norm-ylow)
            l1yErHigh.append(yhigh-norm)
            l1xErLow.append(L1pt_ratio_1.GetBinWidth(n)/2)
            l1xErHigh.append(L1pt_ratio_1.GetBinWidth(n)/2)
            #yval.append(pt_eff_a.Eval(n)/pt_eff_b.Eval(n))

l1xval_ = array('f',l1xval)
l1yval_ = array('f',l1yval)
l1exl = array('f',l1xErLow)
l1exh = array('f',l1xErHigh)
l1eyl = array('f',l1yErLow)
l1eyh = array('f',l1yErHigh)

#-------------------------- nVtx Ratio Plot --------------------------------------------
npv_yErLow,npv_yErHigh=[],[]
npv_xErLow,npv_xErHigh=[],[]
npv_yval,npv_xval=[],[]
for n in range(1,pt_ratio_1.GetNbinsX()+1):
     if npv_eff_b.GetEfficiency(n) != 0 and n!=0:
         norm = npv_eff_a.GetEfficiency(n)/npv_eff_b.GetEfficiency(n)
         if(norm!=0):
             npv_yval.append(norm)
             npv_xval.append(npv_ratio_1.GetBinCenter(n))
             ylow,yhigh = KatzLog(np.array([npv_passed_a.GetBinContent(n),npv_passed_b.GetBinContent(n)]),np.array([npv_total_a.GetBinContent(n),npv_total_b.GetBinContent(n)]))
             npv_yErLow.append(norm-ylow)
             npv_yErHigh.append(yhigh-norm)
             npv_xErLow.append(npv_ratio_1.GetBinWidth(n)/2)
             npv_xErHigh.append(npv_ratio_1.GetBinWidth(n)/2)
             #yval.append(pt_eff_a.Eval(n)/pt_eff_b.Eval(n))

npv_xval_ = array('f',npv_xval)
npv_yval_ = array('f',npv_yval)
npv_exl = array('f',npv_xErLow)
npv_exh = array('f',npv_xErHigh)
npv_eyl = array('f',npv_yErLow)
npv_eyh = array('f',npv_yErHigh)


#-------------------------- Eta Ratio Plot ------------------------------------------
eta_yErLow,eta_yErHigh=[],[]
eta_xErLow,eta_xErHigh=[],[]
eta_yval,eta_xval=[],[]
for n in range(0,eta_ratio_1.GetNbinsX()+1):
     if eta_eff_b.GetEfficiency(n) != 0:
         norm = eta_eff_a.GetEfficiency(n)/eta_eff_b.GetEfficiency(n)
         eta_yval.append(norm)
         eta_xval.append(eta_ratio_1.GetBinCenter(n))
         ylow,yhigh = KatzLog(np.array([eta_passed_a.GetBinContent(n),eta_passed_b.GetBinContent(n)]),np.array([eta_total_a.GetBinContent(n),eta_total_b.GetBinContent(n)]))
         eta_yErLow.append(norm-ylow)
         eta_yErHigh.append(yhigh-norm)
         eta_xErLow.append(eta_ratio_1.GetBinWidth(n)/2)
         eta_xErHigh.append(eta_ratio_1.GetBinWidth(n)/2)
         #yval.append(pt_eff_a.Eval(n)/pt_eff_b.Eval(n))

eta_xval_ = array('f',eta_xval)
eta_yval_ = array('f',eta_yval)
eta_exl = array('f',eta_xErLow)
eta_exh = array('f',eta_xErHigh)
eta_eyl = array('f',eta_yErLow)
eta_eyh = array('f',eta_yErHigh)
#-----------------------------------------------------------------------------------

pt_ratio = ROOT.TGraphAsymmErrors(len(xval),xval_,yval_,exl,exh,eyl,eyh)
l1pt_ratio = ROOT.TGraphAsymmErrors(len(xval),l1xval_,l1yval_,l1exl,l1exh,l1eyl,l1eyh)
eta_ratio = ROOT.TGraphAsymmErrors(len(eta_xval),eta_xval_,eta_yval_,eta_exl,eta_exh,eta_eyl,eta_eyh)
npv_ratio = ROOT.TGraphAsymmErrors(len(npv_xval),npv_xval_,npv_yval_,npv_exl,npv_exh,npv_eyl,npv_eyh)
output_file.WriteTObject(pt_ratio, 'pt_ratio', 'Overwrite')
output_file.WriteTObject(eta_ratio, 'eta_ratio', 'Overwrite')
output_file.Close()
plt.ratioplotPt(pt_eff_a,pt_eff_b,pt_ratio,'pt',labels[0],labels[1],args.ch,False)
plt.ratioplotPt(L1pt_eff_a,L1pt_eff_b,l1pt_ratio,'pt',labels[0],labels[1],args.ch,True)
plt.ratioplotPt(eta_eff_a,eta_eff_b,eta_ratio,'eta',labels[0],labels[1],args.ch,args.ext)
#plt.ratioplotPt(npv_eff_a,npv_eff_b,npv_ratio,'pt',labels[0],labels[1],args.ch,False)
