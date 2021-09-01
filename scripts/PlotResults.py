#! /usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import os
import sys
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument( '--input' , dest='input' , default="./allResults.root" , help='' , type=str )
parser.add_argument( '--input2' , dest='input2' , default=None , help='' , type=str )
parser.add_argument( '--maxLumi' , dest='maxLumi' , default=-1 , help='' , type=float )
parser.add_argument( '--nToSkip' , dest='nToSkip' , default=10 , help='' , type=float )
parser.add_argument( '--logY' , dest='logY' , default=False , help='' , action='store_true' )
parser.add_argument( '--nRebinGroups' , dest='nRebinGroups' , default=1 , help='' , type=int )
parser.add_argument( '--PRJDIR' , dest='PRJDIR' , default="/home/hbakhshi/Documents/PU/MainFiles/" , help='' , type=str )

opt = parser.parse_args()

f = ROOT.TFile.Open(opt.input)
f2 = None
if opt.input2:
    f2 = ROOT.TFile.Open( opt.input2 )
    
varName = None
theVariable = None
h2dVarPU = None
for l1 in f.GetListOfKeys():
    if 'TH2' in l1.GetClassName():
        varName = l1.GetName()
        h2dVarPU = l1.ReadObj()
        nbins = h2dVarPU.GetNbinsX()
        fromVar = h2dVarPU.GetXaxis().GetXmin()
        toVar = h2dVarPU.GetXaxis().GetXmax()

        theVariable = ROOT.RooRealVar( varName , varName , fromVar , toVar )
        theVariable.setBins( nbins )
ROOT.gSystem.Load( '{0}/lib/libPUFit.so'.format(opt.PRJDIR) )


import collections
allResults = collections.OrderedDict()
allFolders = sorted( list([a.GetName() for a in f.GetListOfKeys() if a.IsFolder() ] ) )
f.Close()
fOut = ROOT.TFile.Open('AllResults.root' , "recreate")
for l1 in allFolders:
    #if l1.IsFolder():
        f = ROOT.TFile.Open(opt.input)
        l = f.Get( l1 )

        if f2:
            lold = f2.GetDirectory( l.GetName() )
        
        c1 = ROOT.TCanvas('c1_{0}'.format( l.GetName() ) )
        c1.cd()
        if f2:
            lold.hLumi.Draw()
        else:
            l.hLumi.Draw()

        c1.SaveAs('lumi_{0}.png'.format( l.GetName() ) )

            
        c2 = ROOT.TCanvas('c2_{0}'.format( l.GetName() ) )
        c2.Divide(2,1)
        if f2:
            h2dVarVsXSec = lold.Get( 'h2dVarVsXSec_pdf_{0}'.format( l.GetName() ) )
        else:
            h2dVarVsXSec = l.Get( 'h2dVarVsXSec_pdf_{0}'.format( l.GetName() ) )
        if h2dVarVsXSec == None:
            print( 'no information for {0} is available'.format( l.GetName() ) )
            allResults[l.GetName()] = ( 0 , 0 , 0 , 0 )
            continue
        minXSec = h2dVarVsXSec.GetXaxis().GetXmin()
        maxXSec = h2dVarVsXSec.GetXaxis().GetXmax()
        nBinsXSec = h2dVarVsXSec.GetNbinsX()
        xsecStep = (maxXSec-minXSec)/nBinsXSec

        ws = f.Get('{0}/ws_{0}'.format( l.GetName() ) )
        l.pwd()
        fitRange1 = ( ws.var("minVRange").getVal() ,  ws.var("maxVRange").getVal() )
    
        hvarData = ws.data( '{0}_lumi{1}h'.format( varName , l.GetName() ) )
        varWs = ws.var( varName )
        frameVar = varWs.frame()
        hvarData.plotOn( frameVar )
        dataIntegral = hvarData.sumEntries("{0}>{1} && {0}<{2}".format(varName , fitRange1[0] , fitRange1[1]))
        fanimname = 'animation_{0}.gif'.format( l.GetName() )

        fitRes = ws.allGenericObjects().front()
        bestXSec = fitRes.floatParsFinal()[fitRes.floatParsFinal().index('xsection')]
        bestXSecVal = bestXSec.getVal()
        bestXSecErr = bestXSec.getError()
        #fitRes.plotOn( frameVar , 'xsection' , 'xsection' )
        allResults[l.GetName()] = (bestXSecVal, bestXSecErr , fitRes.minNll() , fitRes.edm() )
            
        binId = 20
        if l.GetName() != 'fullrange':
            binId = int( l.GetName()[5:] )+1
        if binId%5:
            continue
        else:
            print( l.GetName() , binId , binId/5 + 1)
            c = ROOT.TCanvas( "c_"+l.GetName() )
            xsection = ROOT.RooRealVar("xsection" , "" ,  bestXSecVal , 60 , 80)
            mypdf = ROOT.RooVarPDFForLumi( "pdf_"+l.GetName() , "" , xsection , theVariable , h2dVarVsXSec  )

            frame = theVariable.frame()
            hvarData.plotOn(frame).SetTitle( l.GetName() )
            mypdf.plotOn( frame )
            fitRes.plotOn( frame , 'xsection' , varName )
            frame.Draw()
            fOut.cd()
            c.Write()
            #continue

        if os.path.exists( fanimname ):
            os.remove( fanimname )
        yMax = None
        for i in range(1,nBinsXSec+1):
            xsec_i = h2dVarVsXSec.GetXaxis().GetBinCenter(i)
            if i%opt.nToSkip and abs( xsec_i - bestXSecVal ) > 10*xsecStep:
                continue
            print(i, nBinsXSec)
            if f2:
                puHist = lold.PUProfiles.Get('hPuForXSec_{0}'.format(i-1) )
            else:
                puHist = l.PUProfiles.Get('hPuForXSec_{0}'.format(i-1) )
            puHist.GetXaxis().SetTitle('number of PU')
            puHist.SetStats(False)
            c2.cd(1)
            puHist.Draw()

            varHist = h2dVarVsXSec.ProjectionY( '_var' , i , i+1 )
            varHistIntegral = 0
            for b in range( varHist.GetNbinsX() ):
                if fitRange1[0] < varHist.GetBinCenter( b+1 ) < fitRange1[1] :
                    varHistIntegral += varHist.GetBinContent( b+1 )
            if varHistIntegral == 0:
                varHistIntegral = dataIntegral
            
            varHist.GetXaxis().SetTitle(varName)
            varHist.SetStats(False)
            varHist.SetLineColor( ROOT.kRed )
            varHist.SetLineWidth( 2 )
            varHist.Scale( 1 if dataIntegral==0 else opt.nRebinGroups*dataIntegral/varHistIntegral )
            varHist.SetTitle( 'best fit xsec = {0:.2f}+-{1:.2f}'.format( bestXSecVal , bestXSecErr ) )
            pad2 = c2.cd(2)

            if yMax is None:
                yMax = (100 if opt.logY else 1.5) * varHist.GetMaximum()
            frameVar.SetMaximum( yMax )
            frameVar.SetMinimum( 10 )
            frameVar.Draw() #'same')
            varHist.Draw('HIST SAME')

            if opt.logY:
                pad2.SetLogy()
            
            # if abs( xsec_i - bestXSecVal ) < 2:
            #     c2.SaveAs(fanimname + '+5')
            # else:
            c2.SaveAs(fanimname + '+5')

        f.Close()

hMinNLL = ROOT.TH1D('hMinNLL' , '' , len( allResults ) -1 , 0 , opt.maxLumi )
hEDM = ROOT.TH1D('hEDM' , '' , len( allResults ) -1 , 0 , opt.maxLumi )
hAllResults = ROOT.TH1D('hAllResults' , '' , len( allResults ) -1 , 0 , opt.maxLumi )
hAllResultsFR = ROOT.TH1D('hAllResultsFullRange' , '' , 1 , 0 , opt.maxLumi )

for r in allResults:
    #hAllResults.GetXaxis().SetBinLabel( binId , r )
    if r == 'fullrange':
        hAllResultsFR.SetBinContent( 1  , allResults[r][0] )
        hAllResultsFR.SetBinError( 1 , allResults[r][1] )
    else:
        binId = int( r[5:] )+1
        hAllResults.SetBinContent( binId , allResults[r][0] if allResults[r][0] else allResults['fullrange'][0] )
        hAllResults.SetBinError( binId , allResults[r][1] )

        hEDM.SetBinContent( binId , allResults[r][3] if allResults[r][3] else allResults['fullrange'][3] )
        hMinNLL.SetBinContent( binId , allResults[r][2] if allResults[r][2] else allResults['fullrange'][2] )
cAllRecults = ROOT.TCanvas('cAllRecults' )
hAllResults.SetStats(False)
hAllResults.Draw()

hAllResults.GetYaxis().SetRangeUser( 60 , 75)
hAllResultsFR.SetStats(False)
hAllResultsFR.Draw('same')
cAllRecults.SaveAs('AllResults.png')


fOut.cd()
hAllResults.Write()
hAllResultsFR.Write()
cAllRecults.Write()

hEDM.Write()
hMinNLL.Write()

fOut.Close()
