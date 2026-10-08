from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Camiseta Urbana", "category": "mujer", "type": "ropa", "price": 45000, "sizes": ["S", "M", "L"], "emoji": "👚"},
    {"id": 2, "name": "Jean Clásico", "category": "mujer", "type": "ropa", "price": 95000, "sizes": ["6", "8", "10", "12"], "emoji": "👖"},
    {"id": 3, "name": "Tenis Street", "category": "mujer", "type": "calzado", "price": 125000, "sizes": ["35", "36", "37", "38", "39"], "emoji": "👟"},
    {"id": 4, "name": "Vestido Casual", "category": "mujer", "type": "ropa", "price": 110000, "sizes": ["S", "M", "L"], "emoji": "👗"},
    {"id": 5, "name": "Camiseta Oversize", "category": "hombre", "type": "ropa", "price": 55000, "sizes": ["S", "M", "L", "XL"], "emoji": "👕"},
    {"id": 6, "name": "Jean Denim", "category": "hombre", "type": "ropa", "price": 105000, "sizes": ["28", "30", "32", "34", "36"], "emoji": "👖"},
    {"id": 7, "name": "Tenis Urban", "category": "hombre", "type": "calzado", "price": 140000, "sizes": ["39", "40", "41", "42", "43"], "emoji": "👟"},
    {"id": 8, "name": "Chaqueta Street", "category": "hombre", "type": "ropa", "price": 135000, "sizes": ["M", "L", "XL"], "emoji": "🧥"},
]

FAQ = {
    "horario": "Nuestro horario de atención es de lunes a sábado de 9:00 a. m. a 7:00 p. m.",
    "envio": "Sí. Realizamos envíos. El costo y tiempo dependen de la ciudad de destino.",
    "pago": "Puedes pagar mediante transferencia, efectivo y otros medios disponibles al momento de la compra.",
    "cambio": "Aceptamos cambios de prendas en buen estado. Conserva la factura o comprobante y consulta las condiciones de la tienda.",
    "talla": "Las tallas disponibles aparecen en cada producto. Si me dices qué producto buscas, puedo indicarte sus tallas.",
    "ubicacion": "DOLCESUBURBAN es una tienda de moda para dama y hombre. Puedes personalizar esta respuesta con tu dirección real en app.py.",
}

def chatbot_reply(message):
    text = message.lower().strip()

    if any(w in text for w in ["hola", "buenas", "hey", "holi"]):
        return "¡Hola! 👋 Soy el asistente de DOLCESUBURBAN. Puedo ayudarte con productos, tallas, precios, envíos, pagos, cambios y más."
    if any(w in text for w in ["gracias", "thank"]):
        return "¡Con mucho gusto! 😊 ¿Quieres que te ayude a encontrar algún producto?"
    if any(w in text for w in ["horario", "hora", "abren", "cierran"]):
        return FAQ["horario"]
    if any(w in text for w in ["envío", "envio", "domicilio", "entrega"]):
        return FAQ["envio"]
    if any(w in text for w in ["pago", "pagar", "transferencia", "efectivo"]):
        return FAQ["pago"]
    if any(w in text for w in ["cambio", "devolver", "devolución", "devolucion"]):
        return FAQ["cambio"]
    if any(w in text for w in ["talla", "tallas", "tamaño"]):
        return FAQ["talla"]
    if any(w in text for w in ["ubicación", "ubicacion", "dirección", "direccion", "dónde", "donde"]):
        return FAQ["ubicacion"]

    if any(w in text for w in ["precio", "cuesta", "vale", "valor"]):
        matches = [p for p in PRODUCTS if any(word in p["name"].lower() for word in text.split() if len(word) > 3)]
        if matches:
            return "El precio de {} es ${:,} COP.".format(matches[0]["name"], matches[0]["price"]).replace(",", ".")
        return "Tenemos productos desde $45.000 COP. Dime el nombre del producto y te indico su precio."

    if "mujer" in text or "dama" in text:
        names = ", ".join(p["name"] for p in PRODUCTS if p["category"] == "mujer")
        return f"Para dama tenemos: {names}."
    if "hombre" in text or "caballero" in text:
        names = ", ".join(p["name"] for p in PRODUCTS if p["category"] == "hombre")
        return f"Para hombre tenemos: {names}."
    if "zapato" in text or "zapatos" in text or "tenis" in text:
        names = ", ".join(p["name"] for p in PRODUCTS if p["type"] == "calzado")
        return f"En calzado tenemos: {names}."
    if "ropa" in text or "prenda" in text:
        names = ", ".join(p["name"] for p in PRODUCTS if p["type"] == "ropa")
        return f"Tenemos estas prendas: {names}."

    if any(w in text for w in ["qué vendes", "que vendes", "productos", "catálogo", "catalogo"]):
        return "Tenemos ropa y calzado para dama y hombre. Puedes explorar el catálogo usando los filtros de la página."

    return "Puedo ayudarte con productos, precios, tallas, envíos, pagos, cambios y horarios. También puedes preguntarme algo general y trataré de orientarte. 😊"

@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not message.strip():
        return jsonify({"reply": "Escribe una pregunta para que pueda ayudarte."})
    return jsonify({"reply": chatbot_reply(message)})

if __name__ == "__main__":
    app.run(debug=True)
