#!/usr/bin/env python
# coding: utf-8

# # Chatbot documental para la ciudadanía de Santander
# 
# Este notebook construye un chatbot documental para apoyar a la ciudadanía de Santander explicando normativa y rutas de atención. Pipeline breve: carga PDFs desde `data/`, los segmenta en chunks, crea embeddings (Sentence‑Transformers), los indexa en una base vectorial persistente (Chroma), y utiliza un LLM (Gemini via LangChain) para generar respuestas con contexto recuperado.
# 
# Uso: asegúrese de definir las variables de entorno necesarias (por ejemplo `LANGCHAIN_API_KEY`) en un archivo `.env` o exportarlas en el entorno antes de ejecutar las celdas. Este notebook prioriza claridad, trazabilidad y ejemplos de prueba.
"""Aquí NO se cargan PDFs ni se generan embeddings: solo se carga la base ya creada.

Esto significa que el chatbot inicia rápido y no hace trabajo pesado.

responder() construye un prompt HTML limpio, ideal para renderizar en Flask.

Se quitan saltos de línea innecesarios con replace("\n", "") aunque puedes ajustarlo."""

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
# --------------------------
# 2. Cargar base vectorial persistente
# --------------------------
client = chromadb.PersistentClient(path="./vectores")
collection = client.get_collection("documentos_colombia")

# --------------------------
# 3. Cargar modelo de embeddings (una sola vez)
# --------------------------
embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# ## Recuperación de contexto (consulta vector DB)
# Función para consultar la colección y recuperar los fragmentos más relevantes.

# In[8]:

def buscar_contexto(query, top_k=5):
    query_embedding = embedder.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]


# ## Configuración del LLM (Gemini / LangChain)
# Carga de variables de entorno y creación del cliente LLM.

# In[9]:


from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde .env (python-dotenv)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Establecer LANGCHAIN_API_KEY desde .env si existe
api_key = os.getenv('LANGCHAIN_API_KEY')
if api_key:
    os.environ['LANGCHAIN_API_KEY'] = api_key
else:
    print('Advertencia: LANGCHAIN_API_KEY no encontrada en .env')

# Inicializa el LLM de Gemini usando LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",  # nombre del modelo como string
    temperature=0.3,
    max_output_tokens=300
)



# ## Función de respuesta y prompt
# Construcción del prompt que combina contexto recuperado y la pregunta del usuario.

# In[10]:


def responder(question):
    # Obtener contexto (lo que antes hacía buscar_contexto)
    context = "\n".join(buscar_contexto(question))

    # Construir el prompt con contexto y pregunta
    prompt = f"""
Eres un chatbot informativo para la ciudadanía de Santander (Colombia).
Tu objetivo es brindar información clara, segura, actualizada y accesible sobre temas relacionados con:
    Violencia intrafamiliar
        Ley 1257 de 2008
        Decreto 4799 de 2011
        Código Penal (Art. 229)
        Rutas de atención del ICBF
        Rutas de atención de Comisarías de Familia
    Violencia sexual
        Ley 1719 de 2014
        Protocolo de atención para víctimas de Violencias Basadas en Género (VBG)
    Seguridad ciudadana
        Código Nacional de Seguridad y Convivencia Ciudadana – Ley 1801 de 2016
    Niñez
        Ley 1098 de 2006 (Código de Infancia y Adolescencia)
Reglas generales del chatbot:
    1. No das asesoría legal personalizada; solo explicas normativa y rutas oficiales.
    2. No haces juicios, no culpas a la víctima y no interpretas casos específicos.
    3. Siempre proporcionas opciones seguras de atención.
    4. Usa lenguaje claro, empático y respetuoso.
    5. Cuando el usuario parezca estar en riesgo, incluye un mensaje breve de contención y orienta a rutas urgentes.
Responde SIEMPRE en HTML limpio, usando:

- <p> para párrafos
- <ul> o <ol> para listas
- <strong> para negritas
- <br> para saltos de línea

No uses Markdown.
    
Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""

    # Invocación directa de Gemini
    respuesta = llm.invoke(prompt)
    return respuesta.content.replace("\n", "")


# ## Pruebas y ejemplos
# Ejecutar ejemplos rápidos para verificar la integración y respuestas del chatbot.

# In[11]:


#print(responder("¿Qué autoridades están facultadas para aplicar medidas correctivas según el Código?"))

