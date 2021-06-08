import ROOT
#ROOT.gROOT.ProcessLine(".L RooMinBiasXSection.C+")
PRJDIR="/home/hbakhshi/Documents/PU/MainFiles"
ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(PRJDIR) )
xsec = ROOT.RooRealVar("xsection","xsection", 58128 , 80895 )

f = ROOT.TFile.Open("{0}/data/SingleNeutrino_CP1.root".format(PRJDIR))
hMCPUDIST = f.Get("/PUAnalyzer/nTruInteractions/nTruInteractions_SingleNeutrino_CP1_postbug")

a = ROOT.XSectionWeight( "{0}/data/data_latest_eraF.root".format(PRJDIR) , hMCPUDIST , xsec )

tree = f.Get("/PUAnalyzer/Trees/Events")


nVertices = ROOT.RooRealVar( "nVertices" , "Number of Vertices" , 0)
#fixedGridRhoAll = ROOT.RooRealVar('fixedGridRhoAll' , 'Fixed Grid Rho all' , 0 )

nBins = 5

vars = ROOT.RooArgList(nVertices) #, fixedGridRhoAll)
b = ROOT.MultiBinMaker( tree , vars , nBins , True )

bCat = ROOT.RooMultiDimCategory("ProjectedVar" , "ProjectedVar" , vars , b.getKDBinning() )

c = ROOT.RooNdimMinBiasXSection("XSectionPDF" , "" , b , a , vars )
#c = ROOT.RooNdimMinBiasXSection("XSectionPDF" , "" , b , a , bCat )

d = ROOT.TCanvas("C")
d.Divide( nBins/5 , 5 )
frames = {}
for i in range(nBins):
    bcenters = b.GetBinCenter(i)
    nVertices.setVal( bcenters[0] )
    # fixedGridRhoAll.setVal( bcenters[1] )
    fff = xsec.frame()
    c.plotOn( fff )
    d.cd(i+1)
    fff.Draw()
    frames[i] = fff

ee = ROOT.TCanvas("CXSecs")
ee.Divide(6 , 6)
for i in range(36):
    xsecval = 69200 * (100 - i + 18)/100
    xsec.setVal(xsecval)
    fff = bCat.frame()
    c.plotOn(fff)
    ee.cd(i+1)
    fff.Draw()
    frames[len(frames)] = fff


fdata = ROOT.TFile.Open("{0}/data/ZeroBiasF.root".format(PRJDIR))
datatree = fdata.Get("/PUAnalyzer/Trees/Events")
dataset = ROOT.RooDataSet("dataset" , "dataset" , datatree , vars )
dataset.addColumn(bCat)
fitres = c.fitTo( dataset , ROOT.RooFit.NumCPU(6) , ROOT.RooFit.Minimizer("Minuit2") , ROOT.RooFit.Minos(True) , ROOT.RooFit.Save(True) ) #, ROOT.RooFit.Extended(True) , ROOT.RooFit.InitialHesse(True)
f = bCat.frame()
dataset.plotOn(f)
c.plotOn(f)
kk = ROOT.TCanvas("data")
f.Draw()

#c.fitTo(dataset)
