#!/usr/bin/env python
"""
This is a small script that submits a config over many datasets
"""
import os
from optparse import OptionParser

def make_list(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def createBash():

    BASH_SCRIPT = '''
#this is not meant to be run locally
#
echo Check if TTY
if [ "`tty`" != "not a tty" ]; then
  echo "YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES"
else
###ls -lR .
echo "ENV..................................."
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
rm -rf $CMSSW_BASE/lib/
rm -rf $CMSSW_BASE/src/
rm -rf $CMSSW_BASE/module/
rm -rf $CMSSW_BASE/python/
mv lib $CMSSW_BASE/lib
mv src $CMSSW_BASE/src
mv python $CMSSW_BASE/python
echo Found Proxy in: $X509_USER_PROXY
echo "python  jetObservables_crab_extNanoAOD_MC.py ......."
python jetObservables_crab_extNanoAOD_MC.py $1
fi
    '''
    open('runPostProc_MC.sh', 'w').write(BASH_SCRIPT.format(**options.__dict__))


def submitJobs( job, inputFiles, unitJobs ):


    from WMCore.Configuration import Configuration
    config = Configuration()

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException


    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.                                                        =
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.section_("General")
    config.General.workArea = options.dir
    config.General.transferLogs = False
    config.General.transferOutputs = True
    
    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    #config.JobType.maxMemoryMB = 5000
    
    config.section_("Data")
    #config.Data.publication = True
    #config.Data.publishDBS = 'phys03'
    config.Data.inputDBS = 'phys03'
    config.Data.ignoreLocality = True
   
    config.section_("Site")
    config.Site.storageSite = options.storageSite
    #config.Site.whitelist = ['T1_US_FNAL','T2_CH_CSCS','T3_US_FNALLPC']
    #config.Site.blacklist = ['T2_US_Florida','T3_TW_*','T2_BR_*','T2_GR_Ioannina','T2_BR_SPRACE','T2_RU_IHEP','T2_PL_Swierk','T2_KR_KNU','T3_TW_NTU_HEP']


    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print 'Cannot execute command'
            print hte.headers


    requestname = 'jetObservables_'+ job + '_' +options.version
    print requestname
    config.JobType.scriptExe = 'runPostProc_MC.sh'
    config.JobType.inputFiles = [ 'PSet.py','runPostProc_MC.sh', 'boostedWtagging_crab_skimNanoAOD.py' ,'haddnano.py', 'keep_and_drop.txt']
    config.JobType.sendPythonFolder  = True

    #config.Data.userInputFiles = inputFiles
    config.Data.inputDataset = inputFiles
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = unitJobs
    #config.Data.outputPrimaryDataset = job

    # since the input will have no metadata information, output can not be put in DBS
    config.JobType.outputFiles = [ 'boostedWtagging_nanoskim.root']
    config.Data.outLFNDirBase = '/store/user/'+os.environ['USER']+'/boostedWtaggingSF/'

    if len(requestname) > 100: requestname = (requestname[:95-len(requestname)])
    print 'requestname = ', requestname
    config.General.requestName = requestname
    config.Data.outputDatasetTag = requestname
    print 'Submitting ' + config.General.requestName + ', dataset = ' + job
    print 'Configuration :'
    print config
    try :
        from multiprocessing import Process

        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
        #submit(config)
    except :
        print 'Not submitted.'



if __name__ == '__main__':

    usage = ('usage: python submit_all.py -c CONFIG -d DIR -f DATASETS_FILE')

    parser = OptionParser(usage=usage)
    parser.add_option(
            "-D", "--dir",
            dest="dir", default="crab_projects",
            help=("The crab directory you want to use "),
            metavar="DIR" )
    parser.add_option(
        "-d", "--datasets",
            dest="datasets", default='all',
            help=("File listing datasets to run over"),
            metavar="FILE" )
    parser.add_option(
            "-s", "--storageSite",
            dest="storageSite", default="T3_CH_PSI",
            help=("Storage Site"),
            metavar="SITE")
    parser.add_option(
            "-v", "--version",
            dest="version", default="106X_UL_v0",
            help=("Version of output"),
            metavar="VER")


    (options, args) = parser.parse_args()


    dictSamples = {}
    '''

    dictSamples['TTbar_1'] = [ '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/algomez-TTTuneCUETP8M2T413TeV-powheg-pythia8RunIISummer16MiniAODv3-PUMoriond1794XmcRun2-dafc15ff64439ee3efd0c8e48ce3e57e/USER', 1 ]

    dictSamples['TTbar_2'] = ['/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-TTJetsTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv3-PUMoriond1794XmcRun2-dafc15ff64439ee3efd0c8e48ce3e57e/USER', 1]

    dictSamples[ 'QCD_0' ] = [ '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/kadatta-QCDPt-15to7000TuneCUETP8M1FlatP613TeVpythia8RunIISummer16MiniAODv3-PUMoriond1794X-3de7f16b11abe7d2f2c8fb8b12121ea5/USER', 1 ]
    
    dictSamples['SingleTop_1'] = ['/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/algomez-STt-channelantitop4finclusiveDecays13TeV-powhegV2-madspin-pythia8TuneCUETP8M1-dafc15ff64439ee3efd0c8e48ce3e57e/USER',1]

    dictSamples['SingleTop_2'] = ["/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/algomez-STt-channeltop4finclusiveDecays13TeV-powhegV2-madspin-pythia8TuneCUETP8M1-dafc15ff64439ee3efd0c8e48ce3e57e/USER",1]

    dictSamples['SingleTop_3'] = ["/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/algomez-STtWantitop5finclusiveDecays13TeV-powheg-pythia8TuneCUETP8M2T4-dafc15ff64439ee3efd0c8e48ce3e57e/USER",1]

    dictSamples['SingleTop_4'] = ["/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/algomez-STtWtop5finclusiveDecays13TeV-powheg-pythia8TuneCUETP8M2T4-dafc15ff64439ee3efd0c8e48ce3e57e/USER",1]

    dictSamples['Wjets_1'] = ['/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/algomez-WJetsToLNuTuneCUETP8M113TeV-amcatnloFXFX-pythia8RunIISummer16MiniAODv3-PUMoriond1794X-dafc15ff64439ee3efd0c8e48ce3e57e/USER', 1]

    dictSamples['Wjets_2'] = ['/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/algomez-WJetsToLNuTuneCUETP8M113TeV-amcatnloFXFX-pythia8RunIISummer16MiniAODv3-PUMoriond1794X_ext2-v1-dafc15ff64439ee3efd0c8e48ce3e57e/USER', 1]
    '''

    processingSamples = {}
    if 'all' in options.datasets:
        for sam in dictSamples: processingSamples[ sam ] = dictSamples[ sam ]
    else:
        for sam in dictSamples:
            if sam.startswith( options.datasets ): processingSamples[ sam ] = dictSamples[ sam ]

    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

    for isam in processingSamples:

        print('Creating bash file...')
        createBash()

        print ("dataset %s has %d files" % (processingSamples[isam], len(processingSamples[isam][0])))
        submitJobs( isam, processingSamples[isam][0], processingSamples[isam][1] )
