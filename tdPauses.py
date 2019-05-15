import threading, os, datetime, sys

interval = 5
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

    try:
        execfile("agentPauses.py")
    except Exception, e:
        print "Error on AgentPauses! %s" % str(e)

    try:
        execfile("agentPausesCO.py")
    except Exception, e:
        print "Error on AgentPauses! %s" % str(e)

    now = datetime.datetime.today()
    print "End: %s" % now.strftime("%Y-%m-%d %H:%M:%S")
    startTimer()          #start timer for next getData

getData()
