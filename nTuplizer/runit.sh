#! /bin/bash

cd /afs/cern.ch/user/c/cmstandi/Farbod
export PATH=/afs/cern.ch/user/c/cmstandi/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda3/bin:$PATH

runNumber=$1
WDIR=/eos/user/c/cmstandi/Farbod/R${runNumber}/
mkdir -p $WDIR
normtags=('bcm1f' 'hfoc' 'pcc' 'PHYSICS' 'pltzero')

for normtag in ${normtags[@]}
do
    #brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_${normtag}.json -r $runNumber --byls -o $WDIR/${normtag}.csv --output-style csv --xing
    echo "brilcalc step skipped"
done

./AnalyzeBxLumi2.py --run ${runNumber} --wd ${WDIR}
