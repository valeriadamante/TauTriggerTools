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
To create the turn-On for different year data can be done using,
```
python3 TauTagAndProbe/python/TurnOnScript.py --input_run2022 /eos/home-v/vmuralee/run3_tuples/2022v1/Muon2022E.root --input_run2023 /eos/home-v/vmuralee/run3_tuples/2023/miniAOD/Muon0_Run2023C.root --input_mc /eos/home-v/vmuralee/run3_tuples/2022v1/DYJetsToLL_postEE.root --channel single_tau --selection DeepTau --output steam20 --vars tau_pt tau_eta npv --pu MyDataPileupHistogram.root
```
**--input_run2022** : input files for each run 2022 year 
**--input_run2023** : input files for each run 2023 year
**--input_mc** : input files for simulated dataset
**--channel** : all the monitoring path are available, (mutau,ditau,etau and single tau) 
**--selection** : default DeepTau 
**--output**: prefix of output file 
**--vars** : to produce efficiency in terms of pT,eta and no.primary vertices bins use following variable (tau_pt,tau_eta and npv)
**--pu** : The pileup histogram to reweight the MC sample.

The legend and label can edit inside the python script. 
