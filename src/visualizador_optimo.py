import os
import matplotlib.pyplot as plt
from src.algoritmo_optimo import triangularPoligono
from src.generador_poligonos import cargarDatasetJson


def dibujarPoligonoTriangulado(ax, coords: list, titulo: str, mostrarEtiquetas: bool = False):
    res = triangularPoligono(coords)

    # 1. Dibujar el relleno y las diagonales internas de cada triángulo
    for p1, p2, p3 in res["triangulos"]:
        xs = [p1.x, p2.x, p3.x, p1.x]
        ys = [p1.y, p2.y, p3.y, p1.y]
        ax.fill(xs, ys, color="#836AB8", alpha=0.12)
        ax.plot(xs, ys, linestyle="--", color="#836AB8", linewidth=0.9, alpha=0.85)

    # 2. Dibujar el contorno exterior del polígono
    contornoX = [p[0] for p in coords] + [coords[0][0]]
    contornoY = [p[1] for p in coords] + [coords[0][1]]
    ax.plot(contornoX, contornoY, color="#432F64", linewidth=2.2, label="Frontera P")

    # 3. Dibujar los vértices pintados según su 3-coloración {0, 1, 2}
    coloresVertices = {0: "#E63946", 1: "#2A9D8F", 2: "#F4A261"}
    for vertice, colorId in res["diccPoint"].items():
        ax.scatter(vertice.x, vertice.y, color=coloresVertices[colorId], s=45, zorder=4)
        if mostrarEtiquetas:
            ax.annotate(
                f"V{vertice.idVertice}",
                (vertice.x + 0.1, vertice.y + 0.1),
                fontsize=9,
                fontweight="bold",
                color="#222222",
            )

    # 4. Resaltar con un círculo negro dónde se colocan las cámaras óptimas
    camarasX = [c.x for c in res["camaras"]]
    camarasY = [c.y for c in res["camaras"]]
    ax.scatter(
        camarasX,
        camarasY,
        facecolors="none",
        edgecolors="black",
        s=190,
        linewidths=2.0,
        zorder=5,
        label=f"Cámaras ({len(res['camaras'])})",
    )

    ax.set_title(
        f"{titulo}\nTriángulos: {len(res['triangulos'])} | Cámaras: {len(res['camaras'])}/{res['nVertices'] // 3}",
        fontsize=10,
        fontweight="bold",
    )
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", fontsize=8)


def visualizarTodasDesdeJson(rutaJson: str = "data/poligonos_benchmark.json"):
    os.makedirs("graficas", exist_ok=True)
    datos = cargarDatasetJson(rutaJson)

    for nombrePrueba, coords in datos.items():
        fig, ax = plt.subplots(figsize=(7, 7))
        # Solo muestra etiquetas V1, V2... si el polígono tiene 20 vértices o menos para no saturar
        etiquetas = len(coords) <= 20
        dibujarPoligonoTriangulado(ax, coords, f"Prueba: {nombrePrueba} (n={len(coords)})", mostrarEtiquetas=etiquetas)

        rutaImagen = f"graficas/{nombrePrueba}.png"
        plt.tight_layout()
        plt.savefig(rutaImagen, dpi=300)
        plt.close(fig)  # Libera memoria entre gráfica y gráfica
        print(f"Gráfica guardada: {rutaImagen}")


if __name__ == "__main__":
    visualizarTodasDesdeJson()