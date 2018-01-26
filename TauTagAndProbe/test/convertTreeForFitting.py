from ROOT import *
import numpy as n

# the hadd of all the output ntuples
path = "/afs/cern.ch/user/h/hsert/TriggerStudies/ForkedRepo/Samples/2018_01_14/"
fname =  path + "NTuple_Data2017BCDEF_17Nov2017-v1_14_01_2018.root"
#fname =  path +"NTuple_DYJets_RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1_14_01_2018_PU.root"

#pt = [20, 26, 30, 34]
pt = [20, 26, 30, 32, 34]
numberOfHLTTriggers = 23
numberOfHLTTriggersForFit = 27
saveOnlyOS = False # True; save only OS, False; save both and store weight for bkg sub
disabledPScolumns = False  # True; to remove the disabled columns, False; to consider all columns
#######################################################
fIn = TFile.Open(fname)
tIn = fIn.Get('Ntuplizer/TagAndProbe')
tTriggerNames = fIn.Get("Ntuplizer/triggerNames")
outname = fname.replace ('.root', '_forFit.root')
fOut = TFile (outname, 'recreate')
tOut = tIn.CloneTree(0)
tOutNames = tTriggerNames.CloneTree(-1) # copy all

briso   = [n.zeros(1, dtype=int) for x in range (0, len(pt))]
brnoiso = [n.zeros(1, dtype=int) for x in range (0, len(pt))]
bkgSubW = n.zeros(1, dtype=float)
bkgSubANDpuW = n.zeros(1, dtype=float)

hltPathTriggered_OS   = [n.zeros(1, dtype=int) for x in range (0, numberOfHLTTriggersForFit+1)]

for i in range (0, len(pt)):
    name = ("hasL1_" + str(pt[i]))
    tOut.Branch(name, brnoiso[i], name+"/I")
    name += "_iso"
    tOut.Branch(name, briso[i], name+"/I")

for i in range (0, numberOfHLTTriggersForFit):
    tTriggerNames.GetEntry(i)
    if(i < numberOfHLTTriggers):
    	name = ("hasHLTPath_" + str(i))
    elif(i==numberOfHLTTriggers):
    	name = ("hasHLTetauPath_13")# _IsoMu20_LooseChargedIsoPFTau27_plusL1Tau26andHLTTau30")
    elif(i==numberOfHLTTriggers+1):
    	name = ("hasHLTmutauPath_13") #_IsoMu20_LooseChargedIsoPFTau27_plusL1Tau32")
    elif(i==numberOfHLTTriggers+2):
    	name = ("hasHLTditauPath_11or20or21")#_TightTau35orMediumTau40TightIDorTightTau40_plusL1Tau32")
    elif(i==numberOfHLTTriggers+3):
    	name = ("hasHLTditauPath_9or10or11")#_TightTau35TightIDor_MediumTau35TightIDplusHLTTau40or_TightTau35plusHLTTau40_plusL1Tau32")
    tOut.Branch(name, hltPathTriggered_OS[i], name+"/I")

#tOut.Branch("isoHLT", hltPathTriggered_OS[6], name+"/I")

tOut.Branch("bkgSubW", bkgSubW, "bkgSubW/D")
tOut.Branch("bkgSubANDpuW", bkgSubANDpuW, "bkgSubANDpuW/D")

nentries = tIn.GetEntries()
for ev in range (0, nentries):
    tIn.GetEntry(ev)
    if (ev%10000 == 0) : print ev, "/", nentries

    if abs(tIn.tauEta) > 2.1:
        continue

    if saveOnlyOS and not tIn.isOS:
        continue

    for i in range (0, len(pt)):
        briso[i][0] = 0
        brnoiso[i][0] = 0

    for i in range (0, numberOfHLTTriggersForFit):
        hltPathTriggered_OS[i][0] = 0

    L1iso = True if tIn.l1tIso == 1 else False
    L1pt = tIn.l1tPt
    for i in range(0, len(pt)):
        # print L1pt, pt[i]
        #
        if L1pt > pt[i]:
            brnoiso[i][0] = 1
            # print "SUCCESS!! ", brnoiso[i]
            if L1iso:
                briso[i][0] = 1

    triggerBits = tIn.tauTriggerBits
    HLTpt = tIn.hltPt

    for bitIndex in range(0, numberOfHLTTriggers):
	import itertools as it
    	if bitIndex in it.chain(range(6, 13), range(19, 23)):   # apply this L1 cut only for di-tau triggers
            if (bitIndex==9 or bitIndex==10):
                if ((triggerBits >> bitIndex) & 1) == 1 and (L1pt>=32) and HLTpt>40: #and (L1iso):
                    hltPathTriggered_OS[bitIndex][0] = 1
                else:
                    hltPathTriggered_OS[bitIndex][0] = 0
            else:
                if ((triggerBits >> bitIndex) & 1) == 1 and (L1pt>=32): #and (L1iso):
                    hltPathTriggered_OS[bitIndex][0] = 1
                else:
                    hltPathTriggered_OS[bitIndex][0] = 0           
        else:
            if ((triggerBits >> bitIndex) & 1) == 1: #and (L1pt>=32): #and (L1iso):
            	hltPathTriggered_OS[bitIndex][0] = 1
            else:
                hltPathTriggered_OS[bitIndex][0] = 0
                        
        if(bitIndex==13):	
            if (((triggerBits >> bitIndex) & 1) == 1 and L1pt>=26 and HLTpt>30):
                hltPathTriggered_OS[numberOfHLTTriggers][0] = 1	
            else:
                hltPathTriggered_OS[numberOfHLTTriggers][0] = 0

            if ((triggerBits >> bitIndex) & 1) == 1:
                hltPathTriggered_OS[numberOfHLTTriggers+1][0] = 1
            else:
                hltPathTriggered_OS[numberOfHLTTriggers+1][0] = 0       		

    if (((((triggerBits >> 11) & 1) == 1) or (((triggerBits >> 20) & 1) == 1) or (((triggerBits >> 21) & 1) == 1))  and L1pt>=32):
        hltPathTriggered_OS[numberOfHLTTriggers+2][0] = 1
    else:
        hltPathTriggered_OS[numberOfHLTTriggers+2][0] = 0
        
    if (((((triggerBits >> 9) & 1) == 1 and HLTpt>40) or (((triggerBits >> 10) & 1) == 1 and HLTpt>40) or (((triggerBits >> 11) & 1) == 1))  and L1pt>=32):
        hltPathTriggered_OS[numberOfHLTTriggers+3][0] = 1
    else:
        hltPathTriggered_OS[numberOfHLTTriggers+3][0] = 0
		
    bkgSubW[0] = 1. if tIn.isOS else -1.
    #if (L1pt > 26) and (L1iso) and (HLTpt > 32) and (((triggerBits >> 2) & 1) == 1):
    #    hltPathTriggered_OS[6][0] = 1
    #else:
    #    hltPathTriggered_OS[6][0] = 0

    if not "Data" in fname:
        puweight = tIn.puweight
    else:
        puweight = 1

    bkgSubANDpuW[0] = bkgSubW[0]*puweight

    #Mass cuts, mt and mvis
    if(tIn.mT < 30 and tIn.mVis >40 and tIn.mVis < 80): # and tau_genindex == 5): for tau gen matching
        # for removing the disabled PS columns:
        if(disabledPScolumns):
            if((RunNumber<305177 and PS_column>=2) or (RunNumber>=305178 and RunNumber<=305387 and PS_column>=2 and PS_column!=10) or (RunNumber>=305388 and PS_column>=3 and PS_column!=11 and PS_column!=12)):
                tOut.Fill()
        else:
            tOut.Fill()

tOutNames.Write()
tOut.Write()
fOut.Close()
