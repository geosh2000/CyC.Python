import json, requests, datetime
import threading

# url = "http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/Procesos/checkSupGraf"
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

if int(now.strftime("%d")) >= 16:

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
