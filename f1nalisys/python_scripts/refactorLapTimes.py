consRes= open("results.csv","r")
linhas = consRes.read()
linhas = linhas.split("\n")
cabe=linhas[0]+"\n"
linhas.remove(linhas[0])

for l in linhas:
    if len(l)<2:
        break
    dados=l.split(",")
    dados[0]="resultID"+dados[0]
    dados[1]="raceID"+dados[1]
    dados[2]="driverID"+dados[2]
    dados[3]="consID"+dados[3]

    linhaNova=""
    for d in dados:
        linhaNova+=d+","
    
    linhaNova=linhaNova[:-1]
    cabe+=linhaNova+"\n"

wr= open("results.csv", "w")
wr.write(cabe)