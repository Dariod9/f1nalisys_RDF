import requests


def change(string):
        x=string.replace("rdf:langString", "xsd:string")
        return x


print("Parsing txt...")
fA=open("constructors.txt", "r", encoding="utf-8")
texto=fA.read()
tmp=texto.split("\n")
novoFile=""
for t in tmp:
    if(len(t)>2):
        novoFile+=t[4:]+"\n"

lista=novoFile.split("\n")
novo=""
print("Fetching data...")
for l in lista:
    if(len(l)>2):
        response = requests.get("http://dbpedia.org/data/"+str(l)+".n3", verify=False)
        f2 = open("/home/pedralmeida/Documents/f1nalisys_RDF/f1nalisys/rdf/Constructors/"+str(l)+".n3", "w", encoding="utf-8")
        t=change(response.text)
        f2.write(t)


