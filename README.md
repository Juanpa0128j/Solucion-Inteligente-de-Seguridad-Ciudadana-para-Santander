# Solución Inteligente de Seguridad Ciudadana para Santander

## 📋 Descripción del Proyecto

Este proyecto presenta un **Análisis Exploratorio de Datos (EDA) exhaustivo** sobre la seguridad ciudadana en el departamento de Santander, Colombia. Se analizaron **330,184 registros** provenientes de 5 datasets de datos abiertos del gobierno colombiano, abarcando un período de 15 años (2010-2025). El análisis incluyó datasets municipales de Bucaramanga (40 Delitos y 150 Información Delictiva) y datasets nacionales de la Policía Nacional (Delitos Sexuales, Violencia Intrafamiliar y Hurto por Modalidades), todos filtrados para el departamento de Santander. Durante el EDA se identificaron y corrigieron problemas críticos de calidad de datos, incluyendo 6,363 coordenadas geográficas erróneas, 1,904 registros duplicados, y valores faltantes en variables demográficas clave.

Los resultados del análisis revelaron **39 problemas de calidad de datos** distribuidos en 6 categorías principales: coordenadas geográficas erróneas (4.71% del dataset Bucaramanga), valores "NO REPORTA" en hasta el 86.73% de registros para grupo etario en delitos sexuales, inconsistencias en tipos de datos (columnas numéricas almacenadas como texto), y duplicados en datasets nacionales. Se establecieron **decisiones estratégicas de preprocesamiento** que incluyen: (1) geocodificación mediante centroides de barrios para recuperar el 95% de registros sin coordenadas válidas, (2) imputación diferenciada según prevalencia (alta >20%, media 5-20%, baja <5%), y (3) definición de granularidad temporal variable (mensual para Bucaramanga, diaria para datasets nacionales). El informe ejecutivo prioriza acciones en 3 fases: correcciones críticas (semana 1), geocodificación y validación (semana 2), e integración con datos externos (semana 3+).

## 🗂️ Estructura del Proyecto

```
Solucion-Inteligente-de-Seguridad-Ciudadana-para-Santander/
├── datasets/              # Carpeta con datasets descargados en formato CSV (ejecutar eda.ipynb para generación automática)
│   ├── delitos_bucaramanga.csv
│   ├── info_delictiva_bucaramanga.csv
│   ├── delitos_sexuales.csv
│   ├── violencia_intrafamiliar.csv
│   ├── hurto_modalidades.csv
│   └── metadata.json
├── .env                   # Variables de entorno (AppToken para API)
├── .gitignore            # Archivos excluidos de control de versiones
├── eda.ipynb             # Notebook: Análisis Exploratorio de Datos completo
├── pipelines.ipynb       # Notebook: Pipelines de limpieza y preprocesamiento
├── models.ipynb          # Notebook: Modelos de Machine Learning
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo
```

## 📊 Datasets Analizados

| # | Dataset | ID API | Alcance | Registros | Período |
|---|---------|--------|---------|-----------|---------|
| 1 | 40 Delitos Bucaramanga | `75fz-q98y` | Municipal | 135,076 | 2010-2021 |
| 2 | 150 Información Delictiva Bucaramanga | `x46e-abhz` | Municipal | 120,940 | 2010-2025 |
| 3 | Delitos Sexuales Nacional | `fpe5-yrmw` | Nacional (Santander) | 21,859 | 2010-2025 |
| 4 | Violencia Intrafamiliar Nacional | `vuyt-mqpw` | Nacional (Santander) | 50,864 | 2010-2025 |
| 5 | Hurto por Modalidades Nacional | `d4fr-sbn2` | Nacional (Santander) | 1,445 | 2010-2025 |

**Total:** 330,184 registros

## 🚀 Configuración del Entorno

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Jupyter Notebook o JupyterLab
- Cuenta en datos.gov.co para obtener AppToken

### Instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/Juanpa0128j/Solucion-Inteligente-de-Seguridad-Ciudadana-para-Santander.git
   cd Solucion-Inteligente-de-Seguridad-Ciudadana-para-Santander
   ```

2. **Crear entorno virtual (recomendado)**

   ```bash
   # En Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # En Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

   Esto instalará todas las dependencias necesarias incluyendo:
   - pandas, numpy (análisis de datos)
   - matplotlib, seaborn (visualización)
   - scikit-learn (machine learning y pipelines)
   - requests (consumo de APIs)
   - python-dotenv (variables de entorno)
   - jupyter (notebooks interactivos)

4. **Configurar AppToken**

   Crea un archivo `.env` en la raíz del proyecto:

   ```bash
   echo "AppToken=TU_TOKEN_AQUI" > .env
   ```

   Reemplaza `TU_TOKEN_AQUI` con tu token real obtenido de [datos.gov.co](https://www.datos.gov.co).

5. **Ejecutar notebooks en orden**

   ```bash
   jupyter notebook
   ```

   Abrir y ejecutar en este orden:
   1. `eda.ipynb` - Extracción y análisis exploratorio (genera carpeta `datasets/`)
   2. `pipelines.ipynb` - Limpieza y transformación de datos
   3. `models.ipynb` [WIP] - Entrenamiento de modelos predictivos

## 📈 Principales Hallazgos del EDA

### Problemas de Calidad Detectados

- **39 problemas** identificados en total
- **6,363 coordenadas erróneas** (4.71%) corregidas en dataset Bucaramanga
- **1,904 registros duplicados** (8.61% en Delitos Sexuales)
- **86.73% valores "NO REPORTA"** en grupo etario (Delitos Sexuales)
- **Columnas numéricas almacenadas como texto** (ano, dia, cantidad, orden)

### Cobertura de Datos

- **Temporal:** 15 años de datos (2010-2025), sin gaps significativos
- **Geográfica:** 87 barrios en Bucaramanga, múltiples municipios en Santander
- **Completitud general:** 99.50% (media ponderada de valores no nulos)

### Patrones Identificados

- **Estacionalidad mensual:** Distribución relativamente uniforme (~11,000 casos/mes)
- **Tendencia anual:** Pico en 2016-2018 (~13,000 casos/año)
- **Concentración geográfica:** Top 5 municipios representan >60% de casos
- **Delitos más frecuentes:** Hurto a personas, lesiones personales, hurto a residencias

## 🎯 Decisiones de Preprocesamiento

1. Conversión de tipos de datos (ano, dia, cantidad, orden → numéricos)
2. Eliminación de duplicados (1,904 registros)
3. Creación de variables temporales (año, mes, trimestre, día_semana)
4. Validación de coordenadas geográficas (rango válido 6.5-7.5°N, 72.5-73.5°W)
5. Categorización explícita de valores "NO REPORTA"

6. Geocodificación por centroide de barrio (recuperar 6,363 registros)
7. Validación de códigos DANE vs catálogo oficial
8. Normalización de categorías (mayúsculas, sin tildes)
9. Imputación de valores faltantes según prevalencia
10. Creación de dataset maestro integrado

11. Integración con datos demográficos DANE
12. Variables derivadas avanzadas (tasas per cápita, índices)
13. Calendario de festivos y eventos especiales
14. Análisis de outliers espaciales

## 📊 Estrategia de Granularidad Temporal

| Dataset | Granularidad Disponible | Granularidad Recomendada | Uso |
|---------|------------------------|-------------------------|-----|
| 40 Delitos Bucaramanga | Año + Mes | **Mensual** | Tendencias, estacionalidad |
| Datasets Policía Nacional | Fecha completa | **Diaria** | Predicción operativa |
| Análisis estratégico | Todas las fuentes | **Anual** | Evaluación de políticas |

## 🗺️ Estrategia de Geocodificación

### Problema

- 6,363 registros (4.71%) con coordenadas erróneas ("xx.xxxx", "-yy.yyyy")
- Reemplazados con valores nulos (NaN)

### Solución

1. **Calcular centroides por barrio** usando los 128,713 registros con coordenadas válidas
2. **Imputar coordenadas** para registros sin coordenadas usando centroide del barrio
3. **Validar rango geográfico:**
   - Latitud: 6.5°N - 7.5°N
   - Longitud: -73.5°W - -72.5°W
4. **Recuperación esperada:** >95% de registros georreferenciados

## 📚 Tecnologías Utilizadas

- **Python 3.12.3**
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas
- **Matplotlib & Seaborn** - Visualización de datos
- **Scikit-learn** - Pipelines de preprocesamiento y modelos ML
- **Requests** - Consumo de APIs SODA
- **Python-dotenv** - Gestión de variables de entorno
- **Jupyter Notebook** - Entorno de desarrollo interactivo

## 🔄 API de Datos Abiertos

El proyecto utiliza la **API SODA (Socrata Open Data API)** de [datos.gov.co](https://www.datos.gov.co):

- **Endpoint base:** `https://www.datos.gov.co/resource/`
- **Autenticación:** X-App-Token (header)
- **Paginación:** Límite máximo de 50,000 registros por request
- **Filtros:** Soporte de cláusulas WHERE con SoQL
- **Ordenamiento:** Por ID para consistencia en paginación

## 🛠️ Flujo de Trabajo del Proyecto

### 1. Extracción y Análisis Exploratorio (`eda.ipynb`)

- Conexión a APIs de datos.gov.co mediante SODA API
- Extracción de 330,184 registros de 5 datasets
- Análisis estructural, temporal y geográfico
- Detección de 39 problemas de calidad de datos
- **Generación de carpeta `datasets/`** con archivos CSV y metadata
- Informe ejecutivo con decisiones de preprocesamiento

### 2. Limpieza y Transformación (`pipelines.ipynb`)

- Carga de datasets desde carpeta `datasets/`
- Transformadores personalizados para:
  - Conversión de tipos de datos (object → float, datetime)
  - División de fechas en componentes (año, mes, día)
  - One-Hot Encoding de variables categóricas
- Pipelines de scikit-learn configurables por dataset
- Datos transformados listos para modelado

### 3. Modelado Predictivo (`models.ipynb`) [WIP]

- Entrenamiento de modelos de machine learning
- Evaluación y validación de resultados
- Análisis de importancia de features

## 📋 Lineamientos de Código

Para mantener la calidad y consistencia del código, se deben seguir estas convenciones:

### **Mensajes de Commit**

Usar prefijos descriptivos según el tipo de cambio:

- `feat:` - Nueva funcionalidad
  ```
  feat: add geocoding pipeline for missing coordinates
  ```
- `fix:` - Corrección de errores
  ```
  fix: correct date parsing for delitos_sexuales dataset
  ```
- `chore:` - Tareas de mantenimiento, configuración
  ```
  chore: update requirements.txt with scikit-learn
  ```
- `docs:` - Cambios en documentación
  ```
  docs: update README with pipeline workflow
  ```
- `refactor:` - Refactorización de código sin cambiar funcionalidad
  ```
  refactor: extract data loading into separate function
  ```
- `style:` - Cambios de formato, espacios, etc.
  ```
  style: format code with black formatter
  ```

```
✅ Estructura recomendada:
├── eda.ipynb              # Análisis exploratorio
├── pipelines.ipynb        # Preprocesamiento
├── models-ml.ipynb        # Modelos ML
├── feature-engineering.ipynb  # Ingeniería de features
└── utils.py               # Funciones auxiliares
```

### 4. **Nomenclatura de Archivos**

- **Notebooks:** Minúsculas, palabras separadas por guión
- **Extensión:** `.ipynb` para notebooks, `.py` para módulos

```python
# ✅ Correcto
eda.ipynb
pipelines.ipynb
models-ml.ipynb
feature-engineering.ipynb
data-visualization.ipynb

# ❌ Incorrecto
EDA.ipynb                  # Mayúsculas
Pipelines_Data.ipynb       # Guión bajo
modelsML.ipynb             # camelCase
Models ML.ipynb            # Espacios
```

### 5. **Comentarios y Documentación**

- Usar comentarios cuando la lógica no es obvia
- Documentar funciones con docstrings
- Mantener código limpio y auto-explicativo

## 📝 Notas Importantes

### Limitaciones Identificadas

1. **Granularidad temporal heterogénea:**
   - "40 Delitos Bucaramanga" solo tiene año-mes (sin día específico)
   - Limita análisis de patrones diarios para este dataset

2. **Alta prevalencia de valores "NO REPORTA":**
   - Grupo etario: 86.73% en Delitos Sexuales
   - Limita análisis demográfico detallado

3. **Coordenadas faltantes:**
   - 4.71% de registros requieren geocodificación
   - Impacto manejable con estrategia de imputación

4. **Columnas constantes:**
   - "departamento" = "SANTANDER" (100% por diseño del filtro)
   - Sin variabilidad para comparación interdepartamental

## 📄 Licencia

Este proyecto utiliza datos abiertos del Gobierno de Colombia disponibles bajo licencia de datos abiertos.

## 👤 Autor

- **Juan Pablo Mejía Gómez** ([@Juanpa0128j](https://github.com/Juanpa0128j))

- **Sebastián Gómez**

- **Verónica Pérez**

---

**Última actualización:** Noviembre 20, 2025

**Versión del Análisis:** 1.1

