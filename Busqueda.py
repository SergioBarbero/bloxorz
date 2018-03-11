import queue as queue


class Nodo:
    
    def __init__(self,estado,padre,g,f):
        self.estado=estado
        self.padre=padre
        self.g = g
        self.f = f
    def getPadre(self):
        return self.padre
    def getEstado(self):
        return self.estado
    def getG(self):
        return self.g
    def getF(self):
        return self.f
    
    def camino(self): 
        "Create a list of nodes from the root to this node."
        
        # quiero camino de nodos o camino de estados?
        # append(x.getEstado) o append(x)
        x = self
        result =  []
        while x:
            result.append(x.getEstado())
            x = x.getPadre()
        return list(reversed(result))
    
    def __repr__(self):
        return "Nodo "+str(self.estado)+"("+str(self.f)+")"
    
    def __lt__(self, other):
        return self.f<other.f
        

    def __eq__(self, other):
        
        return self.getEstado()==other.getEstado()
        
        
class Abiertos():
    def __init__(self):
        self.colaPrioridad = queue.PriorityQueue()
    
    def put(self,nodo):
        self.colaPrioridad.put((nodo.getF(),nodo))
    
    def pop(self):
        return self.colaPrioridad.get()
    
    def empty(self):
        return self.colaPrioridad.empty();
    
    def getNodo(self,estado):
        for elem in self.colaPrioridad.queue:
            if elem[1].getEstado()==estado:
                return elem[1]
        return None           
    
    
    def update(self,nodoViejo,nodoNuevo):
        self.colaPrioridad.queue.remove((nodoViejo.getF(),nodoViejo))
        self.colaPrioridad.put((nodoNuevo.getF(),nodoNuevo))
        
    def getNodes(self):
        return list(map(lambda x:x[1],self.colaPrioridad.queue))
    
    def __str__(self):
        return str(self.colaPrioridad.queue)
        
        
def AStar(inicial, sucesoresF, metaF, heuristicoF):
    abiertos=Abiertos()
    abiertos.put(inicial)
    cerrados={}
    
    while not abiertos.empty():
        """creo abiertos y cerrados.\n
            abiertos se inicializa con el nodo inicial.\n
            cerrados estará vacía\n"
            \n
            mientras abiertos no esté vacía:\n
                recupero de abiertos el nodo con menor f (nodoActual).\n
                guardo nodoActual en cerrados.\n
                compruebo si es meta:\n
                    si lo es devuelve el camino\n
                obtengo los sucesores\n
                para suc en sucesores:\n
                    si no está en abiertos ni en cerrados \n
                        lo meto en abiertos\n
                    está en abiertos pero suc tiene menor f\n
                        lo actualizo en abiertos\n"
                    esta en cerrados pero suc tiene menor f\n
                       lo elimino de cerrados y lo meto en abiertos
            devuelvo [], no había solución"""
        
        f,actual = abiertos.pop()

        cerrados[actual.getEstado()] = actual
        
        sucesores = sucesoresF(actual)
        if metaF(actual.getEstado()):
            return actual.camino()
            sucesores=sucesoresF(actual)
        
        for suc in sucesores:
            if abiertos.getNodo(suc.getEstado()) is None and cerrados.get(suc.getEstado()) is None:
                abiertos.put(suc)
            elif not abiertos.getNodo(suc.getEstado()) is None and abiertos.getNodo(suc.getEstado()).getF() > suc.getF():
                abiertos.update(abiertos.getNodo(suc.getEstado()), suc)
            elif cerrados.get(suc.getEstado()) is suc and cerrados[suc.getEstado()].getF() > suc.getF():
                del cerrados[suc.getEstado()]
                abiertos.put(suc)
            
    return []
