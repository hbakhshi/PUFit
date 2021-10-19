import sys
sys.path.append('../nTuplizer')
from allInfo import GetRunInformation as GetRunInfo
import array
import ROOT

PRJDIR="/eos/home-c/cmstandi/SWAN_projects/PUFit/"
ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(PRJDIR) )
ROOT.gInterpreter.GenerateDictionary("map<string,RooAbsData*>","map")

class LumiRange:
    def __init__(self , lname , lmin , lmax , nbins , ds , pdf , variable , xsection , hlumidist):
        self.LumiName = lname
        self.Min = lmin
        self.Max = lmax
        self.nBins = nbins
        self.ds = ds
        self.pdf = pdf
        self.xsection = xsection
        self.hLumiDist = hlumidist
        self.BinnedDS = ROOT.RooDataHist( 'dsBinned{0}'.format(self.GetName()) , '' , ROOT.RooArgSet(variable) , ds )
        
    def GetName(self):
        return '{0}_{1}_{2}_{3}'.format( self.LumiName , self.Min , self.Max , self.nBins )
        
        
    def Fit(self , binned=True , ncpus = 8 , var_range = None , verbose = 1):
        dsToFit = self.BinnedDS if binned else self.ds
        args = ROOT.RooLinkedList()
        args.Add(ROOT.RooFit.Save(True) )
        args.Add(ROOT.RooFit.ConditionalObservables(self.xsection))
        args.Add(ROOT.RooFit.NumCPU(ncpus))
        if var_range:
            args.Add( ROOT.RooFit.Range(var_range[0] , var_range[1]) )
            
        args.Add( ROOT.RooFit.Verbose(verbose>0) )
        args.Add( ROOT.RooFit.PrintLevel(verbose-1) )
        args.Add( ROOT.RooFit.Warnings(verbose>1) )

        self.fitResult = self.pdf.fitTo(dsToFit , args)
        self.fitResultVal = self.fitResult.floatParsFinal()[self.fitResult.floatParsFinal().index(self.xsection.GetName())]
        
        return self.fitResultVal.getVal(), self.fitResultVal.getError()
    
    def AddToPlot(self , i , g):
        g.AddPoint( (self.Min+self.Max)/2, self.fitResultVal.getVal() )
        g.SetPointError(i,(self.Max-self.Min)/2 , self.fitResultVal.getError() )
    
class PUDataLoader:
    def __init__(self , objname, runs, varName, lumiName = 'PHYSICSDel', MCTUNE = 5 , var_nb = -1 , var_f = None, var_l = None , 
                 lumi_steps = 10 , lumi_nbinsperstep = 1 , xs_nb = 100 , xs_f = 0 , xs_l = 100 ):
        self.objname = objname
        self.RUNS = runs
        self.varName = varName
        self.lumiName = lumiName
        self.MCTUNE = MCTUNE
    
        self.xsection = ROOT.RooRealVar("xsection_{0}".format(objname) , "" ,  xs_f , xs_l)
        self.xsection.setBins(xs_nb)
        
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
        print('min/max lumi',minlumi,maxlumi)
        stepl = (maxlumi-minlumi)/nsteps
        ret = []
        for i in range(nsteps):
            minl = minlumi+i*stepl 
            maxl = minlumi+(i+1)*stepl
            ds = self.MakeDS(minl , maxl , 'step_{0}'.format(i))
            hlumi , pdf = self.MakePDF(ds ,'step_{0}'.format(i) , nbinsPerStep )
            fitter = LumiRange(self.lumiName , minl , maxl , nbinsPerStep , ds , pdf , self.variable , self.xsection , hlumi)
            ret.append(fitter)
        return ret
    def FitAllRanges(self,binned=True , ncpus = 8 , var_range = None , verbose = 1 ):
        self.graphSigmaVsLumi = ROOT.TGraphErrors()
        for i in range( len(self.lumiRanges) ):
            r = self.lumiRanges[i]
            v,e = r.Fit( binned , ncpus , var_range , verbose )
            r.AddToPlot( i ,self.graphSigmaVsLumi)
            
    def MakePDF(self, ds , name,nbinsPerStep):
        hlumi = ds.createHistogram("histLumi{0}".format(name),self.LumiVar,ROOT.RooFit.Binning(nbinsPerStep))
        pdf = ROOT.RooVarPDFForLumi("pdf{0}".format(name) , "pdf" , self.hPUvsVar , hlumi , self.xsection , self.variable , 1e-3 * 1e6 / (2**18) )
        return hlumi,pdf
    
    def LoadSimHisto(self):
        fSIM = ROOT.TFile.Open('/eos/user/c/cmstandi/PURunIIFiles/{0}/SingleNeutrino_CP{1}{2}.root'.format(self.year,self.MCTUNE,"_APV" if self.APV else ""))
        maxPuSim = int( fSIM.PUAnalyzer.Trees.Events.GetMaximum("nInt") )
        print('maxPU = {0}'.format(maxPuSim))
        fSIM.PUAnalyzer.Trees.Events.Draw("nInt:{0}>>h2d{4}({1},{2},{3} , {5} , 0 , {5})".format(self.varName,self.var_nb, self.var_f , self.var_l , self.objname , maxPuSim-20 ) , "" , "GOFF") 
        self.hPUvsVar = ROOT.gDirectory.Get("h2d{0}".format(self.objname))
        self.hPUvsVar.SetDirectory(0)
        fSIM.Close()

