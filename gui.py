def getInterruptor(listaInterruptores,coords):
    for interruptor in listaInterruptores:
        if interruptor.getCoordenadas()==coords:
            return interruptor


def pintaJuego(juegoActual,label):
    '''    
#  &#9617 LIGHT SHADE
#  &#9618 MEDIUM SHADE
#  &#9619 DARK SHADE
#  &#9608 full block
#  &#9553 dos rayas verticales
#  &#9783 3 horizontales
#  &#10495 braile 8 puntos
#  &#10346 braile 4 puntos
#  &#10032 estrella (cambia este unicode)
#  &#79" O
#  &#88" X
# &nbsp espacio en blanco
# <br/> salto de linea


    '''
    tab = juegoActual.getNivel().getMapa()
    listaInterruptores = juegoActual.getNivel().getInterruptores()
    coordsTemporales = juegoActual.getNivel().getCeldasTemporales()
    bloque=juegoActual.getEstado().getBloque()
    temporalesActivadas = juegoActual.getEstado().getTemporalesActivadas()
    

    
    
    cadenaHTML = '<FONT FACE="Courier New" SIZE=4 >'
    
    
    
    caracter=""
    block = "&#9608"
    
    hueco="&nbsp"
    suelo = "&#9618"   
    
    especial = "&#9617"
    temporal = "&#9783"
    saltoLinea = "<br/>"
    #target = "&#10032"
    target = "&#42" 
    
    
    for fila in range(len(tab)):
        for col in range(len(tab[0])):
            
            if tab[fila][col]==0:
                caracter=hueco
            elif tab[fila][col]==1:
                caracter=suelo 
            elif tab[fila][col]==2:
                caracter=especial
            elif tab[fila][col]==3:
                caracter=suelo
            else:
                caracter=target
            
            ###### pintaInterruptores
            interruptor=getInterruptor(listaInterruptores,[fila,col])
            if not interruptor == None:
                if interruptor.isSoft():
                    caracter= "&#79"
                else:
                    caracter= "&#88"
            
            
            #### pintaTemporales
            for idTemporal in temporalesActivadas:
                for celda in coordsTemporales[idTemporal]:
                    if celda ==[fila,col]:
                        caracter= temporal
                        
            ##### pintaBloque
            for celda in bloque:
                if celda ==[fila,col]:
                    caracter=block
            
                
            cadenaHTML+=caracter
        cadenaHTML+=saltoLinea
    
    cadenaHTML+="</FONT>"
    
    
    
        
    label.value=cadenaHTML
