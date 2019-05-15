import MySQLdb
import time

#ComeyCome
#db = MySQLdb.connect(host="www.comeycome.com",    # your host, usually localhost
#                     user="comeycom_wfm",         # your username
#                     passwd="pricetravel2015",  # your password
#                     db="comeycom_WFM")        # name of the data base

#PTVMN29
db = MySQLdb.connect(host="cundbwf01.pricetravel.com.mx",    # your host, usually localhost
                     user="ccexporter.usr",         # your username
                     passwd="IFaoCJiH09rEqLVZVLsj",  # your password
                     db="ccexporter")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
query= "DELETE FROM mon_live_calls_row WHERE tipo=5 AND Last_Update<CAST(CONCAT(CURDATE(),' ',TIMEDIFF(CURTIME(),'00:01:00')) as DATETIME)"
cur.execute(query)

import xmlrpclib
server_url = "http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/xmlrpc.do";
server = xmlrpclib.Server(server_url);
    
def my_range(start, end, step):
    while start <= end:
        yield str(start)
        start += step
        
getQueues="Select queue FROM Cola_Skill WHERE calls=1 ORDER BY queue"
cur.execute(getQueues)
qrows=cur.fetchall()


queues=["200", "201", "204", "205", "206", "207", "208", "209", "210", "211", "212", "213", "214", "215", "216", "217", "218", "219", "220", "221", "222", "223", "224", "225", "226", "227", "228", "229", "230", "231", "232", "233", "234", "235", "236", "237", "238", "239", "240", "241", "242", "243", "244", "245", "246", "247", "248", "249", "250", "251", "252", "259", "260", "261", "262", "263", "268", "269", "271", "272", "273", "274", "275", "286", "287", "290", "295", "298", "299", "380", "381", "382", "383", "384", "385", "386", "387", "388", "389", "393", "394", "395", "396", "401", "666", "667", "955"]       

result=""

res = server.QM.stats( "201|268|396|955", "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".00:00:00", str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'AgentsDO.AgentOccupancy'] )
res.keys()
for x in range(len(res['AgentsDO.AgentOccupancy'])):
    result=result+ " -Asesor- " +res['AgentsDO.AgentOccupancy'][x][1]+ " -Asesor- " +" -Sesion- "+res['AgentsDO.AgentOccupancy'][x][2]+" -Sesion- "+" -Pausa- "+res['AgentsDO.AgentOccupancy'][x][5]+" -Pausa- "+" -Call- "+res['AgentsDO.AgentOccupancy'][x][7]+" -Call- "
    
print result
query= "INSERT INTO mon_live_calls_row (tipo,live) VALUES (5,\""+result+"\")"
cur.execute(query)

cur.close()
print "Cursor Closed"
db.close()
print "DB Closed"