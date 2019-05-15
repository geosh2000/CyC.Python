import json, requests, threading, MySQLdb, re, sys, progressbar, os, datetime

#PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "ccexporter.usr",                 # your username
        passwd  = "IFaoCJiH09rEqLVZVLsj",           # your password
        db      = "ccexporter")

dbEx = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "albert.sanchez",                 # your username
        passwd  = "3IJVkTzi90hHp9Z",           # your password
        db      = "comeycom_WFM")

curEx = dbEx.cursor()
query = "UPDATE ccexporter.agentDetails SET asesor=GETIDASESOR(descr_agente,2)"
curEx.execute( query )
print "Updating IDS... ",
try:
    dbEx.commit()
    curEx.close()
    dbEx.close()
    print "Done!"
except:
    print "Error!"