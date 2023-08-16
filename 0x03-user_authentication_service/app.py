#!/usr/bin/env python3
"""Basic flask app"""

from auth import Auth
from flask import Flask, request, jsonify

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """home endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
