# Triangulación y Problema de la Galeria de Arte

Proyecto final de Estructura de Datos y Algoritmos. Dado un polígono simple de n vértices, calcula una triangulación y coloca cámaras para vigilar el recinto completo. El teorema de Chvátal garantiza que ⌊n/3⌋ cámaras siempre bastan.

## Cómo ejecutar la fuerza bruta

Todos los comandos se ejecutan desde la **raíz del repositorio**.

Para ejecutar la implementación exhaustiva del archivo raíz:

```bash
python Fuerza_bruta.py
```

También existe `src/fuerza_bruta.py`, que se ejecuta por separado:

```bash
python -m src.fuerza_bruta
```

La versión del archivo raíz enumera todas las triangulaciones posibles y escoge la que usa menos cámaras. La versión de `src/` sigue el algoritmo de recorte de orejas. Ambos imprimen ejemplos; para probar la versión exhaustiva usa el primer comando.

## Cómo ejecutar las pruebas unitarias
```bash
python -m unittest discover -s tests -p "test*.py" -v
python -m unittest tests.tests_fuerza_bruta -v
python -m unittest tests.tests_dcel -v
python -m unittest tests.test_monotone -v
```

## Cómo medir cuándo se vuelve lento

Las pruebas unitarias revisan que el resultado sea correcto; no sirven para medir hasta qué tamaño tarda demasiado. Para ese experimento, desde la raíz ejecuta:

```bash
python benchmark_fuerza_bruta.py --timeout 5
```

Por defecto, evalúa polígonos convexos regulares de 6, 20, 24, 120 y 250 vértices. Para cada uno calcula el conteo esperado según el número de Catalan `C_(n-2)`. Los casos que excedan 100.000 triangulaciones se omiten antes de ejecutarse, ya que el algoritmo exhaustivo guarda todas las triangulaciones en memoria; los demás se ejecutan en procesos separados con límite de tiempo, y un timeout no impide continuar con los siguientes tamaños.

Puedes elegir otros tamaños con `--sizes 6 8 10` o usar `--max-n 12` para evaluar consecutivamente desde 4 hasta 12. Ajusta el timeout con `--timeout 5` y el umbral seguro de resultados con `--max-triangulations 100000`.

## Cómo funciona la versión exhaustiva
1. Construye las diagonales que quedan dentro del polígono.
2. Prueba combinaciones de `n - 3` diagonales y descarta las que se cruzan o no forman una cobertura válida.
3. Para cada triangulación, crea el grafo dual y colorea sus vértices con 3 colores.
4. Elige la clase de color más pequeña como conjunto de cámaras, y conserva la triangulación con menos cámaras.

Las pruebas de `tests/tests_fuerza_bruta.py` comprueban que un cuadrado produce 2 triangulaciones y un hexágono convexo 14. También verifican que cada resultado tenga `n - 2` triángulos, cubra el área, mantenga el árbol dual esperado y permita colocar cámaras dentro del límite. El tiempo crece rápidamente al aumentar el número de vértices, porque se exploran combinaciones.

## Cómo ejecutar el algoritmo óptimo

El proyecto requiere **Python 3.10 o superior**. El núcleo del algoritmo y las pruebas unitarias usan únicamente la librería estándar de Python; solo el visualizador gráfico requiere `matplotlib` (`pip install matplotlib`).

Todos los comandos del algoritmo óptimo se ejecutan como módulos desde la **raíz del repositorio** (sin usar el botón Play de VS Code ni rutas directas como `python src/algoritmo_optimo.py`).

Para ejecutar una verificación directa sobre el polígono en L de 6 vértices y un polígono estrella de 150 vértices:

```bash
python -m src.ver_resultado
```

Imprime las diagonales trazadas, los `n - 2` triángulos resultantes, la 3-coloración asignada a cada vértice, las ubicaciones óptimas de las cámaras y comprueba que la suma del área de los triángulos coincida con el área original del polígono.

## Cómo ejecutar las pruebas unitarias del algoritmo óptimo

```bash
python -m unittest tests.test_algoritmo_optimo -v
```

Las pruebas de `tests/test_algoritmo_optimo.py` verifican el funcionamiento de `ArrayQueue`, `BST` y `DCEL` (aristas gemelas `twin` e inserción de diagonales), la clasificación de los 5 tipos de vértices (`START`, `END`, `SPLIT`, `MERGE` y `REGULAR`), el ejemplo en L de 6 vértices, instancias mayores a 100 vértices (peine de Chvátal de 120 vértices y polígono estrella de 250 vértices) y las excepciones ante polígonos inválidos.

## Cómo generar polígonos grandes y registrar resultados (algoritmo óptimo)

Para evaluar el desempeño y la escalabilidad en polígonos grandes sin capturar vértices manualmente, ejecuta en orden desde la raíz:

1. Generar o actualizar el dataset de polígonos simples (`L_6`, `estrella_20`, `peine_24`, `peine_120` y `estrella_250`) en `data/poligonos_benchmark.json`:

```bash
python -m src.administrar_dataset
```

2. Medir tiempos de ejecución en CPU, conteo de operaciones e invariantes geométricos (`n - 2` triángulos, `n - 3` diagonales, `≤ ⌊n/3⌋` cámaras y conservación de área):

```bash
python -m src.registrar_resultados
```

Este script guarda una tabla alineada en `resultados/tabla_pruebas_optimo.txt` y acumula el historial de mediciones en `resultados/historial_pruebas_optimo.csv`.

3. Generar las gráficas de triangulación, 3-coloración y ubicación de cámaras en la carpeta `graficas/`:

```bash
python -m src.visualizador_optimo
```

## Cómo funciona el algoritmo óptimo
1. Construye una lista doblemente ligada circular (`NodoVertice`) y una estructura `DCEL` orientada en sentido antihorario para representar vértices, caras y medias aristas gemelas (`MediaArista`).
2. Clasifica cada vértice en `START`, `END`, `SPLIT`, `MERGE` o `REGULAR` mediante el producto cruz (`Point.crossProduct`) y ejecuta un barrido plano (`Plane Sweep`) de arriba hacia abajo apoyado en una cola (`ArrayQueue`) y un árbol de búsqueda binaria (`BST`) para dividir el polígono en piezas `y`-monótonas en tiempo `O(n log n)`.
3. Triangula cada subpolígono `y`-monótono en tiempo lineal `O(n)` recorriendo sus cadenas izquierda y derecha con una pila (`Stack`).
4. Construye el árbol dual de la triangulación, asigna 3 colores `{0, 1, 2}` mediante un recorrido en anchura (`BFS` con `ArrayQueue`) y elige la clase de color con menos vértices para ubicar a lo más `⌊n/3⌋` cámaras.

A diferencia de la versión exhaustiva, el algoritmo óptimo evita explorar combinaciones exponenciales y resuelve polígonos de cientos de vértices en fracciones de segundo manteniendo la validez geométrica y la cota teórica de Fisk.