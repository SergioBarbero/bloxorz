class Interruptor:
    '''
    Clase que representa un interruptor.
    '''
    def __init__(self,coords,tipoInterruptor,pon,quita):
        '''
        Constructor interruptor.
        '''
        self.coords = coords
        self.tipoInterruptor = tipoInterruptor
        self.pon = pon
        self.quita = quita
        
    def getCoordenadas(self):
        '''
        Obtiene las coordenadas de un interruptor.
        '''
        return self.coords
    
    def isSoft(self):
        '''
        Obtiene True si el interruptor es soft.
        
        Un interruptor es soft si se activa al tocarlo
        '''
        return self.tipoInterruptor
    
    def getQuita(self):
        '''
        Obtiene el id de las celdas temporales que se desactivan al accionar el interruptor.
        '''
        return self.quita
    
    def getPon(self):
        '''
        Obtiene el id de las celdas temporales que se activan al accionar el interruptor.
        '''
        return self.pon
    
        
    def __str__(self):
        return " "+str(self.coords)+" "+str(self.tipoInterruptor)+" pon "+self.pon+" quita "+self.quita
    
    def __repr__(self):
        return " "+str(self.coords)+" "+str(self.tipoInterruptor)+" pon "+self.pon+" quita "+self.quita




class Estado:
    '''
    Clase que representa un Estado de Bloxorz.
    '''
    def __init__(self,bloque,temporales):
        '''
        Constructor del Estado.
        '''
        self.bloque = bloque
        self.temporales = temporales
    
    def getBloque(self):
        '''
        Obtiene el bloque.
        '''
        return self.bloque
    
    def setBloque(self,bloque):
        '''
        Establece el bloque.
        '''
        self.bloque=bloque
        
    def getTemporalesActivadas(self):
        '''
        Obtiene las temporales activadas.
        '''
        
        return self.temporales
    
    def setTemporalesActivadas(self,temporales):
        '''
        Establece las temporales activadas.
        '''
        self.temporales=temporales
    
    
    def __str__(self):
        return " "+str(self.bloque)+" "+str(self.temporales)
    
    def __eq__(self, other):
        
        b1=self.getBloque()
        b2=other.getBloque()
        ta1 = frozenset(self.getTemporalesActivadas())
        ta2 = frozenset(other.getTemporalesActivadas())
        
        b1.sort()
        b2.sort()

        return b1 == b2 and ta1==ta2
    
    
    def __hash__(self):
        
        tmp = []

        for i in self.getBloque():
            tmp.append(tuple(i))
        tmp.sort()
        hashableBlock=tuple(tmp)
        
        return hash((hashableBlock, frozenset(self.getTemporalesActivadas())))
        


class Nivel:
    '''
    Clase que representa un nivel de Bloxorz.
    '''
    def __init__(self,mapa,interruptores,celdasTemporales):
        '''
        Constructor del Nivel.
        '''
        self.mapa = mapa
        self.interruptores = interruptores
        self.dictTemp=celdasTemporales
        
    def getMapa(self):
        '''
        Obtiene el mapa.
        '''
        return self.mapa
    
    def getInterruptores(self):
        '''
        Obtiene la lista de interruptores.
        '''
        return self.interruptores
    
    def getCeldasTemporales(self):
        '''
        Obtiene el diccionario de celdas temporales.
        
        La clave es el id, el valor la lista de celdas asociadas a ese id
        '''
        return self.dictTemp
        
    def __str__(self):
        interruptoresStr=""
        for i in self.interruptores:
            interruptoresStr+=str(i)+"\n"
        mapaStr=""
        for i in self.mapa:
            mapaStr+=str(i)+"\n"
    
        return mapaStr+"\n"+interruptoresStr+str(self.dictTemp)

    
class Juego:
    '''
    Clase que define un juego de Bloxorz.
    '''
    def __init__(self,nivel,estado):
        '''
        Constructor del Juego.
        '''
        self.nivel=nivel
        self.estado=estado
        
    def getNivel(self):
        '''
        Obtiene el Nivel.
        '''
        return self.nivel
    
    def getEstado(self):
        '''
        Obtiene el estado.
        '''
        return self.estado
    
    def setEstado(self,estado):
        '''
        Modifica el estado.
        '''
        self.estado=estado
        
    def __str__(self):
        return "Nivel \n"+str(self.nivel)+"\n\nEstado\n"+str(self.estado)


        
def getCoordenadasMeta(mapa):
    '''
    Devuelve las coordenadas de la meta.
    '''
    alto = len(mapa)
    ancho = len(mapa[0])
    
    for i in range(alto):
        for j in range(ancho):
            if mapa[i][j]==4:
                return [i,j]
                
def mueve(estado,nivel,mov):
    '''
    Modifica el estado como resultado de empujar el bloque.
    '''
    bloque = estado.getBloque()
    tempAct = estado.getTemporalesActivadas()
    posNueva=[]

    temporales = nivel.getCeldasTemporales()

    #Calculamos las nuevas posiciones del bloque tras el movimiento
    rueda1=list(map(lambda x, y : x + y,bloque[0],mov))
    if estaTumbado(bloque):
        rueda2=list(map(lambda x, y : x + y,bloque[1],mov))
        if rueda1==bloque[1]:
            posNueva=[rueda2]
        elif rueda2==bloque[0]:
            posNueva=[rueda1]
        else:
            posNueva=[rueda1, rueda2]
    else:
        posNueva=[rueda1, list(map(lambda x, y : x + y,rueda1, mov))]
        
    nuevoSet = set(tempAct)    
    nuevoEstado = Estado(posNueva,nuevoSet)
    
    #Comprueba si nuestro nuevo bloque está dentro de límites o encima de una casilla temporal
    if estaDentro(nuevoEstado, nivel):
        indice = activoInterruptor(posNueva, nivel)
        
        #Si esta dentro de limites comprobamos si esta activando un interruptor
        if indice != -1:
            interruptor = nivel.getInterruptores()[indice]
            temporales = activarTemporales(interruptor, estado)
            nuevoEstado.setTemporalesActivadas(temporales)
        
        return nuevoEstado
    else:
        return estado
    
def activarTemporales(interruptor, estado):
    '''
    Devuelve diccionario de todas las temporales mas o menos las que activamos o desactivamos ahora, respectivamente
    '''
    temporales = estado.getTemporalesActivadas()
    pon = interruptor.getPon()
    quita = interruptor.getQuita()

    if(pon in temporales or pon == ''):
        temporales.discard(quita)
    else:
        temporales.add(pon)
    return temporales
    
    
def activoInterruptor(bloque, nivel):
    '''
    Devuelve indice de la lista de interruptores del interruptor que estoy activando, funciona tanto para soft switches como hard switches,
    en el caso de que no esté activando interruptor devuelve -1
    '''
    interruptores = nivel.getInterruptores()
    #En el caso de que la lista de interruptores este vacia (no hay interruptores en el mapa)
    if not interruptores:
        return -1

    rueda1=bloque[0]
    if estaTumbado(bloque):
        rueda2=bloque[1]
    else:
        rueda2=[-1 -1]
    
    max = list(range(len(interruptores)))
    for i in max:
        if rueda1 == interruptores[i].getCoordenadas() or rueda2 == interruptores[i].getCoordenadas():
            if (estaTumbado(bloque) and interruptores[i].isSoft()) or not estaTumbado(bloque):
                return i
                
    return -1

def estaDentro(estado, nivel):
    '''
    Devuelve true si el bloque está dentro de límites o pisando una temporal que esté activada, si no devuelve false
    '''
    mapa = nivel.getMapa()
    rueda1=estado.getBloque()[0]
    temporales=estado.getTemporalesActivadas()
   
    dentro1 = coordDentro(rueda1, nivel) and not esHueco(rueda1, nivel)
    temp1 = hayTempActivada(rueda1, estado, nivel)
    if estaTumbado(estado.getBloque()):
        rueda2 = estado.getBloque()[1]
        temp2 = hayTempActivada(rueda2, estado, nivel)
        dentro2 = coordDentro(rueda2, nivel) and not esHueco(rueda2, nivel)
        
        #Si ambas partes del bloque estan dentro de limites
        if dentro1 and dentro2:
            return True
        #Si una parte del bloque esta dentro del limite y otra en una temporal
        elif (dentro1 or dentro2) and (temp1 or temp2):
            return True
        #Si ambas partes del bloque estan en temporales
        elif (temp1 and temp2):
            return True
    else: 
        #Si el bloque esta en limites o temporales
        if dentro1 or temp1:
            return True
    return False

def coordDentro(coord, nivel):
    '''
    solo mira si una coordenada esta dentro de los limites
    '''
    mapa = nivel.getMapa();
    #Si nuestra coordenada esta dentro del mapa
    if(len(mapa) > coord[0] and len(mapa[0]) > coord[1] and enLimites(coord)):
        return True
    else:
        return False
    
def esHueco(coord, nivel):
    '''
    solo mira si en una coordenada hay un cero
    '''
    mapa = nivel.getMapa();

    if (mapa[coord[0]][coord[1]] == 0):
        return True
    else:
        return False

def hayTempActivada(coord, estado, nivel):
    '''
    solo mira si en una coordenada hay una temporal activada
    '''
    ta = estado.getTemporalesActivadas()
    ct = nivel.getCeldasTemporales()
    for tmp in ta:
        max = list(range(len(ct[tmp])))
        for index in max:
            if (ct[tmp][index] == coord):
                return True
    
    return False


def estaTumbado(bloque):
    '''
    Devuelve true si el bloque esta tumbado, si esta de pie devuelve false
    '''
    if len(bloque)==1:
        return False
    else:
        return True
    
    
def esMeta(estado,nivel):
    '''
    Devuelve True si el estado es Meta.
    '''
    bloque = estado.getBloque()
    mapa = nivel.getMapa()
    
    if len(bloque)==1 and mapa[bloque[0][0]][bloque[0][1]]==4:
        return True
    else:
        return False

def enLimites(coord):
    '''
    Comprueba que no haya componentes negativas en una coordenada
    '''
    for i in [0, 1]:
        if coord[i] < 0:
            return False
    return True
  