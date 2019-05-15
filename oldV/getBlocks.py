import MySQLdb

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
query= "DELETE FROM mon_live_calls_row WHERE tipo IN(1,2,3) AND Last_Update<CAST(CONCAT(CURDATE(),' ',TIMEDIFF(CURTIME(),'00:01:00')) as DATETIME)"
cur.execute(query)

import xmlrpclib
server_url = "http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/xmlrpc.do";
server = xmlrpclib.Server(server_url);
#res = server.QM.realtime( "224", "robot", "robot","", "", [ 'RealtimeDO.RTRiassunto', 'RealtimeDO.RTCallsBeingProc', 'RealtimeDO.RTAgentsLoggedIn' ] )
res = server.QM.realtime( "", "robot", "robot","", "", [ 'RealtimeDO.RTCallsBeingProc','RealtimeDO.RTRiassunto', 'RealtimeDO.RTAgentsLoggedIn' ] )
res.keys()

text_rsm=""
text_cbp=""
text_agn=""
for t in range( len (res['RealtimeDO.RTCallsBeingProc'])):
    text_cbp=text_cbp+"<tr>"
    for c in range( len( res['RealtimeDO.RTCallsBeingProc'][t] )):
        text_cbp=text_cbp+"<td id='" + res['RealtimeDO.RTCallsBeingProc'][0][c] +"'>"+res['RealtimeDO.RTCallsBeingProc'][t][c]+"</td>"
        
    text_cbp=text_cbp+"</tr>"
query= "INSERT INTO mon_live_calls_row (tipo,live) VALUES (2,\""+text_cbp+"\")"
cur.execute(query)   
print query

for t in range( len (res['RealtimeDO.RTRiassunto'])):
    text_rsm=text_rsm+"<tr>"
    for c in range( len( res['RealtimeDO.RTRiassunto'][t] )):
        text_rsm=text_rsm+"<td id='" + res['RealtimeDO.RTRiassunto'][0][c] +"'>"+res['RealtimeDO.RTRiassunto'][t][c]+"</td>"
        
    text_rsm=text_rsm+"</tr>"
query= "INSERT INTO mon_live_calls_row (tipo,live) VALUES (1,\""+text_rsm+"\")"
cur.execute(query)   
print query

for t in range( len (res['RealtimeDO.RTAgentsLoggedIn'])):
    text_agn=text_agn+"<tr>"
    for c in range( len( res['RealtimeDO.RTAgentsLoggedIn'][t] )):
        text_agn=text_agn+"<td id='" + res['RealtimeDO.RTAgentsLoggedIn'][0][c] +"'>"+res['RealtimeDO.RTAgentsLoggedIn'][t][c]+"</td>"
        
    text_agn=text_agn+"</tr>"
query= "INSERT INTO mon_live_calls_row (tipo,live) VALUES (3,\""+text_agn+"\")"
cur.execute(query)   
print query 

cur.close()
print "Cursor Closed"
db.close()
print "DB Closed"
