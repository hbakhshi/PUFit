import ROOT
ROOT.gROOT.ProcessLine(".L RooMinBiasXSection.C+")

all_files = {
    "2016":"out_2016_SingleNeutrinovsZeroBias.root",
    "2016APV":"out_2016_SingleNeutrinovsZeroBias_APV.root",
    "2017":"out_2017_UL_SingleNeutrinovsZeroBias.root",
    "2018":"out_2018_SingleNeutrinovsZeroBias.root"
    }
def Make2DHist(year , varName , tune , era , datamc="SingleNuZeroBias" , normtag="latest"):
    f = ROOT.TFile.Open(all_files[year])
    dir_ = "/{0}/{1}/{2}/{3}/{4}".format( datamc , varName , tune , normtag , era )
    wd = f.GetDirectory(dir_)
    xsections = []
    nBinsX = None
    FromX = None
    ToX = None
    varName = None
    era = None
    j=0

    for a in wd.GetListOfKeys() :
        hname=a.GetName()
        nameParts = hname.split('_')
        if len(nameParts) != 4:
            continue
        varName = nameParts[0]
        lumName = nameParts[1]
        era = nameParts[2]
        xSection = float( nameParts[3] )
        xsections.append( xSection)
        h = wd.Get( hname )
        nBinsX = h.GetNbinsX()
        FromX = h.GetXaxis().GetXmin()
        ToX = h.GetXaxis().GetXmax()

    xsections = sorted( xsections )
    h2d = ROOT.TH2D("{0}_vs_xSection".format(varName) ,
                    "Title;{0};xSection".format( varName ),
                    nBinsX, FromX , ToX ,
                    len(xsections ) , xsections[0] , xsections[-1] )
    h2d.SetDirectory(0)
    for a in wd.GetListOfKeys() :
        hname=a.GetName()
        nameParts = hname.split('_')
        if len(nameParts) != 4:
            continue
        varName = nameParts[0]
        lumName = nameParts[1]
        era = nameParts[2]
        xSection = float( nameParts[3] )

        h = wd.Get( hname )
        for i in range( h.GetNbinsX() ):
            x= h.GetBinCenter(i+1)
            binid = h2d.FindBin(x,xSection)         
            v = h.GetBinContent( i+1 )
            h2d.SetBinContent( binid , v/h.Integral(0,100))

            e = h.GetBinError( i+1 )
            h2d.SetBinError( binid , e )
    h2d.Print("")
    hdata = wd.Get("{0}_{1}".format( era , varName ) ).Clone("hdata")
    hdata.SetDirectory(0)

    x = ROOT.RooRealVar(varName,varName, FromX ,ToX )
    return h2d, hdata , x




xsec = ROOT.RooRealVar("xsection","xsection", 58128 , 80895 )

h2d , hdata , x  = Make2DHist("2016" , "fixedGridRhoFastjetAllCalo" , "TuneCP1" , "All")
pdf = ROOT.RooMinBiasXSection("fixedGridRhoFastjetAllCaloTuneCP1EraG2016" , "fixedGridRhoFastjetAllCaloTuneCP1EraG2016" , h2d , xsec , x )
dataHist = ROOT.RooDataHist( "data" , "data" , ROOT.RooArgList( x ) , hdata )
ll1 = ROOT.RooNLLVar('ll1','ll1',pdf,dataHist)
ll1int = ll1.createIntegral(xsec)
min1 = ROOT.RooMinuit( ll1 )
# min1.setVerbose()
# min1.setPrintLevel(-1)
# min1.migrad()
# min1.hesse()
# min1.minos()
# fit1 = min1.save("fit1")

h2d2 , hdata2 , x2  = Make2DHist("2016" , "nVertices" , "TuneCP1" , "All")
pdf2 = ROOT.RooMinBiasXSection("nVertices" , "nVertices" , h2d2 , xsec , x2 )
dataHist2 = ROOT.RooDataHist( "data2" , "data2" , ROOT.RooArgList( x2 ) , hdata2 )
ll2 = ROOT.RooNLLVar('ll2','ll2',pdf2,dataHist2)
ll2int = ll2.createIntegral(xsec)
min2 = ROOT.RooMinuit( ll2 )
min2.setPrintLevel(-1)

llprod = ROOT.RooProduct( "llProd" , "" , ROOT.RooArgList( ll1 , ll2 ) )
llprodInt = llprod.createIntegral(llprod)
min3 = ROOT.RooMinuit( llprod )
min3.migrad()
min3.hesse()
min3.minos()

ff = xsec.frame(40)
print( llprodInt.getVal() , ll1int.getVal() , ll2int.getVal() )
llprod.plotOn(ff , ROOT.RooFit.LineColor(ROOT.kRed) , ROOT.RooFit.Normalization( 1.0/llprodInt.getVal() , 0 ) )

ff2 = xsec.frame(40)
ll1.plotOn( ff2 ,  ROOT.RooFit.LineColor(ROOT.kBlue) , ROOT.RooFit.Normalization( 1.0/ll1int.getVal() , 0 ))
ll2.plotOn( ff2 ,  ROOT.RooFit.LineColor(ROOT.kBlack)  , ROOT.RooFit.Normalization( 1.0/ll2int.getVal() , 0 ))
c1 = ROOT.TCanvas("C1")
c1.Divide(2)
c1.cd(1)
ff.Draw()

c1.cd(2)
ff2.Draw()

# #test1
# f = x.frame(40)
# pdf.plotOn( f )
# c1 = ROOT.TCanvas("C1")
# f.Draw()

# #test2
# aaa = pdf.chi2FitTo( dataHist )
