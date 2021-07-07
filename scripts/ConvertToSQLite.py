import sqlite3

con = sqlite3.connect('example.db')
cur = con.cursor()
cur.execute('CREATE TABLE Fills (fill INTEGER PRIMARY KEY, DT DATETIME)')
cur.execute('CREATE TABLE Runs (run INTEGER PRIMARY KEY, FillID INTEGER NOT NULL, FOREIGN KEY (FillID) REFERENCES Fills (fill) )')
cur.execute('CREATE TABLE LumiSections (LS INTEGER, RunID INTEGER NOT NULL, FOREIGN KEY (RunID) REFERENCES Runs (run) ,   PRIMARY KEY (LS, RunID) )')
cur.execute('CREATE TABLE BXs (BXID INTEGER, LS INTEGER NOT NULL, RunID INTEGER NOT NULL, DELIVERED REAL , RECORDER REAL, FOREIGN KEY (RunID , LS) REFERENCES LumiSections ( RunID , LS ), PRIMARY KEY (BXID , LS , RunID) )')

con.commit()

import csv
allRuns = {}
with open('../data/f7056.csv', 'r') as csvfile:
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
            print('warning1' , r[1])
            continue
        try:
            bxinfo = r[9]
        except:
            print('warning9', r)
            continue
        if ls1 != ls2:
            print( 'warning' , run , fill , ls1 , ls2)
        runi = int(run)
        filli = int(fill)
        ls = int(ls1)
        if filli not in allRuns:
            allRuns[filli] = {}
            con.execute( 'INSERT INTO Fills Values ({0} , NULL) '.format(filli) )
        if runi not in allRuns[filli]:
            allRuns[filli][runi] = {}
            con.execute( 'INSERT INTO Runs Values ({0} , {1}) '.format(runi,filli) )
        if ls in allRuns[filli][runi]:
            print('warning 2', run , ls )
        else:
            con.execute( 'INSERT INTO LumiSections Values ({0} , {1}) '.format(ls, runi) )
        allbx = {}
        bxi = None
        lrec = None
        ldel = None
        for bx in bxinfo[1:-1].split(' '):
            try:
                bxi = int(bx)
                lrec = ldel = None
            except:
                if ldel == None:
                    ldel = float(bx)
                else:
                    lrec = float(bx)
                    allbx[bxi] = [ldel,lrec]
                    con.execute( 'INSERT INTO BXs Values ({0} , {1} , {2} , {3} , {4}) '.format(bxi , ls , runi , lrec , ldel) )
                    bxi= None
                    
        allRuns[filli][runi][ls] = allbx
        con.commit()
        
con.close()
