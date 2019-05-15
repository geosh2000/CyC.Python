import MySQLdb, datetime
print "Updating DT...",
# PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "comeycom_wfm",                 # your username
        passwd  = "pricetravel2015",           # your password
        db      = "comeycom_WFM")

sk = {}

q = "UPDATE asesores_ausentismos a LEFT JOIN asesores_programacion b ON a.asesor = b.asesor AND a.Fecha = b.Fecha SET pdt_done = COALESCE(TIME_TO_SEC(TIMEDIFF(IF(CHECKLOG(a.Fecha, a.asesor, 'out') > je, je, CHECKLOG(a.Fecha, a.asesor, 'out')), IF(CHECKLOG(a.Fecha, a.asesor, 'in') < js, js, CHECKLOG(a.Fecha, a.asesor, 'in')))) / TIME_TO_SEC(TIMEDIFF(je, js)) * 8,0) WHERE ausentismo = 19 AND a = 1 AND a.Fecha >= ADDDATE(CURDATE(), - 60)"
cur = db.cursor()


try:
    cur.execute( q )
    db.commit()
    print "Done!"
except Exception, e:
    print "Error!"
    print str(e)

cur.close()
db.close()
