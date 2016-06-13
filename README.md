# TauTagAndProbe
Set of tools to evaluate tau trigger performance on T&amp;P

### Install instructions
```
cmsrel CMSSW_8_0_5
cd CMSSW_8_0_5/src
cmsenv
git clone https://github.com/l-cadamuro/TauTagAndProbe
scram b -j4
```

### Tu run on MC (no t&P, select candidates by gen matching)
```
cmsrel CMSSW_7_6_3
cd CMSSW_7_6_3/src
cmsenv
git clone https://github.com/l-cadamuro/TauTagAndProbe
scram b -j4
```
then set isMC = True in test.py
