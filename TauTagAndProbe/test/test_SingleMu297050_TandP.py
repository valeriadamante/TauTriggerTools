import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
process = cms.Process("TagAndProbe")

isMC = True
useGenMatch = False
useCustomHLT = False

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

#### handling of cms line options for tier3 submission
#### the following are dummy defaults, so that one can normally use the config changing file list by hand etc.

options = VarParsing.VarParsing ('analysis')
options.register ('skipEvents',
                  -1, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Number of events to skip")
options.register ('JSONfile',
                  "", # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "JSON file (empty for no JSON)")
if not isMC:
 	options.outputFile = 'NTuple_SingleMu_Data_2017.root'
else:	
 	options.outputFile = 'NTuple_SingleMu_DYMC_2017.root'

options.inputFiles = []
options.maxEvents  = -999
options.parseArguments()


# START ELECTRON CUT BASED ID SECTION
#
# Set up everything that is needed to compute electron IDs and
# add the ValueMaps with ID decisions into the event data stream
#

# Load tools and function definitions
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

process.load("RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi")


#**********************
dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
#**********************

process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
# overwrite a default parameter: for miniAOD, the collection name is a slimmed one
process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')

from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)

# Define which IDs we want to produce
# Each of these two example IDs contains all four standard 
my_id_modules =[
'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',   #Spring16
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',   #Spring16 HZZ
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',  #Fall17 iso
] 


#Add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)


egmMod = 'egmGsfElectronIDs'
mvaMod = 'electronMVAValueMapProducer'
setattr(process,egmMod,process.egmGsfElectronIDs.clone())
setattr(process,mvaMod,process.electronMVAValueMapProducer.clone())
process.electrons = cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod))


# =================================
# START TAU MVA BASED ID SECTION  -- OLD WAY --
# =================================
from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')
from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import *

def loadMVA_WPs_run2_2017(process):

      for training, gbrForestName in tauIdDiscrMVA_trainings_run2_2017.items():
         process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
            cms.PSet(
               record = cms.string('GBRWrapperRcd'),
               tag = cms.string("RecoTauTag_%s%s" % (gbrForestName, tauIdDiscrMVA_2017_version)),
               label = cms.untracked.string("RecoTauTag_%s%s" % (gbrForestName, tauIdDiscrMVA_2017_version))
            )
         )

         for WP in tauIdDiscrMVA_WPs_run2_2017[training].keys():
            process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
               cms.PSet(
                  record = cms.string('PhysicsTGraphPayloadRcd'),
                  tag = cms.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, tauIdDiscrMVA_2017_version, WP)),
                  label = cms.untracked.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, tauIdDiscrMVA_2017_version, WP))
               )
            )

         process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
            cms.PSet(
               record = cms.string('PhysicsTFormulaPayloadRcd'),
               tag = cms.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, tauIdDiscrMVA_2017_version)),
               label = cms.untracked.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, tauIdDiscrMVA_2017_version))
            )
)

# 2017 v1
tauIdDiscrMVA_trainings_run2_2017 = {
  'tauIdMVAIsoDBoldDMwLT2017' : "tauIdMVAIsoDBoldDMwLT2017",
  }
tauIdDiscrMVA_WPs_run2_2017 = {
  'tauIdMVAIsoDBoldDMwLT2017' : {
    'Eff95' : "DBoldDMwLTEff95",
    'Eff90' : "DBoldDMwLTEff90",
    'Eff80' : "DBoldDMwLTEff80",
    'Eff70' : "DBoldDMwLTEff70",
    'Eff60' : "DBoldDMwLTEff60",
    'Eff50' : "DBoldDMwLTEff50",
    'Eff40' : "DBoldDMwLTEff40"
    }
  }
tauIdDiscrMVA_2017_version = "v1"

loadMVA_WPs_run2_2017(process)

process.rerunDiscriminationByIsolationMVArun2v1raw = patDiscriminationByIsolationMVArun2v1raw.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   loadMVAfromDB = cms.bool(True),
   mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1"),  # name of the training you want to use: training with 2017 MC_v1 for oldDM
   mvaOpt = cms.string("DBoldDMwLTwGJ"), # option you want to use for your training (i.e., which variables are used to compute the BDT score)
   requireDecayMode = cms.bool(True),
   verbosity = cms.int32(0)
)

process.rerunDiscriminationByIsolationMVArun2v1VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   toMultiplex = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw'),
   key = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw:category'),
   loadMVAfromDB = cms.bool(True),
   mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_mvaOutput_normalization"), # normalization fo the training you want to use
   mapping = cms.VPSet(
      cms.PSet(
         category = cms.uint32(0),
         cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff90"), # this is the name of the working point you want to use
         variable = cms.string("pt"),
      )
   )
)

# here we produce all the other working points for the training
process.rerunDiscriminationByIsolationMVArun2v1VVLoose = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationMVArun2v1VVLoose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff95")
process.rerunDiscriminationByIsolationMVArun2v1Loose = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationMVArun2v1Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff80")
process.rerunDiscriminationByIsolationMVArun2v1Medium = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationMVArun2v1Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff70")
process.rerunDiscriminationByIsolationMVArun2v1Tight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationMVArun2v1Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff60")
process.rerunDiscriminationByIsolationMVArun2v1VTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationMVArun2v1VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff50")
process.rerunDiscriminationByIsolationMVArun2v1VVTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationMVArun2v1VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff40")

# this sequence has to be included in your cms.Path() before your analyzer which accesses the new variables is called.
process.rerunMvaIsolation2SeqRun2 = cms.Sequence(
   process.rerunDiscriminationByIsolationMVArun2v1raw
   *process.rerunDiscriminationByIsolationMVArun2v1VLoose
   *process.rerunDiscriminationByIsolationMVArun2v1VVLoose
   *process.rerunDiscriminationByIsolationMVArun2v1Loose
   *process.rerunDiscriminationByIsolationMVArun2v1Medium
   *process.rerunDiscriminationByIsolationMVArun2v1Tight
   *process.rerunDiscriminationByIsolationMVArun2v1VTight
   *process.rerunDiscriminationByIsolationMVArun2v1VVTight
)


# embed new id's into new tau collection
embedID = cms.EDProducer("PATTauIDEmbedder",
   src = cms.InputTag('slimmedTaus'),
   tauIDSources = cms.PSet(
      byIsolationMVArun2017v1DBoldDMwLTraw2017 = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw'),
      byVLooseIsolationMVArun2017v1DBoldDMwLT2017 = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1VLoose'),
      byVVLooseIsolationMVArun2017v1DBoldDMwLT2017 = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1VVLoose'),
      byLooseIsolationMVArun2017v1DBoldDMwLT2017 = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1Loose'),
      byMediumIsolationMVArun2017v1DBoldDMwLT2017 = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1Medium'),
      byTightIsolationMVArun2017v1DBoldDMwLT2017 = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1Tight'),
      byVTightIsolationMVArun2017v1DBoldDMwLT2017  = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1VTight'),
      byVVTightIsolationMVArun2017v1DBoldDMwLT2017  = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1VVTight'),
   ),
   )

setattr(process, "NewTauIDsEmbedded", embedID)

# inclusion in the process
#process.taus = cms.Sequence(getattr(process, "NewTauIDsEmbedded"))



"""
# =================================
# START TAU MVA BASED ID SECTION   -- NEW WAY --
# =================================

from TauTagAndProbe.TauTagAndProbe.runTauIdMVA import TauIDEmbedder

toKeep = []
toKeep.extend(("2017v1","2017v2"))

na = TauIDEmbedder(process, cms,
    debug=True,
    toKeep = toKeep
)
na.runTauID()
"""

if not isMC:
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '94X_dataRun2_ReReco_EOY17_v2' # 92X_dataRun2_HLT_v7'
    process.load('TauTagAndProbe.TauTagAndProbe.tagAndProbe_2017_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
          #  '/store/data/Run2017E/SingleMuon/MINIAOD/17Nov2017-v1/50000/000DCB8B-2ADD-E711-9100-008CFAF35AC0.root'
           '/store/data/Run2017B/SingleMuon/MINIAOD/31Mar2018-v1/100000/001642F1-6638-E811-B4FA-0025905B857A.root'
        ),
    )



else:
    process.GlobalTag.globaltag = '94X_mc2017_realistic_v14'
    process.load('TauTagAndProbe.TauTagAndProbe.MCanalysis_2017_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(            
        #   '/store/mc/RunIIFall17MiniAOD/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/20000/12DB4A06-65D7-E711-8DA4-0CC47A78A456.root'
	'/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/20000/00D13F2E-6F44-E811-923E-001E0BED0560.root'

        )
    )


if useCustomHLT:
    process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","MYHLT")
    process.Ntuplizer.triggerSet = cms.InputTag("selectedPatTriggerCustom", "", "MYHLT")
    process.Ntuplizer.triggerResultsLabel = cms.InputTag("TriggerResults", "", "MYHLT")
    process.Ntuplizer.L2CaloJet_ForIsoPix_Collection = cms.InputTag("hltL2TausForPixelIsolation", "", "MYHLT")
    process.Ntuplizer.L2CaloJet_ForIsoPix_IsoCollection = cms.InputTag("hltL2TauPixelIsoTagProducer", "", "MYHLT")


if isMC and useGenMatch:
    process.Ntuplizer.taus = cms.InputTag("genMatchedTaus")


if options.JSONfile:
    print "Using JSON: " , options.JSONfile
    process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
    process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)


process.p = cms.Path(
    process.electrons +
	process.rerunMvaIsolation2SeqRun2 +
	getattr(process, "NewTauIDsEmbedded") +
    process.TAndPseq +
    process.NtupleSeq
)

if isMC and useGenMatch:
    process.p = cms.Path(
    	process.electrons +
		process.rerunMvaIsolation2SeqRun2 +
		getattr(process, "NewTauIDsEmbedded") +
    	process.TAndPseq +
	process.genMatchedSeq +
   	process.NtupleSeq
    )

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
