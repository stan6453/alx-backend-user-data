#!/usr/bin/env python3
""" Session authentication
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """basic auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a unique session for a user

        Note:The same user_id can have multiple Session ID - indeed,
        the user_id is the value in the dictionary user_id_by_session_id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns a User instance based on a cookie value"""
        from models.user import User

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroy the current user session stored in the dictionary
        SessionAuth.user_id_by_session_id"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
