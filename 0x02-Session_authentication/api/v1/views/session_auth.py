#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, make_response
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """User login logic"""
    user_email = request.form.get('email')
    password = request.form.get('password')

    if user_email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        auth_user = User.search({'email': user_email})
    except Exception:
        return None

    assert not len(auth_user) > 1
    if len(auth_user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    auth_user = auth_user[0]
    if not auth_user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # username and password match, create a session for user
    from api.v1.app import auth
    session_id = auth.create_session(auth_user.id)
    session_cookie_name = getenv('SESSION_NAME')

    response = make_response(auth_user.to_json())
    response.set_cookie(session_cookie_name, session_id)
    return response
