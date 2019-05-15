import threading, os, datetime, sys, json, requests

interval = 30
i = interval

def startTimer():
    global i
    sys.stdout.write( '.' )  # same as print
    sys.stdout.flush()
    i = i - 1
    if i == 0:
        i = interval
        getData()
    else:
        threading.Timer(1, startTimer).start()

def getData():
    # os.system('cls')
    now = datetime.datetime.today()
    print ""
    print "Start: %s" % now.strftime("%Y-%m-%d %H:%M:%S")

    headers = {
        'content-type'    : 'application/json',
    }

    params = {}

    print "Revision de contratos... ",
    try:
        resp = requests.get( 'http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/Mailing/contratosVencidos', params = params, headers = headers )
        data = resp.json()

        print "Done!"
    except:
        print "Error en correo de contratos vencidos!"

    print "Revision de faltas consecutivas... ",
    try:
        resp = requests.get( 'http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/Mailing/faltasConsecutivas', params = params, headers = headers )
        data = resp.json()

        print "Done!"
    except:
        print "Error en correo de faltas consecutivas!"

    print "Revision de cumpleaneros Hoy... ",
    try:
        resp = requests.get( 'http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/Mailing/cumpleHoy', params = params, headers = headers )
        data = resp.json()

        print "Done!"
    except:
        print "Error en correo de cumpleanos HOY!"

    print "Revision de cumpleaneros Personalizado... ",
    try:
        resp = requests.get( 'http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/Mailing/cumplePersonalizado', params = params, headers = headers )
        data = resp.json()

        print "Done!"
    except:
        print "Error en correo de cumpleanos Personalizado!"

    print "Revision de cumpleaneros Mes... ",
    try:
        resp = requests.get( 'http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/Mailing/cumpleMes', params = params, headers = headers )
        data = resp.json()

        print "Done!"
    except:
        print "Error en correo de cumpleanos Mes!"

    try:
        execfile("agentUpdateSchedules.py")
    except Exception, e:
        print "Error on AgentSchedules! %s" % str(e)

    try:
        execfile("hxDone.py")
    except Exception, e:
        print "Error on hxDone! %s" % str(e)

    try:
        execfile("dtDone.py")
    except Exception, e:
        print "Error on dtDone! %s" % str(e)

    try:
        execfile("agentDetails.py")
    except:
        print "Error on AgentDetails!"

    try:
        execfile("agentDetailsCO.py")
    except:
        print "Error on AgentDetails!"

    try:
        execfile("callDetails.py")
    except Exception, e:
        print "Error on CallsDetails! %s" % str(e)

    try:
        execfile("callDetailsCO.py")
    except Exception, e:
        print "Error on CallsDetailsCO! %s" % str(e)

    try:
        execfile("agentSessions.py")
    except Exception, e:
        print "Error on AgentSessions! %s" % str(e)

    try:
        execfile("agentSessionsCO.py")
    except Exception, e:
        print "Error on AgentSessions! %s" % str(e)

    now = datetime.datetime.today()
    print "End: %s" % now.strftime("%Y-%m-%d %H:%M:%S")
    startTimer()          #start timer for next getData

getData()
