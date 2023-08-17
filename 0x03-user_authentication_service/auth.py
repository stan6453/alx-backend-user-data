#!/usr/bin/env python3
"""AUTH module
"""
from db import DB
from user import User
from typing import Union
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """generate and return a UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialize auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """check if username and password match"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str):
        """creates and stores a new user session in the DB"""
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """return a user object based on a given session_id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """remove the session from storage for a given user"""
        if not user_id:
            return None
        try:
            self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str):
        """store and return a new reset_token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str):
        """updates a user's password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
