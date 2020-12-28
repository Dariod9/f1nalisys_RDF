def check(palavra):
    if "http" in palavra:
        return "<"+palavra+">"
    else:
        #return "\""+palavra+"\""
        return palavra


def convert(ficheiro,id):
    linhas=ficheiro.read()
    linhas=linhas.split("\n")
    preds=linhas[0]
    predicados=preds.split(",")

    linhas.remove(linhas[0])
    triplos=""

    for linha in linhas:
        dados=linha.split(",")

        if len(dados)>9:                        #CASO O URL CONTENHA UMA VIRGULA VAI FAZER 2 "OBJETOS", ESTE IF JUNTA-OS DE VOLTA NUM SÓ 
            if "http" in dados[8]:
                dados[8]=dados[8]+dados[9]
                dados.remove(dados[9])

        sujeito=dados[id]
        #dados.remove(dados[1])

        for idx, val in enumerate(dados):
            # print("Obj" + val)
            # print("numero:")
            # print(dados[idx])
            # print(predicados[idx]+"\n")
            pred=predicados[idx]
            if val == "":
                continue
            else:
                triplos+=check(sujeito)+","+check(pred)+","+check(val)+" .\n"

    return triplos

circuitos = open("circuits.csv","r")
circuitosW = open("circuit_triples.csv", "w")
circuitosW.write(convert(circuitos,0))

status = open("status.csv","r")
statusW = open("status_triples.csv", "w")
statusW.write(convert(status,0))


drivers = open("drivers.csv","r", encoding='iso-8859-1')
driversW = open("drivers_triples.csv","w", encoding='iso-8859-1')
driversW.write(convert(drivers,0))

cons = open("constructors.csv","r", encoding='utf-8')
consW = open("constructors_triples.csv","w", encoding='utf-8')
consW.write(convert(cons,0))

race = open("races.csv","r", encoding='utf-8')
raceW = open("races_triples.csv","w", encoding='utf-8')
raceW.write(convert(race,0))
