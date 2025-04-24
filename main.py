"""
Interfaz principal de línea de comandos
"""
import ast
from matrices import generar_matriz, generar_pdf
from determinante import calcular_determinante, generar_reporte
from inversa import calcular_inversa, generar_reporte_inversa

def mostrar_menu():
    """Muestra el banner y los créditos del proyecto."""
    print("""
██████╗ ██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗
██╔══██╗╚██╗ ██╔╝████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝
██████╔╝ ╚████╔╝ ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ 
██╔═══╝   ╚██╔╝  ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ 
██║        ██║   ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗
╚═╝        ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
v1.0.1

Universidad Francisco de Paula Santander

Creado por:     
-Juan Felipe Zoghbi Robles 2150004
-Juan Diego Cabrales Hernandez 2150008""")

def menu_opciones():
    """
    Muestra únicamente las opciones disponibles para el usuario
    (sin el banner ni los créditos).
    """
    print("""
Opciones        
1. Generar matriz especial
2. Calcular determinante
3. Calcular matriz inversa
4. Salir""")

def pedir_matriz():
    """
    Solicita al usuario una matriz en forma de texto y la convierte
    a una lista de listas con ast.literal_eval para mayor seguridad.
    Retorna la matriz si es válida, o None en caso de error.
    """
    try:
        entrada = input("Ingresa la matriz como lista de listas (ej. [[1,2],[3,4]]): ")
        matriz = ast.literal_eval(entrada)
        # Verifica que sea una lista de listas
        if isinstance(matriz, list) and all(isinstance(f, list) for f in matriz):
            return matriz
        else:
            print("Formato inválido. Debe ser una lista de listas.")
    except Exception:
        print("Error al interpretar la matriz.")
    return None  # devuelve None si hay fallo


def menu_generar_matriz():
    """
    Submenú para generar matrices especiales.
    - Presenta los tipos disponibles.
    - Lee la opción y pide dimensiones.
    - Llama a generar_matriz y luego a generar_pdf.
    """
    print("\nTipos disponibles:")
    print("1. Diagonal")
    print("2. Triangular superior")
    print("3. Identidad")
    print("4. Rectangular")
    print("5. Cuadrada aleatoria")
    print("6. Volver")  # opción para regresar al menú principal
    opciones = {
        '1': 'diagonal',
        '2': 'triangular_sup',
        '3': 'identidad',
        '4': 'rectangular',
        '5': 'cuadrada',
    }

    tipo = input("Seleccione tipo (1-6): ")
    if tipo == '6':  # detecta la opción "volver"
        return

    if tipo not in opciones:
        print("Tipo inválido")
        return

    try:
        filas = int(input("Número de filas: "))
        columnas = None
        # si es rectangular pide un número de columnas
        if opciones[tipo] == 'rectangular':
            columnas = int(input("Número de columnas: "))
        # genera la matriz y el PDF
        matriz = generar_matriz(opciones[tipo], filas, columnas)
        generar_pdf(matriz, 'matriz')
        print("Matriz generada con éxito")
    except ValueError:
        print("Por favor ingrese números válidos.")


def menu_determinante():
    """
    Submenú para cálculo de determinante:
    - Pide la matriz con pedir_matriz.
    - Comprueba que sea cuadrada.
    - Llama a calcular_determinante y generar_reporte.
    """
    matriz = pedir_matriz()
    if matriz is None:
        return  # vuelve al menú principal
    if len(matriz) != len(matriz[0]):
        print("La matriz debe ser cuadrada.")
        return
    det, pasos = calcular_determinante(matriz)
    generar_reporte(matriz, det, pasos)
    print(f"Determinante calculado: {det:.2f} (ver determinante.pdf)")


def menu_inversa():
    """
    Submenú para cálculo de matriz inversa:
    - Pide la matriz.
    - Comprueba cuadratura.
    - Llama a calcular_inversa y generar_reporte_inversa.
    """
    matriz = pedir_matriz()
    if matriz is None:
        return
    if len(matriz) != len(matriz[0]):
        print("La matriz debe ser cuadrada.")
        return
    resultado = calcular_inversa(matriz)
    generar_reporte_inversa(matriz, resultado)
    if resultado['inversa']:
        print("Inversa calculada con éxito")
    else:
        print("La matriz no es invertible (determinante = 0)")


# ---------- PROGRAMA PRINCIPAL ----------
if __name__ == '__main__':
    try:
        mostrar_menu()  # imprime banner inicial
        while True:
            menu_opciones()  # muestra opciones 1–4
            opcion = input("Seleccione una opción (1-4): ")

            if opcion == '1':
                menu_generar_matriz()
            elif opcion == '2':
                menu_determinante()
            elif opcion == '3':
                menu_inversa()
            elif opcion == '4':
                print("Ejecucion finalizada")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")
    except KeyboardInterrupt:
        # Captura Ctrl+C y sale sin trazar error en consola
        print("\nOperación cancelada por el usuario.")