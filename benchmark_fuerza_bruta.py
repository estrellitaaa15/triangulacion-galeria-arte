import argparse
import math
import subprocess
import sys
import time

from Fuerza_bruta import Point, enumerar_triangulaciones_fuerza_bruta


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


def medir_tamano(n, limite_segundos):
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
        print(f"{n:>3} | >{limite_segundos:>6.1f}s | límite de tiempo")
        return False

    duracion = time.perf_counter() - inicio
    if resultado.returncode != 0:
        print(f"{n:>3} | {duracion:>7.3f}s | error al ejecutar")
        if resultado.stderr:
            print(resultado.stderr.strip())
        return False

    try:
        cantidad = int(resultado.stdout.strip())
    except ValueError:
        print(f"Salida inesperada para n={n}: {resultado.stdout!r}")
        return False

    esperado = catalan(n - 2)
    estado = "OK" if cantidad == esperado else f"esperaba {esperado}"
    print(f"{n:>3} | {duracion:>7.3f}s | {cantidad:>10} | {estado}")
    return cantidad == esperado


def main():
    parser = argparse.ArgumentParser(
        description="Mide la fuerza bruta con polígonos convexos cada vez mayores."
    )
    parser.add_argument("--max-n", type=int, default=12)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--worker", type=int, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.worker is not None:
        poligono = crear_poligono_convexo(args.worker)
        print(len(enumerar_triangulaciones_fuerza_bruta(poligono)))
        return

    if args.max_n < 4:
        parser.error("--max-n debe ser al menos 4")
    if args.timeout <= 0:
        parser.error("--timeout debe ser mayor que 0")

    print("  n |  tiempo | triangulaciones | validación")
    for n in range(4, args.max_n + 1):
        if not medir_tamano(n, args.timeout):
            print(f"Se detiene el experimento en n={n}.")
            break


if __name__ == "__main__":
    main()
