import json, requests, threading, MySQLdb, re, sys, progressbar, os, datetime

#PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "albert.sanchez",                 # your username
        passwd  = "3IJVkTzi90hHp9Z",           # your password
        db      = "comeycom_WFM")

url = 'http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/agent/jsonEditorApi.do'

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}

patternAgent    = re.compile(r"[ ]?\([0-9]*\)[ ]?")
patternKey      = re.compile(r", $")
patternSpace    = re.compile(r"&nbsp;")

keys    = {}
vals    = {}
update  = {}
queries = []

# os.system('clear')

params = {

}

print "Obtaining %s..." % 'Agents Details',
try:
    resp = requests.get( url, params = params, headers = headers )
    print "Done!"

    data = resp.json()

    cur = db.cursor()

    num = len(data)                                                     #Number of Regs

    bar = progressbar.ProgressBar( maxval = num, \
        redirect_stdout=True, \
        widgets=[progressbar.Bar('=', 'Creating queries: [', ']'), ' ',\
            progressbar.Percentage()])                                          #ProgressBar options

    bar.start()

    for idx, row in enumerate(data):

        keys        = "("
        vals        = "("
        update      = ""

        for index, item in enumerate(data[idx]):

            #Key Constructor
            val     = "`%s`, " % item
            keys    = "%s %s" % ( keys, val )

            #Values Constructor
            valor   = "'%s', " % data[idx][item]
            if item == 'descr_agente':
                valor = patternAgent.sub( '', valor )

            vals    = "%s %s" % ( vals, valor )

            #Update Constructor
            update = "%s `%s` = %s" % (update, item, valor)

        keys    = patternKey.sub( " )", keys    )
        vals    = patternKey.sub( " )", vals    )
        update  = patternKey.sub( ""  , update  )

        # query = "INSERT INTO ccexporter.agentDetails %s VALUES %s ON DUPLICATE KEY UPDATE %s" % (keys, vals, update)
        query = "INSERT INTO ccexporter.agentDetails %s VALUES %s ON DUPLICATE KEY UPDATE %s" % (keys, vals, update)
        cur.execute( query )
        bar.update(idx)

    bar.finish()

    print "Committing... ",
    try:
        db.commit()
        print "Done!"
    except:
        cur.close()
        print "Error!"

    query = "UPDATE ccexporter.agentDetails SET asesor=GETIDASESOR(descr_agente,2)"
    cur.execute( query )
    print "Updating IDS... ",
    try:
        db.commit()
        cur.close()
        db.close()
        print "Done!"
    except:
        cur.close()
        db.close()
        print "Error!"

except:
    print "Error!"


# keys[report]    = "("
# vals[report]    = {}
# update[report]  = {}
# keyName         = {}
#
# # try:
# resp = requests.get( url, params = params, headers = headers )
# print "Done!"
# data = resp.json()
#
# cur = db.cursor()
#
# num = len(data[report])                                                     #Number of Regs
#
# bar = progressbar.ProgressBar( maxval = num, \
#     redirect_stdout=True, \
#     widgets=[progressbar.Bar('=', 'Creating queries: [', ']'), ' ',\
#         progressbar.Percentage()])#ProgressBar options
#
# bar.start()
# i   = 0                                                                     #Init iterator
#
# for index, value in enumerate(data[report]):                                #Iteration for each report
#
#     if index != 0:                                                          #Declare string for values
#         vals[report][index]     = "("
#         update[report][index]   = ""
#
#     for idx, item in enumerate(data[report][index]):                        #Iteration for each value
#         if index == 0:                                                      #Fill 'fields' string
#             keyName[idx]    = patternTitle.sub( '', item )
#             val             = "`%s`, " % ( patternTitle.sub( '', item ) )
#             if keyName[idx] != 'events' and keyName[idx] != 'stints':
#                 keys[report]    = "%s %s"   % ( keys[report], val )         #Set key array
#         else:
#             if keyName[idx] != 'events' and keyName[idx] != 'stints':        #ignore event array
#
#                 valor = patternSpace.sub( "", item )
#                 match = re.match(r"(?P<tst>tst?)", keyName[idx])
#                 if match and match.groupdict()['tst'] == 'tst':
#                     valor = datetime.datetime.fromtimestamp(\
#                             int( valor ) ).strftime('%Y-%m-%d %H:%M:%S')
#
#                 val                     = "'%s', "      % valor
#                 vals[report][index]     = "%s %s"       % ( vals[report][index],    val )
#                 update[report][index]   = "%s `%s` = %s"  % ( update[report][index],  keyName[idx],   val )
#
#     keys[report] = patternKey.sub( " )", keys[report] )
#     if index != 0:
#         vals[report][index]     = patternKey.sub( " )", vals[report][index] )
#         update[report][index]   = patternKey.sub( "", update[report][index] )
#         q = "INSERT INTO ccexporter.callsDetails %s VALUES %s ON DUPLICATE KEY UPDATE %s" % ( keys[report], vals[report][index], update[report][index] )
#         # print q
#         cur.execute( q )
#         try:
#             cur.execute( q )
#         except:
#             print "X (%s) " % index,
#
#     i += 1
#     bar.update( i )
#
# bar.finish()
# print "Committing %s... " % report,
# try:
#     db.commit()
#     print "Done!"
# except:
#     print "Error!"
#
#     cur.close()
#
# db.close()
