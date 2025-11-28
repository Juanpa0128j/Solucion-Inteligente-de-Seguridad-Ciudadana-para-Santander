# Solución Inteligente de Seguridad Ciudadana para Santander

## 📋 Descripción del Proyecto

Este repositorio contiene la solución al reto "Ecosistema de Datos" del Ministerio de las TIC de Colombia. Implementa un flujo reproducible para extraer, limpiar, modelar y poner a prueba una solución de seguridad ciudadana para el departamento de Santander.

Resumen breve (330,184 registros procesados, 2010–2025):

- Extracción y EDA: ingesta desde 5 fuentes públicas (municipales y nacionales), detección y corrección de problemas de calidad, y exportación de CSVs con metadata.
- Pipelines: transformadores reproducibles (parsing robusto, `ObjectToFloatTransformer`, variables temporales), generación de Parquet procesados listos para modelado.
- Modelado Bucaramanga: modelos temporales (Prophet/SARIMA), análisis espacial (DBSCAN, KDE), hotspot detection y clasificación de riesgo (XGBoost); resultados y artefactos persistidos en `models/`.
- Modelado Departamento: grilla espacial, agregación a zonas, modelos de conteo (Negative Binomial, Gaussian Process, XGBoost Poisson) y métricas de ranking de hotspots; objetos entrenados guardados para demo.
- Chatbot RAG (opcional): pipeline de ingestión de PDFs, chunking, embeddings (`sentence-transformers`) e indexación persistente en Chroma (`vectores/`) para respuestas con contexto usando LLMs.

Durante el EDA se identificaron y corrigieron problemas críticos de calidad (por ejemplo, 6,363 coordenadas erróneas y 1,904 duplicados) y se definieron reglas de preprocesamiento (geocodificación por centroide de barrio, imputaciones por prevalencia, y validación de rangos geográficos).

## 🗂️ Estructura del Proyecto

```text
Solucion-Inteligente-de-Seguridad-Ciudadana-para-Santander/
├── datasets/              # CSVs originales y metadata (generados por `eda.ipynb`)
├── datasets/processed/    # Parquet procesados (generados por `pipelines.ipynb`)
├── models/                # Modelos y artefactos pre-entrenados (joblib, npy, csv)
├── vectores/              # Base de datos Chroma persistente (chatbot)
├── barrios_bucaramanga.geojson
├── .env                   # Variables de entorno (AppToken, LANGCHAIN_API_KEY)
├── .gitignore
├── eda.ipynb              # Notebook: extracción y análisis exploratorio
├── pipelines.ipynb        # Notebook: limpieza y feature engineering → Parquet
├── models_bucaramanga.ipynb # Notebook: modelos y análisis para Bucaramanga
├── models_depto.ipynb     # Notebook: modelos a nivel departamental (grilla y conteos)
├── chatbot.ipynb          # Notebook: pipeline RAG + Chroma para demo documental
├── requirements.txt
└── README.md
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

## ⚡ Demo rápido (usa modelos pre-entrenados)

Se proveen artefactos pre-entrenados en la carpeta `models/` para acelerar demostraciones y evitar entrenamientos costosos (especialmente el muestreo de Stan). Los notebooks están preparados para *cargar* estos modelos cuando existen y así mostrar resultados reproducibles en minutos.

- **Modelos disponibles (ejemplos):** `models/nb_res_obj.joblib`, `models/gp_obj.joblib`, `models/xgb_model.joblib`, `models/density_grid.npy`, `models/hotspots_info.csv`.
- **Comportamiento para demo:** los notebooks intentan cargar modelos guardados; si los encuentran, saltan los bloques de entrenamiento (incluyendo cualquier bloque de Stan). Por tanto, para demos rápidos, no es necesario ejecutar bloques de muestreo ni reentrenar.

Requisitos previos para el demo rápido:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# (opcional para chatbot) pip install sentence-transformers chromadb langchain google-generativeai pypdf
```

Variables de entorno necesarias:

- `AppToken` : token de datos.gov.co (necesario si ejecutas extracción desde `eda.ipynb`).
- `LANGCHAIN_API_KEY` : (opcional) clave para Gemini si quieres probar el chatbot RAG.

Pasos mínimos de demo (5–8 minutos):

1. Activar el entorno virtual y asegurarse de dependencias instaladas.
2. Colocar `.env` con `AppToken` si vas a ejecutar extracción; para demo rápido no es obligatorio si ya existen los CSV en `datasets/`.
3. Abrir `models_bucaramanga.ipynb` y ejecutar las celdas iniciales hasta la sección **Load pre-trained models / Inference** (estas celdas cargan artefactos desde `models/`).
4. Ejecutar la celda de forecast (Prophet/serie temporal) y la celda de análisis espacial (DBSCAN/KDE) — ambas usarán modelos/artefactos guardados y generarán gráficos y el `hotspots_df` sin reentrenar.
5. Abrir `models_depto.ipynb` y ejecutar la sección de **Load aggregates & Load models** para mostrar métricas (Precision@K, top-pct) y predicciones guardadas (`ensemble_preds.parquet`).
6. (Opcional) Abrir `chatbot.ipynb`, colocar PDFs en `data/`, instalar extras y ejecutar las celdas de chunking + `collection.add` para poblar `vectores/` y probar `responder("...")`.
7. Validar salidas: revisar gráficos, `hotspots_info.csv` y los archivos en `models/`.

Nota: Si deseas forzar reentrenamiento, puedes ejecutar explícitamente las celdas de entrenamiento; sin embargo, el demo oficial evita Stan/sampling (bloques comentados o saltables) y utiliza los objetos persistidos en `models/`.

## 📦 Artifacts & Outputs (resumen)

Lista rápida de los artefactos más relevantes y sus rutas relativas:

- `datasets/*.csv` — datos sin procesar extraídos o exportados por `eda.ipynb`.
- `datasets/processed/*_processed.parquet` — datos limpios y listos para modelado (generados por `pipelines.ipynb`).
- `models/*.joblib`, `models/*.pkl` — modelos preentrenados (NB, GP, XGBoost, etc.).
- `models/hotspots_info.csv` — tabla con hotspots detectados y métricas.
- `models/density_grid.npy`, `models/grid_info.json` — información de la grilla espacial usada en modelos departamentales.
- `vectores/` — base de datos Chroma persistente (embeddings + metadatos) para el chatbot.
- `barrios_bucaramanga.geojson` — geometrías de barrios usadas para geocodificación y validación.

## 🧩 Dependencias extra (chatbot / RAG)

Para ejecutar el demo del chatbot adicionalmente instala:

```bash
pip install sentence-transformers chromadb langchain langchain-community langchain-text-splitters google-generativeai pypdf
```

Nota sobre Stan: las secciones de `models_depto.ipynb` que usan modelos Bayesianos en Stan están etiquetadas como opcionales y, por defecto, no se ejecutan en el demo. Para reproducibilidad y velocidad usamos los artefactos en `models/`.


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

Este proyecto utiliza datos abiertos del Gobierno de Colombia disponibles bajo licencia de datos abiertos. El código fuente de este repositorio se publica bajo la licencia MIT; consulte el archivo `LICENSE` en la raíz del proyecto para el texto completo y los términos.

## 👤 Autor

- **Juan Pablo Mejía Gómez** ([@Juanpa0128j](https://github.com/Juanpa0128j))

- **Sebastián Gómez** ([@segomezz](https://github.com/segomezz))

- **Verónica Pérez** ([@Veritoo123](https://github.com/Veritoo123))

---

**Última actualización:** Noviembre 27, 2025

**Versión del Análisis:** 1.2

