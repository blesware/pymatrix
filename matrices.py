"""
módulo matrices.py

Contiene:
 - generar_matriz: crea matrices especiales con valores aleatorios.
 - _bmatrix_latex: helper para construir el código LaTeX de una bmatrix.
 - generar_pdf: genera siempre un .tex en ./tex/ y, si puede, un .pdf en ./pdf/.
"""

import os
import subprocess
import random
from pylatex import Document, NoEscape, Package
from pylatex.errors import CompilerError

def generar_matriz(tipo: str, filas: int, columnas: int = None) -> list:
    """
    Genera matrices de varios tipos:
      - diagonal, triangular_sup, identidad, rectangular, cuadrada aleatoria.
    Retorna: lista de listas (filas x columnas).
    """
    if tipo == 'diagonal':
        return [[random.randint(1, 9) if i == j else 0
                 for j in range(filas)] for i in range(filas)]
    elif tipo == 'triangular_sup':
        return [[random.randint(1, 9) if j >= i else 0
                 for j in range(filas)] for i in range(filas)]
    elif tipo == 'identidad':
        return [[1 if i == j else 0 for j in range(filas)]
                 for i in range(filas)]
    elif tipo == 'rectangular':
        return [[random.randint(0, 9) for _ in range(columnas)]
                 for _ in range(filas)]
    else:  # 'cuadrada'
        return [[random.randint(0, 9) for _ in range(filas)]
                 for _ in range(filas)]


def _bmatrix_latex(matriz: list) -> str:
    """
    Crea una cadena con el entorno bmatrix de LaTeX para una lista de listas.
    """
    filas = [" & ".join(str(x) for x in fila) for fila in matriz]
    cuerpo = r" \\ ".join(filas)
    return r"\begin{bmatrix}" + cuerpo + r"\end{bmatrix}"


def generar_pdf(matriz: list, nombre_archivo: str):
    """
    1) Construye un documento con la matriz en display-math (bmatrix).
    2) Crea carpetas ./tex/ y ./pdf/ si no existen.
    3) Siempre escribe el .tex en ./tex/{nombre_archivo}.tex.
    4) Intenta generar el .pdf en ./pdf/{nombre_archivo}.pdf usando pdflatex.
       Si no hay compilador, deja solo el .tex.
    """
    # 1) Prepara el documento y añade amsmath
    doc = Document()
    doc.packages.append(Package('amsmath'))
    latex_mat = _bmatrix_latex(matriz)

    # 2) Monta las carpetas de salida
    base = os.getcwd()
    tex_dir = os.path.join(base, 'tex')
    pdf_dir = os.path.join(base, 'pdf')
    os.makedirs(tex_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    tex_base = os.path.join(tex_dir, nombre_archivo)
    pdf_base = os.path.join(pdf_dir, nombre_archivo)

    # 3) Inserta el entorno de la matriz
    doc.append(NoEscape(r"\[" + "\n" + latex_mat + "\n" + r"\]"))

    # 4) Genera .tex (siempre)
    tex_path = tex_base + '.tex'
    doc.generate_tex(tex_base)
    print(f"Archivo .tex generado en: {os.path.abspath(tex_path)}")

    # 5) Genera .pdf (solo si pdflatex existe) y **no** deja el .tex en ./pdf/
    try:
        pdf_path = pdf_base + '.pdf'
        doc.generate_pdf(pdf_base, clean_tex=True, compiler='pdflatex')
        print(f"Archivo .pdf generado en: {os.path.abspath(pdf_path)}")
    except (CompilerError, subprocess.CalledProcessError):
        print("No se pudo compilar, no se encontro compilador de LaTeX, Solo se creó el .tex")