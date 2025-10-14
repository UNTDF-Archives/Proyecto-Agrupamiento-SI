"""
Utilidades para cargar el dataset Adult desde archivos locales
"""
import pandas as pd
import numpy as np
import os

def cargar_dataset_adult():
    """
    Carga el dataset Adult completo desde los archivos locales en Data/adult/
    Combina los archivos de entrenamiento (adult.data) y prueba (adult.test)
    
    Returns:
        pd.DataFrame: Dataset Adult completo con todas las columnas (~48,842 filas)
    """
    # Obtener la ruta del directorio del proyecto (donde está utils.py)
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir las rutas a los archivos de datos
    train_path = os.path.join(project_dir, 'Data', 'adult', 'adult.data')
    test_path = os.path.join(project_dir, 'Data', 'adult', 'adult.test')
    
    # Nombres de las columnas según la documentación de UCI
    column_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
    ]
    
    # Cargar el archivo de entrenamiento
    df_train = pd.read_csv(
        train_path,
        names=column_names,
        skipinitialspace=True,
        na_values=['?', ' ?']
    )
    
    # Cargar el archivo de prueba (tiene una línea de encabezado que hay que saltar)
    df_test = pd.read_csv(
        test_path,
        names=column_names,
        skipinitialspace=True,
        na_values=['?', ' ?'],
        skiprows=1  # Saltar la primera línea que es un comentario
    )
    
    # Limpiar la columna 'income' en el conjunto de prueba (tiene un punto al final)
    df_test['income'] = df_test['income'].str.rstrip('.')
    
    # Combinar ambos DataFrames
    df = pd.concat([df_train, df_test], ignore_index=True)
    
    return df

