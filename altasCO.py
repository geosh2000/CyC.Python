import json, requests
import threading
import MySQLdb

from requests.auth import HTTPBasicAuth


url = 'http://queuemetrics-co.pricetravel.com.mx:8080/qm/agent/-/jsonEditorApi.do'

headers = {
    'content-type'    : 'application/json',
    'Authorization'   : 'Basic cm9ib3Q6cm9ib3Q='
}

auth = HTTPBasicAuth('robot', 'robot')

print "Preparing %s..." % 'Agents',

blocks = [
  {"aliases" : "Ingrid Sanchez (35252)","default_server" : "0",  "descr_agente" : "Ingrid Sanchez (35252)","nome_agente" : "agent/35252"},
  {"aliases" : "Maria Henao (35253)","default_server" : "0",  "descr_agente" : "Maria Henao (35253)","nome_agente" : "agent/35253"},
  {"aliases" : "Marisol Granada (35254)","default_server" : "0",  "descr_agente" : "Marisol Granada (35254)","nome_agente" : "agent/35254"},
  {"aliases" : "Paula Rivera (35255)","default_server" : "0",  "descr_agente" : "Paula Rivera (35255)","nome_agente" : "agent/35255"},
  {"aliases" : "Liliam Ramirez (35256)","default_server" : "0",  "descr_agente" : "Liliam Ramirez (35256)","nome_agente" : "agent/35256"},
  {"aliases" : "Sorany Hoyos (35257)","default_server" : "0",  "descr_agente" : "Sorany Hoyos (35257)","nome_agente" : "agent/35257"},
  {"aliases" : "Astrid Lopez (35258)","default_server" : "0",  "descr_agente" : "Astrid Lopez (35258)","nome_agente" : "agent/35258"},
  {"aliases" : "Karina Oliveros (35259)","default_server" : "0",  "descr_agente" : "Karina Oliveros (35259)","nome_agente" : "agent/35259"},
  {"aliases" : "Paula Gil (35260)","default_server" : "0",  "descr_agente" : "Paula Gil (35260)","nome_agente" : "agent/35260"},
  {"aliases" : "Karolina Paz (35261)","default_server" : "0",  "descr_agente" : "Karolina Paz (35261)","nome_agente" : "agent/35261"},
  {"aliases" : "Alan Gongora (35262)","default_server" : "0",  "descr_agente" : "Alan Gongora (35262)","nome_agente" : "agent/35262"},
  {"aliases" : "Cesar Herrera (35263)","default_server" : "0",  "descr_agente" : "Cesar Herrera (35263)","nome_agente" : "agent/35263"},
  {"aliases" : "Karen Salazar (35264)","default_server" : "0",  "descr_agente" : "Karen Salazar (35264)","nome_agente" : "agent/35264"},
  {"aliases" : "Bryan Bohorquez (35265)","default_server" : "0",  "descr_agente" : "Bryan Bohorquez (35265)","nome_agente" : "agent/35265"},
  {"aliases" : "Maryury Lopez (35266)","default_server" : "0",  "descr_agente" : "Maryury Lopez (35266)","nome_agente" : "agent/35266"},
  {"aliases" : "Luz Alvarez (35267)","default_server" : "0",  "descr_agente" : "Luz Alvarez (35267)","nome_agente" : "agent/35267"},
  {"aliases" : "Ruben Marin (35268)","default_server" : "0",  "descr_agente" : "Ruben Marin (35268)","nome_agente" : "agent/35268"},
  {"aliases" : "Monica Grueso (35269)","default_server" : "0",  "descr_agente" : "Monica Grueso (35269)","nome_agente" : "agent/35269"},
  {"aliases" : "Santiago Narvaez (35270)","default_server" : "0",  "descr_agente" : "Santiago Narvaez (35270)","nome_agente" : "agent/35270"},
  {"aliases" : "Paula Gonzalez (35271)","default_server" : "0",  "descr_agente" : "Paula Gonzalez (35271)","nome_agente" : "agent/35271"},
  {"aliases" : "Natalia Ramirez (35272)","default_server" : "0",  "descr_agente" : "Natalia Ramirez (35272)","nome_agente" : "agent/35272"},
  {"aliases" : "Lorena Matallana (35273)","default_server" : "0",  "descr_agente" : "Lorena Matallana (35273)","nome_agente" : "agent/35273"},
  {"aliases" : "Viviana Rosero (35274)","default_server" : "0",  "descr_agente" : "Viviana Rosero (35274)","nome_agente" : "agent/35274"},
  {"aliases" : "Cristian Mena (35275)","default_server" : "0",  "descr_agente" : "Cristian Mena (35275)","nome_agente" : "agent/35275"},
  {"aliases" : "Miyi Calderon (35276)","default_server" : "0",  "descr_agente" : "Miyi Calderon (35276)","nome_agente" : "agent/35276"},
  {"aliases" : "Stefany Rojas (35277)","default_server" : "0",  "descr_agente" : "Stefany Rojas (35277)","nome_agente" : "agent/35277"},
  {"aliases" : "Luisa Sanchez (35278)","default_server" : "0",  "descr_agente" : "Luisa Sanchez (35278)","nome_agente" : "agent/35278"},
  {"aliases" : "Yendy Garzon (35279)","default_server" : "0",  "descr_agente" : "Yendy Garzon (35279)","nome_agente" : "agent/35279"},
  {"aliases" : "Yajaidy Moreno (35280)","default_server" : "0",  "descr_agente" : "Yajaidy Moreno (35280)","nome_agente" : "agent/35280"},
  {"aliases" : "Darlyn Lucumi (35281)","default_server" : "0",  "descr_agente" : "Darlyn Lucumi (35281)","nome_agente" : "agent/35281"},
  {"aliases" : "Sergio Lopez (35282)","default_server" : "0",  "descr_agente" : "Sergio Lopez (35282)","nome_agente" : "agent/35282"},
  {"aliases" : "Alejandra Argotti (35283)","default_server" : "0",  "descr_agente" : "Alejandra Argotti (35283)","nome_agente" : "agent/35283"},
  {"aliases" : "Vanesa Payan (35284)","default_server" : "0",  "descr_agente" : "Vanesa Payan (35284)","nome_agente" : "agent/35284"},
  {"aliases" : "Kelly Blandon (35285)","default_server" : "0",  "descr_agente" : "Kelly Blandon (35285)","nome_agente" : "agent/35285"},
  {"aliases" : "Yamileth Valencia (35286)","default_server" : "0",  "descr_agente" : "Yamileth Valencia (35286)","nome_agente" : "agent/35286"},
  {"aliases" : "Ronald Pena (35287)","default_server" : "0",  "descr_agente" : "Ronald Pena (35287)","nome_agente" : "agent/35287"},
  {"aliases" : "Andrea Zambrano (35288)","default_server" : "0",  "descr_agente" : "Andrea Zambrano (35288)","nome_agente" : "agent/35288"},
  {"aliases" : "Cesar Perez (35289)","default_server" : "0",  "descr_agente" : "Cesar Perez (35289)","nome_agente" : "agent/35289"},
  {"aliases" : "Jeysson Falla (35290)","default_server" : "0",  "descr_agente" : "Jeysson Falla (35290)","nome_agente" : "agent/35290"},
  {"aliases" : "Geraldine Cespedes (35291)","default_server" : "0",  "descr_agente" : "Geraldine Cespedes (35291)","nome_agente" : "agent/35291"},
  {"aliases" : "Paola Quintana (35292)","default_server" : "0",  "descr_agente" : "Paola Quintana (35292)","nome_agente" : "agent/35292"},
  {"aliases" : "Jose Coronel (35293)","default_server" : "0",  "descr_agente" : "Jose Coronel (35293)","nome_agente" : "agent/35293"},
  {"aliases" : "Freddy Agredo (35294)","default_server" : "0",  "descr_agente" : "Freddy Agredo (35294)","nome_agente" : "agent/35294"},
  {"aliases" : "Sandra Garcia (35295)","default_server" : "0",  "descr_agente" : "Sandra Garcia (35295)","nome_agente" : "agent/35295"},
  {"aliases" : "Daniela Yusti (35296)","default_server" : "0",  "descr_agente" : "Daniela Yusti (35296)","nome_agente" : "agent/35296"},
  {"aliases" : "Jhorman Perez (35297)","default_server" : "0",  "descr_agente" : "Jhorman Perez (35297)","nome_agente" : "agent/35297"},
  {"aliases" : "Judy Suarez (35298)","default_server" : "0",  "descr_agente" : "Judy Suarez (35298)","nome_agente" : "agent/35298"},
  {"aliases" : "Carlos Garcia (35299)","default_server" : "0",  "descr_agente" : "Carlos Garcia (35299)","nome_agente" : "agent/35299"},
  {"aliases" : "Juan Rodriguez (35300)","default_server" : "0",  "descr_agente" : "Juan Rodriguez (35300)","nome_agente" : "agent/35300"},
  {"aliases" : "Estefania Izquierdo (35301)","default_server" : "0",  "descr_agente" : "Estefania Izquierdo (35301)","nome_agente" : "agent/35301"},
  {"aliases" : "Victor Vasquez (35302)","default_server" : "0",  "descr_agente" : "Victor Vasquez (35302)","nome_agente" : "agent/35302"},
  {"aliases" : "Diana Moreno (35303)","default_server" : "0",  "descr_agente" : "Diana Moreno (35303)","nome_agente" : "agent/35303"},
  {"aliases" : "Rocio Bahamon (35304)","default_server" : "0",  "descr_agente" : "Rocio Bahamon (35304)","nome_agente" : "agent/35304"},
  {"aliases" : "Brigitte Caicedo (35305)","default_server" : "0",  "descr_agente" : "Brigitte Caicedo (35305)","nome_agente" : "agent/35305"},
  {"aliases" : "Eliana Rivera (35306)","default_server" : "0",  "descr_agente" : "Eliana Rivera (35306)","nome_agente" : "agent/35306"},
  {"aliases" : "Cristina Cadena (35307)","default_server" : "0",  "descr_agente" : "Cristina Cadena (35307)","nome_agente" : "agent/35307"},
  {"aliases" : "Guillermo Aguilar (35308)","default_server" : "0",  "descr_agente" : "Guillermo Aguilar (35308)","nome_agente" : "agent/35308"},
  {"aliases" : "Wendy Velasquez (35309)","default_server" : "0",  "descr_agente" : "Wendy Velasquez (35309)","nome_agente" : "agent/35309"},
  {"aliases" : "Nelly Mina (35310)","default_server" : "0",  "descr_agente" : "Nelly Mina (35310)","nome_agente" : "agent/35310"},
  {"aliases" : "Stefany Bolivar (35311)","default_server" : "0",  "descr_agente" : "Stefany Bolivar (35311)","nome_agente" : "agent/35311"},
  {"aliases" : "Astrid Zuniga (35312)","default_server" : "0",  "descr_agente" : "Astrid Zuniga (35312)","nome_agente" : "agent/35312"},
  {"aliases" : "Jhon Gomez (35313)","default_server" : "0",  "descr_agente" : "Jhon Gomez (35313)","nome_agente" : "agent/35313"},
  {"aliases" : "Jessica Gomez (35314)","default_server" : "0",  "descr_agente" : "Jessica Gomez (35314)","nome_agente" : "agent/35314"},
  {"aliases" : "Edgar Zuleta (35315)","default_server" : "0",  "descr_agente" : "Edgar Zuleta (35315)","nome_agente" : "agent/35315"},
  {"aliases" : "Yulexis Pitalua (35316)","default_server" : "0",  "descr_agente" : "Yulexis Pitalua (35316)","nome_agente" : "agent/35316"}
]

i = 0

for report in blocks:

    data = report
    params = {}

    with requests.Session() as s:
        p = s.post( url, data = data )
        # print the html returned or something more intelligent to see if it's a successful login page.
        #print p.text

        # An authorised request.
        r = s.get( url, params = params, headers = headers )
        #print r.text

        print "%s..." % report['aliases'],
            # print r.text
        try:
            vega_data = r.text
            print "Done! %s" % vega_data
        except:
            print "Error!"

        p.close()
        r.close()
        s.close()
