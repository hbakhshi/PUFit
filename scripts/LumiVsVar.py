import ROOT

fLumi = ROOT.TFile.Open("../data/F7056Lumi.root")
tlumi = fLumi.LumiInfo
tlumi.BuildIndex("Run" , "LS")

def GetLumi(run, ls , bx , detector):
    if run and ls:
        tlumi.GetEntryWithIndex( run , ls )
    return getattr( tlumi , detector )[bx]

import array

f = ROOT.TFile.Open('../data/outnew_ZeroBiasF7056.root')
tree = f.Events

events = tree.GetEntries()
newfile = ROOT.TFile.Open('newfilename.root','RECREATE')
newtree = tree.CloneTree(0)


allBranches = {}
for ll in ['Del', 'Rec']:
    for nt in ['pcc' , 'hfoc' , 'bcm1f' , 'pltzero' , 'hfet']:
        bname = '{0}{1}'.format(nt,ll)
        allBranches[ bname ] = array.array('d' , [0.0] )
        newBranch = newtree.Branch( bname , allBranches[ bname ], '{0}/D'.format(bname) )
        
for i in range(events):
    tree.GetEntry(i)

    run = int( tree.GetLeaf( "run" ).GetValue() )
    ls = int( tree.GetLeaf( "lumi" ).GetValue() )
    bx = int( tree.GetLeaf( "bx" ).GetValue() )

    for branch in allBranches:
        allBranches[branch][0] = GetLumi( run , ls , bx , branch )

    newtree.Fill()

    if i % 300000 == 0:
	print(i,events,run,ls,bx,allBranches)

newtree.Write()
newfile.Close()
