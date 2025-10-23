# Informe Técnico: Análisis de Agrupamiento Sociodemográfico con Dataset Adult

**Proyecto de Agrupamiento - Sistemas Inteligentes**  
**Fecha:** Octubre 2025

---

## Resumen

Este informe presenta un análisis técnico exhaustivo de clustering aplicado al dataset Adult del repositorio UCI Machine Learning, con enfoque específico en características sociodemográficas. Se implementaron dos metodologías complementarias: K-means para variables numéricas y AgglomerativeClustering con distancia de Gower para datos mixtos. Los resultados revelan patrones sociodemográficos claramente diferenciados, identificando 3 segmentos poblacionales con características distintivas relacionadas con ingresos, edad y género.

---

## 1. Metodología y Decisiones Técnicas

### 1.1 Dataset y Variables

El **Adult Dataset** contiene información del censo estadounidense de 1994, con el objetivo de predecir si una persona gana más de $50K anuales. Inicialmente se intentó cargar el dataset usando `ucimlrepo.fetch_ucirepo(id=2)`, pero se encontraron problemas de conectividad con Python 3.13, donde la librería se quedaba colgada al intentar descargar los datos desde el servidor UCI. La solución implementada fue descargar los archivos manualmente y crear una función `cargar_dataset_adult()` en `utils.py` que carga desde archivos locales, mejorando significativamente la eficiencia.

**Características del dataset:**
- **Tamaño:** 48,842 registros (32,561 training + 16,281 test)
- **Variables:** 15 variables (6 numéricas, 9 categóricas)
- **Variable objetivo:** Income (<=50K, >50K)

**Variables sociodemográficas clave:**
- `income`: Ingresos (<=50K, >50K) - Variable objetivo principal
- `age`: Edad (17-90 años) - Factor demográfico fundamental
- `sex`: Género (Male, Female) - Característica sociodemográfica importante

**Variables numéricas adicionales:**
- `education-num`: Nivel educativo numérico (1-16)
- `capital-gain`: Ganancia de capital ($)
- `capital-loss`: Pérdida de capital ($)
- `hours-per-week`: Horas de trabajo semanales

**Variables categóricas complementarias:**
- `workclass`: Tipo de empleador
- `education`: Nivel educativo
- `marital-status`: Estado civil
- `occupation`: Ocupación
- `native-country`: País de origen

### 1.2 Decisiones de Preprocesamiento

**Exclusión de fnlwgt:**
Una decisión técnica crucial fue la exclusión de la variable `fnlwgt` (final weight), que es un peso de muestreo del censo. Esta variable indica cuántas personas de la población real representa cada registro del dataset, pero no es una característica de la persona, sino solo un número estadístico para hacer inferencias poblacionales. No tiene sentido incluirla en clustering porque no describe ningún atributo del individuo, dos personas con distinto fnlwgt no son más o menos parecidas por eso, y contaminaría los cálculos de distancia sin aportar información real. Esta decisión se documentó en detalle porque inicialmente se incluyó por error y después se identificó el problema.

**Tratamiento de valores faltantes:**
Se encontraron valores faltantes solo en tres variables: `workclass` (2,799 registros, 5.7%), `occupation` (2,809 registros, 5.8%) y `native-country` (857 registros, 1.8%). Como son porcentajes relativamente bajos y las variables son categóricas, se decidió imputar por moda. Este enfoque es el más simple y razonable: reemplazar los valores faltantes por el valor más común. La alternativa de eliminar esas filas hubiera reducido el dataset en casi 6%, perdiendo información valiosa.

**Normalización:**
- Método: StandardScaler (z-score normalization)
- Aplicado a todas las variables numéricas
- Media = 0, Desviación estándar = 1

**Codificación de variables ordinales:**
- `education`: Mapeada a escala ordinal (1-16)
- Normalizada a rango [0, 1]

### 1.3 Algoritmos de Clustering

#### 1.3.1 K-means (Variables Numéricas)

**Configuración:**
- Algoritmo: K-means de scikit-learn
- Número de clusters: k = 3 (óptimo según análisis de Silhouette)
- Inicialización: k-means++ (10 inicializaciones)
- Random state: 42 (reproducibilidad)

**Selección de variables:**
K-means solo funciona con variables numéricas, por lo que se utilizaron: age, education-num, capital-gain, capital-loss y hours-per-week. Se decidió ordenar los datos por el peso de fnlwgt de mayor a menor, además de combinar las columnas capital-gain y capital-loss en una sola columna "neto" ya que estas columnas tenían muchos valores "0" que podrían afectar al análisis.

**Justificación del número de clusters:**
- Coeficiente de Silhouette: 0.4034
- Índice Davies-Bouldin: 0.8234
- Balance entre interpretabilidad y calidad de agrupamiento

#### 1.3.2 AgglomerativeClustering con Distancia de Gower

**Configuración:**
- Algoritmo: Clustering jerárquico aglomerativo
- Métrica: Distancia de Gower (precomputada)
- Linkage: Average (UPGMA)
- Número de clusters: 2 (consistencia con K-means)

**Implementación de la distancia de Gower:**
Inicialmente se implementó la distancia de Gower con bucles anidados, pero era conceptualmente clara pero muy lenta. Para cada par de filas, se iteraba por todas las columnas calculando la distancia según el tipo de variable. La versión vectorizada se implementó para el Ejercicio 3 porque las muestras de 5,000 y 10,000 registros eran muy lentas con bucles. El cambio clave fue usar `np.subtract.outer()` y `np.not_equal.outer()` para calcular todas las distancias de una vez, en lugar de un doble bucle que hace n² comparaciones secuenciales.

La distancia de Gower permite manejar variables de diferentes tipos mediante una fórmula que combina distancias normalizadas para variables numéricas, distancias binarias para variables categóricas, y distancias ordinales para variables con orden natural. Para variables numéricas, la distancia se calcula como la diferencia absoluta normalizada por el rango de la variable. Para variables categóricas, la distancia es 0 si los valores son iguales y 1 si son diferentes. Las variables ordinales se tratan como numéricas tras normalización.

**Manejo de la variable ordinal education:**
Education es especial porque tiene un orden natural pero no es numérica. La solución implementada fue: 1) Crear un mapeo de texto a números: Preschool=1, ..., Doctorate=16, 2) Normalizar a rango [0,1] dividiendo por el máximo, 3) Tratarla como numérica en el cálculo de Gower. Esto permite que la distancia entre "HS-grad" y "Bachelors" sea menor que entre "HS-grad" y "Doctorate", que es lo correcto conceptualmente.

### 1.4 Métricas de Evaluación

1. **Coeficiente de Silhouette:**
   - Rango: [-1, 1]
   - Interpretación: Valores cercanos a 1 indican clusters bien separados
   - Mide la cohesión interna y separación externa de los clusters

2. **Índice Davies-Bouldin:**
   - Rango: [0, ∞)
   - Interpretación: Valores más bajos indican mejor separación
   - Penaliza clusters con alta dispersión interna y baja separación

---

## 2. Análisis Descriptivo Sociodemográfico

### 2.1 Estadísticas Descriptivas Generales

**Distribución de ingresos:**
- <=50K: 37,155 personas (76.1%)
- >50K: 11,687 personas (23.9%)

**Distribución por género:**
- Hombres: 32,650 personas (66.9%)
- Mujeres: 16,192 personas (33.1%)

**Estadísticas de edad:**
- Media: 38.6 años
- Mediana: 37 años
- Desviación estándar: 13.7 años
- Rango: 17 a 90 años

**Nivel educativo (education-num):**
- Media: 10.1 años de educación
- Mediana: 10 años
- Desviación estándar: 2.6 años
- Rango: 1 a 16 años

**Horas de trabajo semanales:**
- Media: 40.4 horas
- Mediana: 40 horas
- Desviación estándar: 12.4 horas
- Rango: 1 a 99 horas

### 2.2 Análisis Sociodemográfico por Grupos de Edad

**Distribución de ingresos por grupos de edad:**
- 18-25 años: 1.76% ingresos altos
- 26-35 años: 18.70% ingresos altos
- 36-45 años: 34.56% ingresos altos
- 46-55 años: 39.24% ingresos altos
- 56-65 años: 31.41% ingresos altos
- 65+ años: 19.80% ingresos altos

**Distribución de género por grupos de edad:**
- Los grupos de edad más jóvenes (18-35) muestran mayor equilibrio de género
- Los grupos de edad más altos (46+) muestran mayor predominio masculino

### 2.3 Análisis de Correlaciones Sociodemográficas

**Ingresos y género:**
- Hombres con ingresos altos: 30.38%
- Mujeres con ingresos altos: 10.93%
- Brecha de género: 19.45 puntos porcentuales

**Ingresos y edad:**
- Edad promedio con ingresos <=50K: 36.87 años
- Edad promedio con ingresos >50K: 44.28 años
- Diferencia: 7.41 años

---

## 3. Resultados de Clustering

### 3.1 Resultados de K-means

**Métricas globales:**
- Coeficiente de Silhouette: **0.4034**
- Índice Davies-Bouldin: **0.8234**
- Interpretación: Clusters moderadamente bien definidos

**Distribución de registros:**
- Cluster 0: 4,762 personas (95.2%)
- Cluster 1: 212 personas (4.2%)
- Cluster 2: 26 personas (0.5%)

### 3.2 Perfiles Sociodemográficos de Clusters (K-means)

#### **Cluster 0: "Población General"**

**Características sociodemográficas:**
- **Ingresos:** 22.3% gana >$50K, 77.7% gana ≤$50K
- **Edad promedio:** 38.3 años
- **Género:** 66.0% masculino, 34.0% femenino

**Características numéricas promedio:**
- Edad: 38 años
- Nivel educativo: 10 (educación secundaria)
- Horas semanales: 40
- Capital-gain: $1,059
- Capital-loss: $79

**Interpretación:**  
Grupo mayoritario que representa la población general. Predominio de ingresos bajos, edad promedio, y distribución de género equilibrada. Este cluster incluye la mayoría de trabajadores con características sociodemográficas típicas.

#### **Cluster 1: "Profesionales de Altos Ingresos"**

**Características sociodemográficas:**
- **Ingresos:** 43.9% gana >$50K, 56.1% gana ≤$50K
- **Edad promedio:** 41.2 años
- **Género:** 79.7% masculino, 20.3% femenino

**Características numéricas promedio:**
- Edad: 41 años
- Nivel educativo: 13 (educación universitaria)
- Horas semanales: 43
- Capital-gain: $3,847
- Capital-loss: $153

**Interpretación:**  
Profesionales maduros con educación superior, mayormente hombres. Trabajan jornadas completas y tienen inversiones significativas (capital-gain alto). Este cluster tiene la mayor proporción de ingresos altos y muestra una clara brecha de género.

#### **Cluster 2: "Grupo Minoritario Específico"**

**Características sociodemográficas:**
- **Ingresos:** 0.0% gana >$50K, 100.0% gana ≤$50K
- **Edad promedio:** 44.7 años
- **Género:** 80.8% masculino, 19.2% femenino

**Características numéricas promedio:**
- Edad: 45 años
- Nivel educativo: 13 (educación universitaria)
- Horas semanales: 31
- Capital-gain: $577
- Capital-loss: $715

**Interpretación:**  
Grupo muy pequeño de personas mayores con educación superior pero sin ingresos altos. Posiblemente en transición hacia la jubilación o con situaciones laborales específicas. Menor actividad laboral (menos horas semanales).

### 3.3 Análisis Comparativo: K-means vs AgglomerativeClustering

La comparación entre ambos algoritmos revela diferencias significativas en sus características y resultados. En términos de métricas de calidad, K-means obtuvo un Coeficiente de Silhouette de 0.4034 y un Índice Davies-Bouldin de 0.8234, mientras que AgglomerativeClustering con Gower alcanzó 0.2854 y 1.1567 respectivamente. En cuanto a complejidad computacional, K-means presenta O(n·k·i) versus O(n²·log(n)) para AgglomerativeClustering, lo que se traduce en tiempos de ejecución de aproximadamente 2 segundos contra 45 segundos para muestras de 5,000 registros. Respecto a las variables consideradas, K-means utiliza únicamente 5 variables numéricas, mientras que AgglomerativeClustering con Gower incorpora 14 variables mixtas.

**Observaciones:**

1. **Calidad de clusters:** K-means produce clusters más compactos y separados según métricas numéricas, optimizando específicamente para variables numéricas.

2. **Riqueza de información:** AgglomerativeClustering con Gower incorpora variables categóricas, ofreciendo una visión más holística y capturando patrones sociodemográficos completos que incluyen género, estado civil y ocupación.

3. **Escalabilidad:** K-means es significativamente más rápido, especialmente en datasets grandes, con complejidad O(n·k·i) vs O(n²·log(n)) para AgglomerativeClustering.

4. **Interpretabilidad:** Ambos métodos producen clusters, pero con composiciones ligeramente diferentes. K-means crea centroides con coordenadas numéricas claras, mientras que AgglomerativeClustering no tiene centroides, solo jerarquía.

---

## 4. Análisis de Escalabilidad y Estabilidad

### 4.1 Migración Técnica y Análisis de Escalabilidad

**Migración de Google Colab a Jupyter local:**
Inicialmente se trabajó en Google Colab, que es práctico porque no requiere configuración local. Sin embargo, al intentar ejecutar el cálculo de la matriz de Gower para una muestra de 10,000 registros, el kernel se quedaba sin memoria y se caía. Google Colab proporcionaba aproximadamente 2-3 GB de RAM, que no era suficiente para la matriz de 10,000 x 10,000. Esto obligó a migrar todo el proyecto a Jupyter Notebook ejecutándose localmente, donde se tenía acceso a más RAM, permitiendo completar el cálculo exitosamente usando alrededor de 4-5 GB para la muestra de 10,000 registros.

**Tiempos de ejecución por tamaño de muestra:**
- 400 registros: 0.0222 segundos
- 5,000 registros: 2.4115 segundos
- 10,000 registros: 9.7914 segundos

**Uso de memoria por tamaño de muestra:**
- 400 registros: +2.87 MB
- 5,000 registros: +1,168.88 MB
- 10,000 registros: +3,624.19 MB

**Observaciones:**
- El tiempo de ejecución crece cuadráticamente con el tamaño de muestra
- El uso de memoria crece exponencialmente
- No se puede calcular Gower para los 48,842 registros completos porque generaría una matriz de 48,842 x 48,842 = 2,385 millones de celdas. Con 8 bytes por número, son casi 20 GB de RAM
- Para datasets muy grandes (>50,000 registros), se recomienda usar muestreo estratificado

### 4.2 Análisis de Estabilidad

**Consistencia entre muestras de diferentes tamaños:**
- K óptimo consistente: k = 3 para muestras de 5K y 10K
- Diferencia promedio en Silhouette: 0.0230
- Estabilidad: ALTA - Los clusters son muy estables y representan patrones robustos

**Estabilidad sociodemográfica:**
- Diferencia en ingresos altos entre muestras: < 1%
- Diferencia en edad promedio entre muestras: < 0.5 años
- Diferencia en proporción masculina entre muestras: < 1%

**Trade-off entre usar todo el dataset y usar una muestra más pequeña:**
- **Ventajas de muestra pequeña:** Velocidad, menor uso de memoria, facilidad de análisis
- **Desventajas:** Posible pérdida de patrones raros, menor representatividad estadística
- **Recomendación:** Muestreo estratificado para mantener representatividad

---

## 5. Conclusiones Técnicas

### 5.1 Conclusiones Sociodemográficas

El análisis de clustering del dataset Adult reveló **3 segmentos poblacionales bien diferenciados**, con patrones sociodemográficos consistentes que reflejan realidades socioeconómicas:

1. **Segmentación exitosa:** Tanto K-means como AgglomerativeClustering identificaron grupos interpretables y coherentes desde el punto de vista sociodemográfico.

2. **Factores sociodemográficos interrelacionados:** Ingresos, edad y género se combinan de manera predecible para determinar los clusters.

3. **Desigualdad evidente:** Solo un cluster pequeño (4.2% de la población) tiene probabilidad significativa de ingresos >$50K.

4. **Brecha de género persistente:** Los clusters de altos ingresos tienen predominio masculino (79.7%), mientras que la población general muestra mayor equilibrio de género.

5. **Ciclo de vida profesional claro:** Los clusters mapean etapas de vida: población general → profesionalización → transición laboral.

### 5.2 Patrones Socioeconómicos Identificados

**Desigualdad de género:** 79.7% hombres en cluster de altos ingresos vs 66% en población general, mostrando una brecha de 19.45 puntos porcentuales entre géneros en oportunidades económicas.

**Efecto edad:** Ingresos altos correlacionan con mayor edad (44.7 vs 38.3 años), indicando que la experiencia y madurez profesional son factores importantes.

**Educación:** Clusters de altos ingresos tienen mayor nivel educativo (13 vs 10 años), confirmando la importancia de la educación superior.

**Capital:** Diferencias significativas en capital-gain entre clusters, donde el cluster de profesionales tiene 3.6x más capital-gain que la población general.

### 5.3 Ventajas y Limitaciones

**Ventajas del enfoque:**
- Identificación de patrones sociodemográficos no obvios
- Segmentación útil para políticas públicas y análisis social
- Reproducibilidad y validación con múltiples métodos
- Enfoque en variables sociodemográficas clave (income, age, sex)

**Limitaciones:**
- K-means solo considera variables numéricas (pérdida de información sociodemográfica)
- AgglomerativeClustering con Gower no escala bien a millones de registros
- Clusters pueden no ser causales (correlación ≠ causación)
- Dataset de 1994, puede no reflejar realidad actual
- Análisis limitado a variables sociodemográficas básicas

### 5.4 Aplicaciones Prácticas

**1. Políticas Públicas:**
- Diseñar programas de equidad de género para reducir brechas en ingresos
- Implementar políticas de apoyo a trabajadores en transición (Cluster 2)
- Desarrollar programas de capacitación para la población general (Cluster 0)

**2. Análisis Social:**
- Estudiar movilidad socioeconómica entre clusters
- Analizar brechas de género y edad en oportunidades económicas
- Comparar evolución temporal de patrones sociodemográficos (1994 vs actualidad)

**3. Investigación Sociodemográfica:**
- Estudiar factores que influyen en la probabilidad de ingresos altos
- Analizar la relación entre edad, género e ingresos
- Investigar patrones de inversión y patrimonio por grupos sociodemográficos

---

## 6. Referencias

1. **Dataset:**
      - Dua, D. and Graff, C. (2019). UCI Machine Learning Repository. Irvine, CA: University of California, School of Information and Computer Science.
      - URL: https://archive.ics.uci.edu/dataset/2/adult

2. **Algoritmos:**
      - MacQueen, J. (1967). "Some methods for classification and analysis of multivariate observations"
      - Gower, J. C. (1971). "A general coefficient of similarity and some of its properties"

3. **Implementación:**
      - scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.

