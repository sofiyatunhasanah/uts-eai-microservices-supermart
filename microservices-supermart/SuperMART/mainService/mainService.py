import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify
from redis import Redis

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")


def create_connection():
    return psycopg2.connect(DATABASE_URL)


# Initialize Redis connection
redis = Redis(host="localhost", port=6379)


# Endpoint untuk mengambil data dari tabel clothing
@app.route("/clothing", methods=["GET"])
def get_clothing_items():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM clothing;")
        clothing_items = cursor.fetchall()

        clothing_list = []
        for item in clothing_items:
            item_dict = {
                "item_id": item[0],
                "item_name": item[1],
                "description": item[2],
                "price": float(item[3]),
                "size": item[4],
                "image_url": item[5],  # Kolom image_url yang telah ditambahkan
            }
            clothing_list.append(item_dict)

        # Publish message to clothing topic
        redis.publish("clothing_topic", str(clothing_list))

        return jsonify(clothing_list), 200

    except psycopg2.Error as e:
        print("Error fetching clothing items:", e)
        return jsonify({"message": "Internal Server Error"}), 500

    finally:
        if conn:
            conn.close()


# Endpoint untuk mengambil data dari tabel electronics
@app.route("/electronics", methods=["GET"])
def get_electronics_items():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM electronics;")
        electronics_items = cursor.fetchall()

        electronics_list = []
        for item in electronics_items:
            item_dict = {
                "item_id": item[0],
                "item_name": item[1],
                "description": item[2],
                "price": float(item[3]),
                "brand": item[4],
                "image_url": item[5],  # Kolom image_url yang telah ditambahkan
            }
            electronics_list.append(item_dict)

        # Publish message to electronics topic
        redis.publish("electronics_topic", str(electronics_list))

        return jsonify(electronics_list), 200

    except psycopg2.Error as e:
        print("Error fetching electronics items:", e)
        return jsonify({"message": "Internal Server Error"}), 500

    finally:
        if conn:
            conn.close()


# Endpoint untuk mengambil data dari tabel snacks
@app.route("/snacks", methods=["GET"])
def get_snacks_items():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM snacks;")
        snacks_items = cursor.fetchall()

        snacks_list = []
        for item in snacks_items:
            item_dict = {
                "item_id": item[0],
                "item_name": item[1],
                "description": item[2],
                "price": float(item[3]),
                "expiration_date": str(
                    item[4]
                ),  # Konversi ke string agar dapat di-JSONify
                "image_url": item[5],  # Kolom image_url yang telah ditambahkan
            }
            snacks_list.append(item_dict)

        # Publish message to snacks topic
        redis.publish("snacks_topic", str(snacks_list))

        return jsonify(snacks_list), 200

    except psycopg2.Error as e:
        print("Error fetching snacks items:", e)
        return jsonify({"message": "Internal Server Error"}), 500

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5432)
