from src.reader import leer_excel
from src.analyzer import analizar_armadura_3d, imprimir_resultados
from src.plotter import plot_estructura, plot_deformada
import matplotlib.pyplot as plt


def main():
    ruta_excel = "data/Datos.xlsx"

    nodos, elementos, cargas, restricciones = leer_excel(ruta_excel)

    resultados = analizar_armadura_3d(
        nodos=nodos,
        elementos=elementos,
        cargas=cargas,
        restricciones=restricciones,
    )

    imprimir_resultados(nodos, resultados)

    # Graficar SIN mostrar aún
    plot_estructura(
        nodos,
        elementos,
        cargas,
        restricciones,
        show=False,
    )

    plot_deformada(
        nodos,
        elementos,
        resultados["desplazamientos"],
        scale=10,
        show=False,
    )

    # Mostrar TODAS las figuras juntas (mejor práctica)
    plt.show()


if __name__ == "__main__":
    main()