from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

config = config()

config.General.workArea = 'work-area'
config.General.requestName = "Muon_Run2022G"
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'produceTuples.py'

config.JobType.maxMemoryMB =2000
config.JobType.numCores = 1

config.Data.inputDataset = '/Muon/Run2022G-PromptReco-v1/MINIAOD'
config.Data.inputDBS = "global"
config.Data.allowNonValidInputDataset = True
config.Data.lumiMask = '/afs/cern.ch/work/v/vmuralee/public/GoldenJson/2022/Cert_Collisions2022_eraG_362433_362760_Golden.json'

config.General.transferOutputs = True
config.General.transferLogs = False
config.Data.publication = False

config.Site.storageSite = 'T2_CH_CERN'
config.Data.outLFNDirBase = "/store/group/phys_tau/vmuralee/run3_tuples/"


config.JobType.allowUndistributedCMSSW = True
config.JobType.pyCfgParams = ['period=Run2022', 'isMC=False', 'runDeepTau=True', 'globalTag=124X_dataRun3_HLT_v4']
config.Data.unitsPerJob = 1000
config.Data.splitting = "Automatic"

