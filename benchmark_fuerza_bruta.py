import argparse
import math
import subprocess
import sys
import time

from Fuerza_bruta import Point, enumerar_triangulaciones_fuerza_bruta

TAMANOS_POR_DEFECTO = (6, 20, 24, 120, 250)


def crear_poligono_convexo(n):
    return [
        Point(
            math.cos(2 * math.pi * i / n),
            math.sin(2 * math.pi * i / n),
            i,
        )
        for i in range(n)
    ]


def catalan(m):
    return math.comb(2 * m, m) // (m + 1)


def medir_tamano(n, limite_segundos, max_triangulaciones):
    esperado = catalan(n - 2)
    if esperado > max_triangulaciones:
        print(
            f"{n:>3} | {'—':>7} | {esperado:>25} | "
            f"omitido (límite: {max_triangulaciones})"
        )
        return

    inicio = time.perf_counter()
    try:
        resultado = subprocess.run(
            [sys.executable, __file__, "--worker", str(n)],
            capture_output=True,
            text=True,
            timeout=limite_segundos,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print(
            f"{n:>3} | >{limite_segundos:>6.1f}s | "
            f"{esperado:>25} | límite de tiempo"
        )
        return

    duracion = time.perf_counter() - inicio
    if resultado.returncode != 0:
        print(f"{n:>3} | {duracion:>7.3f}s | error al ejecutar")
        if resultado.stderr:
            print(resultado.stderr.strip())
        return

    try:
        cantidad = int(resultado.stdout.strip())
    except ValueError:
        print(f"Salida inesperada para n={n}: {resultado.stdout!r}")
        return

    estado = "OK" if cantidad == esperado else f"esperaba {esperado}"
    print(f"{n:>3} | {duracion:>7.3f}s | {cantidad:>25} | {estado}")


def main():
    parser = argparse.ArgumentParser(
        description="Mide la fuerza bruta exhaustiva en polígonos convexos."
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        help="Tamaños a evaluar (por defecto: 6 20 24 120 250).",
    )
    parser.add_argument(
        "--max-n",
        type=int,
        help="Evalúa consecutivamente desde 4 hasta este tamaño.",
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument(
        "--max-triangulations",
        type=int,
        default=100_000,
        help="Omite casos cuyo conteo esperado exceda este límite.",
    )
    parser.add_argument("--worker", type=int, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.worker is not None:
        poligono = crear_poligono_convexo(args.worker)
        print(len(enumerar_triangulaciones_fuerza_bruta(poligono)))
        return

    if args.sizes is not None and args.max_n is not None:
        parser.error("usa --sizes o --max-n, pero no ambos")
    if args.max_n is not None and args.max_n < 4:
        parser.error("--max-n debe ser al menos 4")
    if args.timeout <= 0:
        parser.error("--timeout debe ser mayor que 0")
    if args.max_triangulations < 1:
        parser.error("--max-triangulations debe ser al menos 1")
    if args.sizes is not None:
        tamanos = args.sizes
    elif args.max_n is not None:
        tamanos = range(4, args.max_n + 1)
    else:
        tamanos = TAMANOS_POR_DEFECTO

    if any(n < 4 for n in tamanos):
        parser.error("todos los tamaños deben ser al menos 4")

    print("  n |  tiempo | triangulaciones esperadas | resultado")
    for n in tamanos:
        medir_tamano(n, args.timeout, args.max_triangulations)


if __name__ == "__main__":
    main()
