import ROOT
import sys

fn = sys.argv[1]
FillN = 0
var = ""
for fp in fn.split('/'):
    if 'Fill' in fp:
        FillN = fp[4:]
    if fp in ["nVertices", "nGoodVertices","nChargedHadrons","fixedGridRhoAll","fixedGridRhoFastjetAll" ,"fixedGridRhoFastjetAllCalo" , "fixedGridRhoFastjetCentral" ,"fixedGridRhoFastjetCentralCalo" ,"fixedGridRhoFastjetCentralChargedPileUp" ,"fixedGridRhoFastjetCentralNeutral" ,"nMus","nEles" ,"nLostTracks","nPhotons","nNeutralHadrons"]:
        var = fp
f = ROOT.TFile.Open(fn)

rng = sys.argv[2]
ws = f.Get("{0}/ws_{0}".format( rng ) )
lvar = ws.var("luminosity")
lvar.setBins(1000)
lframe = lvar.frame()
ws.data("{1}_lumi{0}".format(rng , var) ).plotOn(lframe)
lframe.Draw()
  

xsecmin = 60
xsecmax = 80
nbins = 500
xsections = { i:xsecmin+i*(xsecmax-xsecmin)/nbins for i in range( nbins ) }


c = ROOT.TCanvas("F{0}{1}".format(FillN , rng))
ROOT.gStyle.SetPalette( 95 )
ROOT.gStyle.SetOptTitle(False)
opt = "PLC PMC CP"
for i,xsec in xsections.items():
    if xsec not in [60,65,70,75,80]:
        continue
    print(i,xsec)
    hPU = f.Get("{0}/PUProfiles/hPuForXSec_{1}".format( rng , i ) )
    hPU.SetTitle( "XSection={0} mb".format( int(xsec) ) )
    hPU.GetXaxis().SetTitle("PU")
    hPU.GetYaxis().SetTitle("Probability")
    hPU.SetStats(0)
    hPU.SetMarkerStyle( 20 )
    hPU.SetMarkerSize( 1.2 )
    hPU.SetLineWidth(3)
    hPU.Draw(opt)
    
    if "SAME" not in opt:
        opt += " SAME"
c.BuildLegend()

latex = ROOT.TLatex()
latex.SetTextSize(0.05);
if len(sys.argv) > 3:
    rngName = sys.argv[3]
else:
    rngName = rng
latex.DrawLatexNDC( 0.1 , 0.95 , "Fill {0}, {1}".format(FillN , rngName));
