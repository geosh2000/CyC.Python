import json, requests, operator
import re
import threading
import MySQLdb


#PTVMN29
db = MySQLdb.connect(
host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
user    = "ccexporter.usr",                 # your username
passwd  = "IFaoCJiH09rEqLVZVLsj",           # your password
db      = "ccexporter")
cur = db.cursor()

url = 'http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/QmRealtime/jsonStatsApi.do'
# url = 'http://queuemetrics-co.pricetravel.com.mx:8080/qm/QmRealtime/jsonStatsApi.do'

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}

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

block = blocks[13]

print "Preparing %s..." % block,

params = {
    'queues'          : '*',
    'block'           : block
}

resp = requests.post( url, params = params, headers = headers, timeout=60 )
data = resp.json()
print "Done!"

# updateFlag = "UPDATE liveMonitor SET updateFlag = 0"
# cur.execute( updateFlag )
# db.commit()

agents = []

def createFields( item ):
    fields = []

    for field in item:
        fields.append(field)
    
    return fields

def createAgent( item, fields, re ):

    patternQ = re.compile(r"[\(]|[\)]")
    patternSpace    = re.compile(r"&nbsp;")
    patternSp       = re.compile(r" ")
    patternPause    = re.compile(r" \#[0-9]+")
    patternAcb    = re.compile(r"ACB_")
    
    agent = {}

    i = 0
    for field in fields:
        fname = patternSp.sub('',patternAcb.sub('', patternSpace.sub('', field).strip()))
        agent[fname]    = patternSpace.sub('', item[i]).strip()
        i += 1
    
    return agent

dataOK = []

i = 0
for it in data[params['block']]:
    if i > 0:
        dataOK.append(it)
        x = i-1
        # dataOK[x][3] = int(it[3])
    i += 1

# Build Fields
fields = createFields( data[params['block']][0] )

# Sort by Answered
sorter = lambda x: (x[3])

def takeSecond(elem):
    return elem[3]

# Build arrays
for item in sorted(dataOK, key = takeSecond):
    tmp = createAgent( item, fields, re )
    agents.append(tmp)


# for item in agents[0].keys():
#     print item
dupQ = ""
updQ = "agent=agent"

i=1
for item in agents:
    # if item["RT_agent"] == '':
    #     fieldQ = "Agent,"
    #     valQ = "'wait%s'," % i
    #     i += 1
    # else:
    fieldQ = ""
    valQ = "" 
    dupQ = ""
    updQ = ""
    for field in item.keys():
        fieldQ += "%s," % field
        valQ += "'%s'," % item[field]
        dupQ += "%s=VALUES(%s)," % (field, field)
        updQ += "%s=NULL," % (field)
    fieldQ = fieldQ[0:-1]
    valQ = valQ[0:-1]
    dupQ = dupQ[0:-1]
    updQ = updQ[0:-1]
    
    query = "INSERT INTO RT_liveCalls (updateFlag, %s) VALUES (1, %s);" % (fieldQ, valQ)
    cur.execute( query )

print "Commiting... ",
db.commit()                                         #run all update and insert queries
print "Done!"

# print "Deleting inactive... ",
# updateFlag = "UPDATE liveMonitor SET %s WHERE updateFlag = 0" % updQ
# cur.execute( updateFlag )
# db.commit()
print "Done!"
cur.close()
db.close()

