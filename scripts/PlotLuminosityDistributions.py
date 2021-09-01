import ROOT

allFills = { 7056:[ROOT.kRed , 3000], 6413:[ROOT.kBlue , 50000]}

for fill in allFills.keys():
    print(fill)
    f = ROOT.TFile.Open("../data/outnew_ZeroBiasF{0}.root".format(fill))
    fvals = allFills[fill]
    events = f.Get("Events")
    print( events.Draw("luminosity*1000000000>>hlumi{0}( 50 , 0 , 200)".format(fill),"luminosity > -1 && luminosity*1000000000 < {0}".format(fvals[1]) , 'goff') )
    h = ROOT.gDirectory.Get("hlumi{0}".format(fill))
    h.SetDirectory(0)
    h.Scale(1.0 /h.Integral() )
    h.SetMarkerStyle(ROOT.kFullCircle)
    h.SetMarkerColor( fvals[0] )
    h.SetLineColor( fvals[0] )
    h.SetTitle( "Fill #{0}".format( fill ) )
    h.GetXaxis().SetTitle("Luminosity [#mub^{-1}]")
    allFills[fill].append(h)
    f.Close()

c = ROOT.TCanvas("LuminosityDistribution")
hcounter = 0 
for _,finfo in allFills.items():    
    h = finfo[2]
    #h.Draw( "PLC PMC" if hcounter==0 else "SAME PLC PMC" )
    h.Draw( "" if hcounter==0 else "SAME" )
    hcounter += 1
c.SaveAs("LuminosityDistribution.root")
