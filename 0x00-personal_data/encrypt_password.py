#!/usr/bin/env python3
"""Password security module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """return hashed password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str):
    """Use bcrypt to validate that the provided
    password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
