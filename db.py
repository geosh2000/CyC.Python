import MySQLdb

#PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "ccexporter.usr",                 # your username
        passwd  = "IFaoCJiH09rEqLVZVLsj",           # your password
        db      = "ccexporter")                     # name of the data base
