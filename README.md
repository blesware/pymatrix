# PyMatrix

**Versión:** 1.0.0

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![LaTeX](https://img.shields.io/badge/LaTeX-Output%20Support-orange)

## Descripción

PyMatrix es una herramienta de línea de comandos interactiva para:

- Generar matrices especiales (diagonal, triangular superior, identidad, rectangular, cuadrada aleatoria).  
- Calcular determinantes (método de eliminación de Gauss, reporte paso a paso).  
- Calcular matrices inversas (método de cofactores, adjunta y resultado final).

El programa produce siempre un archivo LaTeX (`.tex`) en la carpeta `tex/` y, si dispone de `pdflatex`, un archivo PDF (`.pdf`) en la carpeta `pdf/`. Ambos directorios se crean automáticamente.

## Requisitos

1. **Python 3.8+**  
2. **Dependencias Python** (instalar con `pip`):
   ```bash
   pip install -r requirements.txt
   ```
3. **Distribución LaTeX** (opcional para PDF):
   - **Windows:** MiKTeX ([https://miktex.org/download](https://miktex.org/download))  
     Asegúrate de añadir `pdflatex` al `PATH`.  
   - **Linux (Debian/Ubuntu):**
     ```bash
     sudo apt install texlive-latex-base texlive-latex-extra
     ```
   - **macOS:**
     ```bash
     brew install --cask mactex
     ```

> Si no dispones de LaTeX, PyMatrixCLI generará únicamente los archivos `.tex`.

## Estructura del proyecto

```
PyMatrixCLI/
├── main.py            # Interfaz de usuario y submenús
├── matrices.py        # Generación de matrices y helper LaTeX
├── determinante.py    # Cálculo de determinante y reporte
├── inversa.py         # Cálculo de inversa y reporte
├── requirements.txt   # Dependencias Python
├── tex/               # Carpeta de salida de archivos .tex
└── pdf/               # Carpeta de salida de archivos .pdf
```

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/PyMatrixCLI.git
cd PyMatrixCLI

# (Opcional) Crear entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

Ejecuta el script principal:

```bash
python main.py
```

Aparecerá un menú como el siguiente:

```
1. Generar matriz especial
2. Calcular determinante
3. Calcular matriz inversa
4. Salir
```

### 1. Generar matriz especial

- Elige el tipo (1–5) y dimensiones.  
- Se crearán:
  - `tex/matriz.tex`
  - `pdf/matriz.pdf` (si `pdflatex` está disponible)

### 2. Calcular determinante

- Ingresa la matriz cuadrada en formato Python, por ejemplo `[[2,3],[1,4]]`.  
- Se crearán:
  - `tex/determinante.tex`
  - `pdf/determinante.pdf` (si `pdflatex` está disponible)

### 3. Calcular matriz inversa

- Ingresa la matriz cuadrada.  
- Se crearán:
  - `tex/inversa.tex`
  - `pdf/inversa.pdf` (si `pdflatex` está disponible)

### 4. Salir

Finaliza la ejecución.

## Personalización

- Para cambiar los nombres de salida, modifica el segundo parámetro en las llamadas a `generar_pdf` y `generar_reporte*`.  
- El preámbulo LaTeX (por ejemplo, carga de `amsmath`) se configura en cada módulo.  
- Para usar otro compilador diferente a `pdflatex`, ajusta el argumento `compiler` en `doc.generate_pdf()`.

## Contribuciones

1. Haz fork de este repositorio.  
2. Crea una rama nueva:
   ```bash
   git checkout -b feature/mi-mejora
   ```
3. Realiza tus cambios y haz commit:
   ```bash
   git commit -m "Descripción de la mejora"
   ```
4. Envía tu rama a tu fork:
   ```bash
   git push origin feature/mi-mejora
   ```
5. Abre un Pull Request.

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.