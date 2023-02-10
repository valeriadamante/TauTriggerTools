from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

config = config()

config.General.workArea = 'work-area'
config.General.requestName = "DYJetsToLL_Run2022postEE"
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'produceTuples.py'

config.JobType.maxMemoryMB =2000
config.JobType.numCores = 1

config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Summer22EEMiniAODv3-forPOG_124X_mcRun3_2022_realistic_postEE_v1-v3/MINIAODSIM'
#'/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Summer22MiniAODv3-forPOG_124X_mcRun3_2022_realistic_v12-v4/MINIAODSIM'
#'/Muon/Run2022G-PromptReco-v1/MINIAOD'
config.Data.inputDBS = "global"
config.Data.allowNonValidInputDataset = True
#config.Data.lumiMask = '/afs/cern.ch/work/v/vmuralee/public/GoldenJson/2022/Cert_Collisions2022_eraG_362433_362760_Golden.json'

config.General.transferOutputs = True
config.General.transferLogs = False
config.Data.publication = False

config.Site.storageSite = 'T2_CH_CERN'
config.Data.outLFNDirBase = "/store/group/phys_tau/vmuralee/run3_tuples/"


config.JobType.allowUndistributedCMSSW = True
config.JobType.pyCfgParams = ['period=Run2022', 'isMC=True', 'runDeepTau=True', 'globalTag=124X_mcRun3_2022_realistic_v12']
config.Data.unitsPerJob = 1000
config.Data.splitting = "Automatic"

