from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import time
from http import cookies
import random
import os
import json


def connection():
    conn = mysql.connector.connect(
        user="root", password="", host="localhost", database="pet-store"
    )
    if conn:
        print("Connecting to database successfully!")
    return conn


app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def index(self):
    return jsonify({"message": "Hello from server!"})


@app.route("/products", methods=["GET"])
def getAll():
    conn = connection()
    mycursor = conn.cursor()
    query = "SELECT * FROM `mega_products`"

    mycursor.execute(query)
    products = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return jsonify({"message": "Successfully!", "products": products})


@app.route("/products/<int:id>", methods=["GET"])
def getById(id):
    conn = connection()
    mycursor = conn.cursor()
    query = "SELECT * FROM `mega_products` WHERE `id` = %s"
    mycursor.execute(query, (id,))

    product = mycursor.fetchone()
    mycursor.close()
    conn.close()
    return jsonify({"message": "Successfully!", "product": product})


@app.route("/login", methods=["POST"])
def login():
    conn = connection()
    mycursor = conn.cursor()
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    print(email, password)

    if (email == "") or (password == ""):
        return jsonify({"status": "fail", "message": "Data not empty!"})

    query = "SELECT * FROM `mega_accounts` WHERE `email` = %s and `password` = %s"
    mycursor.execute(query, (email, password))

    user = mycursor.fetchone()

    mycursor.close()
    conn.close()
    if user == None:
        return jsonify({"status": "fail", "message": "Account not exist!"})

    return jsonify(
        {"status": "success", "message": "Login successfully!", "user": user}
    )


@app.route("/register", methods=["POST"])
def register():
    conn = connection()
    mycursor = conn.cursor()
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if (username == "") or (email == "") or (password == ""):
        return jsonify({"status": "fail", "message": "Data not empty!"})

    query = "SELECT * FROM `mega_accounts` WHERE `email` = %s"
    mycursor.execute(query, (email,))

    user = mycursor.fetchone()

    if user == None:
        id = int(time.time())
        query = "INSERT INTO `mega_accounts` (`id`, `username`, `email`, `password`, `enable`) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(query, (id, username, email, password, 1))
        conn.commit()
        mycursor.close()
        conn.close()
        return jsonify(
            {
                "status": "success",
                "message": "Register successfully!",
            }
        )
    else:
        mycursor.close()
        conn.close()
        return jsonify({"status": "fail", "message": "Email is exist!"})


@app.route("/cart", methods=["GET"])
def getCart():
    conn = connection()
    mycursor = conn.cursor()
    userId = request.headers.get("userId")

    query = "SELECT * FROM `mega_carts` WHERE `user_id` = %s"
    mycursor.execute(query, (userId,))

    products = mycursor.fetchall()

    if products == None:
        mycursor.close()
        conn.close()
        return jsonify({"message": "Cart is empty!"})

    productsList = []

    for product in products:
        query = "SELECT * FROM `mega_products` WHERE `id` = %s"
        mycursor.execute(query, (product[2],))
        results = mycursor.fetchall()
        psl = {
            "id": product[0],
            "productId": results[0][0],
            "image": results[0][6],
            "name": results[0][3],
            "price": results[0][7],
            "quanlity": product[3],
        }
        productsList.append(psl)

    mycursor.close()
    conn.close()

    return jsonify({"message": "Update cart success!", "products": productsList})


@app.route("/cart", methods=["POST"])
def postCart():
    conn = connection()
    mycursor = conn.cursor()
    data = request.get_json()

    userId = data.get("userId")
    productId = data.get("productId")
    quanlity = data.get("quanlity")

    id = int(time.time())
    random_int = random.randint(100, 999)

    id = str(id) + str(random_int)

    query = "INSERT INTO `mega_carts` (`id`, `user_id`, `product_id`, `quanlity`) VALUES (%s, %s, %s, %s)"
    mycursor.execute(query, (id, userId, productId, quanlity))
    conn.commit()
    mycursor.close()
    conn.close()
    return jsonify({"message": "success!"})


@app.route("/cart", methods=["PUT"])
def updateCart():
    conn = connection()
    mycursor = conn.cursor()
    data = request.get_json()

    userId = data.get("userId")
    productId = data.get("productId")
    quanlity = data.get("quanlity")

    query = "UPDATE `mega_carts` SET `quanlity` = %s WHERE `product_id` = %s and `user_id` = %s"
    mycursor.execute(
        query,
        (
            quanlity,
            productId,
            userId,
        ),
    )

    conn.commit()
    mycursor.close()
    conn.close()
    return jsonify({"message": "success!"})


@app.route("/cart", methods=["DELETE"])
def deleteCart():
    conn = connection()
    mycursor = conn.cursor()
    data = request.get_json()

    userId = data.get("userId")
    productId = data.get("productId")

    query = "DELETE FROM `mega_carts` WHERE `product_id` = %s and `user_id` = %s"
    mycursor.execute(
        query,
        (
            productId,
            userId,
        ),
    )

    conn.commit()
    mycursor.close()
    conn.close()
    return jsonify({"message": "success!"})


@app.route("/checkout", methods=["POST"])
def postCheckout():
    products = request.get_json()
    conn = connection()
    mycursor = conn.cursor()
    for product in products:
        query = "DELETE FROM `mega_carts` WHERE `id` = %s"
        mycursor.execute(query, (product.get("id"),))
        conn.commit()

    mycursor.close()
    conn.close()

    checkoutData = json.dumps(products, ensure_ascii=False)

    with open("../checkout.json", "a", encoding="utf-8") as file:
        file.write(checkoutData)

    return jsonify(
        {"status": "success", "message": "The order has been placed successfully!"}
    )


if __name__ == "__main__":
    app.run(debug=True, port="8080")
