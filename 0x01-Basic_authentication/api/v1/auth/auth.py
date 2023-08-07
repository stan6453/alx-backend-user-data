#!/usr/bin/env python3
"""AUTHORIZATION Class"""

from flask import request
from typing import TypeVar, List


def verify_partial_path(path: str, excluded_paths: List[str]) -> bool:
    """returns true if partial path requires authentication"""
    if len(excluded_paths) == 0:
        return True
    for item in excluded_paths:
        if path.startswith(item[:-1]):
            return False
    return True


class Auth():
    """AUTHORIZATION Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns true if path requires authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        full_path = [path1 for path1 in excluded_paths if not path1.find('*')]
        # path like : ["/api/v1/stat*"]
        partial_path = [
            path1 for path1 in excluded_paths if path1.endswith('*')]

        if path not in full_path or verify_partial_path(path, partial_path):
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
