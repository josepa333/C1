"""_____________________R0_____________________"""

def fecha_es_tupla(tupla):
    """
    Entradas: Se recibe una tupla con tres valores enteros ano, mes,dia
    Salidas: Se retorna un valor booleano 
    Restricciones: Los valores de las tuplas deben ser enteros
    """
    if isinstance(tupla, tuple) and len(tupla) == 3 and tupla[1]:
        return all(isinstance(x, int) and x>0 for x in tupla)
    return False

"""_____________________R1_____________________"""
def bisiesto(anno):
    """
    Entradas: variable anno que corresponde al año a analizar
    Salidas:  Valor booleano true si el año es booleano o false en caso contrario
    Restricciones: El valor debe ser entero
    Referencia: https://es.wikibooks.org/wiki/Algoritmo_bisiesto
    """
    return anno % 4 == 0 and anno % 100 != 0 or anno % 400 == 0



"""_____________________R2_____________________"""
def fecha_es_valida(tupla):   
    """
    Entradas: Una tupla con tres valores enteros ano, mes,dia
    Salidas: Valor booleano
    Restricciones: Los valores de las tuplas deben ser enteros y seguir el formato (1998,9,13)
    """
    cantidad_dias_mes = {1:31, 2:28, 3:31, 4:31, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    anno = tupla[0]
    mes = tupla[1]
    dia = tupla[2]
    if (not fecha_es_tupla(tupla)):
        print("Error, debe ingresar una fecha de la forma año, mes, dia")
    else:
        if(anno>1000 and 0 <mes< 13):
            if(0< dia <= cantidad_dias_mes[mes]) or (mes == 2 and bisiesto(anno)and dia==29):
                return True
            else:
                return False
        else:
            return False


"""_____________________R3_____________________"""
def dia_siguiente(tupla):
    """
    Entradas: Una tupla año, mes, día formato (1998,9,13)
    Salidas: Una tupla a{o,mes,día formato (1998,9,13)
    Restricciones: Se deben igresar y retorna fechas validas
    """
    cantidad_dias_mes = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    anno = tupla[0]
    mes = tupla[1]
    dia = tupla[2]
    if(not fecha_es_tupla(tupla)):
        print("Error, debe ingresar una fecha de la forma año, mes, dia")
    else:
        if(mes == 12):
            anno +=1
            dia = 1
            mes = 1
        elif dia < cantidad_dias_mes[mes] or (mes == 2 and bisiesto(anno) and dia == 28):
            dia += 1
        else:
            mes += 1
            dia = 1
    return (anno, mes, dia)
            

"""_____________________R4_____________________"""
def dias_desde_primero_enero(tupla):
    """
    Entradas: Tupla con fecha valida (año, mes, día)
    Salidas: Entero con la suma
    Restricciones:
    """
    cantidad_dias_mes = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    anno = tupla[0]
    mes = tupla[1]
    dia = tupla[2]
    if not fecha_es_valida(tupla):
        print("Error, debe ingresar una fecha de la forma año, mes, dia")
    total_dias = 0
    """basados en la lista cantidad_dias_mes se suman los dias de cada mes"""
    for num_mes, dias_mes in cantidad_dias_mes.items():        
        if num_mes < mes:
            total_dias += dias_mes
        else:
            if bisiesto(anno) and mes > 2:
                total_dias += 1
            total_dias += dia
            return total_dias
    


"""_____________________R5_____________________"""
def dia_primero_enero(anno):
    """
    Entradas: Entero positivo correspondiente a un año.
    Salidas: El día de la semana correspondiente al primero
    de enero del año establecido como entrada, con la siguiente
    codificación: 0 = domingo, 1 = lunes, 2 = martes, 3 = miércoles,
    4 = jueves, 5 = viernes, 6 = sábado.
    Restricciones: El año recibido como entrada debe encontrarse entre 1581 y
    9999, el resultado de la función es un número entero.
    """
    if (anno > 1581 and anno < 9999):
            anno -= 1
            temp = anno + anno//4 - anno//100 + anno//400 + 37
            dia = temp % 7
            if dia == 0:
                return 6
            else:
                return dia - 1
    return False

  

"""_____________________R6_____________________"""
def imprimir_3x4(anno):
    """
    Entradas: Entero positivo correspondiente a un año.
    Salidas: Se despliega en consola el calendario del año
    indicado en formato de 3 secuencias (‘filas’) de 4 meses
    cada una.
    Restricciones: El año recibido como entrada debe encontrarse entre 1581 y
    9999, el resultado de la función es impreso en consolas.
    """
    if (anno > 1581 and anno < 9999):
        listaMeses = ["Enero","Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]
        listaDias = ["D", "L", "M", "K", "J", "V", "S"]
        meses = crear_calendario(anno)
        mesActual = 0
        mesLegit = 0
        semanaActual = 0
        mesAux = mesActual
        print("Calendario del año " + str(anno) + " D.C")
        while mesActual < 12:
            diaActual = 0
            contador = 0
            mesAux = mesActual
            while contador < 4:
                print('{:^35s}'.format(listaMeses[mesActual]), end="|")
                mesActual += 1
                contador += 1
            contador = 0
            print()
            while contador < 4:
                while diaActual < 7:
                    print('{:^5s}'.format(listaDias[diaActual]), end="")
                    diaActual += 1
                print("|", end="")
                diaActual = 0
                contador += 1
            print()
            contador = 0
            mesActual = mesAux
            while semanaActual < 6:
                while contador < 4:
                    while diaActual < 7:
                        print('{:^5s}'.format(meses[mesActual][semanaActual][diaActual]),  end = "")
                        diaActual += 1
                    diaActual = 0
                    print("|", end = "")
                    contador += 1
                    mesActual += 1
                mesActual = mesAux
                semanaActual += 1
                contador = 0
                print()
            mesActual = mesAux + 4
            semanaActual = 0
            print()       
    else:
        return False

""" Esta función es auxiliar para la impresión del calendario"""
def crear_calendario(anno):
    """
    Entradas: Entero positivo correspondiente a un año.
    Salidas: Retorna una lista de matrices correspondiete al calendario
    del anno dado.
    Restricciones: El año recibido como entrada debe encontrarse entre 1581 y
    9999, el resultado de la función es una lista de matrices.
    """
    meses = []
    diasMeses = [31,28,31,30,31,30,31,31,30,31,30,31]
    if bisiesto(anno):
        diasMeses[1] = 29
    inicio = dia_primero_enero(anno)
    for i in range(12):
        mes = [[" " for x in range(7)] for y in range(6)]
        dia = 1
        fila = 0
        columna = inicio
        while dia <= diasMeses[i]:
            mes[fila][columna] = str(dia)
            dia += 1
            columna = (columna + 1) % 7
            if columna == 0:
                fila += 1
        inicio = columna
        meses.append(mes)
    return meses