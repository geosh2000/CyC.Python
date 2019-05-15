import json, requests
import threading
import MySQLdb

#PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "ccexporter.usr",                 # your username
        passwd  = "IFaoCJiH09rEqLVZVLsj",           # your password
        db      = "ccexporter")

url = 'http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/agent/jsonEditorApi.do'

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}


cur = db.cursor()

print "Preparing %s..." % 'Agents',

params = {

}

resp = requests.get( url, params = params, headers = headers )
data = resp.json()

query = 'INSERT INTO rtMonitor VALUES (NULL, "%s", "%s", NULL) ON DUPLICATE KEY UPDATE json="%s"' % ('Agents', data, data)
cur.execute( query )
print " Done!"

print "Committing to DB... ",
db.commit()
cur.close()
db.close()
print "Done!"
