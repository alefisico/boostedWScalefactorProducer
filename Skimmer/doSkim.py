#!/Usr-/bin/env python
import os,sys
#from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from boostedWScalefactorProducer.Skimmer.python.skimmer import Skimmer

year = 2018

files = {}
files[2018] = [
  "root://cms-xrd-global.cern.ch//store/data/Run2018C/EGamma/NANOAOD/Nano1June2019-v1/230000/77B1D6B0-11DB-7D4C-83D5-5CDD162BFE61.root", 
]

if len(sys.argv)>1:
   infile = sys.argv[1].split(',')
else:
  infile = files[year] #= [
#      "root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/Nano14Dec2018_ver2-v1/40000/4BF53ABE-BB2D-B147-8BDE-888B21C3E07C.root"
#      "root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv4/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/120000/BB978C6D-1770-CB42-A45E-AFAA249DAA82.root"
#      "root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv4/ZZ_TuneCP5_13TeV-pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/110000/56817FDC-2D4C-7E4B-ABA0-9A1F7BA505C4.root"
      #"root://cms-xrd-global.cern.ch//store/data/Run2018C/EGamma/NANOAOD/Nano1June2019-v1/230000/77B1D6B0-11DB-7D4C-83D5-5CDD162BFE61.root"
#      "root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/Nano1June2019-v1/40000/CB01BD35-453E-254D-A273-A867E34D7E52.root"
#      "root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/DDC35B8C-5718-4F41-8499-EDE8E3283FF5.root"
#      "root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/120000/D23F4374-1259-174E-B968-E914679919BD.root"
  #]

if len(sys.argv)>2: outputDir = sys.argv[2]
else: outputDir = "TEST"	

if len(sys.argv)>3: name = sys.argv[3]
else: name = "test.root"

if len(sys.argv)>4: chunck = sys.argv[4]
else: chunck = ""  

#"keep_and_drop.txt"
jsonfile='./python/JSON/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'

if infile[0].find("SingleMuon")!=-1:
  channel = "mu"
  print "Processing a Single Muon dataset file..."
  p=PostProcessor(outputDir, infile, None, None, #"HLT_Mu50 && nMuon>0 && Muon_pt[0]>55. && nFatJet>0"
                    modules=[Skimmer(channel, year)],provenance=False,fwkJobReport=False,
                    jsonInput=jsonfile)
                   
elif infile[0].find("EGamma")!=-1:
  channel = "el"
  print "Processing a Single Electron dataset file..."
  p=PostProcessor(outputDir, infile, None, None, #"(event.HLT_Ele32_WPTight_Gsf || event.HLT_Ele35_WPTight_Gsf || event.HLT_Ele40_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT) && nElectron>0 && Electron_pt[0]>55. && nFatJet>0"
                    modules=[Skimmer(channel, year)],provenance=False,fwkJobReport=False,
                    jsonInput=jsonfile)
                    
else:
  print "Processing MC..."
  channel = "elmu"
  p=PostProcessor(outputDir, infile, None, None,
                    modules=[Skimmer(channel, year)],provenance=False,fwkJobReport=False, 
                    jsonInput=jsonfile)
p.run()
print "DONE"
