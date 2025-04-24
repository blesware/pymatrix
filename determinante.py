"""
módulo determinante.py

Contiene:
 - calcular_determinante: Gauss para obtener determinante y pasos.
 - _bmatrix_latex: helper para bmatrix LaTeX.
 - generar_reporte: produce ./tex/determinante.tex y ./pdf/determinante.pdf.
"""

import os
from pylatex import Document, Section, NoEscape, Package
from pylatex.errors import CompilerError
from typing import Tuple, List

def calcular_determinante(matriz: List[List[float]]) -> Tuple[float, List]:
    """
    Aplica eliminación gaussiana:
      - Devuelve (determinante, lista_de_pasos)
      - Cada paso es tupla ('intercambio' o 'eliminacion', datos, estado actual).
    """
    n = len(matriz)
    det = 1.0
    pasos = []
    m = [fila.copy() for fila in matriz]

    for col in range(n):
        # 1) Buscar pivote no nulo
        piv = col
        while piv < n and m[piv][col] == 0:
            piv += 1
        if piv == n:
            return 0.0, pasos  # matriz singular

        # 2) Si intercambia filas, det cambia de signo
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det *= -1
            pasos.append(('intercambio', col, piv, [f.copy() for f in m]))

        # 3) Eliminar por debajo de la diagonal
        for fila in range(col+1, n):
            factor = m[fila][col] / m[col][col]
            for c in range(col, n):
                m[fila][c] -= factor * m[col][c]
            pasos.append(('eliminacion', fila, col, factor, [f.copy() for f in m]))

        # 4) Multiplica el pivote
        det *= m[col][col]

    return det, pasos


def _bmatrix_latex(matriz: list) -> str:
    """Igual que en matrices.py: genera el entorno bmatrix LaTeX."""
    filas = [" & ".join(str(x) for x in fila) for fila in matriz]
    cuerpo = r" \\ ".join(filas)
    return r"\begin{bmatrix}" + cuerpo + r"\end{bmatrix}"


def generar_reporte(matriz: list, det: float, pasos: list):
    """
    Crea un documento con:
     1) Sección Matriz Original
     2) Sección Proceso (cada paso con su bmatrix)
     3) Sección Resultado Final
    Lo escribe en ./tex/determinante.tex y ./pdf/determinante.pdf.
    """
    # 1) Documento básico con amsmath
    doc = Document()
    doc.packages.append(Package('amsmath'))

    # 2) Rutas de salida
    base = os.getcwd()
    tex_dir = os.path.join(base, 'tex')
    pdf_dir = os.path.join(base, 'pdf')
    os.makedirs(tex_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    tex_base = os.path.join(tex_dir, 'determinante')
    pdf_base = os.path.join(pdf_dir, 'determinante')

    # 3) Matriz original
    doc.append(Section('Matriz Original'))
    doc.append(NoEscape(r"\[" + "\n" +
               _bmatrix_latex(matriz) + "\n" + r"\]"))

    # 4) Proceso paso a paso
    doc.append(Section('Proceso de Cálculo'))
    for i, paso in enumerate(pasos, 1):
        if paso[0] == 'intercambio':
            _, f1, f2, estado = paso
            doc.append(f'Paso {i}: Intercambio filas {f1+1} ↔ {f2+1}')
        else:
            _, fo, fp, factor, estado = paso
            doc.append(
                f'Paso {i}: Eliminación fila {fo+1} usando fila {fp+1} (factor {factor:.2f})'
            )
        doc.append(NoEscape(r"\[" + "\n" +
                   _bmatrix_latex(estado) + "\n" + r"\]"))

    # 5) Resultado final
    doc.append(Section('Resultado Final'))
    doc.append(f'Determinante = {det:.2f}')

    # 6) Escritura de archivos
    tex_path = tex_base + '.tex'
    doc.generate_tex(tex_base)
    print(f"Archivo .tex generado en: {os.path.abspath(tex_path)}")

    try:
        pdf_path = pdf_base + '.pdf'
        doc.generate_pdf(pdf_base, clean_tex=True, compiler='pdflatex')
        print(f"Archivo .pdf generado en: {os.path.abspath(pdf_path)}")
    except CompilerError:
        print("No se pudo compilar, no se encontro compilador de LaTeX, Solo se creó el .tex")