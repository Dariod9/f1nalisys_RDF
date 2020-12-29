import urllib

import xmltodict, requests, re

from BaseXClient import BaseXClient
from django.shortcuts import render
from lxml import etree

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
session.execute("open f1")


# Create your views here.

# teams com xslt
def teams(request, ano="2020"):
    queryText="import module namespace f1_methods = 'com.f1'; declare variable $ano external; f1_methods:constructors($ano)"
    query = session.query(queryText)
    query.bind("$ano", str(ano))
    exe = query.execute()

    if (exe == ""):
        getTeams(ano)
        return teams(request, ano)

    print(exe)
    root = etree.fromstring(exe)
    print("root:", root)

    xsl_file = etree.parse('webapp/xsl_files/teams.xsl')
    tranform = etree.XSLT(xsl_file)
    html = tranform(root)

    tparams = {
        'urll': "/teams",
        'ano': ano,
        'title': 'teams',
        'html': html
    }
    return render(request, 'teams.html', tparams)


def tracks(request):
    query = " import module namespace f1_methods = 'com.f1'; f1_methods:tracks() "
    queryT=session.query(query)
    # dá erro: nao encontra o local. Não sei em que pasta guardar os queries com as funçoes para chamar aqui
    # query = "xquery <root>{ local:get-constructors() }</root>"
    exe = queryT.execute()

    output = xmltodict.parse(exe)
    print("out: ", output)

    info = dict()
    for t in output['root']['elem']:
        info[t['CircuitName']] = (
            t['Location']['Locality'], t['Location']['Country'], getImagem(t['Location']['Country']))

    print(info)
    tparams = {
        'urll': "/tracks",
        'title': 'Tracks',
        'tracklist': info,
    }
    return render(request, 'tracks.html', tparams)


def fan(request):
    return render(request, 'fan.html')


def drivers_standings(request, ano):
    queryText = "import module namespace f1_methods = 'com.f1'; declare variable $ano external; f1_methods:driver_standings($ano)"
    query= session.query(queryText)
    query.bind("$ano", str(ano))
    exe = query.execute()
    root = etree.fromstring(exe)

    xsl_file = etree.parse("webapp/xsl_files/drivers-standings.xsl")
    tranform = etree.XSLT(xsl_file)
    html = tranform(root)

    tparams = {
        'title': 'Drivers Standings',
        'standings': html,
        'ano': ano,
    }
    return render(request, 'drivers_standings.html', tparams)


def constructors_standings(request, ano):
    queryText = "import module namespace f1_methods = 'com.f1'; declare variable $ano external;f1_methods:team_standings($ano)"
    query=session.query(queryText)
    query.bind("$ano", str(ano))
    exe = query.execute()
    root = etree.fromstring(exe)

    xsl_file = etree.parse("webapp/xsl_files/constructors-standings.xsl")
    tranform = etree.XSLT(xsl_file)
    html = tranform(root)

    tparams = {
        'title': 'Constructors Standings',
        'standings': html,
        'ano': ano,
    }
    return render(request, 'constructors_standings.html', tparams)


def race_results(request, ano, round):
    queryText = "import module namespace f1_methods = 'com.f1'; declare variable $ano external; declare variable $round external; f1_methods:race_results($ano,$round)"
    query=session.query(queryText)
    query.bind("$ano", str(ano))
    query.bind("$round", str(round))
    exe = query.execute()

    if (exe == ""):
        getRace(ano, round)
        return race_results(request, ano, round)

    root = etree.fromstring(exe)

    xsl_file = etree.parse("webapp/xsl_files/race_results.xsl")
    tranform = etree.XSLT(xsl_file)
    html = tranform(root)

    tparams = {
        'title': 'race results',
        'results': html,
        'ano': ano,
    }
    return render(request, 'race_results.html', tparams)


def drivers(request, ano="2020"):
    queryText = "import module namespace f1_methods = 'com.f1'; declare variable $ano external; f1_methods:drivers($ano)"
    query=session.query(queryText)
    query.bind("$ano", str(ano))
    exe = query.execute()

    if (exe == ""):
        getDrivers(ano)
        return drivers(request, ano)

    root = etree.fromstring(exe)

    xsl_file = etree.parse("webapp/xsl_files/drivers.xsl")
    transform = etree.XSLT(xsl_file)
    drivers_html = transform(root)

    tparams = {
        'urll': "/drivers",
        'ano': ano,
        'title': 'drivers',
        'drivers_html': drivers_html,
    }

    return render(request, 'drivers.html', tparams)


def getSeason(ano):
    anoDef = ano
    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/0", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_0", res2)

    response2 = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/drivers", verify=False)
    resposta = change(response2.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_drivers", res2)

    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/constructors", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_constructors", res2)

    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/circuits", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_circuits", res2)

    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/2/results", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_race2", res2)

    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/1/results", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_race1", res2)

    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/3/results", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_race3", res2)

    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/driverStandings", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_driverStandings", res2)

    response = requests.get("http://ergast.com/api/f1/20" + str(anoDef) + "/constructorStandings", verify=False)
    resposta = change(response.text)
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_constructorStandings", res2)


def getDrivers(ano):
    response = requests.get("http://ergast.com/api/f1/" + str(ano) + "/drivers", verify=False)
    resposta = response.text
    res2 = change(resposta)

    session.add(str(ano) + "/" + str(ano) + "_drivers", res2)


def getTeams(ano):
    response = requests.get("http://ergast.com/api/f1/" + str(ano) + "/constructors", verify=False)
    resposta = response.text
    res2 = change(resposta)
    session.add(str(ano) + "/" + str(ano) + "_constructors", res2)


def getRace(ano, corrida):
    response = requests.get("http://ergast.com/api/f1/" + str(ano) + "/" + str(corrida) + "/results", verify=False)
    resposta = response.text
    res2 = change(resposta)
    session.add(str(ano) + "/" + str(ano) + "_" + str(corrida), res2)


def about(request):
    return render(request, 'about.html', {'title': 'About'})


def validate(tree):
    schema_root = etree.parse('webapp/Corridas/2020/seasons.xsd')
    schema = etree.XMLSchema(schema_root)
    print("Validação: " + str(schema.validate(tree)))
    return schema.validate(tree)


def season(request, ano="2020"):
    error = False
    error2=False
    if 'new_title' in request.POST and 'new_text' in request.POST:
        title = request.POST['new_title']
        text = request.POST['new_text']
        if title and text:
            node = '<Comment season="' + str(
                ano) + '"> <Title>' + title + '</Title> <Texto>' + text + '</Texto> </Comment>'
            input_query = ' for $c in collection("f1")//Comments where $c/@season="' + str(
                ano) + '" return insert node ' + node + ' into $c '
            query = session.query(input_query)
            nnode = '<curso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"xsi:noNamespaceSchemaLocation="comment_validator.xsd"> ' + node
            tree = etree.fromstring(node)
            schema_root = etree.parse('webapp/Corridas/comment_validator.xsd')
            schema = etree.XMLSchema(schema_root)
            valido = schema.validate(tree)
            print("Validação: " + str(valido))
            if valido:
                query.execute()
            else:
                error2 = True
        else:
            error2 = True

    # races
    races_query= "import module namespace f1_methods = 'com.f1'; declare variable $ano external; f1_methods:season($ano) "
    query = session.query(races_query)
    query.bind("$ano", str(ano))
    exe_races = query.execute()

    if len(exe_races) < 10:
        print("RACES: _____")

        # buscar o ficheiro à API
        url = "http://ergast.com/api/f1/" + str(ano)
        document = urllib.request.urlopen(url).read()
        tree = etree.fromstring(document)
        str_xml = change(etree.tostring(tree).decode("iso-8859-1"))
        tree = etree.fromstring(str_xml)

        # print("tree: ", str_xml)

        # se validar o ficheiro adiciona à BD
        if validate(tree):
            session.add(str(ano) + "/" + str(ano) + "_0", str_xml)
            return season(request, ano)
        else:
            error = True

    root = etree.fromstring(exe_races)

    xsl_file = etree.parse('webapp/xsl_files/races_overview.xsl')
    tranform = etree.XSLT(xsl_file)
    races_snippet = tranform(root)

    # top3 drivers
    top3drivers_query = "import module namespace f1_methods = 'com.f1'; declare variable $ano external; f1_methods:top3_drivers($ano) "
    query=session.query(top3drivers_query)
    query.bind("$ano", str(ano))
    exe_drivers = query.execute()

    if(len(exe_drivers) < 10):
        print("DRIVER: _____")

        response = requests.get("http://ergast.com/api/f1/" + str(ano) + "/driverStandings", verify=False)
        resposta = response.text
        res2 = change(resposta)
        session.add(str(ano) + "/" + str(ano) + "_driverStandings", res2)
        return season(request, ano)

    root_drivers = etree.fromstring(exe_drivers)

    xsl_file_drivers = etree.parse('webapp/xsl_files/top3drivers.xsl')
    tranform_drivers = etree.XSLT(xsl_file_drivers)
    drivers_snippet = tranform_drivers(root_drivers)

    # top3 teams
    top3teams_query = "import module namespace f1_methods = 'com.f1'; declare variable $ano external; f1_methods:top3_teams($ano) "
    query=session.query(top3teams_query)
    query.bind("$ano", str(ano))
    exe_teams = query.execute()

    if(len(exe_teams)<20):
        print("STANDINGS: _____")
        response = requests.get("http://ergast.com/api/f1/" + str(ano) + "/constructorStandings", verify=False)
        resposta = response.text
        res2 = change(resposta)
        session.add(str(ano) + "/" + str(ano) + "constructorStandings", res2)
        return season(request, ano)

    root_teams = etree.fromstring(exe_teams)

    xsl_file_teams = etree.parse('webapp/xsl_files/top3teams.xsl')
    tranform_teams = etree.XSLT(xsl_file_teams)
    teams_snippet = tranform_teams(root_teams)

    # comments
    query = "xquery <root>{for $c in collection('f1')//Comments where $c/@season=" + str(ano) + " return $c }</root>"
    exe = session.execute(query)
    output = xmltodict.parse(exe)
    # print(output['root'] == None)
    if output['root'] == None:
        input_query = ' let $c := collection("f1")/CommentsGroup return insert node <Comments season="' + str(
            ano) + '"></Comments> into $c '
        query = session.query(input_query)
        query.execute()
        query = "xquery <root>{for $c in collection('f1')//Comments where $c/@season=" + str(
            ano) + " return $c }</root>"
        exe = session.execute(query)
        output = xmltodict.parse(exe)

    info = []
    if 'Comment' in output['root']['Comments']:
        if isinstance(output['root']['Comments']['Comment'], list) and len(output['root']['Comments']['Comment']) > 1:
            for t in output['root']['Comments']['Comment']:
                print(t)
                info += [[t['Title'], t['Texto']]]
        else:
            info = [[output['root']['Comments']['Comment']['Title'], output['root']['Comments']['Comment']['Texto']]]

    tparams = {
        'urll': "/season",
        'info': info,
        'ano': ano,
        'drivers_standings_url': "/season/" + str(ano),
        'constructors_standings_url': "/season/" + str(ano),
        'title': 'overview',
        'races_snippet': races_snippet,
        'drivers_snippet': drivers_snippet,
        'teams_snippet': teams_snippet,
        'error': error,
        'error2': error2,
    }
    return render(request, 'ano.html', tparams)


def print_tree(root, t=""):
    if root.attrib != "":
        info = str(root.attrib)
    else:
        info = t + str(root.tag) + " -> " + str(root.text) + "\n"

    info = info.replace("{}", "").replace("\n", "")
    print(info)
    if len(root.getchildren()):
        for child in root:
            print_tree(child, t + "\t")

def delete_comment(request, ano, title, text):
        if title and text:
            print(title, text)
            input_query = ' for $c in collection("f1")//Comment where $c/@season="' + str(
                ano) + '" and $c/Title="' + title + '" and $c/Texto="' + text + '" return delete node $c '
            query = session.query(input_query)
            query.execute()
        return season(request, str(ano))


def index(request):
    session.execute("open f1")
    try:
        session.execute("delete RSS")
        session.execute("delete rssf1.xml")
        print(session.info())
        # add document

        # GERAR

        exec(open('webapp/Corridas/rssGetter.py').read())

        root = etree.parse("rssf1.xml")
        # print(root)

        session.add("RSS", etree.tostring(root).decode("utf-8"))
        # print(session.info())
    except IOError:
        print(session.info() + "\n ERRO MPTS")

    input = "import module namespace f1_methods = 'com.f1'; declare variable $ano external; f1_methods:rss() "
    queryT=session.query(input)
    query = queryT.execute()

    info = dict()
    capa = dict()
    res = xmltodict.parse(query)

    i = 1;
    for c in res["root"]["elem"]:
        c["description"] = c["description"].replace("<p>", "")
        c["description"] = c["description"].replace("</p>", "")
        if i == 1:
            capa[i] = (c["title"], c["pubDate"], c["author"], c["link"], c["description"])
        else:
            info[i] = (c["title"], c["pubDate"], c["author"], c["link"], c["description"])
        # print(info[i])
        i += 1

    tparams = {
        'news': info,
        'first_news': capa
    }

    return render(request, 'index.html', tparams)


def getImagem(pais):
    path = "/static/img/"
    if pais == "Italy":
        path = path + "italy.png"
    elif pais == "Spain":
        path = path + "spain.png"
    elif pais == "UK":
        path = path + "uk.png"
    elif pais == "Australia":
        path = path + "australia.png"
    elif pais == "USA":
        path = path + "usa.png"
    elif pais == "Bahrain":
        path = path + "bahrain.png"
    elif pais == "Azerbaijan":
        path = path + "azerbeijan.png"
    elif pais == "Germany":
        path = path + "germany.png"
    elif pais == "Hungary":
        path = path + "hungary.png"
    elif pais == "Brazil":
        path = path + "brazil.png"
    elif pais == "Turkey":
        path = path + "turkey.png"
    elif pais == "Singapore":
        path = path + "singapore.png"
    elif pais == "Monaco":
        path = path + "monaco.png"
    elif pais == "Austria":
        path = path + "austria.png"
    elif pais == "France":
        path = path + "france.png"
    elif pais == "Mexico":
        path = path + "mexico.png"
    elif pais == "China":
        path = path + "china.png"
    elif pais == "Russia":
        path = path + "russia.png"
    elif pais == "Belgium":
        path = path + "belgium.png"
    elif pais == "Japan":
        path = path + "japan.png"
    elif pais == "Canada":
        path = path + "canada.png"
    elif pais == "UAE":
        path = path + "abudhabi.png"
    elif pais == "Portugal":
        path = path + "portugal.png"

    return path


def getFlag(pais):
    path = "/static/img/"
    if pais == "Dutch" or pais == "Netherlands":
        path = path + "nethflag.png"
    elif pais == "British" or pais == "UK":
        path = path + "ukflag.png"
    elif pais == "Finnish" or pais == "Finland":
        path = path + "finflag.png"
    elif pais == "Deutsch" or pais == "Germany" or pais == "German":
        path = path + "gerflag.png"
    elif pais == "French" or pais == "France":
        path = path + "fraflag.png"


def change(stringz):
    # str1 = stringz.replace("utf-8", "iso-8859-1")
    str2 = stringz.replace('<?xml-stylesheet type="text/xsl" href="/schemas/mrd-1.4.xsl"?>', '')
    result = re.search('<MRData(.*)>', str2)
    str3 = str2.replace(result.group(1), '')
    return str3
