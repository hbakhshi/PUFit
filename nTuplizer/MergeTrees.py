import ROOT
from allInfo import allInfo
import os

DIR='/eos/home-c/cmstandi/Farbod/'

allFailedRuns = []

allScripts = []
for f,runs in allInfo.items():
    runs = list( set( runs ) )
    if 1L in runs:
        continue

    year , fname = f.split('/')[-2:]
    scriptfname = '{0}/{1}/MakeAll.sh'.format( DIR , year )

    if not os.path.exists( '{0}/{1}'.format( DIR , year ) ):
        os.makedirs( '{0}/{1}'.format( DIR , year ) )
    elif os.path.exists(scriptfname):
        if scriptfname not in allScripts:
            os.remove( scriptfname )
    allScripts.append( scriptfname )
            
    allInputFiles = [ '{0}/R{1}/all.root'.format( DIR , run ) for run in runs ]
    for findex in reversed( range( len(allInputFiles) ) ):
        inputf = allInputFiles[ findex ]
        try:
            #fin = ROOT.TFile.Open( inputf )
            #tree = fin.Events
            #fin.Close()
            if not os.path.isfile( inputf ):
                raise Exception('file not found')
        except Exception as e:
            print('error reading file {0}'.format( inputf ) )
            print( e )
            allInputFiles.pop( findex )
            allFailedRuns.append( inputf )
        
    commandToRun = 'hadd -ff {0} {1};\n'.format( '{0}/{1}/{2}'.format( DIR , year , fname ) , ' '.join( allInputFiles ) )
    with open( scriptfname  , 'a' ) as fcommand:
        fcommand.write( commandToRun )

print( set(allFailedRuns) )
print( len(set(allFailedRuns)) )


print( 'run following commands to merge ntuples' )
for script in set( allScripts ):
    print( 'source {0};'.format( script ) )
