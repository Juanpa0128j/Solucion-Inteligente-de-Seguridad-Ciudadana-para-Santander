## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. Clonar el repositorio y UBICARSE en la carpeta chatbot:
```bash
git clone
...
cd chatbot
```

2. Instalar dependencias ubicado en la carpeta chatbot:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:

Crear un archivo `.env` en la raíz del proyecto con:
```
LANGCHAIN_API_KEY=tu_clave_api_aqui
```

4. Preparar los documentos:

Colocar los archivos PDF en la carpeta `data/`

5. Crear la base vectorial (solo una vez):
```bash
python ingesta.py
```

Este proceso puede tardar varios minutos dependiendo del tamaño de los documentos.

## Uso

### Iniciar el Servidor
```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Interacción con el Chatbot

1. Abrir el navegador en la URL del servidor
2. Escribir preguntas sobre normativa o rutas de atención
3. Recibir respuestas en formato HTML con información clara y estructurada

### Ejemplos de Preguntas

- "¿Qué es la Ley 1257 de 2008?"
- "¿Cuáles son las rutas de atención para violencia intrafamiliar?"
- "¿Qué autoridades pueden aplicar medidas correctivas según el Código de Seguridad?"
- "¿Cómo denunciar violencia sexual?"

## Estructura del Proyecto
```
proyecto/
│
├── data/                   # Carpeta con PDFs fuente
├── vectores/               # Base vectorial persistente (generada)
├── templates/
│   └── index.html         # Interfaz web
├── ingesta.py             # Script de indexación
├── chatbot.py             # Lógica del chatbot
├── app.py                 # Servidor Flask
```