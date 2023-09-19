#!/usr/bin/env python3
"""Password security module"""
import bcrypt

def hash_password(password: str) -> bytes:
    """return hashed password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
