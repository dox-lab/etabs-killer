import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_estructura(
    nodos,
    elementos,
    cargas,
    restricciones,
    save_path="images/estructura.png",
    show=False,
):
    ids = nodos[:, 0].astype(int)
    coords = nodos[:, 1:4]

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Elementos
    for elem in elementos:
        ni, nj = int(elem[1]), int(elem[2])
        i = np.where(ids == ni)[0][0]
        j = np.where(ids == nj)[0][0]

        xi, xj = coords[i], coords[j]

        ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            "k-",
            linewidth=2,
        )

    # Nodos
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], color="b")

    # Cargas
    scale = 0.1
    for fila in cargas:
        nodo = int(fila[0])
        fx, fy, fz = fila[1:4]

        i = np.where(ids == nodo)[0][0]
        x = coords[i]

        ax.quiver(
            x[0], x[1], x[2],
            fx * scale, fy * scale, fz * scale,
            color="r",
        )

    # Restricciones
    for fila in restricciones:
        nodo = int(fila[0])
        ux, uy, uz = fila[1:4]

        i = np.where(ids == nodo)[0][0]
        x = coords[i]

        if ux == 1:
            ax.quiver(x[0], x[1], x[2], 0.2, 0, 0, color="g")
        if uy == 1:
            ax.quiver(x[0], x[1], x[2], 0, 0.2, 0, color="g")
        if uz == 1:
            ax.quiver(x[0], x[1], x[2], 0, 0, 0.2, color="g")

    ax.set_title("Estructura con cargas")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    Path(save_path).parent.mkdir(exist_ok=True)
    plt.savefig(save_path, dpi=300)

    print(f"Imagen guardada en: {save_path}")

    if show:
        plt.show()


def plot_deformada(
    nodos,
    elementos,
    desplazamientos,
    scale=10,
    save_path="images/deformada.png",
    show=False,
):
    ids = nodos[:, 0].astype(int)
    coords = nodos[:, 1:4]

    coords_def = coords.copy()

    for i in range(len(coords)):
        dx, dy, dz = desplazamientos[3*i:3*i+3]
        coords_def[i] += scale * np.array([dx, dy, dz])

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # original
    for elem in elementos:
        ni, nj = int(elem[1]), int(elem[2])
        i = np.where(ids == ni)[0][0]
        j = np.where(ids == nj)[0][0]

        xi, xj = coords[i], coords[j]

        ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            "--",
            color="gray",
        )

    # deformada
    for elem in elementos:
        ni, nj = int(elem[1]), int(elem[2])
        i = np.where(ids == ni)[0][0]
        j = np.where(ids == nj)[0][0]

        xi, xj = coords_def[i], coords_def[j]

        ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            "r-",
            linewidth=2,
        )

    ax.scatter(coords_def[:, 0], coords_def[:, 1], coords_def[:, 2], color="r")

    ax.set_title(f"Deformada (factor = {scale})")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    Path(save_path).parent.mkdir(exist_ok=True)
    plt.savefig(save_path, dpi=300)

    print(f"Imagen guardada en: {save_path}")

    if show:
        plt.show()