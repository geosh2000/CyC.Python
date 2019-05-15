import json, requests, threading, MySQLdb, re, sys, progressbar, os
from datetime import datetime

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
patternDate     = re.compile(r"^20(([1][7-9])|([2][0-5]))-(([0][1-9])|([1][0-2]))-(([0][1-9])|([1-2][0-9])|([3][0-1]))$")

keys    = {}
vals    = {}
valTest = {}
update  = {}
queries = []

print "UPLOAD DE LLAMADAS DE QM A COMEYCOME"
print ""
print "Por favor ingresa los datos que se solicitan..."
print ""

def txt_match( text ):
    match = patternDate.match( text )
    if match:
        return True
    else:
        return False

def inputAsk( msg ):
    tmpInput = raw_input( msg )
    if not txt_match( tmpInput ):
        print "Error, el formato debe ser YYYY-MM-DD, intenta nuevamente"
        inputAsk( msg )
    return tmpInput

start   = inputAsk("Fecha de Inicio (YYYY-MM-DD): ")
end     = inputAsk("Fecha Final (YYYY-MM-DD): ")

print ""
print ""

# os.system('clear')

for report in blocks:

    td = "%s.00:00:00" % start
    tm = "%s.23:59:59" % end

    q = ''
    for i in range(999):
        q = "%s|%i" % (q, i)

    params = {
        'queues'    : q,
        'from'      : td,
        'to'        : tm,
        'block'     : report
    }

    print "%s" % report
    print "  -- Obtaining from QM...",

    keys[report]    = "("
    vals[report]    = {}
    valTest[report] = {}
    update[report]  = {}
    keyName         = {}

    # try:
    resp = requests.get( url, params = params, headers = headers )
    print "Done!"
    data = resp.json()

    for index, value in enumerate(data[report]):                                #Iteration for each report

        vals[report][index] = {}

        for idx, item in enumerate(data[report][index]):                        #Iteration for each value
            if index == 0:                                                      #Fill 'fields' string
                keyName[idx]    = patternTitle.sub( '', item )
            else:
                if keyName[idx] != 'events' and keyName[idx] != 'stints':        #ignore event array

                    valor = patternSpace.sub( "", item )
                    match = re.match(r"(?P<tst>tst?)", keyName[idx])
                    if match and match.groupdict()['tst'] == 'tst':
                        valor = datetime.fromtimestamp(\
                                # int( valor ) ).strftime('%Y-%m-%d %H:%M:%S')
                                int( valor ) ).strftime('%H:%M:%S')

                    val                                 = "'%s', "      % valor
                    vals[report][index][keyName[idx]]   = val

FMT = '%H:%M:%S'

for rep in vals:
    for index in vals[rep]:
        print index,

        tdelta = datetime.strptime("%s"  % (vals[rep][index]['tstEnd']), FMT)-datetime.strptime("%s"  % (vals[rep][index]['tstStart']), FMT)
        print tdelta

db.close()
