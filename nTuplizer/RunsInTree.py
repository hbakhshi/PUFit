import ROOT
from os import listdir
from os.path import isfile, join
from allInfo import allInfo

allRuns = {}
allRunNumbers = []
for fn,runs in allInfo.items():
    f = ROOT.TFile.Open(fn)
    t = f.Get("PUAnalyzer/Trees/Events")
    
    for run in set( [int(r) for r in runs] ):
        #n = t.Draw( "1" , "run=={0}".format( run ) , "goff" )
        #print(run)
        #allRuns[run] = n 
        #print( len(allRuns) )
        pass
    allRunNumbers.extend( list( set( [int(r) for r in runs] ) ) )

    f.Close()

print(allRuns)

# allInfo = {}

# for year in [2016,2017,2018]:
#     dirname = "/eos/home-h/helfaham/PU_work/UL/after_bx/{0}/".format(year)
#     allfiles = [join(dirname, f) for f in listdir(dirname) if isfile(join(dirname, f))]
#     for fname in allfiles:
#         f = ROOT.TFile.Open( fname )
#         t = f.Get("PUAnalyzer/Trees/Events")
#         if not t:
#             continue
#         if t.ClassName() != "TTree":
#             continue

#         allRuns = []
#         lastRun = 0
#         for e in t:
#             r = e.run
#             if lastRun != r:
#                 allRuns.append( r )
#                 lastRun = r

#         allInfo[ fname ] = allRuns


# print( allInfo )
