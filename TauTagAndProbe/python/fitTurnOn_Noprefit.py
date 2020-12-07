import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()

path_prefix = '' if 'TauTriggerTools' in os.getcwd() else 'TauTriggerTools/'
sys.path.insert(0, path_prefix + 'Common/python')
from RootObjects import Histogram, Graph
