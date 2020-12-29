from rdflib import Graph

g = Graph()

g.parse('f1.rdf')

for index, (s, p, o) in enumerate(g):
    print(s, p, o)
    if index == 10:
        break

print(g.serialize(destination="f1.n3", format="rdf"))