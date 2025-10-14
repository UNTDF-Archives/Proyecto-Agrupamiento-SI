from ucimlrepo import fetch_ucirepo
import pandas as pd

# Configurar pandas para mejor visualización
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
pd.set_option('display.max_rows', 100)      # Mostrar hasta 100 filas
pd.set_option('display.width', None)        # Ancho automático
pd.set_option('display.max_colwidth', None) # Mostrar contenido completo de columnas

# Obtener el dataset "Adult" (id=2)
adult = fetch_ucirepo(id=2)

# Data como DataFrames de pandas
X = adult.data.features
y = adult.data.targets

df = pd.concat([X, y], axis=1)

# Mostrar información del dataset
print("=" * 80)
print("INFORMACIÓN DEL DATASET")
print("=" * 80)
print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas\n")
df.info()

print("\n" + "=" * 80)
print("PRIMERAS 10 FILAS")
print("=" * 80)
print(df.head(10))

print("\n" + "=" * 80)
print("ESTADÍSTICAS DESCRIPTIVAS")
print("=" * 80)
print(df.describe())

print("\n" + "=" * 80)
print("VALORES NULOS")
print("=" * 80)
print(df.isnull().sum())
