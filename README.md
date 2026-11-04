# Triangulación y Problema de la Galeria de Arte

Proyecto final de Estructura de Datos y Algoritmos. Dado un polígono simple de n vértices, calcula una triangulación y coloca cámaras para vigilar el recinto completo. El teorema de Chvátal garantiza que ⌊n/3⌋ cámaras siempre bastan.

## Cómo ejecutar la fuerza bruta

Todos los comandos se ejecutan desde la **raíz del repositorio** (la carpeta triangulación-galería-arte)

1. Clonar el repositorio y entrar a la carpeta:

```bash
git clone [https://github.com/estrellitaaa15/triangulacion-galeria-arte](https://github.com/estrellitaaa15/triangulacion-galeria-arte)

cd triangulacion-galeria-arte
```

2. Ejecutar:
```bash
python -m src.fuerza_bruta
```

Imprime los triángulos, el árbol dual, la coloración y las cámaras de dos polígonos de ejemplo.
* No usar el botón del play de VS Code ni de python src/fuerza_bruta.py

## Cómo ejecutar las pruebas unitarias
```bash
python -m unittest discover -s tests -p "test*.py" -v
```

## Cómo funciona la fuerza bruta
1. **Triangulación (recorte de orejas):** se busca un vértice conexo cuyo triángulo no contenga otros vérices, se corta y se repite. Complejidad O(n³).
2. **Grafo dual:** cada triángulo es un nodo; dos triángulos se conectan si comparten una diagonal.
3. **3-Coloración:** se recorre el árbol dual con BFS asignando 3 colores a los vértices
4. **Cámaras:** se elige el color con menos vértices que son lo a lo más ⌊n/3⌋.
