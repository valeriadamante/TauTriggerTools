#!/usr/bin/python

from ROOT import *
from array import array

fIn = TFile.Open('NTuple.root')
tree = fIn.Get('Ntuplizer/TagAndProbe')

binning = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 60, 70, 80, 90, 100, 150]
bins = array('d', binning)

triggerNamesTree = fIn.Get("Ntuplizer/triggerNames")

triggerNamesList = []

l1tCuts = [28, 35, 42]

# hpass = TH1F ("hpass", "hpass", 75, 0, 150)
# htot = TH1F ("htot", "htot", 75, 0, 150)
hPassListHLT_SS = []
hPassListHLT_OS = []
hTotListHLT_SS = []
hTotListHLT_OS = []
hPassListL1T_SS = []
hPassListL1T_OS = []
hTotListL1T_SS = []
hTotListL1T_OS = []

turnOnList_HLT = []
turnOnList_L1T = []

for iTrig in range (0, 1):
    triggerNamesTree.GetEntry(iTrig)
    triggerNamesList.append(triggerNamesTree.triggerNames.Data())

print "Creating histograms"

#Preparing the Histograms
for bitIndex in range(0, len(triggerNamesList)):
    hPassListHLT_OS.append(TH1F("hPassOS_"+triggerNamesList[bitIndex], "hPassOS_"+triggerNamesList[bitIndex], len(binning)-1, bins))
    hTotListHLT_OS.append(TH1F("hTotOS_"+triggerNamesList[bitIndex], "hTotOS_"+triggerNamesList[bitIndex], len(binning)-1, bins))
    hPassListHLT_SS.append(TH1F("hPassSS_"+triggerNamesList[bitIndex], "hPassSS_"+triggerNamesList[bitIndex], len(binning)-1, bins))
    hTotListHLT_SS.append(TH1F("hTotSS_"+triggerNamesList[bitIndex], "hTotSS_"+triggerNamesList[bitIndex], len(binning)-1, bins))
    turnOnList_HLT.append(TGraphAsymmErrors())

for cutIndex in range(0, len(l1tCuts)):
    hTotListL1T_OS.append(TH1F("hTotL1OS_" + str(l1tCuts[cutIndex]), "hTotL1OS_"+str(l1tCuts[cutIndex]), len(binning)-1, bins))
    hPassListL1T_OS.append(TH1F("hPassL1OS_" + str(l1tCuts[cutIndex]), "hPassL1OS_"+str(l1tCuts[cutIndex]), len(binning)-1, bins))
    hTotListL1T_SS.append(TH1F("hTotL1SS_" + str(l1tCuts[cutIndex]), "hTotL1SS_"+str(l1tCuts[cutIndex]), len(binning)-1, bins))
    hPassListL1T_SS.append(TH1F("hPassL1SS_" + str(l1tCuts[cutIndex]), "hPassL1SS_"+str(l1tCuts[cutIndex]), len(binning)-1, bins))
    turnOnList_L1T.append(TGraphAsymmErrors())

print "Populating histograms"

#Populating the histograms
for iEv in range (0, tree.GetEntries()):
    tree.GetEntry(iEv)
    pt = tree.tauPt

    #HLT Plots
    if pt < 85:
        triggerBits = tree.tauTriggerBits
        for bitIndex in range(0, len(triggerNamesList)):
            if tree.isOS == True:
                hTotListHLT_OS[bitIndex].Fill(pt)
                if ((triggerBits >> bitIndex) & 1) == 1:
                    hPassListHLT_OS[bitIndex].Fill(pt)
            else:
                hTotListHLT_SS[bitIndex].Fill(pt)
                if ((triggerBits >> bitIndex) & 1) == 1:
                    hPassListHLT_SS[bitIndex].Fill(pt)
    
    #L1 Plots
    l1tPt = tree.l1tPt
    for cutIndex in range (0, len(l1tCuts)):
        if tree.isOS == True :
            hTotListL1T_OS[cutIndex].Fill(pt)
            if l1tPt > l1tCuts[cutIndex] :
                hPassListL1T_OS[cutIndex].Fill(pt)
        else :
            hTotListL1T_SS[cutIndex].Fill(pt)
            if l1tPt > l1tCuts[cutIndex] :
                hPassListL1T_SS[cutIndex].Fill(pt)

print "Calculating efficiencies"

#Calculating and saving the efficiencies

c1 = TCanvas ("c1", "c1", 600, 600)
c1.SetGridx()
c1.SetGridy()
fOut = TFile ("turnOn.root", "recreate")


'''for bitIndex in range(5, len(triggerNamesList)):
    hPassListHLT_OS[bitIndex].Add(hPassListHLT_SS[bitIndex], -1)
    hTotListHLT_OS[bitIndex].Add(hTotListHLT_SS[bitIndex], -1)
    turnOnList_HLT[bitIndex].Divide(hPassListHLT_OS[bitIndex], hTotListHLT_OS[bitIndex], "cl=0.683 b(1,1) mode")
    turnOnList_HLT[bitIndex].SetMarkerStyle(8)
    turnOnList_HLT[bitIndex].SetMarkerSize(0.8)
    turnOnList_HLT[bitIndex].SetMarkerColor(kRed)
    turnOnList_HLT[bitIndex].GetXaxis().SetTitle("p_t (GeV)");
    turnOnList_HLT[bitIndex].GetYaxis().SetTitle("Efficiency");
    turnOnList_HLT[bitIndex].SetTitle(triggerNamesList[bitIndex] + " turn-on curve")
    turnOnList_HLT[bitIndex].Draw("AP")
    c1.Update()
    c1.Print("turnOn_" + triggerNamesList[bitIndex] + ".pdf", "pdf")
    hTurnOn = hPassListHLT_OS[bitIndex].Clone("hTurnOn_" + triggerNamesList[bitIndex])
    hTurnOn.Divide(hTotListHLT_OS[bitIndex])
    hTurnOn.Write()
    hPassListHLT_OS[bitIndex].Write()
    hTotListHLT_OS[bitIndex].Write()'''

for cutIndex in range(0, len(l1tCuts)):
    hPassListL1T_OS[cutIndex].Add(hPassListL1T_SS[cutIndex], -1)
    hTotListL1T_OS[cutIndex].Add(hTotListL1T_SS[cutIndex], -1)
    turnOnList_L1T[cutIndex].Divide(hPassListL1T_OS[cutIndex], hTotListL1T_OS[cutIndex], "cl=0.683 b(1,1) mode")
    turnOnList_L1T[cutIndex].SetMarkerStyle(8)
    turnOnList_L1T[cutIndex].SetMarkerSize(0.8)
    turnOnList_L1T[cutIndex].SetMarkerColor(kRed)
    turnOnList_L1T[cutIndex].GetXaxis().SetTitle("p_t (GeV)");
    turnOnList_L1T[cutIndex].GetYaxis().SetTitle("Efficiency");
    turnOnList_L1T[cutIndex].SetTitle("L1 trigger cut " + str(l1tCuts[cutIndex]) + " turn-on curve")
    turnOnList_L1T[cutIndex].Draw("AP")
    c1.Update()
    c1.Print("turnOnL1_" + str(l1tCuts[cutIndex]) + ".pdf", "pdf")
    hTurnOn = hPassListL1T_OS[cutIndex].Clone("hTurnOnL1_" + str(l1tCuts[cutIndex]))
    hTurnOn.Divide(hTotListL1T_OS[cutIndex])
    hTurnOn.Write()
    hPassListL1T_OS[cutIndex].Write()
    hTotListL1T_OS[cutIndex].Write()

raw_input()
