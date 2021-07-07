#! /usr/bin/env python

import os
import sys
import argparse
from datetime import datetime

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

def MakeVar(vname , fSim , tune , nfte , nlte , rebin=1):
    dirName = "SingleNuZeroBias/{0}/{1}/latest/All/".format(vname , tune)
    h2dVarPU = fSim.Get("{0}/{1}".format( dirName , vname))
    h2dVarPU.RebinX( rebin )
    
    nbins = h2dVarPU.GetNbinsX()
    fromVar = h2dVarPU.GetXaxis().GetXmin()
    toVar = h2dVarPU.GetXaxis().GetXmax()

    v = ROOT.RooRealVar( vname , vname , fromVar , toVar )
    v.setBins( nbins )

    binSize = (toVar-fromVar)/nbins
    return v,h2dVarPU,fromVar+(nfte*binSize),toVar-(nlte*binSize)

def MakeDS(tree, lumiFrom , lumiTo , var , varArg , lumiVar ,  lumiRnangeName , fileWS = None ):
    ret = None
    if fileWS and fileWS.GetDirectory( lumiRnangeName ):
        ddd = fileWS.GetDirectory( lumiRnangeName )
        wwss = ddd.Get( 'ws_{0}'.format( lumiRnangeName ) )
        ret = wwss.data( '{0}_lumi{1}'.format( var , lumiRnangeName ) )
        #return ( , wwss.data( '{0}_lumi{1}h'.format( var , lumiRnangeName ) ) )
    else:
        ret = ROOT.RooDataSet( '{0}_lumi{1}'.format( var , lumiRnangeName ) , '{0} for lumi between {1} and {2}'.format( var , lumiFrom , lumiTo ) , 
                               tree , ROOT.RooArgSet(varArg , lumiVar) , "{2}>{0} && {2}<{1}".format(lumiFrom , lumiTo , lumiVar.GetName() ) )
        
    ret2 = ROOT.RooDataHist( '{0}_lumi{1}h'.format( var , lumiRnangeName ) , '' , ROOT.RooArgSet(varArg) , ret )
    return (ret,ret2)

def main():
    #parse command line
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '--PRJDIR' , dest='PRJDIR' , default="auto" , help='' , type=str )
    parser.add_argument( '--DataFile' , dest='DataFile' , default="auto" , help='auto: get it from fill number, with respect to the PRJDIR' , type=str )
    parser.add_argument( '--MCFile' , dest='MCFile' , default="auto" , help='auto: get it from fill number, with respect to the PRJDIR' , type=str )
    parser.add_argument( '-f' , '--fill' , dest='fill' , default=-1 , help='if set, input file names (data and MC) and maxLumi are set accordingly' , type=int , choices=[-1,7056,6413] )
    parser.add_argument( '--MCTune' , dest='MCTune' , default="TuneCP1" , choices=['TuneCP1' , 'TuneCP5'] , help='' , type=str )
    parser.add_argument( '--var' , dest='var' , required=True  , choices= ["nVertices", "nGoodVertices","nChargedHadrons","fixedGridRhoAll","fixedGridRhoFastjetAll" ,"fixedGridRhoFastjetAllCalo" , "fixedGridRhoFastjetCentral" ,"fixedGridRhoFastjetCentralCalo" ,"fixedGridRhoFastjetCentralChargedPileUp" ,"fixedGridRhoFastjetCentralNeutral" ,"nMus","nEles" ,"nLostTracks","nPhotons","nNeutralHadrons"], help='' , type=str )
    parser.add_argument( '--nFirstBinsToExclude' , dest='nFirstBinsToExclude' , default=0 , help='' , type=int )
    parser.add_argument( '--nLastBinsToExclude' , dest='nLastBinsToExclude' , default=0 , help='' , type=int )
    parser.add_argument( '--optVarRange' , dest='optVarRange' , default = 0 , help='' , type=float )
    parser.add_argument( '--ngRebinVariable' , dest='ngRebinVariable' , default=1 , help='' , type=int )
    
    parser.add_argument( '--WSFile' , dest='WSFile' , default='auto' , help='The file to load data from, if set to "none" a new file is created even an older already exists' , type=str )
    parser.add_argument( '--PDFFile' , dest='PDFFile' , default='auto' , help='The file to load pdf info from, if set to "none" a new file is created even an older already exists' , type=str )
    parser.add_argument( '--outdir' , dest='outdir' , default='auto' , help='The directory to store results' , type=str )
    parser.add_argument( '--title' , dest='title' , default='{0:%y%m%d_%H%M%S}'.format(datetime.now() ) , help='The title of the last directory to store results, used when outdir==auto' , type=str )
    parser.add_argument( '--nlumibins' , dest='nlumibins' , default=20 , help='' , type=int )
    parser.add_argument( '--minXS' , dest='minXS' , default=50 , help='' , type=int )
    parser.add_argument( '--maxXS' , dest='maxXS' , default=80 , help='' , type=int )
    parser.add_argument( '--nbinsXS' , dest='nbinsXS' , default=40 , help='' , type=int )
    parser.add_argument( '--maxLumi' , dest='maxLumi' , default=-1 , help='' , type=float )
    parser.add_argument( '--lumiVar' , dest='lumiVar' , default='luminosity' , help='' , type=str , choices=['luminosity', 'pccDel' , 'pccRec' , 'hfocDel' , 'hfocRec' , 'bcm1fRec' , 'bcm1fDel' , 'pltzeroDel' , 'pltzeroRec' , 'hfetDel' , 'hfetRec' ] )    
    parser.add_argument( '--ncpu' , dest='ncpu' , default=1 , help='' , type=int )
    parser.add_argument( '--fitMethod' , dest='fitMethod' , default='nll' , choices=['nll', 'chi2' , 'none'] , help='' , type=str )
    parser.add_argument( '--plotNLL' , dest='plotNLL' , default=False , help='' , action='store_true' )    
    parser.add_argument( '--minXSForNLL' , dest='minXSForNLL' , default=None , help='' , type=int )
    parser.add_argument( '--maxXSForNLL' , dest='maxXSForNLL' , default=None , help='' , type=int )
    parser.add_argument( '--nbinsXSForNLL' , dest='nbinsXSForNLL' , default=None , help='' , type=int )
    
    parser.add_argument( '--binnedFit' , dest='binnedFit' , default=False , help='' , action='store_true' )
    
    opt = parser.parse_args()


    if opt.fill != -1:
        print( 'set input files and maxlumi automatically for fill {0}'.format(opt.fill))
        fillsInfo = { 7056:["data/outnew_ZeroBiasF7056.root","data/out_2018_SingleNeutrinovsZeroBias.root",2.33e-07 ] ,
                      6413:["data/outnew_ZeroBiasF6413.root","data/out_2017_UL_SingleNeutrinovsZeroBias.root", 3e-08 ] }

        if opt.fill not in fillsInfo:
            print( 'the given fill information is not available' )
            return 1
        opt.DataFile = fillsInfo[ opt.fill ][0]
        opt.MCFile = fillsInfo[ opt.fill ][1]
        if opt.lumiVar == 'luminosity':
            opt.maxLumi = fillsInfo[ opt.fill ][2]
    
    if opt.fitMethod == 'chi2':
        opt.binnedFit = True
    
    if opt.minXSForNLL is None:
        opt.minXSForNLL = opt.minXS
    if opt.maxXSForNLL is None:
        opt.maxXSForNLL = opt.maxXS
    if opt.nbinsXSForNLL is None:
        opt.nbinsXSForNLL = opt.nbinsXS
    
    if opt.PRJDIR == 'auto':
        opt.PRJDIR = os.path.dirname(os.path.realpath(__file__))
        opt.PRJDIR = '/'.join( opt.PRJDIR.split('/')[:-1] )

    INPUTFILE = None
    if opt.outdir == 'auto':
        if opt.fill > 0:
            dfn = 'Fill{0}'.format(opt.fill)
        else:
            dfn = opt.DataFile.split('/')[-1].split('.')[0]
            if '_' in dfn:
                dfn = dfn.split('_')[-1]

        if opt.MCTune != 'TuneCP1':
            dfn += opt.MCTune
        mainDir = '{0}/{1}/lbins{2}/xsbins{3}/{4}'.format( dfn , opt.var , opt.nlumibins , opt.nbinsXS , opt.lumiVar )
        opt.outdir = '{0}/{1}'.format( mainDir , opt.title )
        if not os.path.exists(opt.outdir):
            os.makedirs(opt.outdir)
        
        INPUTFILE = '{0}/{1}'.format( mainDir , 'INPUTData.root' )
        if os.path.exists( INPUTFILE ):
            if opt.WSFile == 'auto' :
                opt.WSFile = INPUTFILE
            if opt.PDFFile == 'auto':
                opt.PDFFile = INPUTFILE
        else:
            if opt.WSFile == 'auto' :
                opt.WSFile = None
            if opt.PDFFile == 'auto':
                opt.PDFFile = None
            
                
    ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(opt.PRJDIR) )

    fIn = ROOT.TFile.Open("{0}/{1}".format(opt.PRJDIR , opt.DataFile))
    tree = fIn.Events

    fSim = ROOT.TFile.Open("{0}/{1}".format(opt.PRJDIR , opt.MCFile))
    vars = { vn:MakeVar(vn,fSim , opt.MCTune , opt.nFirstBinsToExclude, opt.nLastBinsToExclude , opt.ngRebinVariable) for vn in [opt.var] }
    varName = opt.var
    
    if opt.maxLumi == -1:
        if opt.lumiVar == 'luminosity':
            for a in tree:
                if a.luminosity > opt.maxLumi:
                    opt.maxLumi = a.luminosity
        else:
            opt.maxLumi = tree.GetMaximum( opt.lumiVar )
            
    print("maxLumi", opt.maxLumi)
    lumiStep = opt.maxLumi/opt.nlumibins
    luminosityVar = ROOT.RooRealVar( opt.lumiVar , opt.lumiVar , 0 , opt.maxLumi )
    datasets = {}
    fileWS_ = None
    if opt.WSFile:
        fileWS_ = ROOT.TFile.Open(opt.WSFile)
    filePDF_ = None
    if opt.PDFFile:
        if opt.PDFFile == opt.WSFile:
            filePDF_ = fileWS_
        else:
            filePDF_ = ROOT.TFile.Open(opt.PDFFile)
        
    for ii in range(opt.nlumibins):
        datasets[( ii*lumiStep , (ii+1)*lumiStep , 'range{0}'.format(ii) , opt.minXS , opt.maxXS , 10 if ii in [0,1 , opt.nlumibins-1 , opt.nlumibins-2] else 1 )] = MakeDS( tree, ii*lumiStep , (ii+1)*lumiStep , varName, vars[varName][0], luminosityVar, 'range{0}'.format(ii) , fileWS_ )
    datasets[ (0 , opt.maxLumi , 'fullrange' , opt.minXS , opt.maxXS , opt.nlumibins ) ] = MakeDS( tree, 0 , opt.maxLumi , varName , vars[varName][0], luminosityVar,'fullrange' , fileWS_ )

    #dt = 100000000000/11245
    if opt.lumiVar == 'luminosity':
        dt = 1e-3 * 1e15 / (2**18)
    else:
        dt = 1e-3 * 1e6 / (2**18)
    allpdfs = []
    allhists = {}

    fOut = ROOT.TFile.Open('{0}/allResults.root'.format(opt.outdir) , 'recreate')
    h2dVarPU = vars[varName][1]
    h2dVarPU.Write()

    if opt.plotNLL:
        xsectionMain = ROOT.RooRealVar("xsection" , "" ,  opt.minXSForNLL , opt.maxXSForNLL)
        xsectionMain.setBins( opt.nbinsXSForNLL )
        xsectionFrame = xsectionMain.frame()

    rangeCounter = 1
    for lrange, ds in datasets.items():
        try:
            rangeCounter += 1
            xsection = ROOT.RooRealVar("xsection" , "" ,  lrange[3] , lrange[4])
            xsection.setBins(opt.nbinsXS)

            mydir = fOut.mkdir( lrange[2] )
            mydir.cd()

            hLumi = ROOT.TH1D("hLumi" , "" , lrange[5] , lrange[0] , lrange[1] )
            ds[0].fillHistogram( hLumi , ROOT.RooArgList( luminosityVar ) )
            hLumi.Write()

            binningV = vars[varName][0].getBinning()
            print( binningV.numBins(), binningV.lowBound() , binningV.highBound() )
            hVar = ROOT.TH1D("hVar" , "" , binningV.numBins(), binningV.lowBound() , binningV.highBound() )
            ds[0].fillHistogram( hVar , ROOT.RooArgList( vars[varName][0] ) )
            hVar.Scale( 1./hVar.Integral() )
            hVar.Write()

            minVRange = vars[varName][2]
            maxVRange = vars[varName][3]
            if opt.optVarRange != 0:
                minSet = False
                for vBin in range( hVar.GetNbinsX() ):
                    #print( hVar.GetBinContent( vBin+1 ) , opt.optVarRange)
                    if hVar.GetBinContent( vBin+1 ) > opt.optVarRange:
                        if not minSet:
                            minVRange = hVar.GetBinCenter( vBin + 1 )
                            minSet = True
                    else:
                        if minSet:
                            maxVRange = hVar.GetBinCenter( vBin + 1 )
                            break
                print( 'range automatically set to ({0}..{1})'.format( minVRange , maxVRange ) )
                
            if filePDF_:
                h = filePDF_.Get("{0}/h2dVarVsXSec_pdf_{0}".format(lrange[2]) )
                mypdf = ROOT.RooVarPDFForLumi( "pdf_"+lrange[2] , "" , xsection , vars[varName][0] , h )
            else:
                mypdf = ROOT.RooVarPDFForLumi( "pdf_"+lrange[2] , "" , h2dVarPU , hLumi , xsection , vars[varName][0] , dt , mydir )
            allpdfs.append(mypdf)

            h2d = mypdf.createHistogram( 'xsection:'+varName )
            h2d.Draw('colz')
            allhists[lrange] = h2d

            h2d.Write('crossCheckPDFH2D')

            vars[varName][0].setRange( "fit_{0}".format( lrange[2] ) , minVRange , maxVRange )
            print('new fit')
            if opt.fitMethod == 'nll':
                fitRes = mypdf.fitTo( ds[ int(opt.binnedFit) ] , ROOT.RooFit.Save(True) , ROOT.RooFit.ConditionalObservables(xsection) , ROOT.RooFit.NumCPU(opt.ncpu)  ,ROOT.RooFit.Verbose(False) , ROOT.RooFit.PrintLevel(-1) , ROOT.RooFit.Warnings(False) , ROOT.RooFit.Range(minVRange , maxVRange ) )
            elif opt.fitMethod == 'chi2':
                fitRes = mypdf.chi2FitTo( ds[ int(opt.binnedFit) ] , ROOT.RooFit.Save(True) , ROOT.RooFit.NumCPU(opt.ncpu)  ,ROOT.RooFit.Verbose(False) , ROOT.RooFit.PrintLevel(-1) , ROOT.RooFit.Warnings(False) , ROOT.RooFit.Range(minVRange , maxVRange) ) #, ROOT.RooFit.ConditionalObservables(xsection)



            print('NLL')
            if opt.fitMethod == 'nll':
                ll1 = mypdf.createNLL(ds[ int(opt.binnedFit) ], ROOT.RooFit.NumCPU(opt.ncpu)  , ROOT.RooFit.ConditionalObservables(xsection) , ROOT.RooFit.Verbose(False) , ROOT.RooFit.Range(minVRange , maxVRange) )
            elif opt.fitMethod == 'chi2':
                ll1 = mypdf.createChi2(ds[ int(opt.binnedFit) ], ROOT.RooFit.NumCPU(opt.ncpu) , ROOT.RooFit.Range(minVRange , maxVRange) )
            if opt.plotNLL:
                print('plotOn')
                ll1.plotOn( xsectionFrame , ROOT.RooFit.ShiftToZero() , ROOT.RooFit.NumCPU(opt.ncpu) , ROOT.RooFit.LineColor(rangeCounter) ).SetTitle( lrange[2] )

            ws = ROOT.RooWorkspace( 'ws_' + lrange[2] )
            if fileWS_ == None:
                ws.Import( ds[0] )
            ws.Import( vars[varName][0] )
            ws.Import( ds[1] )
            if opt.fitMethod != 'none':
                ws.Import( fitRes )
            ws.saveSnapshot( "afterFit" , ROOT.RooArgSet( vars[varName][0] ) , True )
            minVRangeVar = ROOT.RooRealVar( 'minVRange' , 'minVRange' , minVRange )
            ws.Import( minVRangeVar )
            maxVRangeVar = ROOT.RooRealVar( 'maxVRange' , 'maxVRange' , maxVRange )
            ws.Import( maxVRangeVar )
            ws.Write()

            #ws2 = ROOT.RooWorkspace( 'ws2_' + lrange[2] )
            #ws2.Import( ll1 )
            #ws2.Write()

        except Exception as e:
            print('there was an error in {0}'.format(lrange[2]))
            print(e)
        except:
            print('there was an error in {0}'.format(lrange[2]))
            print('i dont know')

    fOut.Close()
    if opt.plotNLL:
        cc = ROOT.TCanvas('nllMins')
        xsectionFrame.Draw()
        cc.SaveAs('{0}/nllMins.root'.format(opt.outdir) )

    if INPUTFILE and not os.path.exists( INPUTFILE ):
        os.symlink('{0}/{1}'.format( os.path.dirname(os.path.realpath(__file__)) , fOut.GetName()) , INPUTFILE)
        
    return 0
        
if __name__ == "__main__":
    sys.exit( main() )
    
# exit()
# lumi = ROOT.RooRealVar("lumi" , "lumi" , 0 , 0.0000005 )
# pu = ROOT.RooRealVar("nInt" , "nInt" , 0 , 100)
# pu.setBins(100)

# deltaT = ROOT.RooConstVar("deltaT" , "deltaT" , 250000 )  #1.0/(40000000 )
# Lambda = ROOT.RooProduct("lambda" , "lambda" , ROOT.RooArgList(lumi , xsection , deltaT ) )
# puForLumi = ROOT.RooPoisson("puForLumi" , "puForLumi" , pu , Lambda )

# fSim = ROOT.TFile.Open("../../PU/out_2016_SingleNeutrinovsZeroBias_APV.root")
# dirName = "SingleNuZeroBias/{0}/TuneCP1/latest/All/".format(varName)
# h2dVarPU = fSim.Get("{0}/{1}".format( dirName , varName))
# dataHist = ROOT.RooDataHist('dh_{0}'.format(h2dVarPU.GetName() ) , h2dVarPU.GetTitle() , ROOT.RooArgList( vars[varName][0] , pu ) , h2dVarPU )
# pdf2dSim = ROOT.RooHistPdf( 'pdfSim_{0}'.format(h2dVarPU.GetName() ) , h2dVarPU.GetTitle() , ROOT.RooArgSet( vars[varName][0] , pu ) , dataHist )

# canvas = ROOT.TCanvas()
# canvas.Divide( 2, 2)

# canvas.cd(2)
# puF1 = pu.frame()
# puForLumi.plotOn( puF1 )
# puF1.Draw()

# for lrange, ds in datasets.items():
#     avgLumi = (lrange[0]+lrange[1])/2
#     widthLumi = (lrange[1]-lrange[0])/10
#     nameLumi = ds.GetName().split('_')[-1]
#     lumiProfileMean = ROOT.RooConstVar("lumiProfileMean_"+nameLumi , "" , avgLumi )
#     lumiProfileSigma = ROOT.RooConstVar("lumiProfileSigma_"+nameLumi , "" , widthLumi )
#     lumiProfile = ROOT.RooGaussian("lumiProfile_"+nameLumi , "" , lumi , lumiProfileMean , lumiProfileSigma )

#     canvas.cd(1)
#     flumi1 = lumi.frame()
#     lumiProfile.plotOn(flumi1)
#     flumi1.Draw()
    
#     puProfileT = ROOT.RooProdPdf("puProfileT_"+nameLumi , "puProfileT" , ROOT.RooArgList( lumiProfile )  , ROOT.RooFit.Conditional( ROOT.RooArgSet(puForLumi ) , ROOT.RooArgSet(lumi,xsection)  ) )
#     puProfile = puProfileT.createProjection( ROOT.RooArgSet( lumi ) )

#     canvas.cd(2)
#     puF2 = pu.frame()
#     puProfile.plotOn( puF2 )
#     puF2.Draw()

#     varPdfSimP = ROOT.RooProdPdf( "{0}PdfSim_{1}".format( varName , nameLumi ) , "" , ROOT.RooArgSet( puProfile ) , ROOT.RooFit.Conditional( ROOT.RooArgSet(pdf2dSim) , ROOT.RooArgSet(vars[varName][0]) ) )
#     varPdfSim = varPdfSimP.createProjection( ROOT.RooArgSet( pu ) )

#     canvas.cd(3)
#     varF1 = vars[varName][0].frame()
#     varPdfSim.plotOn( varF1 )
#     varF1.Draw()

