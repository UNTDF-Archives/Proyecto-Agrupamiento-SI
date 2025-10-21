# Notebook del Proyecto de Agrupamiento

Este notebook documenta todas las decisiones, consideraciones y el razonamiento detrás de cada ejercicio del proyecto.


## Ejercicio 1: Preparación de Datos

### Carga del dataset

Originalmente el dataset se cargaba usando `ucimlrepo.fetch_ucirepo(id=2)`, pero tuvimos problemas de conectividad con Python 3.13. La librería se quedaba colgada al intentar descargar los datos desde el servidor UCI. La solución fue descargar los archivos manualmente y crear una función `cargar_dataset_adult()` en `utils.py` que carga desde archivos locales.

El dataset viene en dos archivos separados:
- `adult.data`: 32,561 registros (entrenamiento)
- `adult.test`: 16,281 registros (prueba)

Los combinamos porque para clustering no necesitamos separación train/test, queremos analizar toda la población disponible. Además, el archivo de test tiene algunas particularidades que hay que limpiar, como una línea de comentario al inicio y un punto extra en la columna income.

### Clasificación de variables

Identificamos 14 variables útiles, excluyendo fnlwgt:

Variables numéricas:
- age, education-num, hours-per-week: discretas
- capital-gain, capital-loss: continuas

Variables categóricas:
- workclass, marital-status, occupation, relationship, race, sex, native-country: nominales
- education: ordinal (hay un orden claro desde Preschool hasta Doctorate)

### Exclusión de fnlwgt

La variable fnlwgt (final weight) es un peso de muestreo del censo. Indica cuántas personas de la población real representa cada registro del dataset. No es una característica de la persona, es solo un número estadístico para hacer inferencias poblacionales. 

No tiene sentido incluirla en clustering porque:
- No describe ningún atributo del individuo
- Dos personas con distinto fnlwgt no son más o menos parecidas por eso
- Contaminaría los cálculos de distancia sin aportar información real

Esta decisión la documentamos en detalle porque inicialmente la incluimos por error y después nos dimos cuenta del problema.

### Tratamiento de valores faltantes

Encontramos valores faltantes solo en tres variables:
- workclass: 2,799 (5.7%)
- occupation: 2,809 (5.8%)  
- native-country: 857 (1.8%)

Como son porcentajes bajos y las variables son categóricas, decidimos imputar por moda. Es el enfoque más simple y razonable: reemplazar los valores faltantes por el valor más común. La alternativa de eliminar esas filas hubiera reducido el dataset en casi 6%, perdiendo información valiosa.

---

## Ejercicio 2: Implementación de la Distancia de Gower

### Primera versión

Al principio implementamos la distancia de Gower con bucles anidados, recorriendo fila por fila. Era conceptualmente clara pero muy lenta. Para cada par de filas, iterábamos por todas las columnas calculando la distancia según el tipo de variable.

La función original se llamaba `gower_distance_missing()` y manejaba:
- Variables numéricas: distancia normalizada por el rango
- Variables categóricas: 0 si son iguales, 1 si son distintas
- Variables ordinales: como numéricas después de normalizar
- Valores faltantes: simplemente se saltaban del cálculo

### Versión vectorizada

La implementamos para el Ejercicio 3 porque las muestras de 5,000 y 10,000 registros eran muy lentas con bucles. La idea es usar operaciones matriciales de NumPy en lugar de iterar.

El cambio clave: usar `np.subtract.outer()` y `np.not_equal.outer()` para calcular todas las distancias de una vez. En lugar de un doble bucle que hace n² comparaciones secuenciales, se calcula toda la matriz de golpe.

Después adoptamos esta versión vectorizada también para el Ejercicio 2, aunque solo valida con 5 filas. Es mejor tener el mismo código en todos lados y además es más rápido.

### Manejo de la variable ordinal education

Education es especial porque tiene un orden natural pero no es numérica. La solución:
1. Crear un mapeo de texto a números: Preschool=1, ..., Doctorate=16
2. Normalizar a rango [0,1] dividiendo por el máximo
3. Tratarla como numérica en el cálculo de Gower

Esto permite que la distancia entre "HS-grad" y "Bachelors" sea menor que entre "HS-grad" y "Doctorate", que es lo correcto conceptualmente.

---

## Ejercicio 3: Tratamiento de Conjuntos Grandes

### Migración de Google Colab a Jupyter local

Inicialmente estábamos trabajando en Google Colab, que es práctico porque no requiere configuración local. Sin embargo, al intentar ejecutar el cálculo de la matriz de Gower para una muestra de 10,000 registros, el kernel se quedaba sin memoria y se caía. Google Colab nos daba aproximadamente 2-3 GB de RAM, que no era suficiente para la matriz de 10,000 x 10,000.

Esto nos obligó a migrar todo el proyecto a Jupyter Notebook ejecutándose localmente en nuestras computadoras, donde teníamos acceso a más RAM. Aquí pudimos completar el cálculo exitosamente usando alrededor de 4-5 GB para la muestra de 10,000 registros.

### Muestras de 5,000 y 10,000

No se puede calcular Gower para los 48,842 registros completos porque generaría una matriz de 48,842 x 48,842 = 2,385 millones de celdas. Con 8 bytes por número, son casi 20 GB de RAM.

Por eso usamos muestras. La semilla random_state=42 asegura reproducibilidad.

### Medición de recursos

Agregamos medición de tiempo con `time.time()` y memoria con `psutil.Process().memory_info()`. Los resultados fueron:

Muestra de 5,000:
- Tiempo: ~4-5 segundos
- Memoria adicional: ~1.2 GB

Muestra de 10,000:
- Tiempo: ~17-18 segundos  
- Memoria adicional: ~3.6 GB

La memoria crece cuadráticamente (4x registros = 3x memoria), lo que confirma que el cuello de botella es la matriz de distancias.

### Comparación de estabilidad

La idea es verificar si los clusters encontrados son robustos o dependen mucho del tamaño de muestra.

Aplicamos AgglomerativeClustering con k=3,4,5,6 a ambas muestras y comparamos:
- Silhouette Score de cada configuración
- Cuál es el k óptimo para cada muestra
- Distribución de tamaños de clusters

Si ambas muestras convergen al mismo k óptimo y tienen Silhouette Scores parecidos, los clusters son estables. Si difieren mucho, indica que los agrupamientos no son tan reales, dependen del muestreo.

---

## Ejercicio 4: K-means

### Selección de variables

K-means solo funciona con variables numéricas, así que usamos:
- age
- education-num
- capital-gain
- capital-loss
- hours-per-week

En la primer prueba excluimos fnlwgt por las razones ya mencionadas.

Luego decidimos ordenar los datos por el peso de fnlwgt de mayor a menor, ademas juntamos las columnas capital-gain y capital-loss en una sola columna "neto" ya que estas columnas tenian muchos valores "0" que podrian afectar al analisis.

### Normalización

Antes de K-means, normalizamos con StandardScaler. Esto es crítico porque K-means usa distancia euclidiana y las variables están en escalas muy diferentes:
- age: 17-90
- capital-gain: 0-99,999
- hours-per-week: 1-99

Sin normalizar, capital-gain dominaría completamente el clustering. StandardScaler convierte todo a media=0 y std=1.

### Determinación del k óptimo

Probamos k=2 hasta k=10 y calculamos:
- Silhouette Score: mide qué tan separados están los clusters

El k óptimo fue 2 porque:
- Silhouette relativamente alto (~0.83)

---

## Ejercicio 5: AgglomerativeClustering con Gower

### Uso de matriz precomputada

Aquí reutilizamos la matriz de Gower del Ejercicio 3. AgglomerativeClustering acepta `metric='precomputed'` para usar una matriz de distancias ya calculada.

Importante: NO podemos usar los 48,842 registros completos por memoria. Usamos una muestra de 5,000 registros.

### Elección del linkage

Probamos los tres métodos principales:
- single: tiende a crear cadenas largas (poco útil)
- complete: muy sensible a outliers
- average (UPGMA): balanceado, es el que usamos

### Número de clusters

Mantuvimos k=4 para poder comparar con K-means. También probamos otros valores para ver el comportamiento del Silhouette Score.

El Silhouette fue más bajo que con K-means (~0.28 vs ~0.40) porque:
- Incluye variables categóricas que añaden ruido
- La distancia de Gower no está optimizada para clustering como la euclidiana
- Pero captura más información del dataset real

---

## Ejercicio 6: Evaluación de Clusters

### Comparación K-means vs Agglomerative

K-means:
- Silhouette: 0.40
- Davies-Bouldin: 0.82
- Más rápido
- Solo variables numéricas

Agglomerative con Gower:
- Silhouette: 0.28
- Davies-Bouldin: 1.16
- Más lento
- Todas las variables

### Conclusión

K-means produce clusters más compactos según las métricas, pero esto es engañoso. Solo usa 5 de 14 variables. Agglomerative con Gower tiene peores métricas pero es más completo porque considera toda la información disponible.

La decisión de cuál usar depende del objetivo:
- Si solo importan variables numéricas: K-means
- Si queremos usar toda la información: Agglomerative

Documentamos también las diferencias en interpretabilidad. K-means crea centroides con coordenadas numéricas claras. Agglomerative no tiene centroides, solo jerarquía.

---

## Ejercicio 7: Interpretación y Visualización

### Análisis descriptivo de clusters

Usamos K-means con k=4 porque es más fácil de interpretar. Para cada cluster calculamos:
- Estadísticas de variables numéricas (media, mediana, desviación)
- Distribución de variables categóricas (moda, porcentajes)

Esto nos permitió caracterizar cada cluster:

Cluster 0 (28%): Jóvenes con educación básica
- Edad promedio: 29 años
- Educación: secundaria o menos
- Mayormente solteros
- Ingresos bajos (93% gana ≤50K)

Cluster 1 (24%): Profesionales establecidos
- Edad promedio: 44 años
- Educación universitaria
- Mayormente casados
- Ingresos altos (48% gana >50K)

Cluster 2 (25%): Trabajadores maduros de ingresos medios
- Edad promedio: 39 años
- Educación secundaria
- Muchos casados
- Ingresos moderados

Cluster 3 (23%): Trabajadores maduros con baja actividad
- Edad promedio: 51 años
- Trabajan menos horas (33 h/semana)
- Muchos divorciados
- Ingresos bajos

### Visualizaciones

Creamos varios tipos de gráficos:
- Barras comparativas de variables numéricas por cluster
- Scatter plots 2D para ver separación
- Mapa de calor con características normalizadas
- Distribuciones de variables categóricas



---

## Decisiones Técnicas Generales

### Estructura del proyecto

Creamos `utils.py` con la función `cargar_dataset_adult()` para no repetir código en cada notebook. Esto centraliza la carga de datos y facilita mantenimiento.






---
