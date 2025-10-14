# Proyecto de Agrupamiento con Distancia de Gower


## Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)


## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/LucasA21/Proyecto-Agrupamiento-SI
cd Proyecto-Agrupamiento-SI
```

### 2. Crear un entorno virtual

```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```



### Dependencias incluidas:

- `ucimlrepo==0.0.7` - Para obtener datasets de UCI ML Repository
- `pandas==2.3.3` - Manipulación de datos
- `numpy==2.3.3` - Operaciones numéricas vectorizadas
- `psutil==7.1.0` - Monitoreo de recursos del sistema
- `seaborn==0.13.2` - Visualización estadística
- `matplotlib==3.10.7` - Gráficos y visualizaciones
- `plotly==6.3.1` - Visualizaciones interactivas
- `jupyter==1.1.1` - Metapaquete de Jupyter
- `notebook==7.3.2` - Jupyter Notebook
- `jupyterlab==4.3.5` - JupyterLab (interfaz más moderna)
- `scikit-learn==1.6.1` - Machine Learning (usado para imputación de datos)

## Ejecución

### Opción 1: Jupyter Notebook

1. Iniciar Jupyter Notebook:

```bash
jupyter notebook
```

### Opción 2: JupyterLab

1. Iniciar JupyterLab:

```bash
jupyter lab
```

(Para JupyterLab hay que instalar las extenciones de vscode necesarias)

## Referencias

- Dataset Adult (Census Income): [UCI ML Repository](https://archive.ics.uci.edu/dataset/2/adult)


