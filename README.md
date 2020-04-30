# TauTagAndProbe
Set of tools to evaluate tau trigger performance on T&amp;P

### How to install

```
cmsrel CMSSW_10_2_16
cd CMSSW_10_2_16/src
cmsenv
git cms-init
git cms-addpkg RecoMET/METFilters
git cms-merge-topic cms-egamma:EgammaPostRecoTools
# if you want to run DeepTau
git cms-merge-topic -u cms-tau-pog:CMSSW_10_2_X_tau-pog_DeepTau2017v2p1_nanoAOD

git clone https://github.com/vmuralee/TauTriggerTools.git
git checkout new-ana
scram b -j4
```

### How to run

```
cmsRun TauTriggerTools/TauTagAndProbe/test/produceTuples.py inputFileList=RelValZpTT_1500_13UP18.txt period=Run2018 isMC=True runDeepTau=False pureGenMode=True globalTag=102X_upgrade2018_realistic_v15 maxEvents=-1 outputTupleFile=RelValZpTT_1500_13UP18_CMSSW_10_6_2.root
```

To list all the available options run:
```
python TauTriggerTools/TauTagAndProbe/test/produceTuples.py help
```

### How to submit jobs on CRAB

Submitting task:
```
crab_submit.py --workArea work-area --cfg TauTriggerTools/TauTagAndProbe/test/produceTuples.py --site T2_IN_TIFR --output trigger_tuples mytasks.txt
```
Example of mytaks.txt:
```
period=Run2018 isMC=True runDeepTau=False pureGenMode=True globalTag=102X_upgrade2018_realistic_v15

RelValZpTT_1500_13UP18 /RelValZpTT_1500_13UP18/CMSSW_10_6_2-PUpmx25ns_106X_upgrade2018_realistic_v6_ul18hlt_premix_rs-v1/MINIAODSIM
RelValQQH1352T_13 /RelValQQH1352T_13/CMSSW_10_2_5-PUpmx25ns_102X_upgrade2018_realistic_v15_ECAL-v1/MINIAODSIM
```
To list all the available options run:
```
crab_submit.py --help
```

Checking status of the submitted tasks:
```
crab_cmd.py --workArea work-area --cmd status
```
