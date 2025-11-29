# # Chatbot documental para la ciudadanía de Santander
# 
# Este notebook construye un chatbot documental para apoyar a la ciudadanía de Santander explicando normativa y rutas de atención. Pipeline breve: carga PDFs desde `data/`, los segmenta en chunks, crea embeddings (Sentence‑Transformers), los indexa en una base vectorial persistente (Chroma), y utiliza un LLM (Gemini via LangChain) para generar respuestas con contexto recuperado.

"""Flask importa correctamente responder() desde chatbot.py.

Renderiza el template HTML en /templates/index.html.

Cuando el usuario envía un mensaje, Flask llama responder() y lo muestra en pantalla.

Es totalmente compatible con HTML enriquecido porque no se usa Markdown."""

from flask import Flask, render_template, request
from chatbot import responder
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta = ""
    
    if request.method == "POST":
        mensaje = request.form.get("mensaje")
        if mensaje:
            respuesta = responder(mensaje)

    return render_template("index.html", respuesta=respuesta)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
