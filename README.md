# etabs_killer

Proyecto de análisis estructural en Python desarrollado **desde cero**, sin uso de librerías especializadas de análisis estructural. El objetivo es construir un pipeline claro y modular que permita:

1. Leer datos estructurales desde un archivo Excel
2. Ejecutar el análisis estructural (formulación y solución propia)
3. Visualizar la estructura, cargas y deformada

---

## 🧠 Filosofía del proyecto

- Implementación **100% propia** del análisis estructural
- Uso de **mínimas librerías externas**
- Código **modular, transparente y extensible**
- Enfoque educativo + escalable hacia aplicaciones reales

---

## 📁 Estructura del proyecto

```

etabs_killer/
│
├── README.md
├── environment.yml
├── .gitignore
│
├── main.py                  # Pipeline principal
│
├── src/
│   ├── reader/              # Lectura del Excel
│   │   └── reader.py
│   │
│   ├── analyzer/            # Núcleo de análisis estructural
│   │   └── analyzer.py
│   │
│   ├── plotter/             # Visualización
│   │   └── plotter.py
│
├── data/
│   └── Datos.xlsx           # Input estructural
│
├── images/                  # Outputs (gráficos)

````

---

## ⚙️ Flujo del programa

El pipeline completo se ejecuta desde:

```bash
python main.py
````

### Etapas:

1. **Reader**

   * Lee el archivo `Datos.xlsx`
   * Extrae nodos, elementos, propiedades, cargas y condiciones de borde

2. **Analyzer**

   * Ensambla matrices globales
   * Aplica condiciones de frontera
   * Resuelve el sistema de ecuaciones
   * Calcula desplazamientos y fuerzas internas

3. **Plotter**

   * Grafica:

     * Estructura original
     * Cargas aplicadas
     * Estructura deformada
   * Guarda imágenes en `/images`

---

## 📥 Input esperado (Excel)

El archivo `Datos.xlsx` debe contener hojas estructuradas (por ejemplo):

* `nodes` → coordenadas nodales
* `elements` → conectividad
* `materials` → propiedades mecánicas
* `sections` → propiedades geométricas
* `loads` → cargas nodales o distribuidas
* `supports` → restricciones

> ⚠️ El formato exacto será definido y estandarizado en el módulo `reader`.

---

## 📤 Outputs

Se generan en la carpeta:

```
/images
```

Incluyen:

* Estructura original
* Estructura deformada
* Visualización de cargas

---

## 🧪 Dependencias

Se busca usar **la menor cantidad posible** de librerías:

* `numpy` → operaciones numéricas
* `pandas` → lectura de Excel
* `matplotlib` → visualización

---

## 🧱 Instalación (Conda)

```bash
conda env create -f environment.yml
conda activate etabs_killer
```

---

## 🚀 Ejecución

```bash
python main.py
```

---

## 🛠️ Estado del proyecto

🔧 En desarrollo inicial:

* [x] Definición de arquitectura
* [ ] Implementación del reader
* [ ] Implementación del solver estructural
* [ ] Implementación del graficador
* [ ] Validación con casos simples

---

## 🎯 Roadmap

* Soporte para estructuras 2D y 3D
* Elementos tipo barra (truss) → luego frame
* Cargas distribuidas
* Análisis modal (futuro)
* Interfaz más robusta de inputs

---

## ⚠️ Notas

* Este proyecto **no busca reemplazar software comercial**, sino entender y replicar sus fundamentos.
* El nombre `etabs_killer` es solo un codename 😄

---

## 👨‍💻 Autor

Daniel Medina
MSc Student – Structural / SHM
UTEC – Lima, Perú
