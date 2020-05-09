from ROOT import *
from ROOT import kBlack, kBlue, kRed
import numpy as np
from array import array
import math
import os 

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



def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0.08)  # joins upper and lower plot
    pad1.SetGridx()
    pad1.SetGridy()
    #pad1.SetLogx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.SetGridy()
    #pad2.SetLogx()
    pad2.Draw()
    
    return c, pad1, pad2

def ratioplotPt(eff_a,eff_b,gr,vari,label1,label2,ch,ext):
    #os.makdir('/afs/cern.ch/work/v/vmuralee/private/TagAndProbe/CMSSW_10_6_11_patch1/src/TauTriggerTools/plots')
    eff_a.SetLineWidth(2)
    eff_b.SetLineWidth(2)
    eff_a.SetLineColor(kBlack)
    eff_b.SetLineColor(kRed)
    c1, pad1, pad2 = createCanvasPads()
    # draw everything
    pad1.cd()
    hbase = TH1D()
    if(vari=='pt' and ext==True):
        ext_bins = np.arange(0, 70, step=10)
        ext_bins = np.append(ext_bins, [80, 100,150, 200, 300, 500, 1000])
        hbase = TH1D('hbase','',len(ext_bins)-1,array('d',ext_bins))
    elif(vari=='pt' and ext==False):
         xbins=np.arange(0,120,10)
         #xbins=np.append(xbins,[100,150,200])
         hbase = TH1D('hbase','',len(xbins)-1,array('d',xbins))
    elif(vari=='L1pt' and ext==True):
        ext_bins = np.arange(0, 70, step=10)
        ext_bins = np.append(ext_bins, [80, 100,150, 200, 300, 500, 1000])
        hbase = TH1D('hbase','',len(ext_bins)-1,array('d',ext_bins))
    elif(vari=='L1pt' and ext==False):
         xbins=np.arange(0,120,10)
         #xbins=np.append(xbins,[100,150,200])
         hbase = TH1D('hbase','',len(xbins)-1,array('d',xbins))
    else:
        xbins = np.arange(-2.5,3,0.5)
        hbase = TH1D('hbase','',len(xbins)-1,array('d',xbins))
        
    hbase.Draw()
    #eff_a.Chi2Test(eff_b,'UU')
    eff_a.Draw("sameP")
    eff_b.Draw("sameP")
    hbase.SetMaximum(1.2)
    hbase.SetStats(0)
    #axis.Draw()
    leg = TLegend(.6,.32,.75,.53)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetTextSize(0.03)
    leg.AddEntry(eff_a,label1,'l')
    leg.AddEntry(eff_b,label2,'l')
    leg.Draw()
    pad2.cd()
          
    
    # yErHigh,yErLow=[],[]
    # xErHigh,xErLow=[],[]
    # xval,yval=[0,10,20,30,40,50,60,70,80, 100,150, 200, 300, 500,1000],[]
    # ratio_ab = TH1D('ratio_ab','',len(xval)-1,array('d',xval))
    ratio_ab = hbase.Clone('ratio_ab')
    
    #gr = TGraphAsymmErrors(len(xval),np.array(xval),np.array(yval),,,np.array(yErLow),np.array(yErHigh))
    #gr = TGraph(len(yval),np.array(xval),np.array(yval))
    ratio_ab.SetMaximum(2)
    ratio_ab.SetMinimum(0)
    ratio_ab.SetStats(0)
    ratio_ab.SetMarkerStyle(21)
    #axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    ratio_ab.GetXaxis().SetLabelFont(43)
    ratio_ab.GetYaxis().SetLabelFont(43)
    ratio_ab.GetXaxis().SetLabelSize(15)
    ratio_ab.GetYaxis().SetLabelSize(15)
    if vari == 'pt':
        ratio_ab.GetXaxis().SetTitle('gen_pT(GeV)')
        ratio_ab.GetXaxis().SetTitleSize(15)
    else:
        ratio_ab.GetXaxis().SetTitle('gen_#eta_{#tau}')
        ratio_ab.GetXaxis().SetTitleSize(15)
        
    ratio_ab.GetXaxis().SetTitle('nVtx')
    ratio_ab.Draw()
    gr.SetMarkerStyle(21)
    #gr.SetMarkerSize(2)
    gr.Draw("sameP")
    
    c1.SaveAs("./UL16_plots/"+label1+label2+"_"+vari+"_"+ch+".png".format(vari))


