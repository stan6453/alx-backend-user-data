#!/usr/bin/env python3
"""Basic auth"""

from api.v1.auth.auth import Auth
import base64
from typing import Tuple


class BasicAuth(Auth):
    """basic auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
        for a Basic Authentication:"""
        if authorization_header is None or\
                type(authorization_header) is not str:
            return None

        arr = authorization_header.split(' ')
        if arr[0] != 'Basic':
            return None
        return arr[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """decode base64 encoded string and return the string"""
        if base64_authorization_header is None or\
                type(base64_authorization_header) is not str:
            return None
        try:
            base64_str = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return base64_str
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """extract user's credentials"""
        if decoded_base64_authorization_header is None or\
                type(decoded_base64_authorization_header) is not str:
            return None, None
        if decoded_base64_authorization_header.find(':') == -1:
            return None, None

        result = decoded_base64_authorization_header.split(':')
        return result[0], result[1]
