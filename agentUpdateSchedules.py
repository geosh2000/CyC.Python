import MySQLdb, datetime

# PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "comeycom_wfm",                 # your username
        passwd  = "pricetravel2015",           # your password
        db      = "comeycom_WFM")

sk = {}

q = "SELECT TIMETODATETIME(id) FROM `Historial Programacion` WHERE LastUpdate >= CAST(CONCAT(CURDATE(),' 00:00:00') as DATETIME)"
cur = db.cursor()

print "Updating Schedules...",
try:
    cur.execute( q )
    db.commit()
    print "Done!"
except Exception, e:
    print "Error!"
    print str(e)

cur.close()
db.close()
