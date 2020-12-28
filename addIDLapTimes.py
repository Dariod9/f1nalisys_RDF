consRes= open("lapTimes.csv","r")
linhas = consRes.read()
linhas = linhas.split("\n")
cabe=linhas[0]+"\n"
linhas.remove(linhas[0])
cont=1

for l in linhas:
    if len(l)<2:
        break

    linhaNova="lapID"+str(cont)+","
    
    linhaNova=linhaNova+l
    cabe+=linhaNova+"\n"
    cont+=1

wr= open("lapTimes.csv", "w")
wr.write(cabe)