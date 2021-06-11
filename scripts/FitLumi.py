import ROOT
PRJDIR="/home/hbakhshi/Documents/PU/MainFiles"
ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(PRJDIR) )

fIn = ROOT.TFile.Open("{0}/data/outnew_ZeroBiasF7056.root".format(PRJDIR))
tree = fIn.Events

fSim = ROOT.TFile.Open("{0}/data/out_2016_SingleNeutrinovsZeroBias_APV.root".format(PRJDIR))

def MakeVar(vname):
    dirName = "SingleNuZeroBias/{0}/TuneCP1/latest/All/".format(vname)
    h2dVarPU = fSim.Get("{0}/{1}".format( dirName , vname))

    nbins = h2dVarPU.GetNbinsX()
    fromVar = h2dVarPU.GetXaxis().GetXmin()
    toVar = h2dVarPU.GetXaxis().GetXmax()

    v = ROOT.RooRealVar( vname , vname , fromVar , toVar )
    v.setBins( nbins )

    return v,h2dVarPU

varNames = ["nVertices",
            "nGoodVertices",
            "nChargedHadrons",
            "fixedGridRhoAll",
            "fixedGridRhoFastjetAll" ,
            "fixedGridRhoFastjetAllCalo" , 
            "fixedGridRhoFastjetCentral" ,
            "fixedGridRhoFastjetCentralCalo" ,
            "fixedGridRhoFastjetCentralChargedPileUp" ,
            "fixedGridRhoFastjetCentralNeutral" ,
            "nMus",
            "nEles" ,
            "nLostTracks",
            "nPhotons",
            "nNeutralHadrons"
]
vars = { vn:MakeVar(vn) for vn in varNames }

luminosityVar = ROOT.RooRealVar( 'luminosity' , 'luminosity' , 0 , 0.0000003 )

def MakeDS(lumiFrom , lumiTo , var , lumiRnangeName):
    ret = ROOT.RooDataSet( '{0}_lumi{1}'.format( var , lumiRnangeName ) , '{0} for lumi between {1} and {2}'.format( var , lumiFrom , lumiTo ) , 
                           tree , ROOT.RooArgSet(vars[var][0] , luminosityVar) , "luminosity>{0} && luminosity<{1}".format(lumiFrom , lumiTo) )

    ret2 = ROOT.RooDataHist( '{0}_lumi{1}h'.format( var , lumiRnangeName ) , '' , ROOT.RooArgSet(vars[var][0]) , ret )
    return (ret,ret2)



varName = 'nVertices'
datasets = {(0 , 0.00000007 , 'range1' , 20 , 60):MakeDS( 0 , 0.00000007 , varName , "range1" ),
            ( 0.00000007 , 0.0000001 , 'range2' , 20 , 60 ):MakeDS( 0.00000007 , 0.0000001 , varName , "range2" ),
            ( 0.0000001 , 0.0000002 , 'range3' , 20 , 60):MakeDS( 0.0000001 , 0.0000002 , varName , "range3" ) }
            

dt = 100000000000/11245

allpdfs = []
allhists = {}

fOut = ROOT.TFile.Open('fout.root' , 'recreate')
h2dVarPU = vars[varName][1]
h2dVarPU.Write()

for lrange, ds in datasets.items():
    xsection = ROOT.RooRealVar("xsection" , "" ,  lrange[3] , lrange[4])
    xsection.setBins(1000)

    mydir = fOut.mkdir( lrange[2] )
    mydir.cd()
    
    ws = ROOT.RooWorkspace( 'ws_' + lrange[2] )
    ws.Import( ds[0] )
    ws.Import( ds[1] )

    
    hLumi = ROOT.TH1D("hLumi" , "" , 10 , lrange[0] , lrange[1] )
    ds[0].fillHistogram( hLumi , ROOT.RooArgList( luminosityVar ) )

    hLumi.Write()
    
    mypdf = ROOT.RooVarPDFForLumi( "pdf_"+lrange[2] , "" , h2dVarPU , hLumi , xsection , vars[varName][0] , dt , mydir )
    allpdfs.append(mypdf)
    
    h2d = mypdf.createHistogram( 'xsection:'+varName )
    h2d.Draw('colz')
    allhists[lrange] = h2d

    h2d.Write('crossCheckPDFH2D')
    
    print('new fit')
    fitRes = mypdf.fitTo( ds[0] , ROOT.RooFit.Save(True) ) # , ROOT.RooFit.Warnings(False) )
    ws.Import( fitRes )
    
    ws.Write()

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
dataHist = ROOT.RooDataHist('dh_{0}'.format(h2dVarPU.GetName() ) , h2dVarPU.GetTitle() , ROOT.RooArgList( vars[varName][0] , pu ) , h2dVarPU )
pdf2dSim = ROOT.RooHistPdf( 'pdfSim_{0}'.format(h2dVarPU.GetName() ) , h2dVarPU.GetTitle() , ROOT.RooArgSet( vars[varName][0] , pu ) , dataHist )

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

    varPdfSimP = ROOT.RooProdPdf( "{0}PdfSim_{1}".format( varName , nameLumi ) , "" , ROOT.RooArgSet( puProfile ) , ROOT.RooFit.Conditional( ROOT.RooArgSet(pdf2dSim) , ROOT.RooArgSet(vars[varName][0]) ) )
    varPdfSim = varPdfSimP.createProjection( ROOT.RooArgSet( pu ) )

    canvas.cd(3)
    varF1 = vars[varName][0].frame()
    varPdfSim.plotOn( varF1 )
    varF1.Draw()
