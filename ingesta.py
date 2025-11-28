#!/usr/bin/env python
# coding: utf-8

# # Chatbot documental para la ciudadanía de Santander
# 
# Este notebook construye un chatbot documental para apoyar a la ciudadanía de Santander explicando normativa y rutas de atención. Pipeline breve: carga PDFs desde `data/`, los segmenta en chunks, crea embeddings (Sentence‑Transformers), los indexa en una base vectorial persistente (Chroma), y utiliza un LLM (Gemini via LangChain) para generar respuestas con contexto recuperado.
# 
# Uso: asegúrese de definir las variables de entorno necesarias (por ejemplo `LANGCHAIN_API_KEY`) en un archivo `.env` o exportarlas en el entorno antes de ejecutar las celdas. Este notebook prioriza claridad, trazabilidad y ejemplos de prueba.

"""Este archivo es solo para crear la base vectorial, no para consultarla.

Se cargan todos los PDFs desde data/, se dividen en chunks y se indexan en Chroma.

Genera una carpeta persistente llamada /vectores que luego usa el chatbot.

Este proceso puede tardar mucho dependiendo del tamaño de los documentos y no debe ejecutarse en producción cada vez que el usuario pregunte."""

# ## Carga y preparación de documentos
# Funciones para localizar y cargar PDFs desde `data/` y segmentarlos en chunks para indexado.

# In[1]:


import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = "data/"

def load_documents(path=DATA_PATH):
    docs = []
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(path, file))
            docs.extend(loader.load())

    print(f"Documentos cargados: {len(docs)}")
    return docs

docs = load_documents()


# In[2]:


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(docs)
print(f"Chunks creados: {len(chunks)}")


# ## Indexado vectorial — Chroma + Embeddings
# Creación de la base vectorial persistente y del modelo de embeddings.

# In[3]:


import chromadb
# Nuevo cliente persistente
client = chromadb.PersistentClient(path="./vectores")

# Crear o cargar colección
collection = client.get_or_create_collection(
    name="documentos_colombia",
    metadata={"hnsw:space": "cosine"}
)

print("Chroma inicializado correctamente.")


# In[6]:


from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


# In[7]:


texts = [c.page_content for c in chunks]

embeddings = embedder.encode(texts).tolist()

collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=[f"id_{i}" for i in range(len(texts))]
)

print("Base vectorial creada.")

