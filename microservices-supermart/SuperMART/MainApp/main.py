from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)


# Endpoint untuk merender index.html
@app.route("/")
def index():
    return render_template("index.html")


# Endpoint untuk mendapatkan data pakaian dari API pakaian
@app.route("/clothing", methods=["GET"])
def get_clothing_items():
    try:
        # Mengambil data pakaian dari API pakaian
        response = requests.get("http://localhost:5432/clothing")
        clothing_items = response.json()
        return jsonify(clothing_items), 200
    except Exception as e:
        print("Error getting clothing items:", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Endpoint untuk mendapatkan data elektronik dari API elektronik
@app.route("/electronics", methods=["GET"])
def get_electronics_items():
    try:
        # Mengambil data elektronik dari API elektronik
        response = requests.get("http://localhost:5432/electronics")
        electronics_items = response.json()
        return jsonify(electronics_items), 200
    except Exception as e:
        print("Error getting electronics items:", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Endpoint untuk mendapatkan data snack dari API snack
@app.route("/snacks", methods=["GET"])
def get_snacks_items():
    try:
        # Mengambil data snack dari API snack
        response = requests.get("http://localhost:5432/snacks")
        snacks_items = response.json()
        return jsonify(snacks_items), 200
    except Exception as e:
        print("Error getting snacks items:", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Endpoint untuk menerima pesanan baru
@app.route("/customers", methods=["POST"])
def create_order():
    try:
        data = request.json
        # Mengirim pesanan ke API order
        response = requests.post("http://localhost:8000/customers", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print("Error creating order:", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Endpoint untuk mendapatkan detail pesanan berdasarkan order_id
@app.route("/detail_orders/latest", methods=["GET"])
def get_order():
    try:
        # Mengambil detail pesanan dari API order
        response = requests.get(f"http://localhost:8000/detail_orders/latest")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print("Error getting order details:", e)
        return jsonify({"message": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
