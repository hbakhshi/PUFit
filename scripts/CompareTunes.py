import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

#f1 = ROOT.TFile.Open("/home/hbakhshi/Documents/PU/MainFiles/scripts/Fill7056/nVertices/lbins20/xsbins5000/luminosity/INPUTData.root")
f1 = ROOT.TFile.Open("/home/hbakhshi/Documents/PU/MainFiles/scripts/Fill7056/fixedGridRhoFastjetAllCalo/lbins20/xsbins500/luminosity/nllBinnedFullRange/allResults.root")
f5 = ROOT.TFile.Open("/home/hbakhshi/Documents/PU/MainFiles/scripts/Fill7056TuneCP5/fixedGridRhoFastjetAllCalo/lbins20/xsbins500/luminosity/nllBinnedFullRange/allResults.root")

#f1 = ROOT.TFile.Open("Fill6413/nVertices/lbins20/xsbins5000/nllBinnedFullRange/allResults.root")
#f5 = None
varName = None
theVariable = None
h2dVarPU = None
for l1 in f1.GetListOfKeys():
    if 'TH2' in l1.GetClassName():
        varName = l1.GetName()
        h2dVarPU = l1.ReadObj()
        nbins = h2dVarPU.GetNbinsX()
        fromVar = h2dVarPU.GetXaxis().GetXmin()
        toVar = h2dVarPU.GetXaxis().GetXmax()

        theVariable = ROOT.RooRealVar( varName , varName , fromVar , toVar )
        theVariable.setBins( nbins )

ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format("/home/hbakhshi/Documents/PU/MainFiles/") )

def ReadInfo(f,dname , t):
    ws = f.Get('{0}/ws_{0}'.format( dname ) )
    if not ws:
        return None,None,None,None,0,0
    #fitRange1 = ( ws.var("minVRange").getVal() ,  ws.var("maxVRange").getVal() )
    
    hvarData = ws.data( '{0}_lumi{1}h'.format( varName , dname ) )
    fitRes = ws.allGenericObjects().front()
    bestXSec = fitRes.floatParsFinal()[fitRes.floatParsFinal().index('xsection')]
    bestXSecVal = bestXSec.getVal()
    bestXSecErr = bestXSec.getError()

    xsection = ROOT.RooRealVar("xsection" , "" ,  bestXSecVal , 60 , 80)
    hpdf = f.Get("{0}/h2dVarVsXSec_pdf_{0}".format( dname ) )
    pdf = ROOT.RooVarPDFForLumi( "pdfcp{0}_{1}".format(t,dname) , "" , xsection , theVariable , hpdf  )

    return hvarData,pdf,xsection,hpdf,bestXSecVal,bestXSecErr

fout = ROOT.TFile.Open("fCompareRho.root" , "RECREATE")
for lbin in range(21):
    dirname = "range{0}".format(lbin)
    rng = ( lbin*260/20 , (1+lbin)*260/20 )
    if lbin==20:
        dirname = "fullrange"
        rng = (0,260)

    datacp1,pdfcp1,xs1,h2d1,v1,e1 = ReadInfo( f1 , dirname , 1 )
    if not datacp1:
        continue
    if f5:
        datacp5,pdfcp5,xs5,h2d5,v5,e5 = ReadInfo( f5 , dirname , 5 )

    frame = theVariable.frame( ROOT.RooFit.Name("f"+dirname) , ROOT.RooFit.Title(dirname) )
    d=datacp1.plotOn( frame , ROOT.RooFit.Name("data")  )
    d.SetTitle("Data")
    #datacp1.plotOn(frame , ROOT.RooFit.DrawOption("SAME") ).SetLineColor( 4 )
    p1=pdfcp1.plotOn(frame ,  ROOT.RooFit.LineColor(4)  ,  ROOT.RooFit.Name("CP1")  )
    p1.SetTitle("CP1")
    
    if f5:
        p5=pdfcp5.plotOn(frame ,  ROOT.RooFit.LineColor(2) ,ROOT.RooFit.LineStyle(10)  , ROOT.RooFit.Name("CP5") )
        p5.SetTitle("CP5")

    c = ROOT.TCanvas("cRho"+dirname )    
    frame.Draw()
    legend = ROOT.TLegend(0.1,0.7,0.48,0.9)
    legend.AddEntry( "data" , "Data ({0}<lumi<{1} [mb]^{{-1}})".format(rng[0] , rng[1]))
    legend.AddEntry( "CP1" , "CP1")
    if f5:
        legend.AddEntry( "CP5" , "CP5")
    legend.Draw()
    fout.cd()
    c.Write()
fout.Close()
