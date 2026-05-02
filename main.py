import matplotlib.pyplot as plt

from src.reader import leer_excel
from src.analyzer import analizar_armadura_3d, imprimir_resultados
from src.plotter import (
    plot_estructura,
    plot_deformada_interactiva,
)


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

    plot_config = {
        "show_node_labels": True,
        "show_element_labels": True,
        "show_local_axes": True,

        "node_color": "blue",
        "node_size": 45,

        "deformation_scale": 10,
        "deformed_color": "red",
        "deformed_width": 2.5,

        "reaction_scale": 0.05,
        "reaction_color": "green",
        "reaction_width": 2.0,
    }

    plot_estructura(
        nodos=nodos,
        elementos=elementos,
        cargas=cargas,
        restricciones=restricciones,
        config=plot_config,
        save_path="images/estructura.png",
    )

    plot_deformada_interactiva(
        nodos=nodos,
        elementos=elementos,
        desplazamientos=resultados["desplazamientos"],
        reacciones=resultados["reacciones"],
        fuerzas_internas=resultados["fuerzas_internas"],
        config=plot_config,
        save_path="images/deformada_interactiva.png",
    )

    plt.show()


if __name__ == "__main__":
    main()