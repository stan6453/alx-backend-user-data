#!/usr/bin/env python3
"""
 End-to-end integration test
"""


import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str):
    """Test creating new user endpoint"""
    response = requests.post(
        "{}/users".format(BASE_URL), data={"email": email,
                                           "password": password})
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str):
    """Test creating new user endpoint with wrong password"""
    response = requests.post("{}/sessions".format(BASE_URL),
                             data={"email": email, "password": password})
    assert response.status_code == 401


def profile_unlogged():
    """Test Checking profile while unlogged (no session ID)."""
    response = requests.get("{}/profile".format(BASE_URL))
    assert response.status_code == 403


def log_in(email: str, password: str):
    """Log in with the provided email and password
    and return the session ID."""
    response = requests.post("{}/sessions".format(BASE_URL),
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.cookies.get("session_id") != None


def profile_logged(session_id: str):
    """Check profile while logged in with the given session ID."""
    response = requests.get("{}/profile".format(BASE_URL),
                            cookies={"session_id": session_id})
    assert response.status_code == 200


def log_out(session_id: str):
    """Log out using the provided session ID."""
    response = requests.delete(
        "{}/sessions".format(BASE_URL), cookies={"session_id": session_id})
    assert response.status_code == 302


def reset_password_token(email: str):
    """Request a reset password token for the given email."""
    response = requests.post(
        "{}/reset_password".format(BASE_URL), data={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["reset_token"] is not None


def update_password(email: str, reset_token: str, new_password: str):
    """Update password using the provided reset token and new password."""
    response = requests.put(
        "{}/reset_password".format(BASE_URL),
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password}
    )
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
