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
    return None


def teams(request):
    return None


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






