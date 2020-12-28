consRes= open("status.csv","r", encoding='iso-8859-1')
linhas = consRes.read()
linhas = linhas.split("\n")
cabe=linhas[0]+"\n"
linhas.remove(linhas[0])

for l in linhas:
    if len(l)<2:
        break
    dados=l.split(",")
    dados[0]="statusID"+dados[0]
    linhaNova=""
    for d in dados:
        linhaNova+=d+","
    
    linhaNova=linhaNova[:-1]
    cabe+=linhaNova+"\n"

wr= open("status.csv", "w", encoding='iso-8859-1')
wr.write(cabe)