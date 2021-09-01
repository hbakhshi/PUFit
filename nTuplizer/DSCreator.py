#! /usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import argparse
import os.path
import sys


def correctMinMax(minv , maxv):
    # if minv < 0:
    #     minv *= 1.1
    # else:
    #     minv *= 0.9

    # if maxv < 0:
    #     maxv *= 0.9
    # else:
    #     maxv *= 1.1

    return minv, maxv

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '--input' , dest='input' , default=[] , help='input file name' , type=str , nargs='+' )
    parser.add_argument( '--wsfile' , dest='wsfile' , default='./wsOut.root' , help='the file which contanis ws info, will be created if needed' , type=str )
    opt = parser.parse_args()
    print(opt.input)
    if len(opt.input) == 0:
        print("Please specify input file by --input option")
        return 0

    argSet = ROOT.RooArgSet("AllImportedVars")
    argSetArgs = {}

    allInputs = {}
    for fin in opt.input:
        year = None
        for y in [6,7,8]:
            if '201'+str(y) in fin:
                year = 2010+y
        if not year:
            print( 'the year of the {0} is not known'.format( fin ) )
            return -1

        era = fin[-6]
        allInputs[ (year , era) ] = ROOT.TFile.Open( fin , "UPDATE" )


    if not os.path.exists( opt.wsfile ):
        treeBranchesToImport =  ['run', 'lumi' , 'bx' , 'orbit' , 'nGoodVertices' , 'nVertices' , 'nEles' , 'nMus' , 'nChargedHadrons' , 'nLostTracks' , 'nPhotons' , 'nNeutralHadrons' , 'fixedGridRhoAll' , 'fixedGridRhoFastjetAll' , 'fixedGridRhoFastjetAllCalo' , 'fixedGridRhoFastjetCentral' , 'fixedGridRhoFastjetCentralCalo' , 'fixedGridRhoFastjetCentralChargedPileUp' , 'fixedGridRhoFastjetCentralNeutral']

        for b in treeBranchesToImport:
            bArg = ROOT.RooRealVar()
            bArg.SetNameTitle( b , b)
            for y,e in allInputs:
                tIn = allInputs[ (y,e) ].Events
                minVal, maxVal = correctMinMax( tIn.GetMinimum( b ), tIn.GetMaximum( b ) )
                print( b , y , e , minVal , maxVal )
                bArg.setRange( 'Y{0}Era{1}'.format( y , e ) , minVal , maxVal )
            argSetArgs[b] = bArg
            argSet.add( bArg )

        for nt in ['PHYSICS', 'hfoc' , 'bcm1f' , 'pltzero' ,  'pcc'  ]:
            for tag in ['Del' , 'Rec']:
                b = '{0}{1}'.format( nt , tag )
                bArg = ROOT.RooRealVar( )
                bArg.SetNameTitle( b , nt + ' delivered luminosity' )
                bArg.setUnit( "#mu b/LS" )
                for y,e in allInputs:
                    tIn = allInputs[ (y,e) ].Events
                    minVal, maxVal = correctMinMax( tIn.GetMinimum( b ),  tIn.GetMaximum( b ) )
                    print( b , y , e , minVal , maxVal )
                    bArg.setRange( 'Y{0}Era{1}'.format( y , e ) , minVal , maxVal )
                argSetArgs[b] =  bArg
                argSet.add( bArg )

        ROOT.gInterpreter.ProcessLine("#include <Compression.h>")
        fOut = ROOT.TFile.Open( opt.wsfile , "Recreate" , '' , 9 )
        fOut.SetCompressionAlgorithm( ROOT.ROOT.kLZMA )
        fOut.cd()

        wsOut = ROOT.RooWorkspace( "w" )
        getattr( wsOut , 'import' )( argSet )
        wsOut.Write()

        fOut.Close()

    
    wsf = ROOT.TFile.Open( opt.wsfile )
    ws = wsf.w
    argSet = ws.allVars()

    yearEras = ROOT.RooCategory("YearEras", "YearEras")
    allDatasets = {}
    ROOT.gInterpreter.GenerateDictionary("map<string,RooDataSet*>","map")
    allDatasetLinks = ROOT.std.map("string,RooDataSet*")()
    allDSLnks = []
    index_ii = 1
    for v in argSet:
        mins = []
        maxs = []
        for y,e in allInputs:
            r = 'Y{0}Era{1}'.format( y , e )
            bng = v.getBinning( r )
            mins.append( bng.lowBound() )
            maxs.append( bng.highBound() )
        v.setRange( min(mins) , max( maxs) )
    for y,e in allInputs:
        #for v in argSet:
        #    v.
        ds = None
        dsName = "Events{0}{1}".format( y ,e )
        if hasattr(  allInputs[(y,e)] , dsName ):
            ds = getattr( allInputs[(y,e)] , dsName )
        else:
            ds = ROOT.RooDataSet( dsName , "" , argSet , ROOT.RooFit.Import( allInputs[(y,e)].Events ) )
            allInputs[(y,e)].cd()
            ds.Write()
        catName = "{0}{1}".format( y ,e )
        allDatasets[ catName ] = ds
        allDatasetLinks[ catName ] = ds
        allDSLnks.append( ROOT.RooFit.Link( catName , ds ) )
        yearEras.defineType( catName  , index_ii )
        index_ii += 1

    fullds = ROOT.RooDataSet( "AllEvents" , "" , argSet, ROOT.RooFit.Index( yearEras ) , ROOT.RooFit.Import( allDatasetLinks ) )
    
    #fOut.cd()
    #dsOut.Write()
    #wsOut.Write()
    #fOut.Close()
    return 1

if __name__ == "__main__":
    sys.exit( main() )
    #print( 'main' )
    
