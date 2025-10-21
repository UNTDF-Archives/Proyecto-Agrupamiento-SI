# Ejercicio 1: Análisis Descriptivo del Dataset Adult

## Descripción General del Dataset

El dataset Adult contiene información del censo de Estados Unidos de 1994. Tiene 48,842 registros y 15 variables. El objetivo del dataset es predecir si una persona gana más de 50 mil dólares al año.

## Clasificación de Variables

### Variables Cuantitativas

**Discretas:**
- age: Edad de la persona (17 a 90 años)
- education-num: Años de educación (1 a 16)
- hours-per-week: Horas de trabajo por semana (1 a 99)

**Continuas:**
- capital-gain: Ganancias de capital
- capital-loss: Pérdidas de capital
- income: Ingresos (<=50K o >50K)

### Variables Cualitativas

**Nominales:**
- workclass: Tipo de empleador
- marital-status: Estado civil
- occupation: Ocupación
- relationship: Relación familiar
- race: Raza
- sex: Sexo
- native-country: País de origen

**Ordinales:**
- education: Nivel educativo (desde Preschool hasta Doctorate)

**Nota:** La variable fnlwgt no se incluye en el análisis porque es un peso de muestreo del censo, no una característica real de las personas.

## Estadísticas Descriptivas

### Variables Numéricas

**Edad (age):**
- Media: 38.6 años
- Mediana: 37 años
- Desviación estándar: 13.7 años
- Rango: 17 a 90 años
- La mayoría de las personas tienen entre 28 y 48 años

**Nivel Educativo (education-num):**
- Media: 10.1 años de educación
- Mediana: 10 años
- Desviación estándar: 2.6 años
- Rango: 1 a 16 años
- El 50% tiene educación secundaria o menos

**Horas de Trabajo (hours-per-week):**
- Media: 40.4 horas
- Mediana: 40 horas
- Desviación estándar: 12.4 horas
- Rango: 1 a 99 horas
- La mayoría trabaja jornada completa (40 horas)

**Ganancias de Capital (capital-gain):**
- Media: $1,079
- Mediana: $0
- Desviación estándar: $7,452
- La mayoría de las personas no tiene ganancias de capital
- Hay algunos valores muy altos que aumentan la media

**Pérdidas de Capital (capital-loss):**
- Media: $87.5
- Mediana: $0
- Desviación estándar: $403
- La mayoría no tiene pérdidas de capital

### Variables Categóricas

**Ingresos (income):**
- <=50K: 37,155 personas (76.1%)
- >50K: 11,687 personas (23.9%)
- La mayoría de las personas gana menos de 50 mil dólares

**Sexo (sex):**
- Hombres: 32,650 personas (66.9%)
- Mujeres: 16,192 personas (33.1%)
- Hay el doble de hombres que mujeres en el dataset

**Nivel Educativo (education) - Top 5:**
1. HS-grad (secundaria completa): 15,784 personas (32.3%)
2. Some-college (universidad incompleta): 10,878 personas (22.3%)
3. Bachelors (licenciatura): 8,025 personas (16.4%)
4. Masters (maestría): 2,657 personas (5.4%)
5. Assoc-voc (técnico vocacional): 2,061 personas (4.2%)

**Estado Civil (marital-status) - Top 3:**
1. Married-civ-spouse (casado): 22,379 personas
2. Never-married (nunca casado): 16,117 personas
3. Divorced (divorciado): 6,633 personas

**Ocupación (occupation) - Top 5:**
1. Prof-specialty (profesionales): 6,172 personas
2. Craft-repair (técnicos): 6,112 personas
3. Exec-managerial (ejecutivos): 6,086 personas
4. Adm-clerical (administrativos): 5,611 personas
5. Sales (ventas): 5,504 personas   

**Tipo de Empleador (workclass) - Top 3:**
1. Private (sector privado): 33,906 personas (69.4%)
2. Self-emp-not-inc (trabajador independiente): 3,862 personas (7.9%)
3. Local-gov (gobierno local): 3,136 personas (6.4%)

## Valores Faltantes

Se encontraron valores faltantes en tres variables:

1. **workclass:** 2,799 valores faltantes (5.7%)
2. **occupation:** 2,809 valores faltantes (5.8%)
3. **native-country:** 857 valores faltantes (1.8%)

Las demás variables no tienen valores faltantes.

## Tratamiento de Valores Faltantes

Se decidió usar imputación por moda porque:
- El porcentaje de valores faltantes es mayor a 5%
- Las variables son categóricas nominales
- La moda representa el valor más común, lo que tiene sentido para estas variables

Resultados de la imputación:
- workclass: se reemplazó por "Private" (valor más frecuente)
- occupation: se reemplazó por la ocupación más común en ese tipo de trabajo
- native-country: se reemplazó por "United-States" (valor más frecuente)

## Observaciones Principales

1. El dataset está desbalanceado en cuanto a ingresos, con el 76% ganando menos de 50K.

2. Hay más hombres que mujeres en el dataset (2:1).

3. La edad promedio es de 39 años, con la mayoría de personas en edad laboral activa.

4. La mayoría de las personas trabaja en el sector privado (69%).

5. El nivel educativo más común es secundaria completa, seguido de universidad incompleta.

6. La mayoría trabaja 40 horas semanales (jornada completa).

7. Muy pocas personas tienen ganancias o pérdidas de capital significativas.

8. Los valores faltantes son pocos y se concentran en tres variables relacionadas con el trabajo.

## Conclusión

El dataset Adult es apropiado para análisis de clustering porque tiene una buena combinación de variables numéricas y categóricas. Después de limpiar los valores faltantes, el dataset tiene 48,842 registros completos que representan una muestra diversa de la población trabajadora de Estados Unidos en 1994.

