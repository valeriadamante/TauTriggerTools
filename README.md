# TauTagAndProbe
Set of tools to evaluate tau trigger performance on T&amp;P

### How to install

```
cmsrel CMSSW_13_0_3
cd CMSSW_13_0_3/src
cmsenv
git cms-init

#clone the tool
git clone https://github.com/vmuralee/TauTriggerTools.git
git checkout Run2023
scram b -j4
```

### To run locally

```
cmsRun TauTagAndProbe/test/produceTuples.py inputFileList=Run2023C.txt period=Run2022 isMC=False runDeepTau=True maxEvents=100 outputTupleFile=run2023C.root globalTag=130X_dataRun3_HLT_v2
```

To list all the available options run:
```
python TauTriggerTools/TauTagAndProbe/test/produceTuples.py help
```
If you are interested to submit on crab use the following step.
### How to submit jobs on CRAB

Use the crab configutation file, edit the configuration with appropriate input dataset, output directory and lumimask.
``` 
crab submit TauTriggerTools/TauTagAndProbe/test/crabConfigForData.py

```


### Producing turn-On curves
The plotting script,
```
python3 TauTagAndProbe/python/createTurnOn.py --input  /eos/home-v/vmuralee/run3_tuples/SingleMuon2022*.root --selection DeepTau --var tau_pt --output example --channel ditau
```
