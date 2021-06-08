import ROOT

lumi = ROOT.RooRealVar("lumi" , "lumi" , 0 , 10000 )

lumiProfileMean = ROOT.RooConstVar("lumiProfileMean" , "" , 1000 )
lumiProfileSigma = ROOT.RooConstVar("lumiProfileSigma" , "" , 1000 )
lumiProfile = ROOT.RooGaussian("lumiProfile" , "" , lumi , lumiProfileMean , lumiProfileSigma )

pu = ROOT.RooRealVar("nInt" , "nInt" , 0 , 100)
pu.setBins(100)

xsection = ROOT.RooRealVar("xsection" , "" ,  4000 , 6000)
deltaT = ROOT.RooConstVar("deltaT" , "deltaT" , 1.0/100000 )
mu = ROOT.RooProduct("mu" , "mu" , ROOT.RooArgList(lumi , xsection , deltaT ) )

puForLumi = ROOT.RooPoisson("puForLumi" , "puForLumi" , pu , mu )

puProfileT = ROOT.RooProdPdf("puProfileT" , "puProfileT" , ROOT.RooArgList( lumiProfile , puForLumi )  )

puProfile = puProfileT.createProjection( ROOT.RooArgSet( lumi ) )


fSim = ROOT.TFile.Open("../data/SingleNeutrino_CP1.root")
tree = fSim.Get("PUAnalyzer/Trees/Events")

var1 = ROOT.RooRealVar("nVertices" , "nVertices" , 0 , 160 )
ds = ROOT.RooDataSet( "ds" , "dataset" , tree , ROOT.RooArgSet(var1 , pu ) )
h2dSim = ROOT.RooDataHist("h2dSim" , "h2dSim" , ROOT.RooArgSet(var1 , pu ) , ds )
pdfVarnInt = ROOT.RooHistPdf( "pdfVarnInt" , "pdfVarnInt" , ROOT.RooArgSet(var1 , pu ) , h2dSim )

pdfVar = ROOT.RooProdPdf( "pdfVar" , "pdfVar" 


frame = pu.frame()
puProfile.plotOn(frame)
canvas = ROOT.TCanvas("C")
frame.Draw()



