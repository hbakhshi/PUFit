import ROOT

fSim = ROOT.TFile.Open("../data/out_2018_SingleNeutrinovsZeroBias.root")

tune = 'TuneCP1'
c = ROOT.TCanvas("allPUS")
vars = {'nVertices':[1], 'nChargedHadrons':[10] , 'fixedGridRhoFastjetCentralChargedPileUp':[1]}
c.Divide(1, len(vars) )
for vi in range( len(vars)):
    vname = vars.keys()[vi]
    dirName = "SingleNuZeroBias/{0}/{1}/latest/All/".format(vname , tune)
    h = fSim.Get("{0}/{1}".format( dirName , vname))

    nPuBins = 71# h.GetNbinsY()
    puFirst = h.GetYaxis().GetFirst()
    puLast = h.GetYaxis().GetLast()

    #c = ROOT.TCanvas("allPUS_{0}".format(vname))
    c.cd( vi+1 )
    for puBin in range(nPuBins):
        puBin += 1
        if puBin % 10:
            continue
        pu = h.GetYaxis().GetBinLowEdge( puBin )
        h1d = h.ProjectionX("pu{0}_{1}".format(puBin, vname) , puBin , puBin)
        h1d.Rebin( vars[vname][0] )
        h1d.Scale( 1.0/h1d.Integral() )
        h1d.SetTitle( "PU={0}".format(puBin) )
        h1d.SetMarkerStyle(ROOT.kFullCircle)
        h1d.GetXaxis().SetTitle( vname )
        h1d.Draw( "PLC PMC CPL" if puBin==1 else "SAME PLC PMC CPL" )
    #canvases.append( c )
    
fout = ROOT.TFile.Open("simulation_vsPU.root" , 'recreate')
fout.cd()
c.Write()
fout.Close()
fSim.Close()
