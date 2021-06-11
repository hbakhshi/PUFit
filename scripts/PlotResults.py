import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import os

f = ROOT.TFile.Open('fout.root')

varName = None
for l1 in f.GetListOfKeys():
    if 'TH2' in l1.GetClassName():
        varName = l1.GetName()

import collections
allResults = collections.OrderedDict()
        
for l1 in f.GetListOfKeys():
    if l1.IsFolder():
        l = l1.ReadObj()
        
        c1 = ROOT.TCanvas('c1_{0}'.format( l.GetName() ) )
        c1.cd()
        l.hLumi.Draw()


        c1.SaveAs('lumi_{0}.png'.format( l.GetName() ) )
        
        c2 = ROOT.TCanvas('c2_{0}'.format( l.GetName() ) )
        c2.Divide(2,1)

        h2dVarVsXSec = l.Get( 'h2dVarVsXSec_pdf_{0}'.format( l.GetName() ) )
        minXSec = h2dVarVsXSec.GetXaxis().GetXmin()
        maxXSec = h2dVarVsXSec.GetXaxis().GetXmax()
        nBinsXSec = h2dVarVsXSec.GetNbinsX()


        ws = l.Get('ws_{0}'.format( l.GetName() ) )
        hvarData = ws.data( '{0}_lumi{1}h'.format( varName , l.GetName() ) )
        varWs = ws.var( varName )
        frameVar = varWs.frame()
        hvarData.plotOn( frameVar )
        dataIntegral = hvarData.sumEntries()
        fanimname = 'animation_{0}.gif'.format( l.GetName() )

        fitRes = ws.allGenericObjects().front()
        bestXSec = fitRes.floatParsFinal()[fitRes.floatParsFinal().index('xsection')]
        bestXSecVal = bestXSec.getVal()
        bestXSecErr = bestXSec.getError()
        #fitRes.plotOn( frameVar , 'xsection' , 'xsection' )
        allResults[l.GetName()] = (bestXSecVal, bestXSecErr )
        if os.path.exists( fanimname ):
            os.remove( fanimname )
        for i in range(1,nBinsXSec+1):
            if i%10:
                continue
            print(i, nBinsXSec)
            xsec_i = h2dVarVsXSec.GetXaxis().GetBinCenter(i)
            puHist = l.PUProfiles.Get('hPuForXSec_{0}'.format(i-1) )
            puHist.GetXaxis().SetTitle('number of PU')
            puHist.SetStats(False)
            c2.cd(1)
            puHist.Draw()

            varHist = h2dVarVsXSec.ProjectionY( '_var' , i , i+1 )
            varHist.GetXaxis().SetTitle(varName)
            varHist.SetStats(False)
            varHist.SetLineColor( ROOT.kRed )
            varHist.SetLineWidth( 2 )
            varHist.Scale( dataIntegral/varHist.Integral() )
            varHist.SetTitle( 'best fit xsec = {0:.2f}+-{1:.2f}'.format( bestXSecVal , bestXSecErr ) )
            c2.cd(2)
            varHist.Draw('HIST')
            frameVar.Draw('same')
            
            if abs( xsec_i - bestXSecVal ) < 2:
                c2.SaveAs(fanimname + '+40')
            else:
                c2.SaveAs(fanimname + '+1')
        
hAllResults = ROOT.TH1D('hAllResults' , '' , len( allResults ) , 0 , 10 )

binId = 1
for r in allResults:
    hAllResults.GetXaxis().SetBinLabel( binId , r )
    hAllResults.SetBinContent( binId , allResults[r][0] )
    hAllResults.SetBinError( binId , allResults[r][1] )
    binId += 1

cAllRecults = ROOT.TCanvas('cAllRecults' )
hAllResults.SetStats(False)
hAllResults.Draw()
cAllRecults.SaveAs('AllResults.png')
