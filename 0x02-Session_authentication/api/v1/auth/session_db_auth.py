#!/usr/bin/env python3
""" Session persistent authentication module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime
from typing import TypeVar

UserSession.load_from_file()


class SessionDBAuth(SessionExpAuth):
    """Session persistent authentication class"""

    def create_session(self, user_id=None):
        """creates a persistent session that is stored in json database"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # NOTE: we can ignore the field created_at since
        # UserSession will add the field for us
        new_session = UserSession(id=session_id, user_id=user_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a User ID based on a given Session ID
        """
        if session_id is None:
            return None
        session_object = UserSession.get(session_id)
        if session_object is None:
            return None
        # if there is no session_duration on cookie expiry,
        # then no need to check
        if self.session_duration <= 0:
            return getattr(session_object, 'user_id', None)
        # else, if there is session duration, make sure that the key created_at
        # is set in the session_dictionary
        if not hasattr(session_object, 'created_at'):
            return None
        created_at = getattr(session_object, 'created_at', None)

        if datetime.timestamp(created_at) + self.session_duration <=\
                datetime.timestamp(datetime.utcnow()):
            return None
        return getattr(session_object, 'user_id', None)

    def destroy_session(self, request=None):
        """destroy the current user session stored in the json database"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        session_object = UserSession.get(session_id)
        user_id = getattr(session_object, 'user_id', None)
        if user_id is None:
            return False
        session_object.remove()
        return True

    def current_user(self, request=None) -> TypeVar('User'):
        """returns a User instance based on a cookie value"""
        from models.user import User

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
