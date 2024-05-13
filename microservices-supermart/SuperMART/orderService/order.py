import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from datetime import datetime
from redis import Redis
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")


def create_connection():
    return psycopg2.connect(DATABASE_URL)


# Redis connection
redis_conn = Redis(host="localhost", port=6379)


# Endpoint API untuk menambahkan data pelanggan baru
@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.json
    nama = data["nama"]
    alamat = data["alamat"]
    no_telp = data["no_telp"]

    try:
        conn = create_connection()
        cur = conn.cursor()

        # Menyisipkan data pelanggan baru ke dalam tabel customer
        cur.execute(
            "INSERT INTO customer (nama, alamat, no_telp) VALUES (%s, %s, %s) RETURNING customer_id",
            (nama, alamat, no_telp),
        )
        customer_id = cur.fetchone()[0]

        # Mendapatkan tanggal saat ini
        order_date = datetime.now().strftime("%Y-%m-%d")

        # Menyisipkan data pelanggan baru ke dalam tabel detail_orders
        cur.execute(
            "INSERT INTO detail_orders (customer_id, nama, alamat, no_telp, order_date) VALUES (%s, %s, %s, %s, %s)",
            (customer_id, nama, alamat, no_telp, order_date),
        )

        conn.commit()

        cur.close()
        conn.close()

        # Publish message to Redis
        customer_data = {
            "customer_id": customer_id,
            "nama": nama,
            "alamat": alamat,
            "no_telp": no_telp,
            "order_date": order_date,
        }
        redis_conn.publish("new_customer", json.dumps(customer_data))

        return (
            jsonify(
                {"message": "Customer added successfully.", "customer_id": customer_id}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"message": "Failed to add customer.", "error": str(e)}), 500


# Endpoint API untuk mendapatkan semua data dari tabel detail_orders
@app.route("/detail_orders/latest")
def get_latest_order():
    try:
        # Ambil data pesanan terakhir dari database
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM detail_orders ORDER BY customer_id DESC LIMIT 1")
        order = cur.fetchone()

        cur.close()
        conn.close()

        # Return order data as JSON response
        if order:
            # Hanya kembalikan informasi yang diperlukan
            order_details = {
                "order_id": order[0],
                "nama": order[2],
                "alamat": order[3],
                "no_telp": order[4],
                "order_date": order[5],
            }
            return jsonify(order_details), 200
        else:
            return jsonify({"message": "No order found."}), 404
    except Exception as e:
        return jsonify({"message": "Failed to retrieve order.", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8000)
