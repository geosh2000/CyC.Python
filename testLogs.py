import json, requests, threading, MySQLdb, re, sys, progressbar, os, datetime

# PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "comeycom_wfm",                 # your username
        passwd  = "pricetravel2015",           # your password
        db      = "comeycom_WFM")

sk = {}

#CONSTRUCT QUEUES BY SKILL
def getQueues():
    global db, sk
    skills = "SELECT Skill_sec, queue FROM Cola_Skill WHERE active=1"
    cur = db.cursor()
    cur.execute(skills)

    skRes = cur.fetchall()

    for row in skRes:
        key = "%s" % row[0]
        try:
            sk[key]
            sk[key] = "%s|%s" % ( sk[key], row[1] )
        except:
            sk[key] = "%s" % row[1]

    cur.close()

getQueues()

#ValueKeys for AgentSessions

keyVal = ["Agent", "Start hour", "End hour", "Duration"]
keySQL = {
    "Agent":        "asesor",
    "Start hour":   "",
    "End hour":     "_out",
    "Duration":     "Duracion"
}

url = 'http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/QmStats/jsonStatsApi.do'

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}

blocks = [
    'DetailsDO.AgentSessions',
    # 'DetailsDO.CallsKoRaw'
]

patternTitle    = re.compile(r"(CALLOK_(?=)|CALLKO_(?=))")
patternAgent    = re.compile(r"[ ]?\([0-9]*\)[ ]?")
patternKey      = re.compile(r", $")
patternSpace    = re.compile(r"&nbsp;")
patternDate     = re.compile(r".* - (?=[0-9:]*$)")
patternTime     = re.compile(r" - [0-9:]*$")

keys        = {}
keysNew     = {}
vals        = {}
valsNew     = {}
update      = {}
updateNew   = {}
queries     = []
proc = {}

# os.system('clear')
numQ = len(sk)                                                     #Number of Regs

barQ = progressbar.ProgressBar( maxval = numQ, \
    redirect_stdout=True, \
    widgets=[progressbar.Bar('=', 'Building by Skill: [', ']'), ' ',\
        progressbar.Percentage()])#ProgressBar options

barQ.start()
barIQ = 0

for q in sk:
    for report in blocks:

        now         = datetime.datetime.today()
        now         = now - datetime.timedelta( days = 1 )
        tomorrow    = now + datetime.timedelta( days = 2 )

        td = "%s.00:00:00" % now.strftime("%Y-%m-%d")
        tm = "%s.00:00:00" % tomorrow.strftime("%Y-%m-%d")

        params = {
            'queues'    : sk[q],
            'from'      : td,
            'to'        : tm,
            'block'     : report
        }

        print "%s" % ( report ),
        print "  -- Obtaining for skill %s..." % ( q ),

        keys[report]        = "("
        keysNew[report]     = "("
        vals[report]        = {}
        valsNew[report]     = {}
        update[report]      = {}
        updateNew[report]   = {}
        keyName             = {}
        keyNameSQL          = {}

        # try:
        resp = requests.get( url, params = params, headers = headers )
        print "Done!"
        # print params
        data = resp.json()

        cur = db.cursor()

        num = len(data[report])                                                     #Number of Regs

        bar = progressbar.ProgressBar( maxval = num, \
            redirect_stdout=True, \
            widgets=[progressbar.Bar('=', '  -- progress: [', ']'), ' ',\
                progressbar.Percentage()])#ProgressBar options

        bar.start()
        i   = 0                                                                     #Init iterator

        for index, value in enumerate(data[report]):                                #Iteration for each report

            if index != 0:                                                          #Declare string for values
                vals[report][index]         = "("
                valsNew[report][index]      = "("
                update[report][index]       = ""
                updateNew[report][index]    = ""

            for idx, item in enumerate(data[report][index]):                        #Iteration for each value
                if index == 0:                                                      #Fill 'fields' string
                    keyName[idx]    = patternTitle.sub( '', item )
                    if keyName[idx] in keyVal:
                        if keyName[idx] == 'Start hour' or keyName[idx] == 'End hour':
                            val = "`Fecha%s`, `Hora%s`, " % ( keySQL[patternTitle.sub( '', item )], keySQL[patternTitle.sub( '', item )] )
                            # Construct new table
                            if keySQL[keyName[idx]] == '':
                                k = 'login'
                            else:
                                k = 'logout'

                            

                            keysNew[report] = "%s `%s`, "   % ( keysNew[report], k )         #Set key array
                        else:
                            val = "`%s`, " % ( keySQL[patternTitle.sub( '', item )] )
                            keysNew[report] = "%s %s"   % ( keysNew[report], val )         #Set key array

                        keys[report]    = "%s %s"   % ( keys[report], val )         #Set key array
                        keyNameSQL[idx] = patternKey.sub( "", val )                 #keyName for Updates

                else:
                    if keyName[idx] in keyVal:                                      #Use only mysql cols

                        valor = patternSpace.sub( "", item ).strip()
                        match = re.match(r"(?P<tst>tst?)", keyName[idx])

                        if match and match.groupdict()['tst'] == 'tst':
                            valor = datetime.datetime.fromtimestamp(\
                                    int( valor ) ).strftime('%Y-%m-%d %H:%M:%S')

                        if keyName[idx] == 'Agent':
                            vName = patternAgent.sub( '', valor )
                            proc['asesor'] = "'%s'" % vName
                            valor = "GETIDASESOR('%s', 2)" % vName
                            valor = "IF(%s IS NULL,0,%s)" % ( valor, valor )

                        if keyName[idx] == 'Duration' and len(valor) <= 5:
                            valor = "00:%s" % valor

                        if keyName[idx] == 'Start hour' or keyName[idx] == 'End hour':
                            vDate = "%s/%s" % ( now.strftime('%Y'), patternTime.sub( '', valor ) )
                            vTime = "%s" % ( patternDate.sub( '', valor ) )
                            valorNew = "TZCONVERT('%s/%s %s')" % ( now.strftime('%Y'), patternTime.sub( '', valor ), patternDate.sub( '', valor ) )
                            valor = "%s/%s', '%s" % ( now.strftime('%Y'), patternTime.sub( '', valor ), patternDate.sub( '', valor ) )

                            update[report][index]   = "%s `Fecha%s` = '%s', `Hora%s` = '%s', "  % ( update[report][index],  keySQL[keyName[idx]], vDate ,keySQL[keyName[idx]], vTime )
                            vals[report][index]     = "%s '%s', "       % ( vals[report][index],    valor )

                            # Construct new table
                            if keySQL[keyName[idx]] == '':
                                k = 'login'
                            else:
                                k = 'logout'
                            
                            updateNew[report][index]        = "%s `%s` = %s, "    % ( updateNew[report][index],  k, valorNew )
                            valsNew[report][index]          = "%s %s, "           % ( valsNew[report][index],    valorNew )
                            proc[k] = valorNew
                        else:
                            if keyName[idx] == 'Agent':
                                vals[report][index]         = "%s %s, "         % ( vals[report][index],    valor )
                                valsNew[report][index]      = "%s %s, "         % ( valsNew[report][index],    valor )
                                update[report][index]       = "%s %s = %s, "    % ( update[report][index],  keyNameSQL[idx],   valor )
                                updateNew[report][index]    = "%s %s = %s, "    % ( updateNew[report][index],  keyNameSQL[idx],   valor )
                                # proc['asesor'] = valor
                            else:
                                vals[report][index]         = "%s '%s', "       % ( vals[report][index],    valor )
                                valsNew[report][index]      = "%s '%s', "       % ( valsNew[report][index],    valor )
                                update[report][index]       = "%s %s = '%s', "  % ( update[report][index],  keyNameSQL[idx],   valor )
                                updateNew[report][index]    = "%s %s = '%s', "  % ( updateNew[report][index],  keyNameSQL[idx],   valor )


            keys[report] = patternKey.sub( ", `Skill`)", keys[report] )
            keysNew[report] = patternKey.sub( ", `Skill`)", keysNew[report] )
            if index != 0:
                vals[report][index]         = patternKey.sub( ", %s)" % q, vals[report][index] )
                valsNew[report][index]      = patternKey.sub( ", %s)" % (q), valsNew[report][index] )
                update[report][index]       = patternKey.sub( "", update[report][index] )
                updateNew[report][index]    = patternKey.sub( "", updateNew[report][index] )
                # qInsert     = "INSERT INTO Sesiones %s VALUES %s ON DUPLICATE KEY UPDATE %s" % ( keys[report], vals[report][index], update[report][index] )
                # qInsertNEW  = "INSERT INTO asesores_logs %s VALUES %s ON DUPLICATE KEY UPDATE %s" % ( keysNew[report], valsNew[report][index], updateNew[report][index] )
                qCallProc   = "CALL addLog(%s,%s,%s,%s)" % ( proc['asesor'], proc['login'], proc['logout'], q )
                # cur.execute( qInsert )
                # try:
                #     cur.execute( qInsert )
                # except Exception, e:
                #     print "X (%s) -> %s " % ( index, str(e) )
                # try:
                #     cur.execute( qInsertNEW )
                # except Exception, e:
                #     print "X (%s) -> %s " % ( index, str(e) )
                    # print qInsertNEW
                try:
                    cur.execute( qCallProc )
                except Exception, e:
                    print "X (%s) -> %s " % ( index, str(e) )
                    print qCallProc

            i += 1
            bar.update( i )

        bar.finish()
        print "  -- Committing... ",
        try:
            db.commit()
            print "Done!"
        except:
            print "Error!"

    barIQ += 1
    barQ.update( barIQ )
barQ.finish()

cur.close()
db.close()
