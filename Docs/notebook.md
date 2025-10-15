# Notas del Proyecto de Agrupamiento

## Exclusión de la variable `fnlwgt` del análisis

### ¿Qué es `fnlwgt`?

La variable `fnlwgt` (final weight) en el dataset Adult **NO es una característica descriptiva de los individuos**, sino un **peso de muestreo del censo estadounidense**.

Según la documentación oficial del dataset (líneas 69-92 de `adult.names`):

> *"The weights on the CPS files are controlled to independent estimates of the civilian noninstitutional population of the US. [...] The term estimate refers to population totals derived from CPS by creating "weighted tallies" of any specified socio-economic characteristics of the population."*

En resumen, `fnlwgt` indica **cuántas personas en la población total representa cada fila** del dataset de muestra.

### ¿Por qué se excluye del análisis de clustering?

1. **No es una característica del individuo**: `fnlwgt` no describe ningún atributo de la persona (como edad, educación, ingresos, etc.). Es simplemente un peso estadístico asignado por el censo.

2. **No tiene sentido en cálculos de similitud**: Al calcular la distancia de Gower o cualquier otra métrica de similitud, queremos medir qué tan parecidos son dos individuos basándonos en sus características. Dos personas con diferente `fnlwgt` no son más o menos similares entre sí por este valor.

3. **Contamina los resultados**: Incluir `fnlwgt` en el cálculo de distancias añade ruido sin significado al análisis de clustering, potencialmente generando agrupamientos sin sentido.

4. **No aplica a los objetivos del análisis**: Los algoritmos de clustering (K-means, Agglomerative) buscan agrupar observaciones similares. `fnlwgt` es relevante solo para análisis estadísticos ponderados sobre la población, no para clasificación o agrupamiento de individuos.

### ¿Cuándo SÍ se usa `fnlwgt`?

El peso `fnlwgt` es útil para:
- **Análisis estadísticos ponderados** que buscan hacer inferencias sobre la población total de EE.UU.
- **Estimaciones poblacionales** (ej: "¿Qué porcentaje de la población gana >50K?")
- **Ajustar resultados** para que sean representativos de la población real



