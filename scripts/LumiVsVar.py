import csv

allRuns = {}
with open('f7056.csv', 'rb') as csvfile:
    fillInfo = csv.reader(csvfile, delimiter=',', quotechar='|')
    for r in fillInfo:
        if r[0][0] == '#':
            continue
        try:
            run,fill = r[0].split(':')
        except:
            print('warning0' , r[0])
            continue
        try:
            ls1,ls2 = r[1].split(':')
        except:
            print('warning1' , r[1])
            continue
        try:
            bxinfo = r[9]
        except:
            print('warning9', r)
            continue
        if ls1 != ls2:
            print( 'warning' , run , fill , ls1 , ls2)
        runi = int(run)
        filli = int(fill)
        ls = int(ls1)
        if runi not in allRuns:
            allRuns[runi] = {}
        if ls in allRuns[runi]:
            print('warning 2', run , ls )
        allbx = {}
        bxi = None
        lrec = None
        ldel = None
        for bx in bxinfo[1:-1].split(' '):
            try:
                bxi = int(bx)
                lrec = ldel = None
            except:
                if ldel == None:
                    ldel = float(bx)
                else:
                    lrec = float(bx)
                    allbx[bxi] = [ldel,lrec]
                    bxi= None
                    
        allRuns[runi][ls] = allbx

def GetLumi(run, ls , bx):
    try:
        return allRuns[run][ls][bx][0]
    except:
        return -1

import ROOT
import array

f = ROOT.TFile.Open('out_ZeroBiasF7056.root')
tree = f.PUAnalyzer.Trees.Events

events = tree.GetEntries()
leaves = 'lumi/D'
leafValues = array.array('d', [0.0])
newfile = ROOT.TFile.Open('newfilename.root','RECREATE')
newtree = tree.CloneTree(0)

newBranch = newtree.Branch( 'luminosity' , leafValues, leaves )

for i in range(events):
    tree.GetEntry(i)

    run = tree.GetLeaf( "run" ).GetValue()
    ls = tree.GetLeaf( "lumi" ).GetValue()
    bx = tree.GetLeaf( "bx" ).GetValue()

    leafValues[0] = GetLumi( run , ls, bx )

    newtree.Fill()

    if i % 300000 == 0:
	print(i,events,run,ls,bx,leafValues)

newtree.Write()
newfile.Close()
