from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

config = config()

config.General.workArea = 'work-area'
config.General.requestName = "Muon_Run2022F"
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'produceTuples.py'

config.JobType.maxMemoryMB =2000
config.JobType.numCores = 1

config.Data.inputDataset = '/Muon/Run2022F-PromptReco-v1/MINIAOD'
config.Data.inputDBS = "global"
config.Data.allowNonValidInputDataset = True
config.Data.lumiMask = '/afs/cern.ch/work/v/vmuralee/public/GoldenJson/2022/Cert_Collisions2022_eraF_360390_360491_Golden.json'

config.General.transferOutputs = True
config.General.transferLogs = False
config.Data.publication = False

config.Site.storageSite = 'T2_IN_TIFR'
config.Data.outLFNDirBase = "/store/user/vmuralee/run3_2022F"


config.JobType.allowUndistributedCMSSW = True
config.JobType.pyCfgParams = ['period=Run2022', 'isMC=False', 'runDeepTau=True', 'globalTag=124X_dataRun3_HLT_Pixel_w37_2022_v2']
config.Data.unitsPerJob = 1000
config.Data.splitting = "Automatic"

