#!/usr/bin/env python3
"""Basic auth"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header for a Basic Authentication:"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        
        arr = authorization_header.split(' ')
        if arr[0] != 'Basic':
            return None
        return arr[1]
