import threading, os, datetime, sys
import json, requests

anio = input("Ingresa el anio: ")
mes = input("Ingresa el mes: ")
last = input("Ingresa el ultimo dia del mes: ")

interval = 60
i = interval

def venta(anio, mes, last):
    url = "https://operaciones.pricetravel.com.mx/api/restful/index.php/Procesos/grafGen"

    now         = datetime.datetime.today()

    i1 = "%s-%s-01" % (anio, mes)
    f1 = "%s-%s-15" % (anio, mes)
    i2 = "%s-%s-16" % (anio, mes)
    f2 = "%s-%s-%s" % (anio, mes, last)

    print "Updating Agent Sales 1...",

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    params = {}

    urlOK = "%s/%s/%s" % (url, i1, f1)

    try:
        resp = requests.get( urlOK, params = params, headers = headers )
        data = resp.json()

        print data['msg']
    except:
        print "Error!"

    print "Updating Agent Sales 2...",

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    params = {}
    urlOK = "%s/%s/%s" % (url, i2, f2)

    try:
        resp = requests.get( urlOK, params = params, headers = headers )
        data = resp.json()

        print data['msg']
    except:
        print "Error!"

def calls(anio, mes, last):
    url = "https://operaciones.pricetravel.com.mx/api/restful/index.php/Procesos/genGrafCalls"

    now         = datetime.datetime.today()

    i1 = "%s-%s-01" % (anio, mes)
    f1 = "%s-%s-15" % (anio, mes)
    i2 = "%s-%s-16" % (anio, mes)
    f2 = "%s-%s-%s" % (anio, mes, last)

    print "Updating Agent Calls 1...",

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    params = {}

    urlOK = "%s/%s/%s" % (url, i1, f1)

    try:
        resp = requests.get( urlOK, params = params, headers = headers )
        data = resp.json()

        print data['msg']
    except:
        print "Error!"

    print "Updating Agent Calls 2...",

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    params = {}
    urlOK = "%s/%s/%s" % (url, i2, f2)

    try:
        resp = requests.get( urlOK, params = params, headers = headers )
        data = resp.json()

        print data['msg']
    except:
        print "Error!"

def sups(anio, mes, last):
    url = "https://operaciones.pricetravel.com.mx/api/restful/index.php/Procesos/checkSupGraf"

    now         = datetime.datetime.today()

    i1 = "%s" % now.strftime("%Y-%m-01")
    f1 = "%s" % now.strftime("%Y-%m-15")
    i2 = "%s" % now.strftime("%Y-%m-16")
    f2 = "%s" % now.strftime("%Y-%m-%d")

    print "Updating Agent Sales Supervisors 1...",

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    params = {}

    urlOK = "%s/%s/%s" % (url, i1, f1)

    try:
        resp = requests.get( urlOK, params = params, headers = headers )
        data = resp.json()

        print data['msg']
    except:
        print "Error!"

    print "Updating Agent Sales Supervisors 2...",

    headers = {
        'content-type'    : 'application/json',
        'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
    }

    params = {}
    urlOK = "%s/%s/%s" % (url, i2, f2)

    try:
        resp = requests.get( urlOK, params = params, headers = headers )
        data = resp.json()

        print data['msg']
    except:
        print "Error!"

def getData():
    # os.system('cls')
    now = datetime.datetime.today()
    print ""
    print "Start: %s" % now.strftime("%Y-%m-%d %H:%M:%S")

    venta(anio, mes, last)
    calls(anio, mes, last)
    sups(anio, mes, last)

    now = datetime.datetime.today()
    print "End: %s" % now.strftime("%Y-%m-%d %H:%M:%S")

getData()
