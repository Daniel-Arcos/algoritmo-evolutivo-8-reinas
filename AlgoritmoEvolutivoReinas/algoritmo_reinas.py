import random
import matplotlib.pyplot as plt

# En la terminal de VS Code: python -m pip install matplotlib

'''Clase utilizada para modelar cada tablero
Representacion: hace referencia a la matriz compuesta de 0 y 1
Valor funcion: es el valor de funcion de aptitud para el tablero mencionado,
es decir, el numero de ataques existentes'''
class Tablero:
    def __init__(self, tablero, valor) -> None:
        self.representacion = tablero
        self.valor_funcion = valor

'''Funcion que cuenta los ataques de un tablero, es decir, devuelve el valor de aptitud'''
def contar_ataques(tablero):
  ataques = 0

  for fila in range(8):
    for columna in range(8):

      if tablero[fila][columna] == 1:

        for col2 in range(columna + 1, 8):
          if tablero[fila][col2] == 1:
            ataques += 1

        for row2 in range(fila + 1, 8):
          if tablero[row2][columna] == 1:
            ataques += 1

        #Diagonal
        for row2, col2 in zip(range(fila + 1, 8), range(columna + 1, 8)):
          if tablero[row2][col2] == 1:
            ataques += 1

        #Diagonal
        for row2, col2 in zip(range(fila - 1, -1, -1), range(columna + 1, 8)):
          if tablero[row2][col2] == 1:
            ataques += 1

  return ataques

'''Generar un tablero aleatoriamente'''
def generar_individuo():
    #Crea el individuo de 8 x 8
    tablero = [[0] * 8 for _ in range(8)]
    reinas_colocadas = 0
    #Coloca 8 reinas aleatoriamente
    while reinas_colocadas < 8:
        fila = random.randint(0, 7)
        columna = random.randint(0, 7)
        if tablero[fila][columna] == 0:
            tablero[fila][columna] = 1
            reinas_colocadas += 1
    return tablero

'''Genera un conjunto de 100 tableros con reinas aleatoriamente distribuidas'''
def generar_poblacion(evaluaciones):
    tableros = []
    
    #Genera un conjunto de 100 tableros, con reinas colocadas, es decir, la poblacion
    for i in range(0, 100):
        tablero = generar_individuo()
        #Una vez generado el individuo, se evalua la funcion de aptitud y se guarda
        valor = contar_ataques(tablero)
        evaluaciones = evaluaciones + 1
        objeto_tablero = Tablero(tablero, valor)
        tableros.append(objeto_tablero)
    return tableros, evaluaciones

'''Obtiene 5 elementos padres, los ordena por su funcion de valor y obtiene los mejores dos,
a los cuales agrega como pareja de padres'''
def generar_padres(poblacion):
    #Crea 10 tuplas de padres para 10 descendientes
    padres = [([], []) for _ in range(0, 10)]
    #Padres para los 10 descendientes
    for i in range(0, 10):
        randoms = []
        coleccion_cinco_elementos = []
        #Se seleccionan 5 elementos aleatoriamente 
        while (len(coleccion_cinco_elementos) < 5):
            r = random.randint(0, 99)
            if (r not in randoms):
                randoms.append(r)
                coleccion_cinco_elementos.append(poblacion[r])
        
        #Se ordenan los elementos de menor a mayor valor de funcion de aptitud
        coleccion_cinco_elementos_ordenada = sorted(coleccion_cinco_elementos, key=lambda tablero: tablero.valor_funcion)
        #Se seleccionan como pareja los primeros 2 mejores
        padres[i] = (coleccion_cinco_elementos_ordenada[0], coleccion_cinco_elementos_ordenada[1])
    return padres

'''Retorna el valor mas bajo'''
def obtener_mejor_valor_aptitud(tableros):
    mejor_evaluacion = tableros[0].valor_funcion
    for i in range(1, 100):
        if (tableros[i].valor_funcion < mejor_evaluacion):
            mejor_evaluacion = tableros[i].valor_funcion
    return mejor_evaluacion

'''Obtiene el numero de reinas en un tablero'''
def calcular_numero_reinas(hijo):
    numero_reinas = 0
    for i in range(0, len(hijo)):
        for j in range(0, len(hijo)):
            if hijo[i][j] == 1:
                numero_reinas = numero_reinas + 1
    return numero_reinas

'''Si un tablero, despues de la cruza tiene mas de 8 reinas este elimina las sobrantes'''
def eliminar_reinas_sobrantes(tablero_reinas):
    numero_reinas = 0
    for i in range(0, len(tablero_reinas)):
        for j in range(0, len(tablero_reinas)):
            if tablero_reinas[i][j] == 1:
                if numero_reinas == 8:
                    tablero_reinas[i][j] = 0
                else:
                    numero_reinas = numero_reinas + 1
             
'''Si un tablero, despues de la cruza tiene menos de 8 reinas este suma las restantes'''
def sumar_reinas_faltantes(tablero_reinas, reinas_faltantes):
    reinas_agregadas = 0
    for i in range (0, reinas_faltantes):
        while reinas_agregadas != reinas_faltantes:
            r1 = random.randint(0, 7)
            r2 = random.randint(0, 7)
            if tablero_reinas[r1][r2] != 1:
                tablero_reinas[r1][r2] = 1
                reinas_agregadas = reinas_agregadas + 1
          
'''Utilizado para mutar un hijo moviendo una reina una posicion'''      
def mutar(tablero_reinas):
    for i in range(0, len(tablero_reinas)):
        for j in range(0, len(tablero_reinas)):
            if tablero_reinas[i][j] == 1:
                tablero_reinas[i][j] = 0
                
                #Cada decision evalua que la posicion se encuentre dentro del tablero y que
                #la posicion hacia la que se va a mover no tenga una reina.
                #Puede mover hacia adelante, atras, abajo o arriba
                if j+1 <=7 and tablero_reinas[i][j + 1] != 1:
                    tablero_reinas[i][j + 1] = 1
                elif j-1 >= 0 and tablero_reinas[i][j - 1] != 1:
                    tablero_reinas[i][j - 1] = 1
                elif i + 1 <= 7 and tablero_reinas[i + 1][j] != 1:
                    tablero_reinas[i + 1][j] = 1
                elif i-1 >= 0 and tablero_reinas[i - 1][j] != -1:
                    tablero_reinas[i - 1][j] = 1
                return
                           
'''Cruza las parejas de padres en un arreglo
Padres: las 10 parejas de padres obtenidas previamente
Evaluaciones: al crear un hijo, se evalua con la funcion de aptitud y se guarda, es necesario sumar'''
def cruzar_padres(padres, evaluaciones):
    hijos = []
    for i in range(0, len(padres)):
        hijo = []
        #Se obtiene la primera tupla
        p = padres[i]
        
        #Se accede al primer y segundo padre en la tupla
        p1 = p[0].representacion
        p2 = p[1].representacion
        
        #Se agregan las primeras cuatro filas del primer padre al hijo
        for i in range(0, 4):
            hijo.append(p1[i])
            
        #Se agregan las segundas cuatro filas del segundo padre al hijo
        for i in range(0, 4):
            hijo.append(p2[i])
        
        #Se evalua que se cumpla la restriccion (8 reinas) y si no se cumple
        #se suman o eliminan segun sea necesario.
        cantidad_reinas = calcular_numero_reinas(hijo)
        if cantidad_reinas > 8:
            eliminar_reinas_sobrantes(hijo)
        elif cantidad_reinas < 8:
            sumar_reinas_faltantes(hijo, 8 - cantidad_reinas)
            
        #Se obtiene un valor random para la mutacion y si se esta dentro de la probabilidad
        #se realiza la mutacion
        probabilidad_mutacion = (random.randint(0, 100)/100)
        if probabilidad_mutacion <= .8:
            mutar(hijo)
        
        #Se obtiene el valor de la funcion de aptitud del hijo y se agrega a los hijos obtenidos
        valor = contar_ataques(hijo)
        evaluaciones += 1
        objeto_tablero = Tablero(hijo, valor)
        hijos.append(objeto_tablero)
    return hijos, evaluaciones
    
'''Reemplaza los 10 peores de una poblacion y se reemplazan con los 10 hijos obtenidos'''
def reemplazar(poblacion, hijos):
    #Se obtiene el indice de los 10 peores individuos de la poblacion
    indices_con_mayores_valores = sorted(range(len(poblacion)), key=lambda i: poblacion[i].valor_funcion, reverse=True)[:10]
    #Se hace una tupla (indide, hijo correspondiente) con zip y se reemplaza el individuo en la poblacion en i con el hijo
    for indice_reemplazo, nuevo_hijo in zip(indices_con_mayores_valores, hijos):
        poblacion[indice_reemplazo] = nuevo_hijo
    

def main():
    convergencia = [] #Usada para almacenar la convergencia
    evaluaciones = 0
    poblacion, evaluaciones = generar_poblacion(evaluaciones)
    mejor_evaluacion = obtener_mejor_valor_aptitud(poblacion)
    print(f"Mejor valor de aptitud al inicio: {mejor_evaluacion}")
    convergencia.append(mejor_evaluacion)
    while evaluaciones <= 10000 and mejor_evaluacion != 0:
        padres = generar_padres(poblacion)
        hijos, evaluaciones = cruzar_padres(padres, evaluaciones)
        reemplazar(poblacion, hijos)
        mejor_evaluacion = obtener_mejor_valor_aptitud(poblacion)
        convergencia.append(mejor_evaluacion)
          
    print(f"Mejor valor de aptitud al final: {mejor_evaluacion}")
    generaciones = range(1, len(convergencia) + 1)
    
    # Crear el gráfico de convergencia
    plt.plot(generaciones, convergencia, marker='o', linestyle='-')
    plt.title('Convergencia del Algoritmo Evolutivo para el Problema de las 8 Reinas')
    plt.xlabel('Generación')
    plt.ylabel('Cantidad de Ataques')
    plt.grid(True)
    plt.show()
         
main()
        