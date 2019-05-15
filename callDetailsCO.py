import json, requests, threading, MySQLdb, re, sys, progressbar, os, datetime


def runReport( qs, re, sql, progressbar ):
    #PTVMN29
    db = sql.connect(
            host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
            user    = "ccexporter.usr",                 # your username
            passwd  = "IFaoCJiH09rEqLVZVLsj",           # your password
            db      = "ccexporter")
    
            
    url = 'http://queuemetrics-co.pricetravel.com.mx:8080/qm/QmStats/jsonStatsApi.do'

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    patternTitle    = re.compile(r"(CALLOK_(?=)|CALLKO_(?=))")
    patternKey      = re.compile(r", $")
    patternSpace    = re.compile(r"&nbsp;")

    blocks = [
        'DetailsDO.CallsOkRaw',
        'DetailsDO.CallsKoRaw'
    ]

    keys    = {}
    vals    = {}
    update  = {}
    queries = []

    for report in blocks:

        now         = datetime.datetime.today()
        tomorrow    = now + datetime.timedelta( days = 1 )
        # now         = now - datetime.timedelta( days = 30 )
        # tomorrow    = now + datetime.timedelta( days = 100 )

        td = "%s.00:00:00" % now.strftime("%Y-%m-%d")
        tm = "%s.00:00:00" % tomorrow.strftime("%Y-%m-%d")
        # td = "2018-09-23.00:00:00"
        # tm = "2018-09-28.00:00:00"

        params = {
            'queues'    : qs,
            'from'      : td,
            'to'        : tm,
            'block'     : report
        }

        print "%s" % report
        print "  -- Obtaining from QM CO (%s)..." % qs

        keys[report]    = "("
        vals[report]    = {}
        update[report]  = {}
        keyName         = {}

        # try:
        resp = requests.get( url, params = params, headers = headers )
        print "Done!"
        data = resp.json()
        if len(data[report]) > 1:

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
                    vals[report][index]     = "("
                    update[report][index]   = ""

                for idx, item in enumerate(data[report][index]):                        #Iteration for each value
                    if index == 0:                                                      #Fill 'fields' string
                        keyName[idx]    = patternTitle.sub( '', item )
                        val             = "`%s`, " % ( patternTitle.sub( '', item ) )
                        if keyName[idx] != 'events' and keyName[idx] != 'stints' and keyName[idx] != 'variables' and keyName[idx] != 'features':
                            keys[report]    = "%s %s"   % ( keys[report], val )         #Set key array
                    else:
                        if keyName[idx] != 'events' and keyName[idx] != 'stints' and keyName[idx] != 'variables' and keyName[idx] != 'features':        #ignore event array

                            valor = patternSpace.sub( "", item )
                            match = re.match(r"(?P<tst>tst?)", keyName[idx])
                            if match and match.groupdict()['tst'] == 'tst':
                                valor = datetime.datetime.fromtimestamp(\
                                        int( valor ) ).strftime('%Y-%m-%d %H:%M:%S')

                            if keyName[idx] == 'callid':
                                valor = "co_%s" % valor

                            val                     = "'%s', "      % valor
                            vals[report][index]     = "%s %s"       % ( vals[report][index],    val )

                            if keyName[idx] != 'queue':
                                update[report][index]   = "%s `%s` = %s"  % ( update[report][index],  keyName[idx],   val )

                keys[report] = patternKey.sub( " )", keys[report] )
                if index != 0:
                    vals[report][index]     = patternKey.sub( " )", vals[report][index] )
                    update[report][index]   = patternKey.sub( "", update[report][index] )
                    qr = "INSERT INTO ccexporter.callsDetails %s VALUES %s ON DUPLICATE KEY UPDATE %s" % ( keys[report], vals[report][index], update[report][index] )
                    # print qr
                    # cur.execute( qr )
                    try:
                        cur.execute( qr )
                    except:
                        print "X (%s) " % index,

                i += 1
                bar.update( i )

            print "  -- Committing... ",
            try:
                db.commit()
                print "Done!"
            except:
                print "Error!"
            
            cur.close()
            bar.finish()
    db.close()
        
arrQ = []
maxQ = 10
q = ''
x = 0
for i in range(30000, 30050):
    if x < maxQ:
        q = "%s|%i" % (q, i)
        x += 1
    else:
        arrQ.append(q)
        q = "%s" % i
        x = 0
    # runReport( i )

for i in range(36800, 36950):
    if x < maxQ:
        q = "%s|%i" % (q, i)
        x += 1
    else:
        arrQ.append(q)
        q = "%s" % i
        x = 0

for item in arrQ:
    runReport( item, re, MySQLdb, progressbar )






