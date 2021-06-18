#! /usr/bin/env python

import os
import sys
import argparse
from datetime import datetime

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

def MakeVar(vname , fSim , tune):
    dirName = "SingleNuZeroBias/{0}/{1}/latest/All/".format(vname , tune)
    h2dVarPU = fSim.Get("{0}/{1}".format( dirName , vname))

    nbins = h2dVarPU.GetNbinsX()
    fromVar = h2dVarPU.GetXaxis().GetXmin()
    toVar = h2dVarPU.GetXaxis().GetXmax()

    v = ROOT.RooRealVar( vname , vname , fromVar , toVar )
    v.setBins( nbins )

    return v,h2dVarPU

def MakeDS(tree, lumiFrom , lumiTo , var , varArg , lumiVar ,  lumiRnangeName , fileWS = None ):
    if fileWS and fileWS.GetDirectory( lumiRnangeName ):
        ddd = fileWS.GetDirectory( lumiRnangeName )
        wwss = ddd.Get( 'ws_{0}'.format( lumiRnangeName ) )
        return ( wwss.data( '{0}_lumi{1}'.format( var , lumiRnangeName ) ), wwss.data( '{0}_lumi{1}h'.format( var , lumiRnangeName ) ) )
    else:
        ret = ROOT.RooDataSet( '{0}_lumi{1}'.format( var , lumiRnangeName ) , '{0} for lumi between {1} and {2}'.format( var , lumiFrom , lumiTo ) , 
                               tree , ROOT.RooArgSet(varArg , lumiVar) , "luminosity>{0} && luminosity<{1}".format(lumiFrom , lumiTo) )
        
        ret2 = ROOT.RooDataHist( '{0}_lumi{1}h'.format( var , lumiRnangeName ) , '' , ROOT.RooArgSet(varArg) , ret )
        return (ret,ret2)

def main():
    #parse command line
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '--PRJDIR' , dest='PRJDIR' , default="auto" , help='' , type=str )
    parser.add_argument( '--DataFile' , dest='DataFile' , default="data/outnew_ZeroBiasF7056.root" , help='with respect to the PRJDIR' , type=str )
    parser.add_argument( '--MCFile' , dest='MCFile' , default="data/out_2016_SingleNeutrinovsZeroBias_APV.root" , help='with respect to the PRJDIR' , type=str )
    parser.add_argument( '--MCTune' , dest='MCTune' , default="TuneCP1" , choices=['TuneCP1' , 'TuneCP5'] , help='' , type=str )
    parser.add_argument( '--var' , dest='var' , required=True  , choices= ["nVertices", "nGoodVertices","nChargedHadrons","fixedGridRhoAll","fixedGridRhoFastjetAll" ,"fixedGridRhoFastjetAllCalo" , "fixedGridRhoFastjetCentral" ,"fixedGridRhoFastjetCentralCalo" ,"fixedGridRhoFastjetCentralChargedPileUp" ,"fixedGridRhoFastjetCentralNeutral" ,"nMus","nEles" ,"nLostTracks","nPhotons","nNeutralHadrons"], help='' , type=str )
    parser.add_argument( '--WSFile' , dest='WSFile' , default=None , help='The file to load data from' , type=str )
    parser.add_argument( '--outdir' , dest='outdir' , default='auto' , help='The directory to store results' , type=str )
    parser.add_argument( '--nlumibins' , dest='nlumibins' , default=20 , help='' , type=int )
    parser.add_argument( '--minXS' , dest='minXS' , default=30 , help='' , type=int )
    parser.add_argument( '--maxXS' , dest='maxXS' , default=50 , help='' , type=int )
    parser.add_argument( '--nbinsXS' , dest='nbinsXS' , default=40 , help='' , type=int )
    parser.add_argument( '--maxLumi' , dest='maxLumi' , default=-1 , help='' , type=float )
    parser.add_argument( '--ncpu' , dest='ncpu' , default=1 , help='' , type=int )

    opt = parser.parse_args()

    if opt.PRJDIR == 'auto':
        opt.PRJDIR = os.path.dirname(os.path.realpath(__file__))
        opt.PRJDIR = '/'.join( opt.PRJDIR.split('/')[:-1] )
    if opt.outdir == 'auto':
        dfn = opt.DataFile.split('/')[-1].split('.')[0]
        if '_' in dfn:
            dfn = dfn.split('_')[-1]

        
        opt.outdir = '{0}/{1}/lbins{2}/xsbins{3}/{4:%y%m%d_%H%M%S}'.format( dfn , opt.var , opt.nlumibins , opt.nbinsXS , datetime.now() )
        if not os.path.exists(opt.outdir):
            os.makedirs(opt.outdir)
    ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(opt.PRJDIR) )

    fIn = ROOT.TFile.Open("{0}/{1}".format(opt.PRJDIR , opt.DataFile))
    tree = fIn.Events

    fSim = ROOT.TFile.Open("{0}/{1}".format(opt.PRJDIR , opt.MCFile))

    vars = { vn:MakeVar(vn,fSim , opt.MCTune) for vn in [opt.var] }
    varName = opt.var

    if opt.maxLumi == -1:
        for a in tree:
            if a.luminosity > opt.maxLumi:
                opt.maxLumi = a.luminosity
    print("maxLumi", opt.maxLumi)
    lumiStep = opt.maxLumi/opt.nlumibins
    luminosityVar = ROOT.RooRealVar( 'luminosity' , 'luminosity' , 0 , opt.maxLumi )
    datasets = {}
    fileWS_ = None
    if opt.WSFile:
        fileWS_ = ROOT.TFile.Open(opt.WSFile)

    for ii in range(opt.nlumibins):
        datasets[( ii*lumiStep , (ii+1)*lumiStep , 'range{0}'.format(ii) , opt.minXS , opt.maxXS , 1 )] = MakeDS( tree, ii*lumiStep , (ii+1)*lumiStep , varName, vars[varName][0], luminosityVar, 'range{0}'.format(ii) , fileWS_ )
    datasets[ (0 , opt.maxLumi , 'fullrange' , opt.minXS , opt.maxXS , opt.nlumibins ) ] = MakeDS( tree, 0 , opt.maxLumi , varName , vars[varName][0], luminosityVar,'fullrange' , fileWS_ )

    dt = 100000000000/11245

    allpdfs = []
    allhists = {}

    fOut = ROOT.TFile.Open('{0}/allResults.root'.format(opt.outdir) , 'recreate')
    h2dVarPU = vars[varName][1]
    h2dVarPU.Write()

    xsectionMain = ROOT.RooRealVar("xsection" , "" ,  25 , 45) #opt.minXS , opt.maxXS)
    xsectionMain.setBins( 400 )
    xsectionFrame = xsectionMain.frame()

    rangeCounter = 1
    for lrange, ds in datasets.items():
        try:
            rangeCounter += 1
            xsection = ROOT.RooRealVar("xsection" , "" ,  lrange[3] , lrange[4])
            xsection.setBins(opt.nbinsXS)

            mydir = fOut.mkdir( lrange[2] )
            mydir.cd()

            ws = ROOT.RooWorkspace( 'ws_' + lrange[2] )
            ws.Import( ds[0] )
            ws.Import( ds[1] )


            hLumi = ROOT.TH1D("hLumi" , "" , lrange[5] , lrange[0] , lrange[1] )
            ds[0].fillHistogram( hLumi , ROOT.RooArgList( luminosityVar ) )

            hLumi.Write()

            mypdf = ROOT.RooVarPDFForLumi( "pdf_"+lrange[2] , "" , h2dVarPU , hLumi , xsection , vars[varName][0] , dt , mydir )
            allpdfs.append(mypdf)

            h2d = mypdf.createHistogram( 'xsection:'+varName )
            h2d.Draw('colz')
            allhists[lrange] = h2d

            h2d.Write('crossCheckPDFH2D')

            print('new fit')
            fitRes = mypdf.fitTo( ds[1] , ROOT.RooFit.Save(True) ) # , ROOT.RooFit.Warnings(False) )
            print('NLL')
            ll1 = ROOT.RooNLLVar('ll_'+lrange[2],'',mypdf,ds[1], ROOT.RooFit.NumCPU(opt.ncpu) )
            #ll1int = ll1.createIntegral(xsec)
            #min1 = ROOT.RooMinuit( ll1 )
            # min1.setVerbose()
            # min1.setPrintLevel(-1)
            #min1.migrad()
            #min1.hesse()
            #min1.minos()
            #fitRes = min1.save("fit1")
            print('plotOn')
            ll1.plotOn( xsectionFrame , ROOT.RooFit.ShiftToZero() , ROOT.RooFit.NumCPU(opt.ncpu) , ROOT.RooFit.LineColor(rangeCounter) ).SetTitle( lrange[2] )
            ws.Import( fitRes )
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
        
    cc = ROOT.TCanvas('nllMins')
    xsectionFrame.Draw()
    cc.SaveAs('{0}/nllMins.root'.format(opt.outdir) )


if __name__ == "__main__":
    sys.exit( main() )
    
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

