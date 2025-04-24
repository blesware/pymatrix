"""
módulo inversa.py

Contiene:
 - calcular_inversa: metodo de cofactores para la inversa.
 - _bmatrix_latex: helper idéntico al de determinante.
 - generar_reporte_inversa: crea ./tex/inversa.tex y ./pdf/inversa.pdf.
"""

import os
from pylatex import Document, Section, NoEscape, Package
from pylatex.errors import CompilerError
from determinante import calcular_determinante

def calcular_inversa(matriz: list) -> dict:
    """
    1) Calcula matriz de cofactores.
    2) Transpone (adjunta).
    3) Calcula determinante (usa calcular_determinante).
    4) Si det≠0, divide adjunta/ det.
    Retorna dict con claves 'cofactores', 'adjunta', 'determinante', 'inversa'.
    """
    n = len(matriz)
    cof = []
    for i in range(n):
        fila_cof = []
        for j in range(n):
            # submatriz eliminando fila i y columna j
            sub = [row[:j] + row[j+1:] for row in (matriz[:i] + matriz[i+1:])]
            # determinante 2×2 hardcodeado o trivial 1×1
            det_sub = (sub[0][0]*sub[1][1] - sub[0][1]*sub[1][0]) \
                      if len(sub)==2 else sub[0][0]
            fila_cof.append(det_sub * ((-1)**(i+j)))
        cof.append(fila_cof)

    adj = list(map(list, zip(*cof)))  # transpuesta
    det, _ = calcular_determinante(matriz)
    inv = None if det == 0 else [[x/det for x in fila] for fila in adj]

    return {
        'cofactores': cof,
        'adjunta': adj,
        'determinante': det,
        'inversa': inv
    }

def _bmatrix_latex(matriz: list) -> str:
    """Igual helper que en los demás módulos."""
    filas = [" & ".join(str(x) for x in fila) for fila in matriz]
    cuerpo = r" \\ ".join(filas)
    return r"\begin{bmatrix}" + cuerpo + r"\end{bmatrix}"

def generar_reporte_inversa(matriz: list, resultado: dict):
    """
    Estructura del LaTeX:
      Sec 1: Matriz original
      Sec 2: Cofactores
      Sec 3: Adjunta
      Sec 4: Inversa o mensaje de no invertible
    Guarda .tex en ./tex/inversa.tex y .pdf en ./pdf/inversa.pdf.
    """
    doc = Document()
    doc.packages.append(Package('amsmath'))

    # Preparar rutas
    base = os.getcwd()
    tex_dir = os.path.join(base, 'tex')
    pdf_dir = os.path.join(base, 'pdf')
    os.makedirs(tex_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    tex_base = os.path.join(tex_dir, 'inversa')
    pdf_base = os.path.join(pdf_dir, 'inversa')

    # 1) Matriz original
    doc.append(Section('Matriz Original'))
    doc.append(NoEscape(r"\[" + "\n" +
               _bmatrix_latex(matriz) + "\n" + r"\]"))

    # 2) Cofactores
    doc.append(Section('Matriz de Cofactores'))
    doc.append(NoEscape(r"\[" + "\n" +
               _bmatrix_latex(resultado['cofactores']) + "\n" + r"\]"))

    # 3) Adjunta
    doc.append(Section('Matriz Adjunta'))
    doc.append(NoEscape(r"\[" + "\n" +
               _bmatrix_latex(resultado['adjunta']) + "\n" + r"\]"))

    # 4) Inversa o mensaje
    doc.append(Section('Resultado'))
    if resultado['inversa'] is not None:
        doc.append("Matriz Inversa:")
        doc.append(NoEscape(r"\[" + "\n" +
                   _bmatrix_latex(resultado['inversa']) + "\n" + r"\]"))
    else:
        doc.append("La matriz no es invertible (determinante = 0)")

    # Escritura de archivos
    tex_path = tex_base + '.tex'
    doc.generate_tex(tex_base)
    print(f"Archivo .tex generado en: {os.path.abspath(tex_path)}")

    try:
        pdf_path = pdf_base + '.pdf'
        doc.generate_pdf(pdf_base, clean_tex=True, compiler='pdflatex')
        print(f"Archivo .pdf generado en: {os.path.abspath(pdf_path)}")
    except CompilerError:
        print("No se pudo compilar, no se encontro compilador de LaTeX, Solo se creó el .tex")
