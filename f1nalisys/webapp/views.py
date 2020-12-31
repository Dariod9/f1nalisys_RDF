from django.shortcuts import render
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


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
select DISTINCT ?l ?birthDate ?nationality ?championships
where {
    {
        ?t rdf:type skos:Concept .
        ?d dct:subject ?t .
        ?d dbo:birthDate ?birthDate .
        ?d dbo:championships ?championships .
        ?d dbo:nationality ?nationality .
        ?d rdfs:label ?l .
        filter (lang(?l) = "en") .
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

        if valid:
            teams_info.append(dt)
    #print(teams_info)

    tparams = {
        'info': teams_info
    }

    return render(request, 'drivers.html', tparams)


def teams(request):
    db_info = open_db()
    print(db_info)

    team_dict = dict()
    # {'uri1': {'nome1': 'ferrari', 'races1': '50'}, 'uri2': {'nome': 'redbull', 'races': '33'}, ...}

    # team_names = """
    #             PREFIX dct: <http://purl.org/dc/terms/>
    #             PREFIX dbc: <http://dbpedia.org/resource/Category:>
    #             PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    #             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #             select distinct ?team ?team_name ?link
    #             where {
    #                 ?team dct:subject dbc:Formula_One_constructors .
    #                 ?team rdfs:label ?team_name .
    #                 optional{
    #                     ?team foaf:homepage ?link .
    #                 }
    #                 filter (lang(?team_name) = "en")
    #             }
    #             order by ?team_name
    #     """

    team_names = """
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX dbc: <http://dbpedia.org/resource/Category:>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dbp: <http://dbpedia.org/property/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                select distinct ?team ?team_name ?link ?races ?wins ?poles
                where { 
                    ?team dct:subject dbc:Formula_One_constructors .
                    ?team rdfs:label ?team_name .
                    filter (lang(?team_name) = "en") .
                    optional{
                        ?team foaf:homepage ?link .   
                    }
                    optional{
                        ?team dbp:races ?races .
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

    payload_query = {"query": team_names}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)

    for e in res['results']['bindings']:
        team_uri = e['team']['value']
        if team_uri not in team_dict:
            team_dict[team_uri] = dict()
            team_dict[team_uri]['nome'] = e['team_name']['value']

            if 'link' in e.keys():
                team_dict[team_uri]['link'] = e['link']['value']

            if 'races' in e.keys():
                team_dict[team_uri]['races'] = e['races']['value']

            if 'wins' in e.keys():
                team_dict[team_uri]['wins'] = e['wins']['value']

            if 'poles' in e.keys():
                team_dict[team_uri]['poles'] = e['poles']['value']

        else:
            if 'races' in e.keys():
                if e['races']['value'] not in team_dict[team_uri]['races']:
                    team_dict[team_uri]['races'] = team_dict[team_uri]['races'] + ', ' + e['races']['value']

            if 'wins' in e.keys():
                if e['wins']['value'] not in team_dict[team_uri]['wins']:
                    team_dict[team_uri]['wins'] = team_dict[team_uri]['wins'] + ', ' + e['wins']['value']

            if 'poles' in e.keys():
                if e['poles']['value'] not in team_dict[team_uri]['poles']:
                    team_dict[team_uri]['poles'] = team_dict[team_uri]['poles'] + ', ' + e['poles']['value']

    # Important Figures (to be continued)
    # teams_if = """
    #             PREFIX dct: <http://purl.org/dc/terms/>
    #             PREFIX dbc: <http://dbpedia.org/resource/Category:>
    #             PREFIX dbp: <http://dbpedia.org/property/>
    #             select distinct ?team ?impfig
    #             where {
    #                 ?team dct:subject dbc:Formula_One_constructors .
    #                 ?team dbp:importantFigure ?impfig.
    #             }
    #             order by ?team
    #         """
    # payload_query = {"query": teams_if}
    # res = db_info[1].sparql_select(body=payload_query,
    #                                repo_name=db_info[0])
    # res = json.loads(res)
    #
    # for e in res['results']['bindings']:
    #     team_uri = e['team']['value']
    #     if team_uri not in team_dict:
    #         team_dict[team_uri] = dict()
    #         if 'impfig' in e.keys():
    #             team_dict[team_uri]['impfig'] = e['impfig']['value']
    #     else:
    #         print("not new!")
    #         if 'impfig' in e.keys():
    #             print("tem impfig")
    #             if e['impfig']['value'] not in team_dict[team_uri]['impfig']:
    #                 team_dict[team_uri]['impfig'] = team_dict[team_uri]['impfig'] + ', ' + e['impfig']['value']

    tparams = {
        'info': team_dict,
        'n_teams': len(team_dict.values())
    }

    return render(request, 'teams.html', tparams)


def team_details(request, team_label):
    tparams = {
        'team': team_label
    }
    return render(request, 'hello.html', tparams)


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
        else:
            pistas[nome]["Label"]=pistas[nome]["Label"]+"\n"+e['o']['value']
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
            pistas[nome]["imgP"]=e['imgP']['value']
            pistas[nome]["Laps"]=e['laps']['value']
            pistas[nome]["Name"]=e['name']['value']
            pistas[nome]["MostWin"]=e['mostW']['value']
            pistas[nome]["LinkGP"]=e['link']['value']
            pistas[nome]["Turns"]=e['t']['value']
            pistas[nome]["imgC"]=e['imgC']['value']
            pistas[nome]["Location"]=checkLocation(e['l']['value'])
        else:
            if e['mostW']['value'] not in pistas[nome]["MostWin"]:
                pistas[nome]["MostWin"] = pistas[nome]["MostWin"]+", "+e['mostW']['value']
            if checkLocation(e['l']['value']) not in pistas[nome]["Location"]:
                pistas[nome]["Location"]=pistas[nome]["Location"]+", "+checkLocation(e['l']['value'])
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

def checkLocation(string):

    if "http" in string:
        array=string.split("/")
        return array[len(array)-1]
    else:
        return string





