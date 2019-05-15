import json, requests, threading, MySQLdb, re, sys, progressbar, os, datetime

# PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "comeycom_wfm",                 # your username
        passwd  = "pricetravel2015",           # your password
        db      = "comeycom_WFM")

sk = {}

#CONSTRUCT QUEUES BY SKILL
# def getQueues():
#     global db, sk
#     skills = "SELECT monShow, queue FROM Cola_Skill WHERE active=1"
#     cur = db.cursor()
#     cur.execute(skills)
#
#     skRes = cur.fetchall()
#
#     for row in skRes:
#         key = "%s" % row[0]
#         try:
#             sk[key]
#             sk[key] = "%s|%s" % ( sk[key], row[1] )
#         except:
#             sk[key] = "%s" % row[1]
#
#     cur.close()
#
# getQueues()

#ValueKeys for AgentSessions

keyVal = ["Agent", "Code", "Start hour", "End hour", "Duration"]
keySQL = {
    "Agent":        "asesor",
    "Code":         "tipo",
    "Start hour":   "Inicio",
    "End hour":     "Fin",
    "Duration":     "Duracion"
}

url = 'http://queuemetrics-co.pricetravel.com.mx:8080/qm/QmStats/jsonStatsApi.do'
# urlPauses = 'http://testoperaciones.pricetravel.com.mx/api/restful/index.php/Procesos/pauseCheck'
urlPauses = 'https://operaciones.pricetravel.com.mx/api/restful/index.php/Procesos/pauseCheck'

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}

blocks = [
    'DetailsDO.AgentPauses',
    # 'DetailsDO.CallsKoRaw'
]

patternTitle    = re.compile(r"(CALLOK_(?=)|CALLKO_(?=))")
patternAgent    = re.compile(r"[ ]?\([0-9]*\)[ ]?")
patternKey      = re.compile(r", $")
patternSpace    = re.compile(r"&nbsp;")
patternDate     = re.compile(r".* - (?=[0-9:]*$)")
patternTime     = re.compile(r" - [0-9:]*$")

keys    = {}
vals    = {}
update  = {}
queries = []

# os.system('clear')
numQ = len(sk)                                                     #Number of Regs

# barQ = progressbar.ProgressBar( maxval = numQ, \
#     redirect_stdout=True, \
#     widgets=[progressbar.Bar('=', 'Building by Skill: [', ']'), ' ',\
#         progressbar.Percentage()])#ProgressBar options
#
# barQ.start()
# barIQ = 0

# for q in sk:
for report in blocks:

    now         = datetime.datetime.today()
    tomorrow    = now + datetime.timedelta( days = 1 )

    td = "%s.00:00:00" % now.strftime("%Y-%m-%d")
    tm = "%s.00:00:00" % tomorrow.strftime("%Y-%m-%d")

    params = {
        'queues'    : '*',
        'from'      : td,
        'to'        : tm,
        'block'     : report
    }

    print "%s" % ( report )
    print "  -- Obtaining pauses...",

    keys[report]    = "("
    vals[report]    = {}
    update[report]  = {}
    keyName         = {}
    keyNameSQL      = {}

    # try:
    resp = requests.get( url, params = params, headers = headers )
    print "Done!"
    data = resp.json()

    cur = db.cursor()

    num = len(data[report])                                                     #Number of Regs

    bar = progressbar.ProgressBar( maxval = num, \
        redirect_stdout=True, \
        widgets=[progressbar.Bar('=', '  -- progress: [', ']') , ' ',\
            progressbar.Percentage()])#ProgressBar options

    bar.start()
    i   = 0                                                                     #Init iterator

    for index, value in enumerate(data[report]):                                #Iteration for each report

        if index != 0:                                                          #Declare string for values
            vals[report][index]     = "("
            update[report][index]   = ""

        for idx, item in enumerate(data[report][index]):                        #Iteration for each value
            if index == 0:
                keyName[idx]    = patternTitle.sub( '', item )
                if keyName[idx] in keyVal:
                    val = "`%s`, " % ( keySQL[patternTitle.sub( '', item )] )
                    keys[report]    = "%s %s"   % ( keys[report], val )         #Set key array
                    keyNameSQL[idx] = patternKey.sub( "", val )
            else:
                if keyName[idx] in keyVal:                                      #Use only mysql cols

                    valor = patternSpace.sub( "", item ).strip()
                    match = re.match(r"(?P<tst>tst?)", keyName[idx])

                    if match and match.groupdict()['tst'] == 'tst':
                        valor = datetime.datetime.fromtimestamp(\
                                int( valor ) ).strftime('%Y-%m-%d %H:%M:%S')

                    if keyName[idx] == 'Agent':
                        valor = "GETIDASESOR('%s', 2)" % patternAgent.sub( '', valor )
                        valor = "IF(%s IS NULL,0,%s)" % ( valor, valor )

                    if keyName[idx] == 'Duration' and len(valor) <= 5:
                        valor = "00:%s" % valor

                    if keyName[idx] == 'Start hour' or keyName[idx] == 'End hour':
                        valor = "TZCONVERT('%s/%s %s')" % ( tomorrow.strftime('%Y'), patternTime.sub( '', valor ), patternDate.sub( '', valor ) )

                    if keyName[idx] == 'Agent' or keyName[idx] == 'Start hour' or keyName[idx] == 'End hour':
                        vals[report][index]     = "%s %s, "       % ( vals[report][index],    valor )
                        update[report][index]   = "%s %s = %s, "  % ( update[report][index],  keyNameSQL[idx],   valor )
                    else:
                        vals[report][index]     = "%s '%s', "       % ( vals[report][index],    valor )
                        update[report][index]   = "%s %s = '%s', "  % ( update[report][index],  keyNameSQL[idx],   valor )


        keys[report] = patternKey.sub( ", `Skill`)", keys[report] )
        if index != 0:
            vals[report][index]     = patternKey.sub( ", %s)" % '0', vals[report][index] )
            update[report][index]   = patternKey.sub( "", update[report][index] )
            qInsert = "INSERT INTO asesores_pausas %s VALUES %s ON DUPLICATE KEY UPDATE %s" % ( keys[report], vals[report][index], update[report][index] )
            # print qInsert
            # cur.execute( qInsert )
            try:
                cur.execute( qInsert )
            except Exception, e:
                print "X (%s) -> %s " % ( index, str(e) )

        i += 1
        bar.update( i )

    bar.finish()
    print "  -- Committing... ",
    try:
        db.commit()
        print "Done!"
    except:
        print "Error!"

#     barIQ += 1
#     barQ.update( barIQ )
# barQ.finish()
print "Recalculating Pauses... ",
resp = requests.get( urlPauses, params = '', headers = headers )
print "Done!"

cur.close()
db.close()
