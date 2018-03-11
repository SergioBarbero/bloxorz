import functools
import itertools

from os import listdir
from os.path import isfile, join

from ModeloMueve import Interruptor, Estado, Nivel, Juego

def getAllLevels():
    mypath='levels/'
    onlyfiles = [f for f in listdir(mypath) if f.startswith('level') and f.endswith('.txt') and isfile(join(mypath, f))]
    onlyfiles.sort()
    return onlyfiles



def getCodigoMapa(caracter):
    '''
    Devuelve el código de mapa asociado a cada caracter.
    '''    
    codigo = 0
    if caracter == 'o':
        codigo = 1        
    elif caracter == '.':
        codigo = 2
    elif caracter == 'S':
        codigo = 3
    elif caracter == 'T':
        codigo = 4
    elif caracter.isupper():
        codigo= 1 #los interruptores
    return codigo

def esCeldaTemporal(caracter):
    '''
    Devuelve True si el caracter representa una celda temporal.
    '''
    if caracter.islower() and caracter != 'o':
        return True
    else:
        return False
    

def esInterruptor(caracter):
    '''
    Devuelve True si el caracter representa un interruptor.
    '''
    if caracter.isupper() and caracter not in set(['S','T']):
        return True
    else:
        return False
    
    
def creaInterruptor(stringInterruptor,posTable):
    '''
    Crea un interruptor a partir de la cadena que lo define.
    '''
    idInt = stringInterruptor[1]
    idTipo = stringInterruptor[2]
    coord = posTable[idInt]
    tipo = False
    
    pon=''
    quita=''
    
    if idTipo == 'O':
        tipo = True
    if len(stringInterruptor) == 5:
        pon = stringInterruptor[3]
        quita = stringInterruptor[3]
    elif stringInterruptor[3] == '-':
        quita = stringInterruptor[4]
    else:
        pon = stringInterruptor[4]
    
    
    return Interruptor(coord,tipo,pon,quita)
        
    

def getJuego(filename):
    '''
    Obtiene un juego a partir del archivo que lo codifica
    '''
    
    archivo = open(filename,'r')
    lineas = archivo.readlines()
    interruptores = []
    celdasTemporales ={}
    posicionesInterruptores ={}


    noMapa = set(['#','%'])
    ancho=functools.reduce(max,map(len,lineas))-1


    mapa = []
    bloque =[]
    celdasTemporalesIniciales = set([])



    nFila=0
    for linea in lineas:

        if not linea[0] in noMapa:
            fila = list(itertools.repeat(0, ancho))

            nCol = 0
            for ch in linea:
                if ch =='\n':
                    break

                codigo = getCodigoMapa(ch)
                fila[nCol] = codigo

                if codigo == 3:
                    bloque = [[nFila,nCol]]

                if esCeldaTemporal(ch):
                    if ch not in celdasTemporales:
                        celdasTemporales[ch]=[[nFila,nCol]]
                    else:
                        celdasTemporales[ch].append([nFila,nCol]) 

                elif esInterruptor(ch):
                    posicionesInterruptores[ch]=[nFila,nCol]

                nCol+=1

            mapa.append(fila)
            nFila+=1


        else:        
            ch = linea[0] 
            if ch == '%':
                celdasTemporalesIniciales.add(linea[1])
            if ch == '#':
                interruptores.append(creaInterruptor(linea,posicionesInterruptores))




    est = Estado(bloque,celdasTemporalesIniciales)
    level = Nivel(mapa,interruptores,celdasTemporales)
    juego = Juego(level,est)
    return juego
    
