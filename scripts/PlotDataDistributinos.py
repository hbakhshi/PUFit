import ROOT
import sys

fn = sys.argv[1]
#tree = ROOT.TChain("Events")
#tree.Add("../outnew_ZeroBiasF7*.root" , -1 )
f = ROOT.TFile.Open(fn)
tree = f.Events

lumiVar = 'pccDel'
maxLumi = 260 #tree.GetMaximum( lumiVar )
print(maxLumi)

if len(sys.argv) > 2:
    title = sys.argv[2]
else:
    title = "Title"

vars ={ v:[ROOT.TCanvas(v+title)] for v in ['nVertices' , 'nChargedHadrons']}

vars['nVertices'].extend( [14 , 0 , 140] )
vars['nChargedHadrons'].extend( [20 , 0 , 3000] )

ROOT.gStyle.SetPalette( 95 )
ROOT.gStyle.SetOptTitle(False)

for var,c in vars.items():
    c[0].cd()
    nbins = 10
    opt = "PLC PMC CP"
    for b in range(nbins):
        print("{0}-->{1}".format( var , b ) )
        lumi0 = maxLumi*b/nbins
        lumi1 = maxLumi*(b+1)/nbins
        print( "{0}>{1} && {0}<{2}".format( lumiVar , lumi0 , lumi1  ) )
        a = tree.Draw( "{0}>>h{0}{1}({2},{3},{4})".format(var,b,c[1],c[2],c[3]) , "{0}>{1} && {0}<{2}".format( lumiVar , lumi0 , lumi1  ) , "goff" )
        print( a )
        h = ROOT.gDirectory.Get( "h{0}{1}".format(var,b) )
        c.append(h)
        h.SetTitle( "{0:.0f}<luminosity<{1:.0f} mb".format( lumi0 , lumi1 ) )
        h.GetXaxis().SetTitle(var)
        h.GetYaxis().SetTitle("Probability")
        h.SetStats(0)
        h.SetMarkerStyle( 20 )
        h.SetMarkerSize( 1.2 )
        h.SetLineWidth(3)
        for hb in range( c[1] ):
            newval =  h.GetBinContent( hb+1)/ h.Integral()
            if newval < 0.01:
                newval = 0
            h.SetBinContent( hb+1 ,newval )
            h.SetBinError( hb+1 , 0 ) #10*h.GetBinError( hb+1)/ h.Integral() )
        h.DrawNormalized( opt )
        if "SAME" not in opt:
            opt += " SAME"
            
    c[0].BuildLegend()

latex = ROOT.TLatex()
latex.SetTextSize(0.05);
latex.DrawLatexNDC( 0.1 , 0.95 , title )
