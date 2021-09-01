import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

NOMINALXSEC=69200

f = ROOT.TFile.Open("data_latest_eraF.root")

c = ROOT.TCanvas("cc" , "" )
saveOpt = ""
for i in range(830 ,1171):
    h1 = f.Get("h_{0}".format( i ) )
    if not h1:
        print("ninteractions in data for pu " ,i ," is not found")
        continue
    h1.Scale( 1.0 / h1.Integral() )
    h1.SetTitle( 'xSection = {0}'.format( NOMINALXSEC + (i-1000)*NOMINALXSEC/1000 ) )
    h1.SetLineWidth( 2 ) 
    h1.Draw( "L" )
    c.SaveAs( "a.gif+5" )

    
