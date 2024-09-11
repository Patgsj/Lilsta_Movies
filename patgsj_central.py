# Parte 1: Cargar los datos
def cargar_datos(lineas_archivo):
    generos_peliculas = []
    peliculas_por_genero = []
    info_peliculas = []

    for linea in lineas_archivo:
        titulo, popularidad, voto_promedio, cantidad_votos, generos = linea.strip().split(',')
        popularidad = float(popularidad)
        voto_promedio = float(voto_promedio)
        cantidad_votos = int(cantidad_votos)
        lista_generos = generos.split(';')
        
        # Generar lista de géneros únicos
        for genero in lista_generos:
            if genero not in generos_peliculas:
                generos_peliculas.append(genero)
        
        # Asignar películas a géneros
        for genero in lista_generos:
            encontrado = False
            for item in peliculas_por_genero:
                if item[0] == genero:
                    item[1].append(titulo)
                    encontrado = True
                    break
            if not encontrado:
                peliculas_por_genero.append((genero, [titulo]))
        
        # Guardar la información de las películas
        info_peliculas.append((titulo, popularidad, voto_promedio, cantidad_votos, lista_generos))

    return generos_peliculas, peliculas_por_genero, info_peliculas


# Parte 2: Completar las consultas
def obtener_puntaje_y_votos(nombre_pelicula):
    # Cargar las lineas con la data del archivo
    lineas_archivo = leer_archivo()
    generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(lineas_archivo)
    
    for pelicula in info_peliculas:
        if pelicula[0].strip().lower() == nombre_pelicula.strip().lower():
            return pelicula[2], pelicula[3]
    return None, None


def filtrar_y_ordenar(genero_pelicula):
    # Cargar las lineas con la data del archivo
    lineas_archivo = leer_archivo()
    generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(lineas_archivo)

    peliculas_en_genero = []
    for item in peliculas_por_genero:
        if item[0].strip().lower() == genero_pelicula.strip().lower():
            peliculas_en_genero = item[1]
            break
    
    return sorted(peliculas_en_genero, key=lambda x: x.lower())


def obtener_estadisticas(genero_pelicula, criterio):
    # Cargar las lineas con la data del archivo
    lineas_archivo = leer_archivo()
    generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(lineas_archivo)
    
    valores = []
    
    for pelicula in info_peliculas:
        if genero_pelicula.lower() in [g.lower() for g in pelicula[4]]:
            if criterio == "popularidad":
                valores.append(pelicula[1])
            elif criterio == "voto promedio":
                valores.append(pelicula[2])
            elif criterio == "cantidad votos":
                valores.append(pelicula[3])
    
    if valores:
        maximo = max(valores)
        minimo = min(valores)
        promedio = sum(valores) / len(valores)
        return [maximo, minimo, promedio]
    else:
        return [None, None, None]



# NO ES NECESARIO MODIFICAR DESDE AQUI HACIA ABAJO

def solicitar_accion():
    print("\n¿Qué desea hacer?\n")
    print("[0] Revisar estructuras de datos")
    print("[1] Obtener puntaje y votos de una película")
    print("[2] Filtrar y ordenar películas")
    print("[3] Obtener estadísticas de películas")
    print("[4] Salir")

    eleccion = input("\nIndique su elección (0, 1, 2, 3, 4): ").lower()
    while eleccion not in "01234":
        eleccion = input("\nElección no válida.\nIndique su elección (0, 1, 2, 3, 4): ").lower()
    eleccion = int(eleccion)
    return eleccion


def leer_archivo():
    lineas_peliculas = []
    try:
        with open("peliculas.csv", "r", encoding="utf-8") as datos:
            for linea in datos.readlines()[1:]:
                lineas_peliculas.append(linea.strip())
    except FileNotFoundError:
        print("\nError: El archivo 'peliculas.csv' no se encuentra en el directorio.")
        return []
    return lineas_peliculas


def revisar_estructuras(generos_peliculas, peliculas_por_genero, info_peliculas):
    print("\nGéneros de películas:")
    for genero in generos_peliculas:
        print(f"    - {genero}")

    print("\nTítulos de películas por genero:")
    for genero in peliculas_por_genero:
        print(f"    genero: {genero[0]}")
        for titulo in genero[1]:
            print(f"        - {titulo}")

    print("\nInformación de cada película:")
    for pelicula in info_peliculas:
        print(f"    Nombre: {pelicula[0]}")
        print(f"        - Popularidad: {pelicula[1]}")
        print(f"        - Puntaje Promedio: {pelicula[2]}")
        print(f"        - Votos: {pelicula[3]}")
        print(f"        - Géneros: {pelicula[4]}")


def solicitar_nombre():
    nombre = input("\nIngrese el nombre de la película: ").lower()
    return nombre


def solicitar_genero():
    genero = input("\nIndique el género de película: ").lower()
    return genero


def solicitar_genero_y_criterio():
    genero = input("\nIndique el género de película: ").lower()
    
    criterio = input(
        "\nIndique el criterio (popularidad, voto promedio, cantidad votos): "
    ).strip().lower()
    
    # BUCLE
    while criterio not in ["popularidad", "voto promedio", "cantidad votos"]:
        print("\nCriterio no válido. Intente de nuevo.")
        criterio = input("\nIndique el criterio (popularidad, voto promedio, cantidad votos): ").strip().lower()

    return genero, criterio



def main():
    lineas_archivo = leer_archivo()
    if not lineas_archivo:
        return
    
    datos_cargados = True
    try:
        generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(
            lineas_archivo
        )
    except TypeError as error:
        if "cannot unpack non-iterable NoneType object" in repr(error):
            print(
                "\nTodavía no puedes ejecutar el programa ya que no has cargado los datos\n"
            )
            datos_cargados = False
    if datos_cargados:
        salir = False
        print("\n********** ¡Bienvenid@! **********")
        while not salir:
            accion = solicitar_accion()

            if accion == 0:
                revisar_estructuras(
                    generos_peliculas, peliculas_por_genero, info_peliculas
                )

            elif accion == 1:
                nombre_pelicula = solicitar_nombre()
                ptje, votos = obtener_puntaje_y_votos(nombre_pelicula)
                if ptje is not None and votos is not None:
                    print(f"\nObteniendo puntaje promedio y votos de {nombre_pelicula}")
                    print(f"    - Puntaje promedio: {ptje}")
                    print(f"    - Votos: {votos}")
                else:
                    print(f"\nLa película '{nombre_pelicula}' no fue encontrada.")

            elif accion == 2:
                genero = solicitar_genero()
                nombres_peliculas = filtrar_y_ordenar(genero)
                if nombres_peliculas:
                    print(f"\nNombres de películas del género {genero} ordenados:")
                    for nombre in nombres_peliculas:
                        print(f"    - {nombre}")
                else:
                    print(f"\nNo se encontraron películas del género '{genero}'.")

            elif accion == 3:
                genero, criterio = solicitar_genero_y_criterio()
                estadisticas = obtener_estadisticas(genero, criterio)
                if estadisticas[0] is not None:
                    print(f"\nEstadísticas de {criterio} de películas del género {genero}:")
                    print(f"    - Máximo: {estadisticas[0]}")
                    print(f"    - Mínimo: {estadisticas[1]}")
                    print(f"    - Promedio: {estadisticas[2]}")
                else:
                    print(f"\nNo se encontraron películas del género '{genero}' con criterio '{criterio}'.")

            else:
                salir = True
        print("\n********** ¡Adiós! **********\n")


if __name__ == "__main__":
    main()
