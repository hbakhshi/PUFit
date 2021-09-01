#! /usr/bin/python

import os.path
import sys
import csv
import numpy as np
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import array
import argparse

from allInfo import allInfo 

def ReadOutput(fname):
    allRuns = {}
    with open( fname, 'r') as csvfile:
        fillInfo = csv.reader(csvfile, delimiter=',', quotechar='|')
        for r in fillInfo:
            if r[0][0] == '#':
                continue
            try:
                run,fill = r[0].split(':')
            except:
                print('warning0' , r[0])
                continue
            try:
                ls1,ls2 = r[1].split(':')
            except:
                #print('warning1' , r[1])
                #continue
                ls1 = ls2 = r[1]
            try:
                bxinfo = r[9]
            except:
                print('warning9', r)
                continue
            if ls1 != ls2:
                if ls2 != '0':
                    print( 'warning' , run , fill , ls1 , ls2)
            runi = int(run)
            filli = int(fill)
            ls = int(ls1)
            #if filli not in allRuns:
            #    allRuns[filli] = {}
            if runi not in allRuns:
                allRuns[runi] = {}
            if ls in allRuns[runi]:
                print('warning 2', run , ls )
            allbx = {}
            bxi = None
            lrec = None
            ldel = None
            recs = np.array( 3568*[-1.1] )
            dels = np.array( 3568*[-1.1] )
            for bx in bxinfo[1:-1].split(' '):
                if bx.isspace() or bx == '':
                    continue
                try:
                    bxi = int(bx)
                    lrec = ldel = None
                except:
                    if ldel == None:
                        try:
                            ldel = float(bx)
                        except ValueError as v:
                            print( v)
                            print( runi , ls , bx , bxi , fname )
                    else:
                        lrec = float(bx)
                        #allbx[bxi] = [ldel,lrec]
                        recs[bxi] = lrec
                        dels[bxi] = ldel
                        bxi= None

            allRuns[runi][ls] = [ dels , recs ]

    return allRuns

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '--run' , dest='run' , default=None , help='run number' , type=int )
    parser.add_argument( '--wd' , dest='wd' , default=None , help='wd' , type=str )
    #parser.add_argument( '--input' , dest='input' , default=None , help='input file name' , type=str )

    opt = parser.parse_args()
    
    if not opt.run or not opt.wd:
        print( "--run, --wd are mandatory options")
        return 0

    normtags = {'pcc':None , 'hfoc':None , 'bcm1f':None , 'pltzero':None ,  'PHYSICS':None  } #'hfet':None ,
    for nt in normtags:
        fname = '{0}/{1}.csv'.format(opt.wd,nt) 
        if not os.path.isfile(fname):
            print( 'WARNING: {0} not found, {1} skipped'.format( fname , nt ) )
            continue
        normtags[nt] = ReadOutput( fname )
        if opt.run not in normtags[nt]:
            print( 'WARNING: {0} skipped, because no entry can be found'.format(nt ) )
            normtags[nt] = None

    
    inputFName = None
    for fname in allInfo :
        if opt.run in allInfo[fname]:
            inputFName = fname
    if not inputFName:
        print( "WARNING: No file is found for run {0}".format( opt.run ) )
        return 0
    else:
        print( "File {0} is being loaded for run {1}".format( inputFName , opt.run ) )

    fIn = ROOT.TFile.Open( inputFName )
    inTree = fIn.Get("PUAnalyzer/Trees/Events")
    inTree.Draw( ">>indicesOfRun" , "run=={0}".format(opt.run) )
    indicesOfRun = ROOT.gDirectory.Get("indicesOfRun")

    ROOT.gInterpreter.ProcessLine("#include <Compression.h>")
    fOut = ROOT.TFile.Open( '{0}/all.root'.format( opt.wd ) , 'recreate' , '' , 9 )
    fOut.SetCompressionAlgorithm( ROOT.ROOT.kLZMA )

    tree = ROOT.TTree('Events' , 'Events with lumi information')  #inTree.CopyTree( "run=={0}".format(opt.run) )

    treeBranches = {}
    for b in ['run/i', 'lumi/i' , 'bx/I' , 'orbit/I' , 'nGoodVertices/I' , 'nVertices/I' , 'nInt/I' , 'nInt50ns/I' , 'nEles/I' , 'nMus/I' , 'nChargedHadrons/I' , 'nLostTracks/I' , 'nPhotons/I' , 'nNeutralHadrons/I' , 'fixedGridRhoAll/F' , 'fixedGridRhoFastjetAll/F' , 'fixedGridRhoFastjetAllCalo/F' , 'fixedGridRhoFastjetCentral/F' , 'fixedGridRhoFastjetCentralCalo/F' , 'fixedGridRhoFastjetCentralChargedPileUp/F' , 'fixedGridRhoFastjetCentralNeutral/F' , 'W/D']:

        _rootBranchType2PythonArray = {
            'b': 'B',
            'B': 'b',
            'i': 'I',
            'I': 'i',
            'F': 'f',
            'D': 'd',
            'l': 'L',
            'L': 'l',
            'O': 'B'
        }

        bname, bformat = b.split('/')
        initial_value = 0 if bformat in ['i' , 'I'] else 0.0
        treeBranches[ bname ] = array.array( _rootBranchType2PythonArray[bformat] , [initial_value] )

        tree.Branch( bname , treeBranches[bname] , b )

    lumiBranches = {}
    for nt in normtags:
        lumiBranches[nt] = [ array.array('d' , [0.0] ) ,
                             array.array('d' , [0.0] ) ]
    
        tree.Branch( '{0}Del'.format( nt ) , lumiBranches[nt][0] , '{0}Del/D'.format( nt ) )
        tree.Branch( '{0}Rec'.format( nt ) , lumiBranches[nt][1] , '{0}Rec/D'.format( nt ) )
        

    for eventindex in range( indicesOfRun.GetN() ):
        eventid = indicesOfRun.GetEntry( eventindex )
        inTree.GetEntry( eventid )
        for nt in normtags:
            if not normtags[nt]:
                lumiBranches[nt][0][0] = -1
                lumiBranches[nt][1][0] = -1
                continue
            if int(inTree.lumi) in normtags[nt][int(inTree.run)]:
                lumiBranches[nt][0][0] = normtags[nt][int(inTree.run)][int(inTree.lumi)][0][inTree.bx]
                lumiBranches[nt][1][0] = normtags[nt][int(inTree.run)][int(inTree.lumi)][1][inTree.bx]
            else:
                lumiBranches[nt][0][0] = -2
                lumiBranches[nt][1][0] = -2

        for tb in treeBranches:
            treeBranches[tb][0] = getattr( inTree , tb )
            
        tree.Fill()
        
    tree.Write()
    fOut.Close()

    return 1
    
if __name__ == "__main__":     
    sys.exit( main() )
    
