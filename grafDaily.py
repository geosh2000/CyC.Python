import json, requests
import threading

# url = "http://testoperaciones.pricetravel.com.mx/api/restfulbck/index.php/Procesos/grafAsesoresDaily/"
url = "https://operaciones.pricetravel.com.mx/api/restful/index.php/Procesos/grafAsesoresDaily/"

print "Updating Agent Graphs...",

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}

params = {}

try:
    resp = requests.get( url, params = params, headers = headers )
    data = resp.json()

    print data['msg']
except:
    print "Error!"
