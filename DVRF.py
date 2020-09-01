import math 
inf = math.inf 

Venicinos=[]
def EncontrarVecinos(nodo,nombreNodo):
    Venicinos=[]
    for i in range(len(nodo)):
        tempo=nodo[i][1]
        if tempo< inf:
            Venicinos.append(nodo[i][0])
    Venicinos.remove(nombreNodo)
    return Venicinos
#####################################################
letras=["a","b","c","d","e","f","g","h","i"]
CostoIndividual=[]
TablaCostosA=[]
ValoresOperables=[]
def PesosVecinos(tablasN,vecinos,nodo):
    CostoIndividual=[]  
    TablaCostosA=[]
    ValoresOperables=[]
    for i in tablasN:
        if i in vecinos:
            # print(i)
            tablasN.index(i)
            for j in range(len(nodo[tablasN.index(i)])):
                CostoIndividual.append(nodo[tablasN.index(i)][j][1])
            TablaCostosA.append(CostoIndividual)
            CostoIndividual=[]
    return TablaCostosA