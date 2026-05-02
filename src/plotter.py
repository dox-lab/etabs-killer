from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def _get_node_index(ids, node_id):
    return np.where(ids == node_id)[0][0]


def _set_axes_real_scale(ax, coords):
    """
    Mantiene proporciones reales en X, Y, Z.
    Evita que matplotlib deforme visualmente la estructura.
    """
    x = coords[:, 0]
    y = coords[:, 1]
    z = coords[:, 2]

    x_mid = (x.max() + x.min()) / 2
    y_mid = (y.max() + y.min()) / 2
    z_mid = (z.max() + z.min()) / 2

    max_range = max(
        x.max() - x.min(),
        y.max() - y.min(),
        z.max() - z.min(),
    )

    if max_range == 0:
        max_range = 1

    ax.set_xlim(x_mid - max_range / 2, x_mid + max_range / 2)
    ax.set_ylim(y_mid - max_range / 2, y_mid + max_range / 2)
    ax.set_zlim(z_mid - max_range / 2, z_mid + max_range / 2)

    ax.set_box_aspect([1, 1, 1])


def _draw_local_axes(ax, xi, xj, scale=0.4):
    """
    Dibuja eje local x del elemento.
    Por ahora se dibuja solo el eje axial local.
    """
    direction = xj - xi
    length = np.linalg.norm(direction)

    if length == 0:
        return

    ex = direction / length
    center = (xi + xj) / 2

    ax.quiver(
        center[0], center[1], center[2],
        ex[0] * scale, ex[1] * scale, ex[2] * scale,
        color="orange",
        linewidth=1.5,
        arrow_length_ratio=0.25,
    )

    ax.text(
        center[0] + ex[0] * scale,
        center[1] + ex[1] * scale,
        center[2] + ex[2] * scale,
        "x'",
        color="orange",
        fontsize=8,
    )


def _draw_support(ax, point, restrained_xyz, size=0.25, color="green"):
    """
    Dibuja restricciones.

    Si el nodo está restringido en Ux, Uy y Uz, se representa con una pirámide.
    Si solo hay algunas restricciones, se dibujan flechas verdes en las direcciones restringidas.
    """
    ux, uy, uz = restrained_xyz

    if ux == 1 and uy == 1 and uz == 1:
        x, y, z = point

        base = np.array([
            [x - size, y - size, z - size],
            [x + size, y - size, z - size],
            [x + size, y + size, z - size],
            [x - size, y + size, z - size],
        ])

        apex = np.array([x, y, z])

        faces = [
            [base[0], base[1], apex],
            [base[1], base[2], apex],
            [base[2], base[3], apex],
            [base[3], base[0], apex],
            [base[0], base[1], base[2], base[3]],
        ]

        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        pyramid = Poly3DCollection(
            faces,
            alpha=0.6,
            facecolor=color,
            edgecolor="black",
            linewidth=0.5,
        )

        ax.add_collection3d(pyramid)

    else:
        if ux == 1:
            ax.quiver(
                point[0], point[1], point[2],
                size, 0, 0,
                color=color,
                linewidth=1.5,
                arrow_length_ratio=0.25,
            )

        if uy == 1:
            ax.quiver(
                point[0], point[1], point[2],
                0, size, 0,
                color=color,
                linewidth=1.5,
                arrow_length_ratio=0.25,
            )

        if uz == 1:
            ax.quiver(
                point[0], point[1], point[2],
                0, 0, size,
                color=color,
                linewidth=1.5,
                arrow_length_ratio=0.25,
            )


def plot_estructura(
    nodos,
    elementos,
    cargas,
    restricciones,
    config=None,
    save_path="images/estructura.png",
):
    if config is None:
        config = {}

    show_node_labels = config.get("show_node_labels", True)
    show_element_labels = config.get("show_element_labels", True)
    show_local_axes = config.get("show_local_axes", False)

    load_scale = config.get("load_scale", 0.1)
    load_color = config.get("load_color", "red")
    load_width = config.get("load_width", 2.0)

    element_color = config.get("element_color", "black")
    element_width = config.get("element_width", 2.0)

    node_color = config.get("node_color", "blue")
    node_size = config.get("node_size", 35)

    support_color = config.get("support_color", "green")
    support_size = config.get("support_size", 0.25)

    local_axis_scale = config.get("local_axis_scale", 0.4)

    ids = nodos[:, 0].astype(int)
    coords = nodos[:, 1:4].astype(float)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(projection="3d")

    # Elementos
    for elem in elementos:
        elem_id = int(elem[0])
        ni = int(elem[1])
        nj = int(elem[2])

        i = _get_node_index(ids, ni)
        j = _get_node_index(ids, nj)

        xi = coords[i]
        xj = coords[j]

        ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            color=element_color,
            linewidth=element_width,
        )

        center = (xi + xj) / 2

        if show_element_labels:
            ax.text(
                center[0],
                center[1],
                center[2],
                f"E{elem_id}",
                fontsize=8,
                color="black",
            )

        if show_local_axes:
            _draw_local_axes(
                ax,
                xi,
                xj,
                scale=local_axis_scale,
            )

    # Nodos
    ax.scatter(
        coords[:, 0],
        coords[:, 1],
        coords[:, 2],
        color=node_color,
        s=node_size,
    )

    if show_node_labels:
        for node_id, coord in zip(ids, coords):
            ax.text(
                coord[0],
                coord[1],
                coord[2],
                f"N{node_id}",
                fontsize=8,
                color=node_color,
            )

    # Cargas
    for fila in cargas:
        node_id = int(fila[0])
        fx, fy, fz = fila[1:4].astype(float)

        i = _get_node_index(ids, node_id)
        point = coords[i]

        ax.quiver(
            point[0], point[1], point[2],
            fx * load_scale,
            fy * load_scale,
            fz * load_scale,
            color=load_color,
            linewidth=load_width,
            arrow_length_ratio=0.25,
        )

        ax.text(
            point[0] + fx * load_scale,
            point[1] + fy * load_scale,
            point[2] + fz * load_scale,
            f"({fx:.2f}, {fy:.2f}, {fz:.2f})",
            color=load_color,
            fontsize=8,
        )

    # Restricciones
    for fila in restricciones:
        node_id = int(fila[0])
        restrained_xyz = fila[1:4].astype(int)

        i = _get_node_index(ids, node_id)
        point = coords[i]

        _draw_support(
            ax,
            point,
            restrained_xyz,
            size=support_size,
            color=support_color,
        )

    ax.set_title("Estructura 3D con cargas y restricciones")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    _set_axes_real_scale(ax, coords)

    Path(save_path).parent.mkdir(exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")

    print(f"Imagen guardada en: {save_path}")


def plot_deformada(
    nodos,
    elementos,
    desplazamientos,
    config=None,
    save_path="images/deformada.png",
):
    if config is None:
        config = {}

    deformation_scale = config.get("deformation_scale", 10)

    show_node_labels = config.get("show_node_labels", True)
    show_element_labels = config.get("show_element_labels", False)

    original_color = config.get("original_color", "gray")
    original_width = config.get("original_width", 1.0)

    deformed_color = config.get("deformed_color", "red")
    deformed_width = config.get("deformed_width", 2.0)

    node_size = config.get("node_size", 35)

    ids = nodos[:, 0].astype(int)
    coords = nodos[:, 1:4].astype(float)

    coords_def = coords.copy()

    for i in range(len(coords)):
        dx, dy, dz = desplazamientos[3 * i:3 * i + 3]
        coords_def[i] += deformation_scale * np.array([dx, dy, dz])

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(projection="3d")

    # Estructura original
    for elem in elementos:
        ni = int(elem[1])
        nj = int(elem[2])

        i = _get_node_index(ids, ni)
        j = _get_node_index(ids, nj)

        xi = coords[i]
        xj = coords[j]

        ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            "--",
            color=original_color,
            linewidth=original_width,
        )

    # Estructura deformada
    for elem in elementos:
        elem_id = int(elem[0])
        ni = int(elem[1])
        nj = int(elem[2])

        i = _get_node_index(ids, ni)
        j = _get_node_index(ids, nj)

        xi = coords_def[i]
        xj = coords_def[j]

        ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            color=deformed_color,
            linewidth=deformed_width,
        )

        if show_element_labels:
            center = (xi + xj) / 2
            ax.text(
                center[0],
                center[1],
                center[2],
                f"E{elem_id}",
                fontsize=8,
                color=deformed_color,
            )

    ax.scatter(
        coords_def[:, 0],
        coords_def[:, 1],
        coords_def[:, 2],
        color=deformed_color,
        s=node_size,
    )

    if show_node_labels:
        for node_id, coord in zip(ids, coords_def):
            ax.text(
                coord[0],
                coord[1],
                coord[2],
                f"N{node_id}",
                fontsize=8,
                color=deformed_color,
            )

    ax.set_title(f"Deformada 3D, factor = {deformation_scale}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    all_coords = np.vstack([coords, coords_def])
    _set_axes_real_scale(ax, all_coords)

    Path(save_path).parent.mkdir(exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")

    print(f"Imagen guardada en: {save_path}")

def plot_deformada_interactiva(
    nodos,
    elementos,
    desplazamientos,
    reacciones,
    fuerzas_internas,
    config=None,
    save_path="images/deformada_interactiva.png",
):
    import mplcursors

    if config is None:
        config = {}

    deformation_scale = config.get("deformation_scale", 10)

    ids = nodos[:, 0].astype(int)
    coords = nodos[:, 1:4].astype(float)

    coords_def = coords.copy()

    for i in range(len(coords)):
        dx, dy, dz = desplazamientos[3 * i:3 * i + 3]
        coords_def[i] += deformation_scale * np.array([dx, dy, dz])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d")

    hover_artists = []

    # Estructura original
    for elem in elementos:
        ni = int(elem[1])
        nj = int(elem[2])

        i = _get_node_index(ids, ni)
        j = _get_node_index(ids, nj)

        xi = coords[i]
        xj = coords[j]

        ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            "--",
            color="gray",
            linewidth=1,
            alpha=0.5,
        )

    # Barras deformadas con tooltip
    for k, elem in enumerate(elementos):
        elem_id = int(elem[0])
        ni = int(elem[1])
        nj = int(elem[2])

        i = _get_node_index(ids, ni)
        j = _get_node_index(ids, nj)

        xi = coords_def[i]
        xj = coords_def[j]

        axial = fuerzas_internas[k, 3]

        line, = ax.plot(
            [xi[0], xj[0]],
            [xi[1], xj[1]],
            [xi[2], xj[2]],
            color=config.get("deformed_color", "red"),
            linewidth=config.get("deformed_width", 2.5),
            picker=True,
        )

        line.etabs_info = (
            f"Elemento E{elem_id}\n"
            f"Nodos: {ni} - {nj}\n"
            f"Fuerza axial: {axial:.6e}"
        )

        hover_artists.append(line)

    # Nodos deformados con tooltip
    node_scatter = ax.scatter(
        coords_def[:, 0],
        coords_def[:, 1],
        coords_def[:, 2],
        color=config.get("node_color", "blue"),
        s=config.get("node_size", 40),
        depthshade=True,
    )

    node_scatter.etabs_type = "nodes"
    hover_artists.append(node_scatter)

    # Reacciones con tooltip
    reaction_points = []
    reaction_labels = []

    # Escala geométrica de la estructura
    bbox = coords.max(axis=0) - coords.min(axis=0)
    L_ref = np.max(bbox)

    # Magnitud máxima de reacciones
    Rmax = np.max(np.abs(reacciones))

    # Evitar división por cero
    if Rmax < 1e-12:
        Rmax = 1.0

    # Factor automático (ajustable)
    reaction_scale = config.get("reaction_scale", 0.2 * L_ref / Rmax)
    reaction_color = config.get("reaction_color", "green")
    reaction_width = config.get("reaction_width", 2.0)

    for i, node_id in enumerate(ids):
        rx, ry, rz = reacciones[3 * i:3 * i + 3]

        if abs(rx) > 1e-10 or abs(ry) > 1e-10 or abs(rz) > 1e-10:
            p = coords[i]

            ax.quiver(
                p[0], p[1], p[2],
                rx * reaction_scale,
                ry * reaction_scale,
                rz * reaction_scale,
                color=reaction_color,
                linewidth=reaction_width,
                arrow_length_ratio=0.25,
            )

            reaction_points.append(p)
            reaction_labels.append(
                f"Reacción nodo N{node_id}\n"
                f"Rx: {rx:.6e}\n"
                f"Ry: {ry:.6e}\n"
                f"Rz: {rz:.6e}"
            )

    if len(reaction_points) > 0:
        reaction_points = np.array(reaction_points)

        reaction_scatter = ax.scatter(
            reaction_points[:, 0],
            reaction_points[:, 1],
            reaction_points[:, 2],
            color=reaction_color,
            s=80,
            marker="^",
        )

        reaction_scatter.etabs_type = "reactions"
        reaction_scatter.etabs_labels = reaction_labels

        hover_artists.append(reaction_scatter)

    # Tooltips
    cursor = mplcursors.cursor(hover_artists, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        artist = sel.artist

        if hasattr(artist, "etabs_info"):
            sel.annotation.set_text(artist.etabs_info)

        elif hasattr(artist, "etabs_type") and artist.etabs_type == "nodes":
            i = sel.index

            node_id = ids[i]
            ux, uy, uz = desplazamientos[3 * i:3 * i + 3]

            sel.annotation.set_text(
                f"Nodo N{node_id}\n"
                f"Ux: {ux:.6e}\n"
                f"Uy: {uy:.6e}\n"
                f"Uz: {uz:.6e}"
            )

        elif hasattr(artist, "etabs_type") and artist.etabs_type == "reactions":
            i = sel.index
            sel.annotation.set_text(artist.etabs_labels[i])

    ax.set_title(f"Deformada interactiva 3D, factor = {deformation_scale}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    all_coords = np.vstack([coords, coords_def])
    _set_axes_real_scale(ax, all_coords)

    Path(save_path).parent.mkdir(exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")

    print(f"Imagen guardada en: {save_path}")