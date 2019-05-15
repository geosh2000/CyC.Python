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
                     #user="albert.sanchez",
                     passwd="IFaoCJiH09rEqLVZVLsj",
                     #passwd="3IJVkTzi90hHp9Z",  # your password
                     db="ccexporter")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
#query= "DELETE FROM mon_live_calls_row WHERE tipo=4 AND Last_Update<CAST(CONCAT(CURDATE(),' ',TIMEDIFF(CURTIME(),'00:01:00')) as DATETIME)"
#cur.execute(query)

import xmlrpclib
server_url = "http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/xmlrpc.do";
server = xmlrpclib.Server(server_url);
    
getQueues="Select * FROM Skill_queue"
#cur.execute(getQueues)
#qrows=cur.fetchall()

result=""

queue="224|206|207|208|227|232|234|259|220"
grupo="Ventas"

#def updateCalls(queue, grupo):
query="SELECT IF(MIN(Hora) IS NULL,'00:00:00',ADDTIME(MIN(HORA),'-00:30:00')) as Hora FROM mon_calls_details WHERE Desconexion NOT IN ('Abandon', 'Agent', 'Caller') AND Hora>=ADDTIME(CURTIME(),'-04:00:00') AND Fecha=CURDATE() AND grupo='"
query= query + str(grupo) + "'"
cur.execute(query)
time_query=cur.fetchall()
res = server.QM.stats( str(queue), "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +"." + str(time_query[0][0]), str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'DetailsDO.CallsOK' , 'DetailsDO.CallsKO'] )
#res = server.QM.stats( str(queue), "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +"." + "18:35:00", str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'DetailsDO.CallsOK' , 'DetailsDO.CallsKO'] )
time_query = None
for t in res.keys():
    for r in range( len(res[t]) ):
         print str(r+1) + " de " + str(len(res[t])) + " //s " + grupo + " " + t
         query=""
         
         if(t=="DetailsDO.CallsKO"):
             if (r==0):
		 continue
             elif res[t][r][2]=="*":
                 continue
             
             waittmp=str(res[t][r][7]).replace(" &nbsp;","")
             wait=int(waittmp[:waittmp.find(":")])*60 + int(waittmp[-2:])
                      
             try:
                query= "INSERT INTO mon_calls_details VALUES (NULL,'" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "', '" + str(res[t][r][0])[8:] + "','" + str(res[t][r][1]).replace(" &nbsp;","") + "','" + str(res[t][r][2]).replace(" &nbsp;","") + "','" + str(res[t][r][3]).replace(" &nbsp;","") + "','" + str(res[t][r][4]).replace(" &nbsp;","") + "','" + str(res[t][r][6]).replace(" &nbsp;","") + "','" + str(wait) + "',0,NULL,NULL,0,'" + str(grupo) + "',NULL)"    
                cur.execute(query)
                db.commit()
                query_status="INSERT"
             except:
                try:
                    query= "UPDATE mon_calls_details SET Agente= '" + str(res[t][r][1]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][4]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][6]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=0 WHERE Fecha='" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "' AND Hora='" + str(res[t][r][0])[8:] + "' AND Caller='" + str(res[t][r][2]) + "' AND Cola='" + str(res[t][r][3]) + "' AND flag_manual=0"    
                    cur.execute(query)
                    db.commit()
                    query_status="UPDATE"
                except:
                    query_status="ERROR"
                    a=1
             print query_status
         elif (t=="DetailsDO.CallsOK"):

             

             if (r==0):
                 
                 continue
             elif res[t][r][1]=="*":
                 
                 continue
             
             
             
             waittmp=str(res[t][r][4]).replace(" &nbsp;","")
             wait=int(waittmp[:waittmp.find(":")])*60 + int(waittmp[-2:])
             
             durtmp=str(res[t][r][5]).replace(" &nbsp;","")
             durlen=len(durtmp)
             if durlen==7:
                 dur=int(durtmp[:durtmp.find(":")])*60*60 + int(durtmp[(durtmp.find(":")+1):durtmp.find(":",durtmp.find(":")+1)])*60 + int(durtmp[-2:])
             else:
                 dur=int(durtmp[:durtmp.find(":")])*60 + int(durtmp[-2:])
            
             
             
             try:
                query= "INSERT INTO mon_calls_details VALUES (NULL,'" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "', '" + str(res[t][r][0])[8:] + "','" + str(res[t][r][8]).replace(" &nbsp;","") + "','" + str(res[t][r][1]).replace(" &nbsp;","") + "','" + str(res[t][r][2]).replace(" &nbsp;","") + "','" + str(res[t][r][7]).replace(" &nbsp;","") + "','" + str(res[t][r][3]).replace(" &nbsp;","") + "','" + str(wait) + "',1,'" + str(dur) + "',NULL,0,'" + str(grupo) + "',NULL)"    
                cur.execute(query)
                db.commit()
                query_status="INSERT"
             except:
		try:
                    query= "UPDATE mon_calls_details SET Agente= '" + str(res[t][r][8]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][7]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][3]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=1, Duracion='" + str(dur) + "' WHERE Fecha='" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "' AND Hora='" + str(res[t][r][0])[8:] + "' AND Caller='" + str(res[t][r][1]) + "' AND Cola='" + str(res[t][r][2]) + "' AND flag_manual=0"    
                    cur.execute(query)
                    db.commit()
                    query_status="UPDATE"
                except:
		    query_status="ERROR"
                    a=1
             print query_status
         else:
             continue

queue="226|229|233|235|230|666"
grupo="SAC"

#def updateCalls(queue, grupo):
query="SELECT IF(MIN(Hora) IS NULL,'00:00:00',ADDTIME(MIN(HORA),'-00:30:00')) as Hora FROM mon_calls_details WHERE Desconexion NOT IN ('Abandon', 'Agent', 'Caller') AND Hora>=ADDTIME(CURTIME(),'-04:00:00') AND Fecha=CURDATE() AND grupo='"
query= query + str(grupo) + "'"
cur.execute(query)
time_query=cur.fetchall()
res = server.QM.stats( str(queue), "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +"." + str(time_query[0][0]), str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'DetailsDO.CallsOK' , 'DetailsDO.CallsKO'] )
#res = server.QM.stats( str(queue), "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +"." + "18:35:00", str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'DetailsDO.CallsOK' , 'DetailsDO.CallsKO'] )
time_query = None
for t in res.keys():
    for r in range( len(res[t]) ):
         print str(r+1) + " de " + str(len(res[t])) + " // " + grupo + " " + t
         query=""
         for c in range( len( res[t][r] )):
            query=query + str(res[t][r][c])
         if(t=="DetailsDO.CallsKO"):
             if (r==0):
                 continue
             elif res[t][r][2]=="*":
                 continue
             
             waittmp=str(res[t][r][7]).replace(" &nbsp;","")
             wait=int(waittmp[:waittmp.find(":")])*60 + int(waittmp[-2:])
                      
             try: 
                query= "INSERT INTO mon_calls_details VALUES (NULL,'" + str(ime.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "', '" + str(res[t][r][0])[8:] + "','" + str(res[t][r][1]).replace(" &nbsp;","") + "','" + str(res[t][r][2]).replace(" &nbsp;","") + "','" + str(res[t][r][3]).replace(" &nbsp;","") + "','" + str(res[t][r][4]).replace(" &nbsp;","") + "','" + str(res[t][r][6]).replace(" &nbsp;","") + "','" + str(wait) + "',0,NULL,NULL,0,'" + str(grupo) + "',NULL) ON DUPLICATE KEY UPDATE Agente= '" + str(res[t][r][1]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][4]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][6]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=0"    
                cur.execute(query)
                db.commit()
                query_status="INSERT"
             except:
                try:
                    query= "UPDATE mon_calls_details SET Agente= '" + str(res[t][r][1]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][4]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][6]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=0 WHERE Fecha='" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "' AND Hora='" + str(res[t][r][0])[8:] + "' AND Caller='" + str(res[t][r][2]) + "' AND Cola='" + str(res[t][r][3]) + "' AND flag_manual=0"    
                    cur.execute(query)
                    db.commit()
                    query_status="UPDATE"
                except:
		    query_status="ERROR"
                    a=1
             print query_status
         elif (t=="DetailsDO.CallsOK"):
             if (r==0):
                 continue
             elif res[t][r][1]=="*":
                 continue
             
             waittmp=str(res[t][r][4]).replace(" &nbsp;","")
             wait=int(waittmp[:waittmp.find(":")])*60 + int(waittmp[-2:])
             
             durtmp=str(res[t][r][5]).replace(" &nbsp;","")
             durlen=len(durtmp)
             if durlen==7:
                 dur=int(durtmp[:durtmp.find(":")])*60*60 + int(durtmp[(durtmp.find(":")+1):durtmp.find(":",durtmp.find(":")+1)])*60 + int(durtmp[-2:])
             else:
                 dur=int(durtmp[:durtmp.find(":")])*60 + int(durtmp[-2:])
            
            
             
             try:
                query= "INSERT INTO mon_calls_details VALUES (NULL,'" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "', '" + str(res[t][r][0])[8:] + "','" + str(res[t][r][8]).replace(" &nbsp;","") + "','" + str(res[t][r][1]).replace(" &nbsp;","") + "','" + str(res[t][r][2]).replace(" &nbsp;","") + "','" + str(res[t][r][7]).replace(" &nbsp;","") + "','" + str(res[t][r][3]).replace(" &nbsp;","") + "','" + str(wait) + "',1,'" + str(dur) + "',NULL,0,'" + str(grupo) + "',NULL) ON DUPLICATE KEY UPDATE Agente= '" + str(res[t][r][8]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][7]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][3]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=1, Duracion='" + str(dur) + "'"    
                cur.execute(query)
                db.commit()
                query_status="INSERT"
             except:
                try:
                    query= "UPDATE mon_calls_details SET Agente= '" + str(res[t][r][8]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][7]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][3]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=1, Duracion='" + str(dur) + "' WHERE Fecha='" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "' AND Hora='" + str(res[t][r][0])[8:] + "' AND Caller='" + str(res[t][r][1]) + "' AND Cola='" + str(res[t][r][2]) + "' AND flag_manual=0"    
                    cur.execute(query)
                    db.commit()
                    query_status="UPDATE"
                except:
                    query_status="ERROR"
                    a=1
             print query_status
         else:
             continue
         
queue="231|236|222|223|204|212|396|955|261|262|263|252|239|251|249|288|218"
grupo="Others"

#def updateCalls(queue, grupo):
query="SELECT IF(MIN(Hora) IS NULL,'00:00:00',ADDTIME(MIN(HORA),'-00:30:00')) as Hora FROM mon_calls_details WHERE Desconexion NOT IN ('Abandon', 'Agent', 'Caller') AND Hora>=ADDTIME(CURTIME(),'-04:00:00') AND Fecha=CURDATE() AND grupo='"
query= query + str(grupo) + "'"
cur.execute(query)
time_query=cur.fetchall()
res = server.QM.stats( str(queue), "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +"." + str(time_query[0][0]), str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'DetailsDO.CallsOK' , 'DetailsDO.CallsKO'] )
#res = server.QM.stats( str(queue), "robot", "robot","", "",str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +"." + "18:35:00", str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) +".23:59:59", "", [ 'DetailsDO.CallsOK' , 'DetailsDO.CallsKO'] )
time_query = None
for t in res.keys():
    for r in range( len(res[t]) ):
         print str(r+1) + " de " + str(len(res[t])) + " // " + grupo + " " + t
         query=""
         for c in range( len( res[t][r] )):
            query=query + str(res[t][r][c])
         if(t=="DetailsDO.CallsKO"):
             if (r==0):
                 continue
             elif res[t][r][2]=="*":
                 continue
             
             waittmp=str(res[t][r][7]).replace(" &nbsp;","")
             wait=int(waittmp[:waittmp.find(":")])*60 + int(waittmp[-2:])
                      
             try:
                query= "INSERT INTO mon_calls_details VALUES (NULL,'" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "', '" + str(res[t][r][0])[8:] + "','" + str(res[t][r][1]).replace(" &nbsp;","") + "','" + str(res[t][r][2]).replace(" &nbsp;","") + "','" + str(res[t][r][3]).replace(" &nbsp;","") + "','" + str(res[t][r][4]).replace(" &nbsp;","") + "','" + str(res[t][r][6]).replace(" &nbsp;","") + "','" + str(wait) + "',0,NULL,NULL,0,'" + str(grupo) + "',NULL) ON DUPLICATE KEY UPDATE Agente= '" + str(res[t][r][1]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][4]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][6]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=0"                    
		cur.execute(query)
                db.commit()
                query_status="INSERT"
             except:
                try:
                    query= "UPDATE mon_calls_details SET Agente= '" + str(res[t][r][1]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][4]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][6]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=0 WHERE Fecha='" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "' AND Hora='" + str(res[t][r][0])[8:] + "' AND Caller='" + str(res[t][r][2]) + "' AND Cola='" + str(res[t][r][3]) + "' AND flag_manual=0"    
                    cur.execute(query)
                    db.commit()
                    query_status="UPDATE"
                except:
		    query_status="ERROR"
                    a=1
             print query_status
         elif (t=="DetailsDO.CallsOK"):
             if (r==0):
                 continue
             elif res[t][r][1]=="*":
                 continue
             
             waittmp=str(res[t][r][4]).replace(" &nbsp;","")
             wait=int(waittmp[:waittmp.find(":")])*60 + int(waittmp[-2:])
             
             durtmp=str(res[t][r][5]).replace(" &nbsp;","")
             durlen=len(durtmp)
             if durlen==7:
                 dur=int(durtmp[:durtmp.find(":")])*60*60 + int(durtmp[(durtmp.find(":")+1):durtmp.find(":",durtmp.find(":")+1)])*60 + int(durtmp[-2:])
             else:
                 dur=int(durtmp[:durtmp.find(":")])*60 + int(durtmp[-2:])
            
            
             
             try:
                query= "INSERT INTO mon_calls_details VALUES (NULL,'" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "', '" + str(res[t][r][0])[8:] + "','" + str(res[t][r][8]).replace(" &nbsp;","") + "','" + str(res[t][r][1]).replace(" &nbsp;","") + "','" + str(res[t][r][2]).replace(" &nbsp;","") + "','" + str(res[t][r][7]).replace(" &nbsp;","") + "','" + str(res[t][r][3]).replace(" &nbsp;","") + "','" + str(wait) + "',1,'" + str(dur) + "',NULL,0,'" + str(grupo) + "',NULL) ON DUPLICATE KEY UPDATE Agente= '" + str(res[t][r][8]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][7]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][3]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=1, Duracion='" + str(dur) + "'"    
                cur.execute(query)
                db.commit()
                query_status="INSERT"
             except:
                try:
                    query= "UPDATE mon_calls_details SET Agente= '" + str(res[t][r][8]).replace(" &nbsp;","") + "' , Desconexion='" + str(res[t][r][7]).replace(" &nbsp;","") + "' , IVR='" + str(res[t][r][3]).replace(" &nbsp;","") + "' , Wait='" + str(wait) + "' , Answered=1, Duracion='" + str(dur) + "' WHERE Fecha='" + str(time.localtime()[0]) + "-" + str(res[t][r][0])[:2] + "-" + str(res[t][r][0])[3:-11] + "' AND Hora='" + str(res[t][r][0])[8:] + "' AND Caller='" + str(res[t][r][1]) + "' AND Cola='" + str(res[t][r][2]) + "' AND flag_manual=0"    
                    cur.execute(query)
                    db.commit()
                    query_status="UPDATE"
                except:
		    query_status="ERROR"
                    a=1
             print query_status
         else:
             continue

#def start():
#    try:
#       updateCalls("224|227|232|234|259|207|206|208|220","Ventas")
#       updateCalls("226|229|233|235|230|666","SAC")
#       updateCalls("231|236|222|223|204|212|261|262|263|252|239","Others")
#    except:
#       pass

         
#start()
#updateCalls("224|227|232|234|259|207|206|208|220","Ventas")
#updateCalls("226|229|233|235|230|666","SAC")
#updateCalls("231|236|222|223|204|212|261|262|263|252|239","Others")
         
cur.close()
print "Cursor Closed"
db.close()       
print "DB Closed" 
        
 

