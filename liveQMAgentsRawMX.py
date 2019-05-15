import json, requests
import re
import threading
import MySQLdb

def createFields( item ):
        fields = []

        for field in item:
            fields.append(field)
        
        return fields

def createAgent( item, fields, re ):

    patternQ        = re.compile(r"[\(]|[\)]")
    patternSpace    = re.compile(r"&nbsp;")
    patternSp       = re.compile(r" ")
    patternPause    = re.compile(r" \#[0-9]+")
    patternAcb      = re.compile(r"ACB_")
    
    agent = {}

    i = 0
    for field in fields:
        fname = patternSp.sub('',patternAcb.sub('', patternSpace.sub('', field).strip()).title())
        agent[fname]    = patternSpace.sub('', item[i]).strip()
        i += 1
    
    return agent



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

block = blocks[12]

print "Preparing %s..." % block,

params = {
    'queues'          : '*',
    'block'           : block
}

resp = requests.post( url, params = params, headers = headers, timeout=60 )
data = resp.json()
print "Done!"

updateFlag = "UPDATE liveMonitorMX SET updateFlag = 0"
cur.execute( updateFlag )
db.commit()

agents = []

i = 0
for item in data[params['block']]:
    # print item
    if i == 0:
        fields = createFields( item )

    if i > 0:
        tmp = createAgent( item, fields, re )
        agents.append(tmp)

    i += 1

# for item in agents[0].keys():
#     print item

for item in agents:
    fieldQ = ""
    valQ = ""
    dupQ = ""
    for field in item.keys():
        fieldQ += "%s," % field
        valQ += "'%s'," % item[field]
        dupQ += "%s=VALUES(%s)," % (field, field)
    fieldQ = fieldQ[0:-1]
    valQ = valQ[0:-1]
    dupQ = dupQ[0:-1]
    
    query = "INSERT INTO liveMonitorMX (updateFlag, %s) VALUES (1, %s) ON DUPLICATE KEY UPDATE updateFlag=1, %s;" % (fieldQ, valQ, dupQ)
    print query
    
#     cur.execute( query )

# print "Commiting... ",
# db.commit()                                         #run all update and insert queries
# print "Done!"

# print "Deleting inactive... ",
# updateFlag = "DELETE FROM liveMonitorMX WHERE updateFlag = 0 AND Agent NOT LIKE 'wait%'"
# cur.execute( updateFlag )
# db.commit()
# print "Done!"
cur.close()
db.close()



