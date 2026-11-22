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
