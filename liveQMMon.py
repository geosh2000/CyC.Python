import json, requests
import re
import threading
import MySQLdb

interval = 1

# def startTimer():
#     threading.Timer(interval, startTimer).start()
#     getData()

def services():
    url = 'http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/QmRealtime/jsonStatsApi.do'

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    patternU = re.compile(r"(?![{\[ ])u(?=['])")
    patternN = re.compile(r"(?:&nbsp;)")

    blocks = [
        # "RealTimeDO.RTRiassunto",
        # "RealTimeDO.RTCallsBeingProc",
        # "RealTimeDO.RTAgentsLoggedIn",
        # "RealTimeDO.WallRiassunto",
        # "RealTimeDO.WallCallsBeingProc",
        # "RealTimeDO.VisitorCallsProc",
        # "RealTimeDO.VisitorTodaysOk",
        # "RealTimeDO.VisitorTodaysKo",
        # "RealTimeDO.RtLiveQueues",
        # "RealTimeDO.RtLiveCalls",
        # "RealTimeDO.RtLiveAgents",
        # "RealTimeDO.RtLIveStatus",
        # "RealTimeDO.RtAgentsRaw",
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

        # query = 'INSERT INTO rtMonitor VALUES (NULL, "%s", "%s", NULL) ON DUPLICATE KEY UPDATE json="%s"' % (report, data, data)
        # cur.execute( query )
        # print query
        print " Done!"

        values = []
        for i in range(len(data[report])):
            if i == 0:
                fields = []

            vals = []

            for x in range(len(data[report][i])):
                if i == 0:
                    fields.append(data[report][i][x])
                else:
                    vals.append(data[report][i][x])

            if i != 0:
                values.append(vals)


        upload(fields, values)

def upload( fields, values ):
    payload = {"fields": fields, "values": values}
    url = "http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/RtMonitor/rtCalls/"
    headers = {"Content-Type": "application/json"}
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    # result = r.json()
    print r.json()
    #
    # for f in result['data']:
    #     print f

services()
