import sys
sys.path.append('../nTuplizer')
from allInfo import GetRunInformation as GetRunInfo
import array
import ROOT

PRJDIR="/eos/home-c/cmstandi/SWAN_projects/PUFit/"
ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(PRJDIR) )
ROOT.gInterpreter.GenerateDictionary("map<string,RooAbsData*>","map")

from collections import namedtuple
class FitResult:
    def __init__(self , **args):
        for p in ['Index' , 'RooFitResult' , 'RooFitResultVal' , 'val' , 'err' , 'RangeName' , 'Canvas' , 'Info' , 'Frame1' , 'Frame2' , 'hpull']:
            setattr( self , p , args.get( p , None ) )
            
class LumiRange:
    def __init__(self , lname , lmin , lmax , nbins , ds , pdf , variable , xsection , xsectionR , hlumidist , minv , maxv):
        self.LumiName = lname
        self.Min = lmin
        self.Max = lmax
        self.nBins = nbins
        self.ds = ds
        self.pdf = pdf
        self.xsection = xsection
        self.xsectionR = xsectionR
        self.hLumiDist = hlumidist
        self.BinnedDS = ROOT.RooDataHist( 'dsBinned{0}'.format(self.GetName()) , '' , ROOT.RooArgSet(variable) , ds )
        self.Variable = variable
        self.MinV = minv 
        self.MaxV = maxv
        self.Fits = {}
        self.FitResults = {}
    def GetName(self):
        return '{0}_{1}_{2}_{3}'.format( self.LumiName , self.Min , self.Max , self.nBins )
        
        
    def ChooseDsToFit(self, binned):
        self.dsToFit = self.BinnedDS if binned else self.ds
        
    def Fit(self , binned=True , ncpus = 8 , var_range = [0,0] , verbose = 1 , xsec_cond=True):
        fitInfo = ( var_range[0], var_range[1] , binned , xsec_cond )
        if fitInfo in self.Fits:
            print('fit has already been done')
            fitIndex = self.Fits[ fitInfo ]
            self.fitResultVal = self.FitResults[fitIndex].RooFitResult
            self.fitResult = self.FitResults[fitIndex].RooFitResultVal
            return self.FitResults[fitIndex].val , self.FitResults[fitIndex].err
        
        fitIndex = len(self.FitResults)
        fr = FitResult( Index=fitIndex , Info=fitInfo )
        self.lastFitIndex = fitIndex
        self.ChooseDsToFit(binned)
        
        args = ROOT.RooLinkedList()
        args.Add(ROOT.RooFit.Save(True) )
        if xsec_cond:
            args.Add(ROOT.RooFit.ConditionalObservables(self.xsection))
        args.Add(ROOT.RooFit.NumCPU(ncpus))
        
        fr.RangeName = ""
        if var_range[0] != 0 and var_range[1] != 0:
            fr.RangeName = "fitrange_{0}".format(fitIndex)
            self.Variable.setRange( fr.RangeName  , self.MinV + var_range[0] , self.MaxV - var_range[1] )
            args.Add( ROOT.RooFit.Range( fr.RangeName) )
            
        args.Add( ROOT.RooFit.Verbose(verbose>0) )
        args.Add( ROOT.RooFit.PrintLevel(verbose-1) )
        args.Add( ROOT.RooFit.Warnings(verbose>1) )

        fr.RooFitResult = self.pdf.fitTo(self.dsToFit , args)
        fr.RooFitResultVal = fr.RooFitResult.floatParsFinal()[fr.RooFitResult.floatParsFinal().index(self.xsection.GetName())]
        fr.val = fr.RooFitResultVal.getVal()
        fr.err = fr.RooFitResultVal.getError()
        
        self.Fits[ fitInfo ] = fitIndex
        self.FitResults[ fitIndex ] = fr

        return fitIndex
    
    def AddToPlot(self ,  g , fitIndex = -1):
        if fitIndex < 0:
            fitIndex = self.lastFitIndex
        fr = self.FitResults[ fitIndex ]
        status = fr.RooFitResult.status()
        if status < len(g):
            for gi,gg in g.items():
                vv , ve = 0 , 0
                if gi==status:
                    vv = fr.val
                    ve = fr.err
                gg.AddPoint( (self.Min+self.Max)/2, vv  )
                gg.SetPointError( gg.GetN()-1 ,(self.Max-self.Min)/2 , ve )
        
    def MakeCanvas(self , xsection_value = None , fitIndex = -1):
        if fitIndex < 0:
            fitIndex = self.lastFitIndex
        fr = self.FitResults[ fitIndex ]
        if fr.Canvas:
            return fr.Canvas
        
        fr.Canvas = ROOT.TCanvas( "C_{0}_{1}".format( self.GetName() , fitIndex ) , self.GetName(), 1200 , 500 )

        fr.Canvas.Divide( 4 , 1 )
        fr.Canvas.cd(1)
        
        fr.Frame1 = self.Variable.frame()
        binned = fr.Info[2]
        dsToFit = self.BinnedDS if binned else self.ds
        dsToFit.plotOn( fr.Frame1 )
        
        if xsection_value:
            self.xsection.setVal( xsection_value )
        else:
            self.xsection.setVal( fr.val )
        self.pdf.plotOn( fr.Frame1 , ROOT.RooFit.NormRange(fr.RangeName) )
        fr.Frame1.Draw()
        
        fr.Canvas.cd(2)
        fr.hpull = fr.Frame1.pullHist()
        fr.Frame2 = self.Variable.frame()
        fr.Frame2.addPlotable( fr.hpull, "P")
        fr.Frame2.GetYaxis().SetTitleOffset(1.6)
        fr.Frame2.Draw()
        
        fr.Canvas.cd(3)
        #self.hLumiDist.Print()
        self.hLumiDist.Draw("HIST")
        
        fr.Canvas.cd(4)
        self.hLumiDist.Draw("E3")
        
        return fr.Canvas
    
class PUDataLoader:
    def __init__(self , objname, runs, varName, lumiName = 'PHYSICSDel', MCTUNE = 5 , var_nb = -1 , var_f = None, var_l = None , 
                 lumi_steps = 10 , lumi_nbinsperstep = 1 , xs_nb = 100 , xs_f = 0 , xs_l = 100 , fout = None):
        
        self.fout = fout
        self.objname = objname
        self.RUNS = runs
        self.varName = varName
        self.lumiName = lumiName
        self.MCTUNE = MCTUNE
    
        #self.xsection = ROOT.RooRealVar("xsection_{0}".format(objname) , "" ,  xs_f , xs_l)
        #self.xsection.setBins(xs_nb)
        self.xsectionInfo = [xs_f , xs_l , xs_nb ]
        
        self.RunCat = ROOT.RooCategory("Run", "Run")
        self.allDatasets = {}
        self.allOpenFiles = {}
        self.WS = None
        self.year = None
        self.APV = None
        index_ii = 1
        for r in runs:
            year , era = GetRunInfo(r)
            year_ext = "_APV" if year == '2016' and r > 277772 and r < 278770 else ""
    
            if not self.year :
                self.year = int(year)
            elif self.year != int(year):
                raise ValueError('all runs should belong to one year ')

            if self.APV == None:
                self.APV = r < 278770
            elif self.APV != r < 278770:
                raise ValueError('all runs should belong in after/before apv')
                
            fWS = ROOT.TFile.Open("/eos/user/c/cmstandi/PURunIIFiles/R{0}/wsfile.root".format(r))
            self.allOpenFiles[r] = fWS
            
            if self.WS == None:
                self.WS = fWS.w
                for v in self.WS.allVars():
                    if v.GetName() == self.varName:
                        self.variable = v
                    if v.GetName() == self.lumiName:
                        self.LumiVar = v
                self.vars = ROOT.RooArgSet(self.LumiVar , self.variable)
                        
            dsAll = getattr( fWS , "DSR{0}".format( r ) )
            catName = 'Run{0}'.format(r)
            self.allDatasets[ catName ] = dsAll
            self.RunCat.defineType( catName  , index_ii )
            index_ii += 1
        
        self.AllGraphs = {}
        self.AllMGraphs = {}
        
        self.ds = self.MakeDS( 0 , None , None)

        if var_f == None or var_l == None:
            minv, maxv = self.GetRange(self.ds , self.variable)
            self.var_f = var_f if var_f else minv
            self.var_l = var_l if var_l else maxv
        else:
            self.var_f = var_f
            self.var_l = var_l
        
        self.variable.setRange(self.var_f , self.var_l)
        if var_nb < 0:
            var_nb = self.var_l - self.var_f
        self.var_nb = var_nb
        print( self.var_f , self.var_l , self.var_nb)
        self.variable.setBins( int(self.var_nb) )

        self.LoadSimHisto()
        self.lumiRanges = self.SplitLumiRange(lumi_steps , lumi_nbinsperstep)
        
    def MakeDS(self , lumi_f , lumi_l , name):
        objname = self.objname
        if name:
            objname += "_" + name
        cuts = []
        if lumi_f != None :
            cuts.append('({0}>{1})'.format(self.lumiName , lumi_f))
        if lumi_l != None :
            cuts.append('({0}>{1})'.format( lumi_l , self.lumiName ))
            
        print( '&&'.join(cuts) )
        allDatasetLinks = ROOT.std.map("string,RooAbsData*")()
        for c,d in self.allDatasets.items():
            allDatasetLinks[c] = self.allDatasets[ c ].reduce('&&'.join(cuts))
        ds = ROOT.RooDataSet( "DS_{0}".format(objname) , "" , self.vars  , ROOT.RooFit.Index( self.RunCat ) , ROOT.RooFit.Link( allDatasetLinks ) )
        setattr( self , 'DSLinkDSs_{0}'.format(objname) , allDatasetLinks)
        return ds
    
    def GetRange(self , ds, v):
        minv = array.array('d', [0.0])
        maxv = array.array('d', [0.0])
        ds.getRange(v , minv , maxv)
        v.Print()
        print(minv, maxv)
        return [minv[0],maxv[0]]

    def SplitLumiRange(self, nsteps , nbinsPerStep):
        minlumi, maxlumi = self.GetRange( self.ds,self.LumiVar )
        self.LumiVar.setRange( minlumi , maxlumi)
        print('min/max lumi',minlumi,maxlumi)
        stepl = (maxlumi-minlumi)/nsteps
        ret = []
        for i in range(nsteps):
            xsection = ROOT.RooRealVar("xsection_{0}{1}".format(self.objname , i) , "" ,  self.xsectionInfo[0] , self.xsectionInfo[1])
            xsection.setBins(self.xsectionInfo[2])
            
            minl = minlumi+i*stepl 
            maxl = minlumi+(i+1)*stepl
            self.LumiVar.setRange( minl , maxl )
            ds = self.MakeDS(minl , maxl , 'step_{0}'.format(i))
            minv,maxv = self.GetRange( ds , self.variable )
            var = ROOT.RooRealVar( self.varName , "" , minv , maxv )
            var.setBins( int( self.var_nb * (maxv-minv) / (self.var_l - self.var_f)) )
            #var = ROOT.RooRealVar( self.varName , "" , self.var_f , self.var_l )
            #var.setBins( int( self.var_nb ) )
            #minv,maxv = self.var_f , self.var_l
            hlumi , pdf = self.MakePDF(ds ,'step_{0}'.format(i) , nbinsPerStep , xsection , var )
            fitter = LumiRange(self.lumiName , minl , maxl , nbinsPerStep , ds , pdf , var , xsection , self.xsectionInfo , hlumi , minv , maxv)
            ret.append(fitter)
        return ret
    def FitAllRanges(self,binned=True , ncpus = 8 , var_range = [0,0] , verbose = 1  , xsec_cond=True):
        graphSigmaVsLumi = ROOT.TMultiGraph()
        graphsSigmaVsLumi = {i:ROOT.TGraphErrors() for i in range(6)}
        fit_index = 0
        for i in range( len(self.lumiRanges) ):
            r = self.lumiRanges[i]
            fit_index = r.Fit( binned , ncpus , var_range , verbose ,  xsec_cond )
            r.AddToPlot(graphsSigmaVsLumi)
        for i,g in graphsSigmaVsLumi.items():
            g.SetTitle( "fit status={0}".format(i) )
            g.SetName("status{0}".format(i) )
            if any( [ g.GetPointY(i) > 0 for i in range(g.GetN()) ] ):
                graphSigmaVsLumi.Add( g , "PL" )
                
        self.AllGraphs[ fit_index ] = graphsSigmaVsLumi
        self.AllMGraphs[ fit_index ] = graphSigmaVsLumi
        return graphSigmaVsLumi
        
    def MakePDF(self, ds , name,nbinsPerStep , xs , var):
        hlumi = ds.createHistogram("histLumi{0}".format(name),self.LumiVar,ROOT.RooFit.Binning(nbinsPerStep) )
        dir_ = None
        if self.fout :
            dir_ = self.fout.mkdir( name )
        pdf = ROOT.RooVarPDFForLumi("pdf{0}".format(name) , "pdf" , self.hPUvsVar , hlumi , xs , var , 1e-3 * 1e6 / (2**18) , dir_ )
        return hlumi,pdf
    
    def LoadSimHisto(self):
        fSIM = ROOT.TFile.Open('/eos/user/c/cmstandi/PURunIIFiles/{0}/SingleNeutrino_CP{1}{2}.root'.format(self.year,self.MCTUNE,"_APV" if self.APV else ""))
        maxPuSim = int( fSIM.PUAnalyzer.Trees.Events.GetMaximum("nInt") )
        print('maxPU = {0}'.format(maxPuSim))
        fSIM.PUAnalyzer.Trees.Events.Draw("nInt:{0}>>h2d{4}( {1},{2},{3} , {6} , 1 , {5} )".format(self.varName,self.var_nb, self.var_f , self.var_l , self.objname , maxPuSim-20 , maxPuSim-21 ) , "" , "GOFF") 
        self.hPUvsVar = ROOT.gDirectory.Get("h2d{0}".format(self.objname))
        self.hPUvsVar.SetDirectory(0)
        fSIM.Close()

    def DrawAllPlots(self , fitIndex = -1 ):
        for lr in self.lumiRanges:
            lr.MakeCanvas(fitIndex = fitIndex).Draw()
