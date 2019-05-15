import MySQLdb
import time

#ComeyCome
db = MySQLdb.connect(host="cundbwf01.pricetravel.com.mx",    # your host, usually localhost
                     user="comeycom_wfm",         # your username
                     passwd="pricetravel2015",  # your password
                     db="comeycom_WFM")        # name of the data base

#PTVMN29
#db = MySQLdb.connect(host="cundbwf01.pricetravel.com.mx",    # your host, usually localhost
#                     user="ccexporter.usr",         # your username
                     #user="albert.sanchez",
#                     passwd="IFaoCJiH09rEqLVZVLsj",
                     #passwd="3IJVkTzi90hHp9Z",  # your password
#                     db="ccexporter")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
#query= "DELETE FROM mon_live_calls_row WHERE tipo=4 AND Last_Update<CAST(CONCAT(CURDATE(),' ',TIMEDIFF(CURTIME(),'00:01:00')) as DATETIME)"
#cur.execute(query)

import xmlrpclib
server_url = "http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/xmlrpc.do";
server = xmlrpclib.Server(server_url);
    
getQueues="Select * FROM Skill_queue"
cur.execute(getQueues)
qrows=cur.fetchall()

result=""

for y in range(len(qrows)):
    skill=str(qrows[y][0])
    queue=str(qrows[y][1])
    res = server.QM.stats( queue, "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".00:00:00", str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'OkDO.DnisOk' , 'KoDO.DnisKo'] )
    res.keys()

    for r in range( len(res['OkDO.DnisOk']) ):
        if r<1:
            continue
        query_insert="INSERT INTO d_dids_calls VALUES('" + res['OkDO.DnisOk'][r][0] + "', '" + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) + "'," + skill + "," + res['OkDO.DnisOk'][r][1] + ", NULL, NULL)"
        query_update="UPDATE d_dids_calls SET Calls=" + str(res['OkDO.DnisOk'][r][1]).replace("&nbsp;","") + " WHERE Did='" + res['OkDO.DnisOk'][r][0] + "' AND Fecha='" + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) + "' AND Skill=" + skill
        try:
            cur.execute(query_insert)
            print "Inserted!" + " // " + query_insert
        except:
            cur.execute(query_update)
            print "Updated!" + " // " + query_update
            
    for r in range( len(res['KoDO.DnisKo']) ):
        if r<1:
            continue
        query_insertKO="INSERT INTO d_dids_calls VALUES('" + res['KoDO.DnisKo'][r][0] + "', '" + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) + "'," + skill + ", NULL, " + res['KoDO.DnisKo'][r][1] + ", NULL)"
        query_updateKO="UPDATE d_dids_calls SET Unanswered='" + str(res['KoDO.DnisKo'][r][1]).replace("&nbsp;","0") + "' WHERE Did='" + res['KoDO.DnisKo'][r][0] + "' AND Fecha='" + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) + "' AND Skill=" + skill
        try:
            cur.execute(query_insertKO)
            print "Inserted!" + " // " + query_insertKO
        except:
            cur.execute(query_updateKO)
            print "Updated!" + " // " + query_updateKO

cur.close()
print "Cursor Closed"
db.close()
print "DB Closed"

print "DONE!"