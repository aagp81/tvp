# app.py
from flask import Flask, jsonify, render_template_string
from scraper import buscar_estado_ot
import os

app = Flask(__name__)

@app.route("/ot/<numero>")
def estado_ot(numero):
    try:
        resultados = buscar_estado_ot(numero)
        if not resultados:
            return jsonify({"error": "No se encontraron datos para esa OT"}), 404
        return render_template_string(f"""
            <html>
            <head><meta charset="utf-8"><title>Vista Previa OT {numero}</title></head>
            <body>{resultados}</body>
            </html>
        """)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render define el puerto en PORT
    app.run(host="0.0.0.0", port=port)
