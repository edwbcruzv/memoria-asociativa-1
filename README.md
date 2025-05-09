# Memorias Morfológicas Autoasociativas

## Descripción del Proyecto

Este proyecto implementa una memoria morfológica autoasociativa para el reconocimiento y recuperación de patrones binarios, específicamente imágenes de dígitos del 0 al 9. Utiliza morfología matemática para construir matrices \(W\) (máxima) y \(M\) (mínima), diseñadas para corregir ruido artificial (aditivo, sustractivo y mixto) y evaluar el reconocimiento de imágenes a mano alzada. El análisis se realiza en dos fases:

- **Fase 1**: Recuperación del Conjunto Fundamental de Patrones (CFP) con ruido artificial en porcentajes del 1% al 90%.
- **Fase 2**: Evaluación con patrones de prueba a mano alzada sin ruido.

El proyecto está implementado en Python 3.12 y utiliza las siguientes librerías fundamentales:

- `numpy`: Para operaciones matriciales y cálculos de las matrices \(W\) y \(M\).
- `matplotlib`: Para generar visualizaciones de las imágenes ruidosas y recuperadas.
- `pillow`: Para leer y procesar las imágenes de entrada en formato BMP.

## Requisitos

- **Python 3.12**: Asegúrate de tener instalada esta versión de Python.
- **Sistema operativo**: Compatible con Windows, Linux o macOS.

## Instalación del Entorno de Pruebas

Sigue estos pasos para configurar el entorno y ejecutar el proyecto:

### 1. Clonar o Descargar el Repositorio
Descarga el código fuente del proyecto a tu máquina local. Si está en un repositorio Git, puedes clonarlo con:

```bash
git clone https://github.com/edwbcruzv/memoria-asociativa-1.git
cd memoria-asociativa-1
```

### 2. Crear un Entorno Virtual (Recomendado)
Crea y activa un entorno virtual para aislar las dependencias:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar las Dependencias
El proyecto incluye un archivo `requirements.txt` con las librerías necesarias. Instálalas con:

```bash
pip install -r requirements.txt
```

Si no tienes el archivo `requirements.txt`, puedes instalar las librerías manualmente:

```bash
pip install numpy==2.2.5 matplotlib==3.10.1 pillow==11.2.1
```

Esto también instalará las dependencias necesarias (`contourpy`, `cycler`, `fonttools`, `kiwisolver`, `packaging`, `pyparsing`, `python-dateutil`, `six`).

### 4. Verificar la Instalación
Asegúrate de que las librerías estén instaladas correctamente ejecutando:

```bash
pip list
```

Deberías ver las versiones especificadas de `numpy`, `matplotlib`, y `pillow`, entre otras.

## Estructura del Proyecto

- `main.py`: Script principal que ejecuta las pruebas de las memorias morfológicas.
- `train_chica/`: Carpeta con las imágenes del CFP (dígitos del 0 al 9 en formato BMP).
- `test/`: Carpeta con las imágenes de prueba a mano alzada (en formato BMP).
- `requirements.txt`: Archivo con las dependencias del proyecto.

## Ejecución de las Pruebas

1. **Preparar las Imágenes**:
   - Asegúrate de que las carpetas `train_chica/` y `test/` contengan las imágenes en formato BMP.
   - Las imágenes deben ser en escala de grises o binarias, y preferiblemente de tamaño uniforme (ej., 28x28 píxeles).

2. **Ejecutar el Script**:
   Desde la raíz del proyecto, ejecuta:

   ```bash
   python main.py
   ```

   Esto ejecutará las dos fases:
   - **Fase 1**: Aplica ruido artificial al CFP y genera gráficas de las imágenes ruidosas y recuperadas.
   - **Fase 2**: Evalúa las imágenes de prueba a mano alzada y genera gráficas de las imágenes de prueba y recuperadas.

3. **Ver los Resultados**:
   - Las gráficas se guardarán como archivos PNG en la raíz del proyecto, con nombres como `resultado_numeros_patronX_<tipo_ruido>_<porcentaje>_fase1.png` (Fase 1) o `resultado_numeros_patronX_fase2.png` (Fase 2).
   - También se mostrarán las gráficas en pantalla durante la ejecución.

## Notas

- Asegúrate de tener suficiente espacio en disco para las imágenes generadas.
- Si encuentras problemas de compatibilidad con las versiones de las librerías, verifica que estás usando Python 3.12.

## Autor

Edwin BErnardo Cruz Villalba - Estudiante de ISC en ESCOM - IPN.