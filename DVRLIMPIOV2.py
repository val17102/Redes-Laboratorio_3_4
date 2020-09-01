from DVRF import *
import math 
inf = math.inf 
a=[
	["a", 0,   "a"],
	["b", 2,   "b"],
	["c", 3,   "c"],
	["d", inf, "-"],
    ["e", inf, "-"],
    ["f", inf, "-"],
    ["g", inf, "-"],
    ["h", inf, "-"],
    ["i", 7,   "i"]
]
b=[
	["a", 2,   "a"],
	["b", 0,   "b"],
	["c", inf, "-"],
	["d", inf, "-"],
    ["e", inf, "-"],
    ["f", 4,   "f"],
    ["g", inf, "-"],
    ["h", inf, "-"],
    ["i", inf, "-"]
]
c=[
	["a", 3,   "a"],
	["b", inf, "-"],
	["c", 0,   "c"],
	["d", 2,   "d"],
    ["e", inf, "-"],
    ["f", inf, "-"],
    ["g", inf, "-"],
    ["h", inf, "-"],
    ["i", inf, "-"]
]
d=[
	["a", inf, "-"],
	["b", inf, "-"],
	["c", 2,   "c"],
	["d", 0,   "d"],
    ["e", 2,   "e"],
    ["f", 3,   "f"],
    ["g", inf, "-"],
    ["h", inf, "-"],
    ["i", 2,   "i"]
]
e=[
	["a", inf, "-"],
	["b", inf, "-"],
	["c", inf, "-"],
	["d", 2,   "d"],
    ["e", 0,   "e"],
    ["f", inf, "-"],
    ["g", 3,   "g"],
    ["h", inf, "-"],
    ["i", inf, "-"]
]
f=[
	["a", inf, "-"],
	["b", 4,   "b"],
	["c", inf, "-"],
	["d", 3,   "d"],
    ["e", inf, "-"],
    ["f", 0,   "f"],
    ["g", 1,   "g"],
    ["h", 1,   "h"],
    ["i", inf, "-"]
]
g=[
	["a", inf, "-"],
	["b", inf, "-"],
	["c", inf, "-"],
	["d", inf, "-"],
    ["e", 3,   "e"],
    ["f", 1,   "f"],
    ["g", 0,   "g"],
    ["h", inf, "-"],
    ["i", inf, "-"]
]
h=[
	["a", inf, "-"],
	["b", inf, "-"],
	["c", inf, "-"],
	["d", inf, "-"],
    ["e", inf, "-"],
    ["f", 1,   "f"],
    ["g", inf, "-"],
    ["h", 0,   "h"],
    ["i", inf, "-"]
]
i=[
	["a", 7,   "a"],
	["b", inf, "-"],
	["c", inf, "-"],
	["d", 2,   "d"],
    ["e", inf, "-"],
    ["f", inf, "-"],
    ["g", inf, "-"],
    ["h", inf, "-"],
    ["i", 0,   "i"]
]
##############################################################################
tablas=[a,b,c,d,e,f,g,h,i]
tablasN=["a","b","c","d","e","f","g","h","i"]
vecinos=[]
#Se conocen todos los vecinos
for i in range(len(tablas)):
    VA=EncontrarVecinos(tablas[i],tablasN[i])
    vecinos.append(VA)
print("Vecinos de nodos: ",vecinos)
# for i in range(len(vecinos)):
#     PesosVecinos(tablasN,vecinos[i])
valores=[]
for i in range(len(tablas)):#aqui iria toda la tabla de nodos
    for j in range(1):
        cv=PesosVecinos(tablasN,vecinos[i],tablas)
        valores.append(cv)
###############################################################################
for i in valores:
    print(i)
ValoresOperables=[]
for i in range(len(valores)):
    temp=[]
    for j in range(len(valores[i])):
        temp.append(valores[i][j][i])
    ValoresOperables.append(temp)
print(ValoresOperables)
#####################################################################################Comparacion de todas
print("##############")
TablaComparacion=[]
for n in range(len(valores)):
    tempo2=[]
    add=valores[n]
    # print(add)
    # print(ValoresOperables[0])
    for i in range(len(valores)):
        tempo=[]
        for j in range(len(ValoresOperables[n])):
            ba=add[j][i]+ValoresOperables[n][j]
            tempo.append(ba)
        tempo2.append(tempo)
    TablaComparacion.append(tempo2)
for i in TablaComparacion:
    print(i)
print("##############")
#########################################################################################
ff=[]
for j in range(len(TablaComparacion)):
    temp2=[]
    for i in range(len(TablaComparacion[j])):
        temp=[]
        indice=TablaComparacion[j][i].index(min(TablaComparacion[j][i]))
        letra=vecinos[j][indice]
        valor=min(TablaComparacion[j][i])
        temp.append(valor)
        temp.append(letra)
        temp2.append(temp)
    ff.append(temp2)
for i in ff:
    print(i)
##############################
for j in range(len(tablas)):
    for i in range(len(tablas[j])):
        if ff[j][i][0]<tablas[j][i][1]:
            tablas[j][i][1]=ff[j][i][0]
            tablas[j][i][2]=ff[j][i][1]
for j in range(len(tablas)):
    print("nueva tabla")
    for i in tablas[j]:
        print(i)
###################################################################Termina primera vuelta################################################
tablasN=["a","b","c","d","e","f","g","h","i"]
vecinos=[]
#Se conocen todos los vecinos
for i in range(len(tablas)):
    VA=EncontrarVecinos(tablas[i],tablasN[i])
    vecinos.append(VA)
print("Vecinos de nodos: ",vecinos)
# for i in range(len(vecinos)):
#     PesosVecinos(tablasN,vecinos[i])
valores=[]
for i in range(len(tablas)):#aqui iria toda la tabla de nodos
    for j in range(1):
        cv=PesosVecinos(tablasN,vecinos[i],tablas)
        valores.append(cv)
###############################################################################
for i in valores:
    print(i)
ValoresOperables=[]
for i in range(len(valores)):
    temp=[]
    for j in range(len(valores[i])):
        temp.append(valores[i][j][i])
    ValoresOperables.append(temp)
print(ValoresOperables)
#####################################################################################
print("##############")
TablaComparacion=[]
for n in range(len(valores)):
    tempo2=[]
    add=valores[n]
    # print(add)
    # print(ValoresOperables[0])
    for i in range(len(valores)):
        tempo=[]
        for j in range(len(ValoresOperables[n])):
            ba=add[j][i]+ValoresOperables[n][j]
            tempo.append(ba)
        tempo2.append(tempo)
    TablaComparacion.append(tempo2)
for i in TablaComparacion:
    print(i)
print("##############")
#########################################################################################
ff=[]
for j in range(len(TablaComparacion)):
    temp2=[]
    for i in range(len(TablaComparacion[j])):
        temp=[]
        indice=TablaComparacion[j][i].index(min(TablaComparacion[j][i]))
        letra=vecinos[j][indice]
        valor=min(TablaComparacion[j][i])
        temp.append(valor)
        temp.append(letra)
        temp2.append(temp)
    ff.append(temp2)
for i in ff:
    print(i)
##############################
for j in range(len(tablas)):
    for i in range(len(tablas[j])):
        if ff[j][i][0]<tablas[j][i][1]:
            tablas[j][i][1]=ff[j][i][0]
            tablas[j][i][2]=ff[j][i][1]
for j in range(len(tablas)):
    print("nueva tabla")
    for i in tablas[j]:
        print(i)