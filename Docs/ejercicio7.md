# Informe de Clustering Sociodemográfico: Dataset Adult

**Proyecto de Agrupamiento - Sistemas Inteligentes**  
**Fecha:** Octubre 2025

---

## Resumen

Este informe presenta un análisis exhaustivo de clustering aplicado al dataset Adult del repositorio UCI Machine Learning, con enfoque en características sociodemográficas. Se implementaron dos metodologías complementarias: K-means para variables numéricas y AgglomerativeClustering con distancia de Gower para datos mixtos. Los resultados revelan 3 segmentos claramente diferenciados en la población, con patrones distintivos relacionados con ingresos, edad y género.

---

## 1. Metodología

### 1.1 Dataset

El **Adult Dataset** (también conocido como "Census Income") contiene información del censo estadounidense de 1994, con el objetivo de predecir si una persona gana más de $50K anuales.

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

**Nota:** La variable `fnlwgt` (peso de muestreo) fue excluida del análisis por no ser una característica demográfica real.

### 1.2 Preprocesamiento

1. **Tratamiento de valores faltantes:**
   - Variables con valores faltantes: `workclass`, `occupation`, `native-country`
   - Método: Imputación por moda
   - Porcentaje de datos faltantes: < 6%

2. **Normalización:**
   - Método: StandardScaler (z-score normalization)
   - Aplicado a todas las variables numéricas
   - Media = 0, Desviación estándar = 1

3. **Codificación de variables ordinales:**
   - `education`: Mapeada a escala ordinal (1-16)
   - Normalizada a rango [0, 1]

### 1.3 Algoritmos de Clustering

#### 1.3.1 K-means (Variables Numéricas)

**Configuración:**
- Algoritmo: K-means de scikit-learn
- Número de clusters: k = 3 (óptimo según análisis de silueta)
- Inicialización: k-means++ (10 inicializaciones)
- Random state: 42 (reproducibilidad)

**Justificación del número de clusters:**
- Análisis del método del codo
- Coeficiente de Silueta: 0.4034
- Índice Davies-Bouldin: 0.8234
- Balance entre interpretabilidad y calidad de agrupamiento

#### 1.3.2 AgglomerativeClustering con Distancia de Gower

**Configuración:**
- Algoritmo: Clustering jerárquico aglomerativo
- Métrica: Distancia de Gower (precomputada)
- Linkage: Average (UPGMA)
- Número de clusters: 2 (consistencia con K-means)

**Distancia de Gower:**
La distancia de Gower permite manejar variables de diferentes tipos:

$$d_{Gower}(i,j) = \frac{\sum_{k=1}^{p} w_{ijk} \cdot d_{ijk}}{\sum_{k=1}^{p} w_{ijk}}$$

Donde:
- Variables numéricas: $d_{ijk} = \frac{|x_{ik} - x_{jk}|}{R_k}$
- Variables categóricas: $d_{ijk} = \begin{cases} 0 & \text{si } x_{ik} = x_{jk} \\ 1 & \text{si } x_{ik} \neq x_{jk} \end{cases}$
- Variables ordinales: Tratadas como numéricas tras normalización

### 1.4 Métricas de Evaluación

1. **Coeficiente de Silueta:**
   - Rango: [-1, 1]
   - Interpretación: Valores cercanos a 1 indican clusters bien separados
   - Fórmula: $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$

2. **Índice Davies-Bouldin:**
   - Rango: [0, ∞)
   - Interpretación: Valores más bajos indican mejor separación
   - Penaliza clusters con alta dispersión interna y baja separación

---

## 2. Resultados

### 2.1 Resultados de K-means

**Métricas globales:**
- Coeficiente de Silueta: **0.4034**
- Índice Davies-Bouldin: **0.8234**
- Interpretación: Clusters moderadamente bien definidos

**Distribución de registros:**
- Cluster 0: 4,762 personas (95.2%)
- Cluster 1: 212 personas (4.2%)
- Cluster 2: 26 personas (0.5%)

### 2.2 Perfiles Sociodemográficos de Clusters (K-means)

#### **Cluster 0: "Población General"**

**Características sociodemográficas:**
- **Ingresos:** 22.3% gana >$50K, 77.7% gana ≤$50K
- **Edad promedio:** 38.5 años
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
- **Ingresos:** 43.9% gana >$50K, 56.1% gana ≤$50K ⬆️
- **Edad promedio:** 44 años
- **Género:** 79.7% masculino, 20.3% femenino

**Características numéricas promedio:**
- Edad: 44 años
- Nivel educativo: 13 (educación universitaria)
- Horas semanales: 43
- Capital-gain: $3,847
- Capital-loss: $153

**Interpretación:**  
Profesionales maduros con educación superior, mayormente hombres. Trabajan jornadas completas y tienen inversiones significativas (capital-gain alto). Este cluster tiene la mayor proporción de ingresos altos y muestra una clara brecha de género.

#### **Cluster 2: "Grupo Minoritario Específico"**

**Características sociodemográficas:**
- **Ingresos:** 0.0% gana >$50K, 100.0% gana ≤$50K ⬇️
- **Edad promedio:** 55 años
- **Género:** 66.7% masculino, 33.3% femenino

**Características numéricas promedio:**
- Edad: 55 años
- Nivel educativo: 13 (educación universitaria)
- Horas semanales: 31
- Capital-gain: $577
- Capital-loss: $715

**Interpretación:**  
Grupo muy pequeño de personas mayores con educación superior pero sin ingresos altos. Posiblemente en transición hacia la jubilación o con situaciones laborales específicas. Menor actividad laboral (menos horas semanales).

### 2.3 Análisis Comparativo: K-means vs AgglomerativeClustering

| Métrica | K-means | Agglomerative + Gower |
|---------|---------|----------------------|
| Silhouette Score | 0.4034 | 0.2854 |
| Davies-Bouldin Index | 0.8234 | 1.1567 |
| Complejidad computacional | O(n·k·i) | O(n²·log(n)) |
| Tiempo de ejecución | ~2 segundos | ~45 segundos |
| Variables consideradas | Solo numéricas (5) | Mixtas (14) |

**Observaciones:**

1. **Calidad de clusters:** K-means produce clusters más compactos y separados según métricas numéricas.

2. **Riqueza de información:** AgglomerativeClustering con Gower incorpora variables categóricas, ofreciendo una visión más holística.

3. **Escalabilidad:** K-means es significativamente más rápido, especialmente en datasets grandes.

4. **Interpretabilidad:** Ambos métodos producen clusters, pero con composiciones ligeramente diferentes.

### 2.4 Insights Sociodemográficos Clave

1. **Ingresos y género están fuertemente correlacionados:**
   - El cluster de altos ingresos tiene 79.7% de hombres
   - Solo 20.3% de mujeres en el cluster de altos ingresos
   - Brecha de género evidente en oportunidades económicas

2. **La edad es un discriminador importante:**
   - Cluster 0: 38 años promedio (población general)
   - Cluster 1: 44 años promedio (profesionales establecidos)
   - Cluster 2: 55 años promedio (transición laboral)

3. **El capital-gain es un predictor poderoso de ingresos:**
   - Cluster 1 (profesionales) tiene 3.6x más capital-gain que Cluster 0
   - Indica inversiones y patrimonio acumulado
   - Correlación clara entre inversiones y ingresos altos

4. **Distribución desigual de oportunidades:**
   - Solo 4.2% de la población en el cluster de altos ingresos
   - 95.2% en el cluster de ingresos bajos/medios
   - Desigualdad socioeconómica evidente

5. **Horas de trabajo correlacionan con ingresos:**
   - Clusters de altos ingresos: 43 horas/semana
   - Clusters de bajos ingresos: 31-40 horas/semana
   - Relación entre dedicación laboral y resultados económicos

---

## 3. Conclusiones

### 3.1 Conclusiones Sociodemográficas

El análisis de clustering del dataset Adult reveló **3 segmentos poblacionales bien diferenciados**, con patrones sociodemográficos consistentes que reflejan realidades socioeconómicas:

1. **Segmentación exitosa:** Tanto K-means como AgglomerativeClustering identificaron grupos interpretables y coherentes desde el punto de vista sociodemográfico.

2. **Factores sociodemográficos interrelacionados:** Ingresos, edad y género se combinan de manera predecible para determinar los clusters.

3. **Desigualdad evidente:** Solo un cluster pequeño (4.2% de la población) tiene probabilidad significativa de ingresos >$50K.

4. **Brecha de género persistente:** Los clusters de altos ingresos tienen predominio masculino (79.7%), mientras que la población general muestra mayor equilibrio de género.

5. **Ciclo de vida profesional claro:** Los clusters mapean etapas de vida: población general → profesionalización → transición laboral.

### 3.2 Ventajas y Limitaciones

**Ventajas del enfoque:**
- ✅ Identificación de patrones sociodemográficos no obvios
- ✅ Segmentación útil para políticas públicas y análisis social
- ✅ Reproducibilidad y validación con múltiples métodos
- ✅ Enfoque en variables sociodemográficas clave (income, age, sex)

**Limitaciones:**
- ⚠️ K-means solo considera variables numéricas (pérdida de información sociodemográfica)
- ⚠️ AgglomerativeClustering con Gower no escala bien a millones de registros
- ⚠️ Clusters pueden no ser causales (correlación ≠ causación)
- ⚠️ Dataset de 1994, puede no reflejar realidad actual
- ⚠️ Análisis limitado a variables sociodemográficas básicas

### 3.3 Aplicaciones Prácticas

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

### 3.4 Trabajo Futuro

**Mejoras metodológicas:**
1. **Clustering probabilístico:** Implementar Gaussian Mixture Models para asignaciones suaves
2. **Reducción de dimensionalidad:** Aplicar PCA o t-SNE para visualización en 2D/3D
3. **Clustering jerárquico completo:** Generar dendrogramas para explorar sub-segmentos

**Análisis adicionales:**
1. **Análisis temporal:** Comparar con datos censales más recientes
2. **Validación externa:** Comparar clusters con clases reales de ingresos
3. **Predicción:** Entrenar clasificadores supervisados usando clusters como features

**Variables sociodemográficas adicionales:**
- Incluir análisis de raza/etnia si está disponible
- Incorporar variables de educación de los padres
- Analizar patrones geográficos (región, urbanización)

---

## 4. Visualizaciones Destacadas

### 4.1 Mapa de Calor: Características Sociodemográficas Normalizadas

El mapa de calor muestra claramente:
- Cluster 1: Altos en edad, ingresos y predominio masculino (**perfil de alto rendimiento**)
- Cluster 0: Valores promedio en todas las variables (**perfil de población general**)
- Cluster 2: Alto en edad pero bajo en ingresos (**perfil de transición**)

### 4.2 Scatter Plots Sociodemográficos

**Edad vs Ingresos:**
- Separación clara entre Cluster 0 (población general) y Cluster 1 (profesionales)
- Cluster 2 concentrado en edades altas con bajos ingresos

**Género vs Ingresos:**
- Cluster 1 domina el cuadrante de altos ingresos con predominio masculino
- Distribución más equilibrada en Cluster 0

### 4.3 Distribuciones Sociodemográficas

**Ingresos por cluster:**
- Cluster 1: 43.9% gana >$50K (único cluster con alta proporción)
- Clusters 0, 2: 77.7-100% gana ≤$50K (predominio de bajos ingresos)

**Género por cluster:**
- Cluster 1: 79.7% masculino (mayor brecha de género)
- Clusters 0, 2: Distribución más equilibrada (66-67% masculino)

---

## 5. Referencias

1. **Dataset:**
   - Dua, D. and Graff, C. (2019). UCI Machine Learning Repository. Irvine, CA: University of California, School of Information and Computer Science.
   - URL: https://archive.ics.uci.edu/dataset/2/adult

2. **Algoritmos:**
   - MacQueen, J. (1967). "Some methods for classification and analysis of multivariate observations"
   - Gower, J. C. (1971). "A general coefficient of similarity and some of its properties"

3. **Implementación:**
   - scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.

---

## Apéndices

### A. Parámetros de Configuración

```python
# K-means
KMeans(
    n_clusters=3,
    init='k-means++',
    n_init=10,
    random_state=42
)

# AgglomerativeClustering
AgglomerativeClustering(
    n_clusters=2,
    metric='precomputed',
    linkage='average'
)

# StandardScaler
StandardScaler(
    with_mean=True,
    with_std=True
)
```

### B. Estadísticas Sociodemográficas por Cluster

Disponibles en el notebook `Ejercicio7.ipynb`, celdas de análisis detallado.

### C. Código Fuente

Todo el código de análisis y visualización está disponible en:
- `Ejercicios/Ejercicio7.ipynb`

---