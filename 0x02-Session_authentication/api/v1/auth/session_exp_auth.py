#!/usr/bin/env python3
""" Session expiration authentication Module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """Session expiration authentication class"""
    user_id_by_session_id = {}

    def __init__(self, *args, **kwargs):
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Overload of SessionAuth.create_session()
        create a unique session for a user

        Note:The same user_id can have multiple Session ID - indeed,
        the user_id is the value in the dictionary user_id_by_session_id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        SessionExpAuth.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload of SessionAuth.create_session()
        returns a User ID based on a given Session ID
        """
        if session_id is None:
            return None
        session_dictionary = SessionExpAuth.user_id_by_session_id.get(
            session_id)
        if session_dictionary is None:
            return None
        if 'created_at' not in session_dictionary:
            return None
        created_at = session_dictionary.get('created_at')
        if datetime.timestamp(created_at) + self.session_duration <=\
                datetime.timestamp(datetime.now()):
            return None
        return session_dictionary.get('user_id')
