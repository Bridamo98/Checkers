f = open("resultados", "r")
total = 0
rand = 0
proy = 0
for line in f:
    total = total+1
    if line == "proyecto.py\n":
        proy = proy+1
    else:
        rand = rand+1
print("Total: "+str(total))
print("Random: "+str(rand/total*100)+"%")
print("Proyecto: "+str(proy/total*100)+"%")
