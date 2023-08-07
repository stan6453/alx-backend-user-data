#!/usr/bin/env python3
"""AUTHORIZATION Class"""

from flask import request
from typing import TypeVar, List


class Auth():
    """AUTHORIZATION Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns true if path requires authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """get auth info from the authorization header"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """get and return the current user"""
        return None
