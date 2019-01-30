 # locatie/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.http import HttpResponse
import sqlite3
import xmltodict
import requests
import csv
import os
import operator
import datetime
now = datetime.datetime.now()
gemeentecodes = {'Amersfoort': 'GM0307', 'Baarn': 'GM0308', 'De Bilt': 'GM0310', 'Bunnik': 'GM0312', 'Bunschoten': 'GM0313', 'Eemnes': 'GM0317','Houten': 'GM0321', 'IJsselstein': 'GM0353', 'Leusden': 'GM0327', 'Lopik': 'GM0331', 'Montfoort': 'GM0335', 'Nieuwegein': 'GM0356', 'Oudewater': 'GM0589', 'Renswoude': 'GM0339', 'Rhenen': 'GM0340', 'De Ronde Venen': 'GM0736', 'Soest': 'GM0342', 'Stichtse Vecht': 'GM1904', 'Utrecht (gemeente)': 'GM0344', 'Utrechtse Heuvelrug': 'GM1581', 'Veenendaal': 'GM0345', 'Wijk bij Duurstede': 'GM0352', 'Woerden': 'GM0632', 'Woudenberg': 'GM0351',  'Zeist': 'GM0355'}



#### REQUEST FUNCTIES ####



#Return template
def index(request):
    adreslist = "Zeist"
    template = 'index.html'
    return render(request, template, { "adreslist": adreslist })
    
#Get slider data from js and return adreslist 
def search(request):
    if request.method == 'POST':
        slider1 = request.POST['slider1'].split('","')
        slider2 = request.POST['slider2'].split('","')
        slider3 = request.POST['slider3'].split('","')
        slider4 = request.POST['slider4'].split('","')
        slider5 = request.POST['slider5'].split('","')
        template = 'index.html'
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name, SUM(bewoners.aantal) FROM  bewoners, steden, horeca, inkomen, partijen WHERE steden.id = bewoners.id AND inkomen.id = steden.id AND horeca.id = steden.id AND partijen.id = steden.id AND horeca.aantal<={} AND horeca.aantal>={} AND leeftijd<={} AND leeftijd>={} AND inkomen<={} AND inkomen>={} AND percentage<={} AND percentage>={} GROUP BY bewoners.id HAVING SUM(bewoners.aantal) <= {} AND SUM(bewoners.aantal) >= {}".format(slider3[1][:-5],slider3[0][2:-3],slider2[1][:-5],slider2[0][2:-3],slider4[1][:-3],slider4[0][2:-1],slider5[1][:-3],slider5[0][2:-1],slider1[1][:-5],slider1[0][2:-3]))
        steden = c.fetchall()
        adreslist = []
        for stad in steden:
            adreslist += [stad[0]]
        return HttpResponse(getbest(adreslist,slider1,slider2,slider3,slider4,slider5))

#De algoritme voor de beste plek
def getbest(adreslist,slider1,slider2,slider3,slider4,slider5):
    try:
        dicto = {}
        lijst = ""
        for adres in adreslist:
            dicto.update({adres:0})
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name ,MAX(totaal) FROM(SELECT name, horeca.aantal AS totaal FROM  bewoners, steden, horeca, inkomen, partijen WHERE steden.id = bewoners.id AND inkomen.id = steden.id AND horeca.id = steden.id AND partijen.id = steden.id AND horeca.aantal<={} AND horeca.aantal>={} AND leeftijd<={} AND leeftijd>={} AND inkomen<={} AND inkomen>={} AND percentage<={} AND percentage>={} GROUP BY bewoners.id HAVING SUM(bewoners.aantal) <= {} AND SUM(bewoners.aantal) >= {})".format(slider3[1][:-5],slider3[0][2:-3],slider2[1][:-5],slider2[0][2:-3],slider4[1][:-3],slider4[0][2:-1],slider5[1][:-3],slider5[0][2:-1],slider1[1][:-5],slider1[0][2:-3]))
        dicto[c.fetchall()[0][0]] += 1
        c.execute("SELECT name ,MAX(totaal) FROM(SELECT name, percentage AS totaal FROM  bewoners, steden, horeca, inkomen, partijen WHERE steden.id = bewoners.id AND inkomen.id = steden.id AND horeca.id = steden.id AND partijen.id = steden.id AND horeca.aantal<={} AND horeca.aantal>={} AND leeftijd<={} AND leeftijd>={} AND inkomen<={} AND inkomen>={} AND percentage<={} AND percentage>={} GROUP BY bewoners.id HAVING SUM(bewoners.aantal) <= {} AND SUM(bewoners.aantal) >= {})".format(slider3[1][:-5],slider3[0][2:-3],slider2[1][:-5],slider2[0][2:-3],slider4[1][:-3],slider4[0][2:-1],slider5[1][:-3],slider5[0][2:-1],slider1[1][:-5],slider1[0][2:-3]))
        dicto[c.fetchall()[0][0]] += 1
        c.execute("SELECT name, MAX(totaal) FROM (SELECT name,(SUM(bewoners.aantal) / horeca.aantal) AS totaal FROM  bewoners, steden, horeca, inkomen, partijen WHERE steden.id = bewoners.id AND inkomen.id = steden.id AND horeca.id = steden.id AND partijen.id = steden.id AND horeca.aantal<={} AND horeca.aantal>={} AND leeftijd<={} AND leeftijd>={} AND inkomen<={} AND inkomen>={} AND percentage<={} AND percentage>={} GROUP BY bewoners.id HAVING SUM(bewoners.aantal) <= {} AND SUM(bewoners.aantal) >= {})".format(slider3[1][:-5],slider3[0][2:-3],slider2[1][:-5],slider2[0][2:-3],slider4[1][:-3],slider4[0][2:-1],slider5[1][:-3],slider5[0][2:-1],slider1[1][:-5],slider1[0][2:-3]))
        dicto[c.fetchall()[0][0]] += 1
        maximum = max(dicto, key=dicto.get)
    except:
        maximum = ""
    for adres in adreslist:
        if adres == "Utrecht (gemeente)":
            lijst += "Utrecht,"
        else:
            lijst += adres + ","
    lijst += maximum 
    return lijst
    

#Update the database
def update(request):
#Database name
    dbfilename = "database.db"

    #Query's
    sql_create_steden_table = """ CREATE TABLE IF NOT EXISTS steden (
                                        id integer PRIMARY KEY,
                                        name text,
                                        regiocode text
                                    ); """
    sql_create_bewoners_table = """ CREATE TABLE IF NOT EXISTS bewoners (
                                        id integer,
                                        regiocode text,
                                        geslacht text,
                                        leeftijd int,
                                        aantal integer,
                                        FOREIGN KEY (id) REFERENCES steden(id)
                                    ); """
    sql_create_horeca_table = """ CREATE TABLE IF NOT EXISTS horeca (
                                        id integer PRIMARY KEY,
                                        regiocode text,
                                        aantal int,
                                        FOREIGN KEY (id) REFERENCES steden(id)
                                    ); """
    sql_create_inkomen_table = """ CREATE TABLE IF NOT EXISTS inkomen (
                                        id integer PRIMARY KEY,
                                        regiocode text,
                                        inkomen integer,
                                        FOREIGN KEY (id) REFERENCES steden(id)
                                    ); """
    sql_create_partijen_table = """ CREATE TABLE IF NOT EXISTS partijen (
                                        id integer PRIMARY KEY,
                                        regiocode text,
                                        percentage integer,
                                        FOREIGN KEY (id) REFERENCES steden(id)
                                    ); """
                                    
    #Create database if not excist
    if request.method == 'POST':
        data = request.POST['update']
        if data == "update":
            os.remove("database.db")
            conn = sqlite3.connect('database.db')
            db = open(dbfilename,'w')
            create_db_tables(conn, sql_create_steden_table,sql_create_bewoners_table,sql_create_horeca_table,sql_create_inkomen_table,sql_create_partijen_table)
            create_steden_values(conn)
            create_bewoners_values(conn)
            create_horeca_values(conn)
            create_inkomen_values(conn)
            create_partijen_values(conn)
            return HttpResponse("Database updated.")



###### DATABASE FUNCTIES #######


#Create Database
def create_db_tables(conn, steden, bewoners, horeca, inkomen, partijen):
    c = conn.cursor()
    c.execute(steden)
    c.execute(bewoners)
    c.execute(horeca)
    c.execute(inkomen)
    c.execute(partijen)
    conn.commit()



#Create Values for Datatvase
def create_steden_values(conn):
    for gemeente in gemeentecodes:
        c = conn.cursor()
        value = "INSERT INTO steden VALUES ("+gemeentecodes[gemeente][2:]+",'"+gemeente+"','"+gemeentecodes[gemeente]+"')"
        c.execute(value)
    conn.commit()

def create_bewoners_values(conn):
    for gemeente in gemeentecodes:
        c = conn.cursor()
        jaar = now.year
        nul = True
        while nul == True:
            gegevens = xmltodict.parse(api_leeftijd_ophalen(gemeentecodes[gemeente], str(jaar) + "JJ00"))
            try:
                test = (gegevens["feed"]["entry"][0]["content"]["m:properties"]["d:BevolkingOp1Januari_1"]["#text"])
                nul = False
            except:
                jaar-=1
        leeftijd = 1
        for i in range(110, 204):
            value = ("INSERT INTO bewoners VALUES ({},'{}','{}',{},{})".format(int(gemeentecodes[gemeente][2:]),gemeentecodes[gemeente],"M",leeftijd,gegevens["feed"]["entry"][i]["content"]["m:properties"]["d:BevolkingOp1Januari_1"]["#text"]))
            c.execute(value)
            leeftijd += 1
        leeftijd = 1
        for i in range(218, 312):
            value = ("INSERT INTO bewoners VALUES ({},'{}','{}',{},{})".format(int(gemeentecodes[gemeente][2:]),gemeentecodes[gemeente],"V",leeftijd,gegevens["feed"]["entry"][i]["content"]["m:properties"]["d:BevolkingOp1Januari_1"]["#text"]))
            c.execute(value)
            leeftijd += 1
        conn.commit()

def create_horeca_values(conn):
    for gemeente in gemeentecodes:
        c = conn.cursor()
        jaar = now.year
        nul = True
        while nul == True:
            gegevens = xmltodict.parse(api_horeca_ophalen(str(jaar) + "JJ00", gemeentecodes[gemeente]))
            try:
                value = ("INSERT INTO horeca VALUES ({},'{}',{})".format(int(gemeentecodes[gemeente][2:]),gemeentecodes[gemeente],gegevens["feed"]["entry"]["content"]["m:properties"]["d:Vestigingen_1"]["#text"]))
                c.execute(value)
                nul = False
            except:
                jaar-=1
        conn.commit()
                
def create_inkomen_values(conn):
    for gemeente in gemeentecodes:
        c = conn.cursor()
        jaar = now.year
        nul = True
        while nul == True:
            gegevens = xmltodict.parse(api_inkomen_ophalen(gemeentecodes[gemeente], str(jaar) + "JJ00"))
            try:
                value = ("INSERT INTO inkomen VALUES ({},'{}',{})".format(gemeentecodes[gemeente][2:],gemeentecodes[gemeente],gegevens["feed"]["entry"][0]["content"]["m:properties"]["d:MediaanBesteedbaarInkomen_6"]["#text"]))
                c.execute(value)
                nul = False
            except:
                jaar-=1
        conn.commit()

def create_partijen_values(conn):
    try:
        with open ("locatie/verkiezingen.csv", 'r', encoding='utf-8') as uitlsagenCSV:
            reader = csv.reader(uitlsagenCSV, delimiter=';')
            for row in reader:
                for gemeente in gemeentecodes:
                    c = conn.cursor()
                    if row[1] == (gemeentecodes[gemeente].replace("M", "")):
                        stemmen = int(row[9])
                        glstemmen = int(row[14])
                        gemiddeld = (glstemmen / stemmen) * 100
                        value = ("INSERT INTO partijen VALUES ({},'{}',{:.2f})".format(gemeentecodes[gemeente][2:],gemeentecodes[gemeente],gemiddeld))
                        c.execute(value)
            conn.commit()
    except:
        return HttpResponse("Error; verkiezingen.csv")

#Get data for the datatase
def api_horeca_ophalen(jaar, code):
    url = "https://opendata.cbs.nl/ODataApi/OData/81575NED/TypedDataSet?$filter=startswith(BedrijfstakkenBranchesSBI2008,'389100') and startswith(Perioden,'{}') and startswith(RegioS,'{}')&$format=xml".format(jaar,code)
    r = requests.get(url)
    return (r.text)

def api_leeftijd_ophalen(code, jaar):
    url = "https://opendata.cbs.nl/ODataApi/OData/03759ned/TypedDataSet?$filter=startswith(RegioS,'{}') and startswith(Perioden,'{}') and startswith(BurgerlijkeStaat, 'T001019')&$format=xml".format(code,jaar)
    r = requests.get(url)
    return r.text 

def api_inkomen_ophalen(code, jaar):
    url="https://opendata.cbs.nl/ODataApi/OData/84341ned/TypedDataSet?$filter=startswith(RegioS,'{}') and startswith(Perioden,'{}') and startswith(Populatie, '1050010')&$format=xml".format(code,jaar)
    r = requests.get(url)
    return r.text




