# Informe de Clustering: Dataset Adult

**Proyecto de Agrupamiento - Sistemas Inteligentes**  
**Fecha:** Octubre 2025

---

## Resumen

Este informe presenta un análisis exhaustivo de clustering aplicado al dataset Adult del repositorio UCI Machine Learning. Se implementaron dos metodologías complementarias: K-means para variables numéricas y AgglomerativeClustering con distancia de Gower para datos mixtos. Los resultados revelan 4 segmentos claramente diferenciados en la población, con patrones distintivos relacionados con edad, educación, ingresos y situación laboral.

---

## 1. Metodología

### 1.1 Dataset

El **Adult Dataset** (también conocido como "Census Income") contiene información del censo estadounidense de 1994, con el objetivo de predecir si una persona gana más de $50K anuales.

**Características del dataset:**
- **Tamaño:** 48,842 registros (32,561 training + 16,281 test)
- **Variables:** 15 variables (6 numéricas, 9 categóricas)
- **Variable objetivo:** Income (<=50K, >50K)

**Variables numéricas:**
- `age`: Edad (17-90 años)
- `education-num`: Nivel educativo numérico (1-16)
- `capital-gain`: Ganancia de capital ($)
- `capital-loss`: Pérdida de capital ($)
- `hours-per-week`: Horas de trabajo semanales

**Variables categóricas clave:**
- `workclass`: Tipo de empleador
- `education`: Nivel educativo
- `marital-status`: Estado civil
- `occupation`: Ocupación
- `sex`: Sexo
- `income`: Ingresos (<=50K, >50K)

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
- Número de clusters: k = 4 (óptimo según análisis de silueta)
- Inicialización: k-means++ (10 inicializaciones)
- Random state: 42 (reproducibilidad)

**Justificación del número de clusters:**
- Análisis del método del codo
- Coeficiente de Silueta: 0.3967
- Índice Davies-Bouldin: 0.8234
- Balance entre interpretabilidad y calidad de agrupamiento

#### 1.3.2 AgglomerativeClustering con Distancia de Gower

**Configuración:**
- Algoritmo: Clustering jerárquico aglomerativo
- Métrica: Distancia de Gower (precomputada)
- Linkage: Average (UPGMA)
- Número de clusters: 4 (consistencia con K-means)

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
- Coeficiente de Silueta: **0.3967**
- Índice Davies-Bouldin: **0.8234**
- Interpretación: Clusters moderadamente bien definidos

**Distribución de registros:**
- Cluster 0: 13,528 personas (27.7%)
- Cluster 1: 11,894 personas (24.4%)
- Cluster 2: 12,156 personas (24.9%)
- Cluster 3: 11,264 personas (23.1%)

### 2.2 Perfiles de Clusters (K-means)

#### **Cluster 0: "Trabajadores Jóvenes con Educación Básica"**

**Características numéricas promedio:**
- Edad: 29 años
- Nivel educativo: 10 (educación secundaria)
- Horas semanales: 39
- Capital-gain: $429
- Capital-loss: $42

**Características categóricas dominantes:**
- Sexo: 67% hombres, 33% mujeres
- Estado civil: 81% nunca casados
- Trabajo: 78% sector privado
- Ocupación: Ventas y servicios (35%)
- Ingresos: **93% gana ≤$50K**

**Interpretación:**  
Grupo de trabajadores jóvenes, mayormente solteros, con educación secundaria o menos. Predominantemente empleados en el sector privado en posiciones de nivel inicial o medio-bajo. Este es el grupo con menor probabilidad de altos ingresos.

#### **Cluster 1: "Profesionales Establecidos"**

**Características numéricas promedio:**
- Edad: 44 años
- Nivel educativo: 13 (educación universitaria)
- Horas semanales: 43
- Capital-gain: $3,847
- Capital-loss: $153

**Características categóricas dominantes:**
- Sexo: 72% hombres, 28% mujeres
- Estado civil: 89% casados
- Trabajo: 76% sector privado
- Ocupación: Profesiones especializadas (42%)
- Ingresos: **48% gana >$50K** ⬆️

**Interpretación:**  
Profesionales maduros con educación superior, mayormente casados. Trabajan jornadas completas y tienen inversiones significativas (capital-gain alto). Este cluster tiene la mayor proporción de ingresos altos.

#### **Cluster 2: "Trabajadores Maduros de Ingresos Medios"**

**Características numéricas promedio:**
- Edad: 39 años
- Nivel educativo: 10 (educación secundaria)
- Horas semanales: 41
- Capital-gain: $562
- Capital-loss: $51

**Características categóricas dominantes:**
- Sexo: 59% hombres, 41% mujeres
- Estado civil: 55% casados
- Trabajo: 81% sector privado
- Ocupación: Técnicos y trabajadores calificados (38%)
- Ingresos: **85% gana ≤$50K**

**Interpretación:**  
Trabajadores de mediana edad con educación secundaria, muchos casados. Empleados principalmente en trabajos técnicos o calificados. Grupo mayoritario con ingresos modestos pero estables.

#### **Cluster 3: "Trabajadores Maduros con Baja Actividad Económica"**

**Características numéricas promedio:**
- Edad: 51 años
- Nivel educativo: 10 (educación secundaria)
- Horas semanales: 33 ⬇️
- Capital-gain: $315
- Capital-loss: $38

**Características categóricas dominantes:**
- Sexo: 46% hombres, 54% mujeres
- Estado civil: 42% divorciados, 31% casados
- Trabajo: 66% sector privado
- Ocupación: Servicios (28%)
- Ingresos: **95% gana ≤$50K**

**Interpretación:**  
Grupo de mayor edad con menor actividad laboral (menos horas semanales). Muchos divorciados o viudos, trabajando tiempo parcial o en transición hacia la jubilación. Predominio femenino y bajos ingresos.

### 2.3 Análisis Comparativo: K-means vs AgglomerativeClustering

| Métrica | K-means | Agglomerative + Gower |
|---------|---------|----------------------|
| Silhouette Score | 0.3967 | 0.2854 |
| Davies-Bouldin Index | 0.8234 | 1.1567 |
| Complejidad computacional | O(n·k·i) | O(n²·log(n)) |
| Tiempo de ejecución | ~2 segundos | ~45 segundos |
| Variables consideradas | Solo numéricas (5) | Mixtas (14) |

**Observaciones:**

1. **Calidad de clusters:** K-means produce clusters más compactos y separados según métricas numéricas.

2. **Riqueza de información:** AgglomerativeClustering con Gower incorpora variables categóricas, ofreciendo una visión más holística.

3. **Escalabilidad:** K-means es significativamente más rápido, especialmente en datasets grandes.

4. **Interpretabilidad:** Ambos métodos producen 4 clusters, pero con composiciones ligeramente diferentes.

### 2.4 Insights Clave

1. **Edad y educación son discriminadores primarios:**
   - La edad promedio varía de 29 a 51 años entre clusters
   - El nivel educativo correlaciona fuertemente con ingresos

2. **Brecha de género persistente:**
   - Los clusters de altos ingresos tienen 70%+ de hombres
   - El cluster de bajos ingresos y tiempo parcial tiene mayoría femenina

3. **El capital-gain es un predictor poderoso:**
   - Cluster 1 (profesionales) tiene 9x más capital-gain que Cluster 0
   - Indica inversiones y patrimonio acumulado

4. **Estado civil y edad están entrelazados:**
   - Jóvenes: 81% nunca casados
   - Maduros: mayoría casados o divorciados

5. **Horas de trabajo correlacionan con ingresos:**
   - Clusters de altos ingresos: 43 horas/semana
   - Clusters de bajos ingresos: 33-39 horas/semana

---

## 3. Conclusiones

### 3.1 Conclusiones Generales

El análisis de clustering del dataset Adult reveló **4 segmentos poblacionales bien diferenciados**, con patrones consistentes que reflejan realidades socioeconómicas:

1. **Segmentación exitosa:** Tanto K-means como AgglomerativeClustering identificaron grupos interpretables y coherentes.

2. **Factores socioeconómicos interrelacionados:** Edad, educación, estado civil y horas de trabajo se combinan de manera predecible para determinar los ingresos.

3. **Desigualdad evidente:** Solo un cluster (Cluster 1: 24% de la población) tiene probabilidad significativa de ingresos >$50K.

4. **Ciclo de vida profesional claro:** Los clusters mapean etapas de vida: juventud laboral → profesionalización → estabilidad → declive.

### 3.2 Ventajas y Limitaciones

**Ventajas del enfoque:**
- ✅ Identificación de patrones no obvios en datos multidimensionales
- ✅ Segmentación útil para políticas públicas y marketing
- ✅ Reproducibilidad y validación con múltiples métodos

**Limitaciones:**
- ⚠️ K-means solo considera variables numéricas (pérdida de información)
- ⚠️ AgglomerativeClustering con Gower no escala bien a millones de registros
- ⚠️ Clusters pueden no ser causales (correlación ≠ causación)
- ⚠️ Dataset de 1994, puede no reflejar realidad actual

### 3.3 Aplicaciones Prácticas

**1. Políticas Públicas:**
- Diseñar programas de capacitación para Cluster 0 (jóvenes con baja educación)
- Incentivos para empleadores que contraten a tiempo completo (Cluster 3)
- Programas de reinserción laboral para divorciados de mediana edad

**2. Marketing y Segmentación:**
- Productos financieros sofisticados → Cluster 1 (profesionales)
- Servicios educativos → Cluster 0 (jóvenes)
- Seguros y planificación de retiro → Cluster 3 (maduros)

**3. Investigación Social:**
- Estudiar movilidad socioeconómica entre clusters
- Analizar brechas de género y edad
- Comparar evolución temporal (1994 vs actualidad)

### 3.4 Trabajo Futuro

**Mejoras metodológicas:**
1. **Clustering probabilístico:** Implementar Gaussian Mixture Models para asignaciones suaves
2. **Reducción de dimensionalidad:** Aplicar PCA o t-SNE para visualización en 2D/3D
3. **Clustering jerárquico completo:** Generar dendrogramas para explorar sub-segmentos

**Análisis adicionales:**
1. **Análisis temporal:** Comparar con datos censales más recientes
2. **Validación externa:** Comparar clusters con clases reales de ingresos
3. **Predicción:** Entrenar clasificadores supervisados usando clusters como features

**Datasets complementarios:**
- Cruzar con datos de salud, criminalidad, educación por región
- Análisis geográfico (actualmente solo "native-country" disponible)

---

## 4. Visualizaciones Destacadas

### 4.1 Mapa de Calor: Características Normalizadas

El mapa de calor muestra claramente:
- Cluster 1: Altos en edad, educación y capital-gain (**perfil de alto rendimiento**)
- Cluster 0: Bajos en edad y educación (**perfil joven en desarrollo**)
- Cluster 3: Bajo en horas-per-week (**perfil de baja actividad**)

### 4.2 Scatter Plots

**Edad vs Educación:**
- Separación clara entre Cluster 0 (jóvenes-baja educación) y Cluster 1 (maduros-alta educación)

**Capital-gain vs Horas trabajadas:**
- Cluster 1 domina el cuadrante superior derecho (alto capital + muchas horas)

### 4.3 Distribuciones Categóricas

**Ingresos por cluster:**
- Cluster 1: 48% gana >$50K (único cluster balanceado)
- Clusters 0, 2, 3: 85-95% gana ≤$50K (predominio de bajos ingresos)

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
    n_clusters=4,
    init='k-means++',
    n_init=10,
    random_state=42
)

# AgglomerativeClustering
AgglomerativeClustering(
    n_clusters=4,
    metric='precomputed',
    linkage='average'
)

# StandardScaler
StandardScaler(
    with_mean=True,
    with_std=True
)
```

### B. Estadísticas Descriptivas por Cluster

Disponibles en el notebook `Ejercicio7.ipynb`, celdas de análisis detallado.

### C. Código Fuente

Todo el código de análisis y visualización está disponible en:
- `Ejercicios/Ejercicio7.ipynb`
---



