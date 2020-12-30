import requests
import os
import json
import codecs

def change(string):
        x=string.replace("rdf:langString", "xsd:string")
        return x

ar = os.listdir('/Users/ruisantos/Desktop/ano4/edc/project/f1nalisys_RDF/f1nalisys/rdf/drivers2')
print(ar)
cont = 0
f2 = open("/Users/ruisantos/Desktop/ano4/edc/project/f1nalisys_RDF/f1nalisys/rdf/drivers.txt", "w", encoding="utf-8")
for f in ar:
    fA=codecs.open('/Users/ruisantos/Desktop/ano4/edc/project/f1nalisys_RDF/f1nalisys/rdf/drivers2/'+f, "r", encoding="utf-8", errors='ignore')
    texto=fA.read()
    tmp=texto.split("\n")
    novoFile=""
    f3 = open("/Users/ruisantos/Desktop/ano4/edc/project/f1nalisys_RDF/f1nalisys/rdf/drivers.txt", "r", encoding="utf-8")
    for t in tmp:
        if('	dct:subject' in t):
            t = t.split('	dct:subject')[0]
            texto=f3.read()
            if not t in texto and not "<" in t:
                f2.write(t+"\n")
                cont+=1
print(str(cont))


