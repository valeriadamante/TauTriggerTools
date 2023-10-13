from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

config = config()

config.General.workArea = 'work-area'
config.General.requestName = "Muon0_Run2023D"
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'produceTuples.py'

config.JobType.maxMemoryMB =2000
config.JobType.numCores = 1

config.Data.inputDataset = '/Muon0/Run2023D-PromptReco-v2/MINIAOD'
config.Data.inputDBS = "global"
config.Data.allowNonValidInputDataset = True
config.Data.lumiMask = '/afs/cern.ch/work/v/vdamante/public/CMSSW_13_0_3/src/TauTriggerTools/Cert_Collisions2023_366442_370790_Golden.json'

config.General.transferOutputs = True
config.General.transferLogs = False
config.Data.publication = False

config.Site.storageSite = 'T2_CH_CERN'
config.Data.outLFNDirBase = "/store/group/phys_tau/vdamante/run3_tuples/"


config.JobType.allowUndistributedCMSSW = True
config.JobType.pyCfgParams = ['period=Run2023', 'isMC=False', 'runDeepTau=True', 'globalTag=130X_dataRun3_HLT_v2']
config.Data.unitsPerJob = 1000
config.Data.splitting = "Automatic"

