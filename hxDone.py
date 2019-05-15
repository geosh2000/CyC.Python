import MySQLdb, datetime
print "Updating HX...",
# PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "comeycom_wfm",                 # your username
        passwd  = "pricetravel2015",           # your password
        db      = "comeycom_WFM")

sk = {}

# q = "UPDATE asesores_logs a RIGHT JOIN asesores_programacion b ON a.asesor = b.asesor AND ((login < x1e AND logout > x1s) OR (login < x2e AND logout > x2s)) SET  phx_done = IF(COALESCE(TIME_TO_SEC(TIMEDIFF(IF(login < x1e AND logout > x1s, IF(logout > x1e, x1e, logout), NULL), IF(login < x1e AND logout > x1s,IF(login < x1s, x1s, login),NULL))) / 60 / 60,0) + COALESCE(TIME_TO_SEC(TIMEDIFF(IF(login < x2e AND logout > x2s,IF(logout > x2e, x2e, logout),NULL),IF(login < x2e AND logout > x2s,IF(login < x2s, x2s, login),NULL))) / 60 / 60,0) > COALESCE(TIMEDIFF(x1e, x1s),0) + COALESCE(TIMEDIFF(x2e, x2s),0), COALESCE(TIMEDIFF(x1e, x1s),0) + COALESCE(TIMEDIFF(x2e, x2s),0),COALESCE(TIME_TO_SEC(TIMEDIFF(IF(login < x1e AND logout > x1s,IF(logout > x1e, x1e, logout),NULL),IF(login < x1e AND logout > x1s,IF(login < x1s, x1s, login),NULL))) / 60 / 60,0) + COALESCE(TIME_TO_SEC(TIMEDIFF(IF(login < x2e AND logout > x2s,IF(logout > x2e, x2e, logout),NULL),IF(login < x2e AND logout > x2s,IF(login < x2s,x2s, login),NULL))) / 60 / 60,0)) WHERE (x1s != x1e OR x2s != x2e) AND x1s >= ADDDATE(CURDATE(),-60)"
q = ("UPDATE asesores_programacion "
    "SET  "
    "    phx_done = IF(COALESCE(TIME_TO_SEC(TIMEDIFF(IF(CHECKLOG(Fecha, asesor, 'in') < x1e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x1s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'out') > x1e, "
    "                                        x1e, "
    "                                        CHECKLOG(Fecha, asesor, 'out')), "
    "                                    NULL), "
    "                                IF(CHECKLOG(Fecha, asesor, 'in') < x1e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x1s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'in') < x1s, "
    "                                        x1s, "
    "                                        CHECKLOG(Fecha, asesor, 'in')), "
    "                                    NULL))) / 60 / 60, "
    "                0) + COALESCE(TIME_TO_SEC(TIMEDIFF(IF(CHECKLOG(Fecha, asesor, 'in') < x2e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x2s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'out') > x2e, "
    "                                        x2e, "
    "                                        CHECKLOG(Fecha, asesor, 'out')), "
    "                                    NULL), "
    "                                IF(CHECKLOG(Fecha, asesor, 'in') < x2e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x2s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'in') < x2s, "
    "                                        x2s, "
    "                                        CHECKLOG(Fecha, asesor, 'in')), "
    "                                    NULL))) / 60 / 60, "
    "                0) > COALESCE(TIMEDIFF(x1e, x1s), 0) + COALESCE(TIMEDIFF(x2e, x2s), 0), "
    "        COALESCE(TIMEDIFF(x1e, x1s), 0) + COALESCE(TIMEDIFF(x2e, x2s), 0), "
    "        COALESCE(TIME_TO_SEC(TIMEDIFF(IF(CHECKLOG(Fecha, asesor, 'in') < x1e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x1s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'out') > x1e, "
    "                                        x1e, "
    "                                        CHECKLOG(Fecha, asesor, 'out')), "
    "                                    NULL), "
    "                                IF(CHECKLOG(Fecha, asesor, 'in') < x1e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x1s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'in') < x1s, "
    "                                        x1s, "
    "                                        CHECKLOG(Fecha, asesor, 'in')), "
    "                                    NULL))) / 60 / 60, "
    "                0) + COALESCE(TIME_TO_SEC(TIMEDIFF(IF(CHECKLOG(Fecha, asesor, 'in') < x2e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x2s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'out') > x2e, "
    "                                        x2e, "
    "                                        CHECKLOG(Fecha, asesor, 'out')), "
    "                                    NULL), "
    "                                IF(CHECKLOG(Fecha, asesor, 'in') < x2e "
    "                                        AND CHECKLOG(Fecha, asesor, 'out') > x2s, "
    "                                    IF(CHECKLOG(Fecha, asesor, 'in') < x2s, "
    "                                        x2s, "
    "                                        CHECKLOG(Fecha, asesor, 'in')), "
    "                                    NULL))) / 60 / 60, "
    "                0)) "
    "WHERE "
    "    (x1s != x1e OR x2s != x2e) "
    "        AND x1s >= ADDDATE(CURDATE(), - 60) ")

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
