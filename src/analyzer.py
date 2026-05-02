import numpy as np


def analizar_armadura_3d(nodos, elementos, cargas, restricciones, E=2.1e7, A=0.0008):
    """
    Analiza una armadura 3D usando el método de rigidez directa.

    Parámetros
    ----------
    nodos : ndarray
        Matriz con columnas: Nodo, X, Y, Z

    elementos : ndarray
        Matriz con columnas: Elemento, Nodo i, Nodo j

    cargas : ndarray
        Matriz con columnas: Nodo, Fx, Fy, Fz

    restricciones : ndarray
        Matriz con columnas: Nodo, Ux, Uy, Uz, Rx, Ry, Rz

    E : float
        Módulo de elasticidad.

    A : float
        Área transversal.

    Retorna
    -------
    dict
        Diccionario con matriz global, fuerzas, desplazamientos,
        reacciones y fuerzas internas.
    """

    ids_nodos = nodos[:, 0].astype(int)
    coords = nodos[:, 1:4].astype(float)

    ids_elementos = elementos[:, 0].astype(int)
    conectividad = elementos[:, 1:3].astype(int)

    num_nodos = len(ids_nodos)
    num_gdl = 3 * num_nodos

    K_global = np.zeros((num_gdl, num_gdl))
    F_global = np.zeros(num_gdl)
    R_global = np.zeros(num_gdl, dtype=int)

    # =========================
    # Vector de cargas global
    # =========================
    for fila in cargas:
        nodo = int(fila[0])
        fx, fy, fz = fila[1:4]

        idx = np.where(ids_nodos == nodo)[0][0]
        gdl = 3 * idx

        F_global[gdl:gdl + 3] = [fx, fy, fz]

    # =========================
    # Vector de restricciones
    # =========================
    for fila in restricciones:
        nodo = int(fila[0])
        ux, uy, uz = fila[1:4]

        idx = np.where(ids_nodos == nodo)[0][0]
        gdl = 3 * idx

        R_global[gdl:gdl + 3] = [ux, uy, uz]

    # =========================
    # Ensamblaje de K global
    # =========================
    for elemento in conectividad:
        nodo_i = elemento[0]
        nodo_j = elemento[1]

        idx_i = np.where(ids_nodos == nodo_i)[0][0]
        idx_j = np.where(ids_nodos == nodo_j)[0][0]

        xi, yi, zi = coords[idx_i]
        xj, yj, zj = coords[idx_j]

        L = np.sqrt((xj - xi)**2 + (yj - yi)**2 + (zj - zi)**2)

        lx = (xj - xi) / L
        ly = (yj - yi) / L
        lz = (zj - zi) / L

        k = (E * A / L) * np.array([
            [ lx*lx,  lx*ly,  lx*lz, -lx*lx, -lx*ly, -lx*lz],
            [ ly*lx,  ly*ly,  ly*lz, -ly*lx, -ly*ly, -ly*lz],
            [ lz*lx,  lz*ly,  lz*lz, -lz*lx, -lz*ly, -lz*lz],
            [-lx*lx, -lx*ly, -lx*lz,  lx*lx,  lx*ly,  lx*lz],
            [-ly*lx, -ly*ly, -ly*lz,  ly*lx,  ly*ly,  ly*lz],
            [-lz*lx, -lz*ly, -lz*lz,  lz*lx,  lz*ly,  lz*lz],
        ])

        gdl_i = 3 * idx_i
        gdl_j = 3 * idx_j

        gdl_elemento = [
            gdl_i, gdl_i + 1, gdl_i + 2,
            gdl_j, gdl_j + 1, gdl_j + 2,
        ]

        for a in range(6):
            for b in range(6):
                K_global[gdl_elemento[a], gdl_elemento[b]] += k[a, b]

    # =========================
    # Aplicar restricciones
    # =========================
    gdl_libres = np.where(R_global == 0)[0]

    K_reducida = K_global[np.ix_(gdl_libres, gdl_libres)]
    F_reducida = F_global[gdl_libres]

    # =========================
    # Resolver sistema
    # =========================
    desplazamientos = np.zeros(num_gdl)
    desplazamientos[gdl_libres] = np.linalg.solve(K_reducida, F_reducida)

    # =========================
    # Reacciones
    # =========================
    reacciones = K_global @ desplazamientos - F_global

    # =========================
    # Fuerzas internas
    # =========================
    fuerzas_internas = []

    for e, elemento in enumerate(conectividad):
        nodo_i = elemento[0]
        nodo_j = elemento[1]

        idx_i = np.where(ids_nodos == nodo_i)[0][0]
        idx_j = np.where(ids_nodos == nodo_j)[0][0]

        xi, yi, zi = coords[idx_i]
        xj, yj, zj = coords[idx_j]

        L = np.sqrt((xj - xi)**2 + (yj - yi)**2 + (zj - zi)**2)

        lx = (xj - xi) / L
        ly = (yj - yi) / L
        lz = (zj - zi) / L

        u_i = desplazamientos[3*idx_i:3*idx_i + 3]
        u_j = desplazamientos[3*idx_j:3*idx_j + 3]

        delta_u = u_j - u_i

        axial = (E * A / L) * np.dot([lx, ly, lz], delta_u)

        fuerzas_internas.append([
            ids_elementos[e],
            nodo_i,
            nodo_j,
            axial,
        ])

    fuerzas_internas = np.array(fuerzas_internas)

    return {
        "K_global": K_global,
        "F_global": F_global,
        "R_global": R_global,
        "desplazamientos": desplazamientos,
        "reacciones": reacciones,
        "fuerzas_internas": fuerzas_internas,
        "gdl_libres": gdl_libres,
    }


def imprimir_resultados(nodos, resultados):
    ids_nodos = nodos[:, 0].astype(int)

    desplazamientos = resultados["desplazamientos"]
    reacciones = resultados["reacciones"]
    fuerzas_internas = resultados["fuerzas_internas"]

    print("\n=== RESULTADOS DEL ANÁLISIS ===")

    print("\n--- Desplazamientos nodales ---")
    print("Nodo\tUx\t\tUy\t\tUz")

    for i, nodo in enumerate(ids_nodos):
        ux, uy, uz = desplazamientos[3*i:3*i + 3]
        print(f"{nodo}\t{ux:.6e}\t{uy:.6e}\t{uz:.6e}")

    print("\n--- Reacciones nodales ---")
    print("Nodo\tRx\t\tRy\t\tRz")

    for i, nodo in enumerate(ids_nodos):
        rx, ry, rz = reacciones[3*i:3*i + 3]

        if abs(rx) > 1e-10 or abs(ry) > 1e-10 or abs(rz) > 1e-10:
            print(f"{nodo}\t{rx:.6e}\t{ry:.6e}\t{rz:.6e}")

    print("\n--- Fuerzas internas en elementos ---")
    print("Elemento\tNodo i\tNodo j\tFuerza axial")

    for fila in fuerzas_internas:
        elemento, nodo_i, nodo_j, axial = fila
        print(f"{int(elemento)}\t\t{int(nodo_i)}\t{int(nodo_j)}\t{axial:.6e}")

    print("\n=== ANÁLISIS COMPLETADO ===")