# DOLCESUBURBAN

Tienda web de ropa y calzado desarrollada con Python + Flask.

## Requisitos

- Python 3.10 o superior
- Navegador web

## Instalación

Abre una terminal dentro de esta carpeta y ejecuta:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Luego abre en el navegador:

http://127.0.0.1:5000

## Chatbot

El chatbot está implementado en `app.py` mediante la función `chatbot_reply()` y responde preguntas sobre:

- productos
- precios
- tallas
- envíos
- pagos
- cambios
- horarios
- ubicación
- categorías

Puedes ampliar sus respuestas modificando esa función.

## Personalización

Los productos se encuentran al inicio de `app.py`, dentro de `PRODUCTS`.

La respuesta de ubicación también está en `FAQ["ubicacion"]`; reemplázala por la dirección real de la tienda si corresponde.

## Nota

Esta versión funciona completamente de forma local. El carrito se guarda en el navegador mediante localStorage. El botón de finalizar compra es demostrativo y no procesa pagos reales.
