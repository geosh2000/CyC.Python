import json, requests
import re
import threading
import MySQLdb

interval = 3

def startTimer():
    threading.Timer(interval, startTimer).start()
    getData()

def services():
    #PTVMN29
    db = MySQLdb.connect(
    host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
    user    = "ccexporter.usr",                 # your username
    passwd  = "IFaoCJiH09rEqLVZVLsj",           # your password
    db      = "ccexporter")
    cur = db.cursor()

    url = 'http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/QmRealtime/jsonStatsApi.do'

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    patternU = re.compile(r"(?![{\[ ])u(?=['])")
    patternN = re.compile(r"(?:&nbsp;)")

    blocks = [
        "RealTimeDO.RTRiassunto",
        "RealTimeDO.RTCallsBeingProc",
        "RealTimeDO.RTAgentsLoggedIn",
        "RealTimeDO.WallRiassunto",
        "RealTimeDO.WallCallsBeingProc",
        "RealTimeDO.VisitorCallsProc",
        "RealTimeDO.VisitorTodaysOk",
        "RealTimeDO.VisitorTodaysKo",
        "RealTimeDO.RtLiveQueues",
        "RealTimeDO.RtLiveCalls",
        "RealTimeDO.RtLiveAgents",
        "RealTimeDO.RtLIveStatus",
        "RealTimeDO.RtAgentsRaw",
        "RealTimeDO.RtCallsRaw"
    ]

    for report in blocks:                               #Run every report of the array set
        print "Preparing %s..." % report,

        params = {                                      #Set parameters for post request
            'queues'          : '',
            'block'           : report
        }

        resp = requests.post( url, params = params, headers = headers, timeout=60 )
        data = resp.json()

        query = 'INSERT INTO rtMonitor VALUES (NULL, "%s", "%s", NULL) ON DUPLICATE KEY UPDATE json="%s"' % (report, data, data)
        cur.execute( query )
        # print query
        print " Done!"

    print "Committing to DB... ",
    db.commit()                                         #run all update and insert queries
    cur.close()
    db.close()

def getData():
    try:
        services()
        print "Done!"
        print "Obtaining Asesor Data..."
        try:
            execfile("agents.py")
            print "Done!"
        except:
            print "Error!"
        threading.Timer(interval, getData).start()          #start timer for next getData
    except:
        print "Error!"
        threading.Timer(interval, getData).start()

# startTimer()
getData()
