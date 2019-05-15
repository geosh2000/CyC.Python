import json, requests, threading, MySQLdb, re, sys, progressbar, os, datetime

#PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "ccexporter.usr",                 # your username
        passwd  = "IFaoCJiH09rEqLVZVLsj",           # your password
        db      = "ccexporter")

cur = db.cursor()
delete = "DELETE FROM ccexporter.callsDetails WHERE tstStart < CAST(CONCAT(ADDDATE(CURDATE(),-1),' 20:00:00') as DATE)"
cur.execute( delete )
db.commit()
cur.close()

url = 'http://queuemetrics.pricetravel.com.mx:8080/queuemetricscc/QmStats/jsonStatsApi.do'

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}

blocks = [
    'DetailsDO.CallsOkRaw',
    'DetailsDO.CallsKoRaw'
]

patternTitle    = re.compile(r"(CALLOK_(?=)|CALLKO_(?=))")
patternKey      = re.compile(r", $")
patternSpace    = re.compile(r"&nbsp;")

keys    = {}
vals    = {}
update  = {}
queries = []

# os.system('clear')

for report in blocks:

    now         = datetime.datetime.today()
    tomorrow    = now + datetime.timedelta( days = 1 )

    td = "%s.00:00:00" % now.strftime("%Y-%m-%d")
    tm = "%s.00:00:00" % tomorrow.strftime("%Y-%m-%d")

    q = ''
    for i in range(100, 500):
        q = "%s|%i" % (q, i)

    for i in range(650, 670):
        q = "%s|%i" % (q, i)

    for i in range(900, 999):
        q = "%s|%i" % (q, i)

    for i in range(11800, 11899):
        q = "%s|%i" % (q, i)

    params = {
        'queues'    : q,
        'from'      : td,
        'to'        : tm,
        'block'     : report
    }

    print "%s" % report
    print "  -- Obtaining from QM..."

    keys[report]    = "("
    vals[report]    = {}
    update[report]  = {}
    keyName         = {}

    # try:
    resp = requests.get( url, params = params, headers = headers )
    print "Done!"
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
            vals[report][index]     = "("
            update[report][index]   = ""

        for idx, item in enumerate(data[report][index]):                        #Iteration for each value
            if index == 0:                                                      #Fill 'fields' string
                keyName[idx]    = patternTitle.sub( '', item )
                val             = "`%s`, " % ( patternTitle.sub( '', item ) )
                if keyName[idx] != 'events' and keyName[idx] != 'stints':
                    keys[report]    = "%s %s"   % ( keys[report], val )         #Set key array
            else:
                if keyName[idx] != 'events' and keyName[idx] != 'stints':        #ignore event array

                    valor = patternSpace.sub( "", item )
                    match = re.match(r"(?P<tst>tst?)", keyName[idx])
                    if match and match.groupdict()['tst'] == 'tst':
                        valor = datetime.datetime.fromtimestamp(\
                                int( valor ) ).strftime('%Y-%m-%d %H:%M:%S')

                    val                     = "'%s', "      % valor
                    vals[report][index]     = "%s %s"       % ( vals[report][index],    val )

                    if keyName[idx] != 'queue':
                        update[report][index]   = "%s `%s` = %s"  % ( update[report][index],  keyName[idx],   val )

        keys[report] = patternKey.sub( " )", keys[report] )
        if index != 0:
            vals[report][index]     = patternKey.sub( " )", vals[report][index] )
            update[report][index]   = patternKey.sub( "", update[report][index] )
            q = "INSERT INTO ccexporter.callsDetails %s VALUES %s ON DUPLICATE KEY UPDATE %s" % ( keys[report], vals[report][index], update[report][index] )
            # print q
            cur.execute( q )
            try:
                cur.execute( q )
            except:
                print "X (%s) " % index,

        i += 1
        bar.update( i )

    bar.finish()
    print "  -- Committing... ",
    try:
        db.commit()
        print "Done!"
    except:
        print "Error!"

        cur.close()

db.close()
