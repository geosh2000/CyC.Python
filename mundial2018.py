import json, requests, threading, MySQLdb, re, sys, progressbar, os, datetime

#PTVMN29
db = MySQLdb.connect(
        host    = "cundbwf01.pricetravel.com.mx",   # your host, usually localhost
        user    = "comeycom_wfm",                 # your username
        passwd  = "pricetravel2015",           # your password
        db      = "comeycom_WFM")

cur = db.cursor()

partidos = 'http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/MundialFutbol/partidosRAW/'


# try:
#     resp = requests.get( partidos )
#     ptd = resp.json()
# except:
class matches():
    myInstances = []
    def __init__(self, idMatch ):
        self.idCompetition = '17'
        self.idSeason = '254645'
        self.idStage = '275093'
        self.idMatch = idMatch
        self.__class__.myInstances.append(self)

    def __getitem__(self, item):
        return getattr(self, item)

class jsonResp():
    myInstances = []
    def __init__(self, match1, match2, match3 ):
        self.data = [ match1, match2, match3 ]
        self.__class__.myInstances.append(self)

    def __getitem__(self, item):
        return getattr(self, item)


ptd = jsonResp(matches('300331511'),matches('300331530'),matches('300331496'))

cur = db.cursor()

for match in ptd['data']:
    print "%s Getting data..." % match['idMatch'],
    url = 'https://api.fifa.com/api/v1/live/football/%s/%s/%s/%s?language=en-GB' % (match['idCompetition'], match['idSeason'], match['idStage'], match['idMatch'])
    response = requests.get( url )
    print "Done! || ",
    data = response.json()

    fht = 0 if data['FirstHalfTime'] == None else 1
    fhet = 0 if data['FirstHalfExtraTime'] == None else 1
    sht = 0 if data['SecondHalfTime'] == None else 1
    shet = 0 if data['SecondHalfExtraTime'] == None else 1
    bph = data['BallPossession']['OverallHome'] if data['BallPossession']['OverallHome'] != None else 0
    bpa = data['BallPossession']['OverallAway'] if data['BallPossession']['OverallAway'] != None else 0
    gf = data['HomeTeam']['Score']
    gc = data['AwayTeam']['Score']
    finish = 1 if data['MatchStatus'] == 0 else 0
    live = 1 if data['MatchStatus'] == 3 else 0

    queryA = "UPDATE mundial2018_partidos SET gf=%d, gc=%d, finalizado=%d, live=%d, min=\"%s\", SecondHalfTime=%s, FirstHalfTime=%s, FirstHalfExtraTime=%s, SecondHalfExtraTime=%s, ballPosHome=%r, ballPosAway=%r, matchStatus=%s WHERE idMatch=%s AND local=1" % (gf, gc, finish, live, data['MatchTime'], sht, fht, fhet, shet, bph, bpa, data['MatchStatus'], match['idMatch'])
    queryB = "UPDATE mundial2018_partidos SET gc=%d, gf=%d, finalizado=%d, live=%d, min=\"%s\", SecondHalfTime=%s, FirstHalfTime=%s, FirstHalfExtraTime=%s, SecondHalfExtraTime=%s, ballPosAway=%r, ballPosHome=%r, matchStatus=%s WHERE idMatch=%s AND local!=1" % (gf, gc, finish, live, data['MatchTime'], sht, fht, fhet, shet, bph, bpa, data['MatchStatus'], match['idMatch'])
    # print query
    print "Updating db... ",
    cur.execute( queryA )
    cur.execute( queryB )
    print "Done!"

print "Commiting data... ",
db.commit()
print "Done!"
cur.close()
db.close()


# for report in blocks:
#
#     now         = datetime.datetime.today()
#     tomorrow    = now + datetime.timedelta( days = 1 )
#
#     td = "%s.00:00:00" % now.strftime("%Y-%m-%d")
#     tm = "%s.00:00:00" % tomorrow.strftime("%Y-%m-%d")
#
#     q = ''
#     for i in range(100, 500):
#         q = "%s|%i" % (q, i)
#
#     for i in range(650, 670):
#         q = "%s|%i" % (q, i)
#
#     for i in range(900, 999):
#         q = "%s|%i" % (q, i)
#
#     for i in range(11800, 11899):
#         q = "%s|%i" % (q, i)
#
#     params = {
#         'queues'    : q,
#         'from'      : td,
#         'to'        : tm,
#         'block'     : report
#     }
#
#     print "%s" % report
#     print "  -- Obtaining from QM..."
#
#     keys[report]    = "("
#     vals[report]    = {}
#     update[report]  = {}
#     keyName         = {}
#
#     # try:
#     resp = requests.get( url, params = params, headers = headers )
#     print "Done!"
#     data = resp.json()
#
#     cur = db.cursor()
#
#     num = len(data[report])                                                     #Number of Regs
#
#     bar = progressbar.ProgressBar( maxval = num, \
#         redirect_stdout=True, \
#         widgets=[progressbar.Bar('=', '  -- progress: [', ']'), ' ',\
#             progressbar.Percentage()])#ProgressBar options
#
#     bar.start()
#     i   = 0                                                                     #Init iterator
#
#     for index, value in enumerate(data[report]):                                #Iteration for each report
#
#         if index != 0:                                                          #Declare string for values
#             vals[report][index]     = "("
#             update[report][index]   = ""
#
#         for idx, item in enumerate(data[report][index]):                        #Iteration for each value
#             if index == 0:                                                      #Fill 'fields' string
#                 keyName[idx]    = patternTitle.sub( '', item )
#                 val             = "`%s`, " % ( patternTitle.sub( '', item ) )
#                 if keyName[idx] != 'events' and keyName[idx] != 'stints':
#                     keys[report]    = "%s %s"   % ( keys[report], val )         #Set key array
#             else:
#                 if keyName[idx] != 'events' and keyName[idx] != 'stints':        #ignore event array
#
#                     valor = patternSpace.sub( "", item )
#                     match = re.match(r"(?P<tst>tst?)", keyName[idx])
#                     if match and match.groupdict()['tst'] == 'tst':
#                         valor = datetime.datetime.fromtimestamp(\
#                                 int( valor ) ).strftime('%Y-%m-%d %H:%M:%S')
#
#                     val                     = "'%s', "      % valor
#                     vals[report][index]     = "%s %s"       % ( vals[report][index],    val )
#
#                     if keyName[idx] != 'queue':
#                         update[report][index]   = "%s `%s` = %s"  % ( update[report][index],  keyName[idx],   val )
#
#         keys[report] = patternKey.sub( " )", keys[report] )
#         if index != 0:
#             vals[report][index]     = patternKey.sub( " )", vals[report][index] )
#             update[report][index]   = patternKey.sub( "", update[report][index] )
#             q = "INSERT INTO ccexporter.callsDetails %s VALUES %s ON DUPLICATE KEY UPDATE %s" % ( keys[report], vals[report][index], update[report][index] )
#             # print q
#             cur.execute( q )
#             try:
#                 cur.execute( q )
#             except:
#                 print "X (%s) " % index,
#
#         i += 1
#         bar.update( i )
#
#     bar.finish()
#     print "  -- Committing... ",
#     try:
#         db.commit()
#         print "Done!"
#     except:
#         print "Error!"
#
#         cur.close()
#
# db.close()
