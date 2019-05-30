import random as rand
import time
from copy import deepcopy

vComida=2
vCCoronada=3
vCoronar=4

BLANCO='-'
TOT=0
J1={
    'pieces':'xX',
    'adversary':'oO',
    'crown':7,
    'direction':{
        'x':[(1,1),(1,-1)],
        'X':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}

J2={
    'pieces':'oO',
    'adversary':'xX',
    'crown':0,
    'direction':{
        'o':[(-1,1),(-1,-1)],
        'O':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}
J={
    'pieces':'xX',
    'adversary':'oO',
    'crown':7,
    'direction':{
        'x':[(1,1),(1,-1)],
        'X':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}

def recmov(tablero,J,i,j):
    R=[]
    T=[]
    for dir in J['direction'][tablero[i][j]]:
        i_=i+2*dir[0]
        j_=j+2*dir[1]
        if i_ in range(8) and j_ in range(8) and tablero[i+dir[0]][j+dir[1]] in J['adversary'] and tablero[i_][j_]==BLANCO:
            T=recmov(makeMove(tablero,[(i,j),(i_,j_)],J),J,i_,j_)
            for k in range(len(T)):
                T[k]=[(i,j)]+T[k]
            R=R+T
    if len(R)==0:
        return [[(i,j)]]
    return R

def makeMove(tablero,m,J):
    E=[[tablero[i][j] for j in range(8)]for i in range(8)]
    if not (m is None):
        for i in range(1,len(m)):
            E[m[i][0]][m[i][1]]=E[m[i-1][0]][m[i-1][1]]
            E[m[i-1][0]][m[i-1][1]]=BLANCO
            if abs(m[i-1][0]-m[i][0])>1:
                x=int((m[i-1][0]+m[i][0])/2)
                y=int((m[i-1][1]+m[i][1])/2)
                E[x][y]=BLANCO
            if m[i][0]==J['crown']:
                E[m[i][0]][m[i][1]]=J['pieces'][1]

    return E

def moves(tablero,J):
    M=[]
    take=False
    for i in range(8):
        for j in range(8):
            if tablero[i][j] in J['pieces']:
                T=recmov(tablero,J,i,j)
                if len(T[0])>1:
                    take=True
                    M=M+T
    if not take:
        for i in range(8):
            for j in range(8):
                if tablero[i][j] in J['pieces']:
                    for dir in J['direction'][tablero[i][j]]:
                        if i+dir[0] in range(8) and j+dir[1] in range(8) and tablero[i+dir[0]][j+dir[1]]==BLANCO:
                            M=M+[[(i,j),(i+dir[0],j+dir[1])]]
    return M
##Funcion que evalua cuantas fichas amigas tiene cerca y retorna una puntuacion de prioridad
def near(mov,T):
    ficha=T[i][j]
    tot=0
    if(T[i+1][j+1]==ficha):
        tot+=1
    if(T[i-1][j-1]==ficha):
        tot+=1
    if(T[i-1][j+1]==ficha):
        tot+=1
    if(T[i+1][j-1]==ficha):
        tot+=1
    return tot
#end def

def tail(mov,T):
    m=mov[0]
    print("primera jugada",m)
    i=m[0]
    j=m[1]
    if(T[i][j] in J1['pieces'] and i==0):
        return -1
    #end if
    if(T[i][j] in J2['pieces'] and i==7):
        return -1
    #end if
    return 0
#end def

def chip_majority(T):
    sx,so= 0,0
    for i in range(8):
        for j in range (8):
            if(T[i][j] in J1['pieces']):
                sx+=1
            if(T[i][j] in J2['pieces']):
                so+=1
    if(so>sx):
        if('o' in J['pieces']): return 1
        else: return -1
    if(sx>so):
        if('x' in J['pieces']):
            return 1
        else: return -1
    #end if
    return 0
#end def

def feed(mov, tablero):
    cuenta = 0
    for i in range(len(mov)-1):
        jugada = mov[i]
        siguiente = mov[i+1]
        if abs(jugada[0]-siguiente[0]) != 1:
            if siguiente[0]-jugada[0] > 0:
                if siguiente[1]-jugada[1] > 0:
                    if tablero[jugada[0]+1][jugada[1]+1] == "O" or tablero[jugada[0]+1][jugada[1]+1] == "X":
                        cuenta = cuenta + 3
                    else:
                        cuenta = cuenta + 2
                else:
                    if tablero[jugada[0]+1][jugada[1]-1] == "O" or tablero[jugada[0]+1][jugada[1]-1] == "X":
                        cuenta = cuenta+3
                    else:
                        cuenta = cuenta+2
            else:
                if siguiente[1]-jugada[1] > 0:
                    if tablero[jugada[0]-1][jugada[1]+1] == "O" or tablero[jugada[0]-1][jugada[1]+1] == "X":
                        cuenta = cuenta + 3
                    else:
                        cuenta = cuenta + 2
                else:
                    if tablero[jugada[0]-1][jugada[1]-1] == "O" or tablero[jugada[0]-1][jugada[1]-1] == "X":
                        cuenta = cuenta+3
                    else:
                        cuenta = cuenta+2
    return cuenta
# end_def


def crown(mov, J, tablero):
    actual = mov[0]
    x = actual[0]
    y = actual[1]
    if J in J1['pieces']:
        if mov[len(mov)-1][1] == 7 and tablero[x][y] != "X":
            return vCoronar
        else:
            return 0
    else:
        if mov[len(mov)-1][1] == 0 and tablero[x][y] != "O":
            return vCoronar
        else:
            return 0
#end_def

def block(mov, tablero):
    ultimoMov = mov[len(mov)-1]
    #print("ultimoMov:",ultimoMov)
    penultimoMov = mov[len(mov)-2]
    #print("penultimoMov:",penultimoMov)
    miFicha = tablero[mov[0][0]][mov[0][1]]
    #print("MI FICHA ES:",miFicha)
    #print(mov)
    resultado=0
    estadoLateral = 4 #{-1=ocupadoPorRival, 0=desprotegido,1=respaldo,2=amenaza,3=amenazaReina,4=vacio}
    estadoDiagonal = 4
    estadoSuperior = 4
    for i in range(-1,2):
        ii=ultimoMov[0]+i
        #print("ii",ii)
        for j in range(-1,2):
            jj=ultimoMov[1]+j
            #print("jj",jj)
            if ii in range(0,8) and jj in range(0,8) and j!=0 and i!=0 and ii!=penultimoMov[0] and jj!=penultimoMov[1] and (jj+j) in range(0,8) and (ii+i) in range(0,8):
                if(ii == penultimoMov[0]):
                    if(tablero[ii][jj] == miFicha or tablero[ii][jj].upper()==miFicha):
                        if(tablero[ii+i][jj+j].isupper()):
                            if(tablero[ii+i][jj+j].lower()!=miFicha):
                                estadoLateral=3
                            else:
                                estadoLateral=1
                            #endif
                        else:
                            if(tablero[ii+i][jj+j]=="-"):
                                estadoLateral=0
                            elif(tablero[ii+i][jj+j]==miFicha):
                                estadoLateral=1
                            else:
                                estadoLateral=2
                            #endif
                        #end if
                    #end if
                elif(tablero[ii][jj]!="-"):
                    estadoLateral=-1
                #endif
                if(ii == penultimoMov[0]):
                    if(tablero[ii][jj] == miFicha or tablero[ii][jj].upper()==miFicha):
                        if(tablero[ii+i][jj+j].isupper()):
                            if(tablero[ii+i][jj+j].lower()!=miFicha):
                                estadoSuperior=3
                            else:
                                estadoSuperior=1
                            #endif
                        else:
                            if(tablero[ii+i][jj+j]=="-"):
                                estadoSuperior=0
                            elif(tablero[ii+i][jj+j]==miFicha):
                                estadoSuperior=1
                            else:
                                estadoSuperior=2
                            #endif
                        #end if
                    #end if
                elif(tablero[ii][jj]!="-"):
                    estadoSuperior=-1
                #endif
                if(ii == penultimoMov[0]):
                    if(tablero[ii][jj] == miFicha or tablero[ii][jj].upper()==miFicha):
                        if(tablero[ii+i][jj+j].isupper()):
                            if(tablero[ii+i][jj+j].lower()!=miFicha):
                                estadoDiagonal=3
                            else:
                                estadoDiagonal=1
                            #endif
                        else:
                            if(tablero[ii+i][jj+j]=="-"):
                                estadoDiagonal=0
                            elif(tablero[ii+i][jj+j]==miFicha):
                                estadoDiagonal=1
                            else:
                                estadoDiagonal=2
                            #endif
                        #end if
                    #end if
                elif(tablero[ii][jj]!="-"):
                    estadoLateral=-1
                #endif
            #endif
        #endfor
    #end for
    if(estadoDiagonal==-1 or estadoSuperior==-1):
        return -2
    #end if
    if((estadoLateral==3 or estadoSuperior==3 or estadoDiagonal==3) and (estadoLateral==0 or estadoSuperior==0 or estadoDiagonal==0)):
        return 4
    #end if
    if(estadoDiagonal==2 or estadoDiagonal==3 or estadoSuperior==2 or estadoDiagonal==3):
        resultado+=2
        if(estadoLateral==0):
            resultado+=2
        #end if
    #end if
    return resultado
#end def

T=[
['x','-','x','-','x','-','x','-'],
['-','x','-','x','-','x','-','x'],
['x','-','-','-','-','-','x','-'],
['-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-'],
['-','-','-','o','-','o','-','o'],
['o','-','o','-','o','-','o','-'],
['-','o','-','o','-','o','-','o']
]

def player(E, J):
    jj = None
    M = []
    cuenta = []
    if J in J1['pieces']:
        M = moves(E, J1)
    elif J in J2['pieces']:
        M = moves(E, J2)
    if len(M) == 0:
        return None
    M_sorted = deepcopy(M)
    M_sorted = sorted(M_sorted, key=lambda ele: tail(ele, E)+block(ele,E)+crown(ele,J,E)+feed(ele,E), reverse=True)
    if M_sorted[0] <= 0:
        return rand.choice(M)
    else:
        return M_sorted[0]