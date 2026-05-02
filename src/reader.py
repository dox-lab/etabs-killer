import numpy as np
import pandas as pd


def leer_excel(ruta_excel, hoja="Hoja1"):
    """
    Lee el archivo Excel del modelo estructural.

    Formato actual del Excel:
    - Nodos:        B:E  -> Nodo, X, Y, Z
    - Elementos:    G:I  -> Elemento, Nodo i, Nodo j
    - Cargas:       K:N  -> Nodo, Fx, Fy, Fz
    - Restricciones P:V  -> Nodo, Ux, Uy, Uz, Rx, Ry, Rz

    Por ahora solo se leen los datos tal como están.
    """

    nodos = pd.read_excel(
        ruta_excel,
        sheet_name=hoja,
        usecols="B:E",
        skiprows=3,
        header=None,
    ).dropna().to_numpy()

    elementos = pd.read_excel(
        ruta_excel,
        sheet_name=hoja,
        usecols="G:I",
        skiprows=3,
        header=None,
    ).dropna().to_numpy()

    cargas = pd.read_excel(
        ruta_excel,
        sheet_name=hoja,
        usecols="K:N",
        skiprows=3,
        header=None,
    ).dropna().to_numpy()

    restricciones = pd.read_excel(
        ruta_excel,
        sheet_name=hoja,
        usecols="P:V",
        skiprows=3,
        header=None,
    ).dropna().to_numpy()

    return nodos, elementos, cargas, restricciones