import requests

def change(string):
        x=string.replace("rdf:langString", "xsd:string")
        return x

fA=open("/Users/ruisantos/Desktop/ano4/edc/project/f1nalisys_RDF/f1nalisys/rdf/drivers_by_team.txt", "r", encoding="utf-8")
texto=fA.read()
tmp=texto.split("\n")
novoFile=""
for t in tmp:
    if(len(t)>2):
        novoFile+=t+"\n"
        

#f = open("circuitos.txt", "r", encoding="utf-8")
#a=f.read()
lista=novoFile.split("\n")
novo=""
for l in lista:
    if(len(l)>2):
        response = requests.get("http://dbpedia.org/data/Category:"+str(l)+".n3", verify=False)
        f2 = open("/Users/ruisantos/Desktop/ano4/edc/project/f1nalisys_RDF/f1nalisys/rdf/drivers_by_team/"+str(l)+".n3", "w", encoding="utf-8")
        t=change(response.text)
        f2.write(t)


