import ROOT
PRJDIR="/home/hbakhshi/Documents/PU/MainFiles"
ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(PRJDIR) )

fIn = ROOT.TFile.Open("newfilename.root")
tree = fIn.Events

vars = {"nVertices" : ROOT.RooRealVar( "nVertices" , "nVertices"  , 0 , 80 ) , #, 74
        "nGoodVertices" : ROOT.RooRealVar("nGoodVertices", "nGoodVertices", 5 , 59) , #54
        "nChargedHadrons" : ROOT.RooRealVar("nChargedHadrons", "nChargedHadrons" , 0 , 2000 ), #2000
        "fixedGridRhoAll" : ROOT.RooRealVar("fixedGridRhoAll", "fixedGridRhoAll"  , 0 , 60 ), #, 60
        "fixedGridRhoFastjetAll" : ROOT.RooRealVar("fixedGridRhoFastjetAll", "fixedGridRhoFastjetAll"  , 0 , 40 ), #40
        "fixedGridRhoFastjetAllCalo" : ROOT.RooRealVar("fixedGridRhoFastjetAllCalo", "fixedGridRhoFastjetAllCalo"  , 0 , 25 ), #25
        "fixedGridRhoFastjetCentral" : ROOT.RooRealVar("fixedGridRhoFastjetCentral", "fixedGridRhoFastjetCentral"  , 0 , 50 ), #50
        "fixedGridRhoFastjetCentralCalo" : ROOT.RooRealVar("fixedGridRhoFastjetCentralCalo", "fixedGridRhoFastjetCentralCalo"  , 0 , 20 ), #20
        "fixedGridRhoFastjetCentralChargedPileUp" : ROOT.RooRealVar("fixedGridRhoFastjetCentralChargedPileUp", "fixedGridRhoFastjetCentralChargedPileUp"  , 0 , 35 ), #35
        "fixedGridRhoFastjetCentralNeutral" : ROOT.RooRealVar("fixedGridRhoFastjetCentralNeutral", "fixedGridRhoFastjetCentralNeutral"  , 0 , 12 ),#12
        "nMus" : ROOT.RooRealVar("nMus", "nMus"  , 0 , 10 ), #10
        "nEles" : ROOT.RooRealVar("nEles" , "nEles"  , 0 , 10 ) , #10
        "nLostTracks": ROOT.RooRealVar("nLostTracks" , "nLostTracks"  , 0 , 35 ), #35
        "nPhotons" : ROOT.RooRealVar("nPhotons", "nPhotons" , 0 , 600 ), #600
        "nNeutralHadrons" : ROOT.RooRealVar("nNeutralHadrons" , "nNeutralHadrons"  , 0 , 120 ) #120
}

luminosityVar = ROOT.RooRealVar( 'luminosity' , 'luminosity' , 0 , 0.0000003 )

def MakeDS(lumiFrom , lumiTo , var , lumiRnangeName):
    ret = ROOT.RooDataSet( '{0}_lumi{1}'.format( var , lumiRnangeName ) , '{0} for lumi between {1} and {2}'.format( var , lumiFrom , lumiTo ) , 
                           tree , ROOT.RooArgSet(vars[var] , luminosityVar) , "luminosity>{0} && luminosity<{1}".format(lumiFrom , lumiTo) )

    ret2 = ROOT.RooDataHist( '{0}_lumi{1}h'.format( var , lumiRnangeName ) , '' , ROOT.RooArgSet(vars[var]) , ret )
    return (ret,ret2)



varName = 'nVertices'
datasets = {(0 , 0.00000007 , 'range1'):MakeDS( 0 , 0.00000007 , varName , "bin0" )}
            #( 0.00000007 , 0.0000001 , 'range2'):MakeDS( 0.00000007 , 0.0000001 , varName , "bin1" ),
            #( 0.0000001 , 0.0000002 , 'range3'):MakeDS( 0.0000001 , 0.0000002 , varName , "bin2" ) }
            
vars[varName].setBins(74)

fSim = ROOT.TFile.Open("../../PU/out_2016_SingleNeutrinovsZeroBias_APV.root")
dirName = "SingleNuZeroBias/{0}/TuneCP1/latest/All/".format(varName)
h2dVarPU = fSim.Get("{0}/{1}".format( dirName , varName))

xsection = ROOT.RooRealVar("xsection" , "" ,  50 , 90)
xsection.setBins(1000)

dt = 100000000000/11245

allpdfs = []
allhists = {}

fOut = ROOT.TFile.Open('fout.root' , 'recreate')
h2dVarPU.Write()

for lrange, ds in datasets.items():
    mydir = fOut.mkdir( lrange[2] )
    mydir.cd()
    
    ws = ROOT.RooWorkspace( 'ws_' + lrange[2] )
    ws.Import( ds[0] )
    ws.Import( ds[1] )
    ws.Write()
    
    hLumi = ROOT.TH1D("hLumi" , "" , 10 , lrange[0] , lrange[1] )
    ds[0].fillHistogram( hLumi , ROOT.RooArgList( luminosityVar ) )

    hLumi.Write()
    
    mypdf = ROOT.RooVarPDFForLumi( "pdf_"+lrange[2] , "" , h2dVarPU , hLumi , xsection , vars[varName] , dt , mydir )
    allpdfs.append(mypdf)
    
    h2d = mypdf.createHistogram( 'xsection:'+varName )
    h2d.Draw('colz')
    allhists[lrange] = h2d

    h2d.Write('crossCheckPDFH2D')
    
    print('new fit')
    mypdf.fitTo( ds[1] ) #, ROOT.RooFit.PrintLevel(-1) , ROOT.RooFit.Warnings(False) )


exit()
lumi = ROOT.RooRealVar("lumi" , "lumi" , 0 , 0.0000005 )
pu = ROOT.RooRealVar("nInt" , "nInt" , 0 , 100)
pu.setBins(100)

deltaT = ROOT.RooConstVar("deltaT" , "deltaT" , 250000 )  #1.0/(40000000 )
Lambda = ROOT.RooProduct("lambda" , "lambda" , ROOT.RooArgList(lumi , xsection , deltaT ) )
puForLumi = ROOT.RooPoisson("puForLumi" , "puForLumi" , pu , Lambda )

fSim = ROOT.TFile.Open("../../PU/out_2016_SingleNeutrinovsZeroBias_APV.root")
dirName = "SingleNuZeroBias/{0}/TuneCP1/latest/All/".format(varName)
h2dVarPU = fSim.Get("{0}/{1}".format( dirName , varName))
dataHist = ROOT.RooDataHist('dh_{0}'.format(h2dVarPU.GetName() ) , h2dVarPU.GetTitle() , ROOT.RooArgList( vars[varName] , pu ) , h2dVarPU )
pdf2dSim = ROOT.RooHistPdf( 'pdfSim_{0}'.format(h2dVarPU.GetName() ) , h2dVarPU.GetTitle() , ROOT.RooArgSet( vars[varName] , pu ) , dataHist )

canvas = ROOT.TCanvas()
canvas.Divide( 2, 2)

canvas.cd(2)
puF1 = pu.frame()
puForLumi.plotOn( puF1 )
puF1.Draw()

for lrange, ds in datasets.items():
    avgLumi = (lrange[0]+lrange[1])/2
    widthLumi = (lrange[1]-lrange[0])/10
    nameLumi = ds.GetName().split('_')[-1]
    lumiProfileMean = ROOT.RooConstVar("lumiProfileMean_"+nameLumi , "" , avgLumi )
    lumiProfileSigma = ROOT.RooConstVar("lumiProfileSigma_"+nameLumi , "" , widthLumi )
    lumiProfile = ROOT.RooGaussian("lumiProfile_"+nameLumi , "" , lumi , lumiProfileMean , lumiProfileSigma )

    canvas.cd(1)
    flumi1 = lumi.frame()
    lumiProfile.plotOn(flumi1)
    flumi1.Draw()
    
    puProfileT = ROOT.RooProdPdf("puProfileT_"+nameLumi , "puProfileT" , ROOT.RooArgList( lumiProfile )  , ROOT.RooFit.Conditional( ROOT.RooArgSet(puForLumi ) , ROOT.RooArgSet(lumi,xsection)  ) )
    puProfile = puProfileT.createProjection( ROOT.RooArgSet( lumi ) )

    canvas.cd(2)
    puF2 = pu.frame()
    puProfile.plotOn( puF2 )
    puF2.Draw()

    varPdfSimP = ROOT.RooProdPdf( "{0}PdfSim_{1}".format( varName , nameLumi ) , "" , ROOT.RooArgSet( puProfile ) , ROOT.RooFit.Conditional( ROOT.RooArgSet(pdf2dSim) , ROOT.RooArgSet(vars[varName]) ) )
    varPdfSim = varPdfSimP.createProjection( ROOT.RooArgSet( pu ) )

    canvas.cd(3)
    varF1 = vars[varName].frame()
    varPdfSim.plotOn( varF1 )
    varF1.Draw()
