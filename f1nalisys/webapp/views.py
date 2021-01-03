from django.shortcuts import render
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json
from f1nalisys import forms
from django.http import HttpResponse, HttpRequest


# Create your views here.


def open_db():
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    return 'f1', accessor


def index(request):
    open_db()
    return render(request, 'index.html')


def hello(request):
    db_info = open_db()
    print(db_info)

    # "@prefix dbc: < http: // dbpedia.org / resource / Category: >."
    info = """
        select * where { 
	        ?s ?p ?o .
        } limit 5 
    """

    payload_query = {"query": info}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    print(res)
    list = []

    for e in res['results']['bindings']:
        list.append(e['p']['value'])

    print(list)

    tparams = {
        'info': list
    }

    return render(request, 'hello.html', tparams)


def drivers(request):
    db_info = open_db()
    print(db_info)

    driver_names = """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
select DISTINCT ?l ?birthDate ?nationality ?championships ?fanRating
where {
    {
        ?t rdf:type skos:Concept .
        ?d dct:subject ?t .
        ?d dbo:birthDate ?birthDate .
        ?d dbo:championships ?championships .
        ?d dbo:nationality ?nationality .
        ?d rdfs:label ?l .
        filter (lang(?l) = "en") .
        optional {
            ?d dbo:fanRating ?fanRating .
        }
    }
    UNION
    {
        ?t rdf:type skos:Concept .
        ?d dct:subject ?t .
        ?d dbo:birthDate ?birthDate .
        ?d dbo:championships ?championships .
        ?d dbp:nationality ?nationality .
        ?d rdfs:label ?l .
        filter (lang(?l) = "en") .
        optional {
            ?d dbo:fanRating ?fanRating .
        }
    }
} 
ORDER BY DESC(?birthDate)
        """

    payload_query = {"query": driver_names}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    # print(res)
    teams_info = []
    names = []
    for e in res['results']['bindings']:
        valid = True
        #print("e: ", e)
        dt = dict()
        #dt['nome'] = e['l']['value']

        if 'l' in e.keys():
            if e['l']['value'] in names:
                valid = False
            dt['l'] = e['l']['value']
            names.append(e['l']['value'])
        if 'birthDate' in e.keys():
            dt['birthDate'] = e['birthDate']['value']
        if 'nationality' in e.keys():
            n = e['nationality']['value']
            if "/" in n:
                n = n.split("/")[-1]
            dt['nationality'] = n
        if 'championships' in e.keys():
            if int(e['championships']['value']) < 20:
                dt['championships'] = e['championships']['value']
        if 'fanRating' in e.keys():
            dt['fanRating'] = e['fanRating']['value']
        else:
            dt['fanRating'] = 0


        if valid:
            teams_info.append(dt)
    #print(teams_info)

    tparams = {
        'info': teams_info
    }

    return render(request, 'drivers.html', tparams)


def new_rate(request, name, value, text):
    db_info = open_db()
    value = int(value)
    print(db_info)
    print(name, value)

    query = '''
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dct: <http://purl.org/dc/terms/>
        delete {
            ?d dbo:fanRating ?fanRating
        }
        where {
            ?t rdf:type skos:Concept .
            ?d dct:subject ?t .
            ?d rdfs:label "'''+ name +'''"@en .
            ?d dbo:fanRating ?fanRating .
        }
    '''
    payload_query = {"update": query}
    db_info[1].sparql_update(body=payload_query, repo_name=db_info[0])

    return addRate(request, name, value, text)

def addRate(request, name, value, text):
    db_info = open_db()
    print(db_info)
    if text == "like":
        rate = 1
    elif text == "dislike":
        rate = -1
    print(int(value) + rate)
    v  = ''' + str(int(value) + rate) + '''
    query2 = '''
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dct: <http://purl.org/dc/terms/>
            insert {
                ?d dbo:fanRating "''' + str(int(value) + rate) + '''"
            }
            where {
                ?t rdf:type skos:Concept .
                ?d dct:subject ?t .
                ?d rdfs:label "''' + name + '''"@en .
            }
        '''
    payload_query2 = {"update": query2}
    db_info[1].sparql_update(body=payload_query2, repo_name=db_info[0])

    return drivers(request)


def query_teams_basic_info(min_races=0, min_wins=0, search=""):
    db_info = open_db()

    # {'uri1': {'nome1': 'ferrari', 'races1': '50'}, 'uri2': {'nome': 'redbull', 'races': '33'}, ...}

    if min_races is None:
        min_races = 0
    if min_wins is None:
        min_wins = 0

    # filtrar
    if min_races != 0 and min_wins != 0:
        the_query = """PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dbc: <http://dbpedia.org/resource/Category:>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select distinct ?team ?team_name ?link ?location ?races ?wins ?poles
        where { 
            ?team dct:subject dbc:Formula_One_constructors .
            ?team rdfs:label ?team_name .
            filter (lang(?team_name) = "en") .
            ?team dbp:base ?location
            optional{
                ?team foaf:homepage ?link .   
            }
            ?team dbp:races ?races .
            filter(datatype(?races) = xsd:integer) .   
            filter (?races > %d) .

            ?team dbp:wins ?wins .
            filter(datatype(?wins) = xsd:integer)
            filter (?wins > %d) .

            optional{
                ?team dbp:poles ?poles .
                filter(datatype(?poles) = xsd:integer)   
            }
        }
        order by desc (?races) (?wins) (?poles)""" % (min_races, min_wins)

    # search
    elif search != "":
        the_query = """PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dbc: <http://dbpedia.org/resource/Category:>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select distinct ?team ?team_name ?link ?location ?races ?wins ?poles
        where { 
            ?team dct:subject dbc:Formula_One_constructors .
            ?team rdfs:label ?team_name .
            filter (lang(?team_name) = "en") .
            FILTER regex(?team_name, "%s", "i") .
            ?team dbp:base ?location .
            optional{
                ?team foaf:homepage ?link .   
            }
            optional{
                ?team dbp:races ?races .
                filter(datatype(?races) = xsd:integer) .   
                filter (?races > 400) .
            }
            optional{
                ?team dbp:wins ?wins .
                filter(datatype(?wins) = xsd:integer)
            }
            optional{
                ?team dbp:poles ?poles .
                filter(datatype(?poles) = xsd:integer)   
            }
        }
        order by desc (?races) (?wins) (?poles)""" % search
    # default (mostra todas as equipas)
    else:
        the_query = """
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dbc: <http://dbpedia.org/resource/Category:>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            select distinct ?team ?team_name ?location ?link ?races ?wins ?poles
            where { 
                ?team dct:subject dbc:Formula_One_constructors .
                ?team rdfs:label ?team_name .
                filter (lang(?team_name) = "en") .
                optional{
                    ?team dbp:base ?location .   
                }
                optional{
                    ?team foaf:homepage ?link .   
                }
                optional{
                    ?team dbp:races ?races .
                    filter(datatype(?races) = xsd:integer)   
                }
                optional{
                    ?team dbp:wins ?wins .
                    filter(datatype(?wins) = xsd:integer)
                }
                optional{
                    ?team dbp:poles ?poles .
                    filter(datatype(?poles) = xsd:integer)   
                }
            }
            order by desc (?races) (?wins) (?poles)    
                """

    payload_query = {"query": the_query}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)

    return save_teams_info(res)


def save_teams_info(res):
    team_dict = dict()
    for e in res['results']['bindings']:
        team_uri = e['team']['value']
        if team_uri not in team_dict:
            team_dict[team_uri] = dict()
            team_dict[team_uri]['nome'] = e['team_name']['value']

            if 'link' in e.keys():
                team_dict[team_uri]['link'] = e['link']['value']

            if 'location' in e.keys():
                team_dict[team_uri]['location'] = check(e['location']['value'])

            if 'races' in e.keys():
                team_dict[team_uri]['races'] = e['races']['value']

            if 'wins' in e.keys():
                team_dict[team_uri]['wins'] = e['wins']['value']

            if 'poles' in e.keys():
                team_dict[team_uri]['poles'] = e['poles']['value']

        else:
            if 'location' in e.keys():
                if e['location']['value'] not in team_dict[team_uri]['location']:
                    if check(e['location']['value']) not in team_dict[team_uri]['location']:    # para nao haver repetidos
                        team_dict[team_uri]['location'] = team_dict[team_uri]['location'] + ', ' + check(e['location']['value'])

            if 'races' in e.keys():
                if e['races']['value'] not in team_dict[team_uri]['races']:
                    team_dict[team_uri]['races'] = team_dict[team_uri]['races'] + ', ' + e['races']['value']

            if 'wins' in e.keys():
                if e['wins']['value'] not in team_dict[team_uri]['wins']:
                    team_dict[team_uri]['wins'] = team_dict[team_uri]['wins'] + ', ' + e['wins']['value']

            if 'poles' in e.keys():
                if e['poles']['value'] not in team_dict[team_uri]['poles']:
                    team_dict[team_uri]['poles'] = team_dict[team_uri]['poles'] + ', ' + e['poles']['value']

    return team_dict


def teams(request):
    db_info = open_db()
    team_dict = {}

    if request.method == 'POST':
        form = forms.Filter(request.POST)
        # filtrar
        if 'reset' in request.POST:
            form = forms.Filter()
            team_dict = query_teams_basic_info()

        if 'submit' in request.POST:
            if form.is_valid():
                min_races = form.cleaned_data['races']
                min_wins = form.cleaned_data['wins']
                team_dict = query_teams_basic_info(min_races, min_wins)
        # search
        if 'search' in request.POST:
            if 'input' in request.POST:
                inp = request.POST['input']
                team_dict = query_teams_basic_info(search=inp)

    else:   # mostra tudo
        form = forms.Filter()
        team_dict = query_teams_basic_info()

    tparams = {
        'info': team_dict,
        'n_teams': len(team_dict.values()),
        'form': form
    }

    return render(request, 'teams.html', tparams)


def get_team_uri(team):
    db_info = open_db()

    q = '''PREFIX dbc: <http://dbpedia.org/resource/Category:>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dct: <http://purl.org/dc/terms/>
            select distinct ?team_uri
            where {{
                ?team_uri dct:subject dbc:Formula_One_constructors .
                ?team_uri rdfs:label ?l .
                filter (lang(?l) = "en") .
                filter regex((?l), "^%s")
            }}''' % team

    payload_query = {"query": q}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    return res['results']['bindings'][0]['team_uri']['value']


def query_team_resume(team):
    db_info = open_db()

    query_resume = """PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>
select distinct ?resume
where {
    <%s> dct:subject dbc:Formula_One_constructors .  
    <%s> dbo:abstract ?resume
    filter (lang(?resume) = "en")
}""" % (team, team)

    payload_query = {"query": query_resume}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)

    return res['results']['bindings'][0]['resume']['value']


def impfig_team(team):
    db_info = open_db()
    query = """PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
select distinct ?i
where {
    <%s> dct:subject dbc:Formula_One_constructors . 
    <%s> dbp:importantFigure ?i.
}""" % (team, team)

    payload_query = {"query": query}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)

    l = []
    for e in res['results']['bindings']:
        value = e['i']['value']
        if value not in l:
            l.append(check(value))
    return l


def img_team(team):
    db_info = open_db()
    query = """PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dbo: <http://dbpedia.org/ontology/>
select distinct ?img
where {
    <%s> dct:subject dbc:Formula_One_constructors .
    <%s> dbo:thumbnail ?img
}""" % (team, team)

    payload_query = {"query": query}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])

    res = json.loads(res)

    if not res['results']['bindings']:
        return "", 300

    src = res['results']['bindings'][0]['img']['value']
    return get_img_width(src)


def team_details(request, team_label):
    teamURI = get_team_uri(team_label)

    all_teams = query_teams_basic_info()
    this_team = all_teams[teamURI]

    resume = query_team_resume(teamURI)
    impfig = impfig_team(teamURI)
    img, width = img_team(teamURI)
    # TODO: sq ir buscar mais info sobre uma team

    tparams = {
        'team_name': team_label,
        'info': this_team,
        'resume': resume,
        'impfig': impfig,
        'img': img,
        'width': width
    }
    return render(request, 'team_details.html', tparams)


def media(request):
    db_info = open_db()
    print(db_info)
    # "@prefix dbc: < http: // dbpedia.org / resource / Category: >."

    info = """
                PREFIX dbc: <http://dbpedia.org/resource/Category:>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX prov: <http://www.w3.org/ns/prov#>
                select ?s ?o ?h
                where { 
                    ?s ?p dbc:Formula_One_media .
                    ?s rdfs:label ?o .
                    ?s prov:wasDerivedFrom ?h
                    filter (lang(?o)="en" ||lang(?o)="pt" || lang(?o)="fr" || lang(?o)="es")
                }


            """

    payload_query = {"query": info}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])

    res = json.loads(res)
    pistas=dict()
    nome=""
    novaNome=""

    for e in res['results']['bindings']:
        nome=e['s']['value']
        if nome not in pistas:
            pistas[nome]=dict()
            pistas[nome]["Label"]=e['o']['value']
            pistas[nome]["URL"]=e['h']['value']
            #pistas[nome]["Label"]=pistas[nome]["Label"]+"\n"+e['o']['value']
        # if pista is novaPista:
        #     pass
        # else:
        #     pistas[pista]=[]

        #list.append(e['s']['value'])

    print(pistas)

    tparams = {
        'lista': pistas,
        'n_media': len(pistas.values())

    }
    print(len(pistas.values()))

    return render(request, 'media.html', tparams)


def tracks(request):
    db_info = open_db()
    print(db_info)

    # "@prefix dbc: < http: // dbpedia.org / resource / Category: >."
    info = """
            PREFIX dbc: <http://dbpedia.org/resource/Category:>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX dbp: <http://dbpedia.org/property/>
            select ?s ?imgP ?laps ?name ?mostW ?c ?link ?t ?imgC ?l
            where { 
                ?s ?p dbc:Formula_One_Grands_Prix .
                ?s dbo:thumbnail ?imgP.
                ?s dbp:laps ?laps.
                ?s dbp:name ?name.
                ?s dbp:mostWinsDriver ?mostW.
                ?s prov:wasDerivedFrom ?link.
                ?s dbp:circuit ?c.
                ?c dbp:turns ?t.
                ?c dbo:thumbnail ?imgC.
                ?c dbp:location ?l .
                
            }

        """

    payload_query = {"query": info}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    print(res)
    pistas = dict()
    nome = ""
    novaNome = ""

    for e in res['results']['bindings']:
        nome=e['s']['value']
        if nome not in pistas:
            pistas[nome]=dict()
            pistas[nome]["TAG"]=check(e['s']['value'])
            pistas[nome]["imgP"]=e['imgP']['value']
            pistas[nome]["Laps"]=e['laps']['value']
            pistas[nome]["Name"]=e['name']['value']
            pistas[nome]["MostWin"]=e['mostW']['value']
            pistas[nome]["LinkGP"]=e['link']['value']
            pistas[nome]["TAGC"]=check(e['c']['value'])
            pistas[nome]["Turns"]=e['t']['value']
            pistas[nome]["imgC"]=e['imgC']['value']
            pistas[nome]["Location"]=check(e['l']['value'])
        else:
            if e['mostW']['value'] not in pistas[nome]["MostWin"]:
                pistas[nome]["MostWin"] = pistas[nome]["MostWin"]+", "+e['mostW']['value']
            if check(e['l']['value']) not in pistas[nome]["Location"]:
                pistas[nome]["Location"]=pistas[nome]["Location"]+", "+check(e['l']['value'])
        # if pista is novaPista:
        #     pass
        # else:
        #     pistas[pista]=[]

        # list.append(e['s']['value'])

    print(pistas)

    tparams = {
        'lista': pistas,
        'n_tracks': len(pistas.values())
    }

    return render(request, 'tracks.html', tparams)


def season(request):
    return None


def check(string):
    if "http" in string:
        array = string.split("/")
        w = array[len(array)-1]
        return str(w).replace("_", " ")
    else:
        return string


# retorna um tuplo (src, width)
def get_img_width(src):
    if '?width' in src:
        array = src.split("?")
        print(array)
        w = str(array[1]).split("=")[1]
        return src, w

