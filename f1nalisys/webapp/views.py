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
            select DISTINCT ?t ?d ?l
                        where {
                            ?t rdf:type skos:Concept .
                            ?d dct:subject ?t .
                            ?d rdfs:label ?l 
                            filter (lang(?l) = "en")
                        } 
        """

    payload_query = {"query": driver_names}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    # print(res)
    teams_info = []
    for e in res['results']['bindings']:
        print("e: ", e)
        dt = dict()
        #dt['nome'] = e['l']['value']

        if 'l' in e.keys():
            dt['l'] = e['l']['value']

        teams_info.append(dt)

    print(teams_info)

    tparams = {
        'info': teams_info
    }

    return render(request, 'drivers.html', tparams)


def teams(request):
    db_info = open_db()
    print(db_info)

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
                    filter(datatype(?races) = xsd:integer)   
                }
                optional{
                    ?team dbp:wins ?wins .
                    filter(datatype(?wins) = xsd:integer)   
                }
                optional{
                    ?team dbp:wins ?poles .
                    filter(datatype(?poles) = xsd:integer)   
                }
            }
                order by desc (?races)    
        """

    payload_query = {"query": team_names}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    # print(res)
    teams_info = []
    for e in res['results']['bindings']:
        print("e: ", e)
        dt = dict()
        dt['nome'] = e['team_name']['value']

        if 'link' in e.keys():
            dt['link'] = e['link']['value']

        if 'races' in e.keys():
            dt['races'] = e['races']['value']

        if 'wins' in e.keys():
            dt['wins'] = e['wins']['value']

        if 'poles' in e.keys():
            dt['poles'] = e['poles']['value']

        teams_info.append(dt)

    print(teams_info)

    tparams = {
        'info': teams_info
    }

    return render(request, 'teams.html', tparams)


def tracks(request):
    db_info = open_db()
    print(db_info)

    # "@prefix dbc: < http: // dbpedia.org / resource / Category: >."
    info = """
            PREFIX dbo:	<http://dbpedia.org/ontology/>
            PREFIX dbp:	<http://dbpedia.org/property/>
            PREFIX dct:	<http://purl.org/dc/terms/> 
            PREFIX dbr:	<http://dbpedia.org/resource/> 
            PREFIX dbc: <http://dbpedia.org/resource/Category:>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select DISTINCT ?s ?o ?l ?i
            where {
                ?s dct:subject dbc:Formula_One_circuits .
                ?s rdfs:label ?o .
                ?s dbp:location ?l .
                ?s dbo:thumbnail ?i
                filter (lang(?o) = "en")
            }  

        """

    payload_query = {"query": info}
    res = db_info[1].sparql_select(body=payload_query,
                                   repo_name=db_info[0])
    res = json.loads(res)
    print(res)
    pistas=dict()
    nome=""
    novaNome=""

    for e in res['results']['bindings']:
        nome=e['o']['value']
        if nome not in pistas:
            pistas[nome]=dict()
            pistas[nome]["Location"]=e['l']['value']
            pistas[nome]["Picture"]=e['i']['value']
        else:
            pistas[nome]["Location"]=pistas[nome]["Location"]+", "+e['l']['value']
        # if pista is novaPista:
        #     pass
        # else:
        #     pistas[pista]=[]

        #list.append(e['s']['value'])

    print(pistas)

    tparams = {
        'lista': pistas
    }

    return render(request, 'tracks.html', tparams)


def season(request):
    return None






