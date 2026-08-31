"""Google sign-in (OAuth 2.0 authorization code flow) and cookie sessions.

Configuration comes from the environment:
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET  — from Google Cloud Console
    BASE_URL   — public URL of this deployment (for the redirect URI)
    SESSION_SECRET — cookie signing key
"""

from __future__ import annotations

import os
import secrets
from urllib.parse import urlencode

import httpx
from itsdangerous import BadSignature, URLSafeSerializer

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


def client_id() -> str:
    return os.environ.get("GOOGLE_CLIENT_ID", "")


def _client_secret() -> str:
    return os.environ.get("GOOGLE_CLIENT_SECRET", "")


def base_url() -> str:
    return os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")


def configured() -> bool:
    return bool(client_id() and _client_secret())


_serializer = URLSafeSerializer(
    os.environ.get("SESSION_SECRET") or secrets.token_hex(32), salt="teachme-session"
)


def make_session_cookie(email: str, name: str) -> str:
    return _serializer.dumps({"email": email, "name": name})


def read_session_cookie(value: str | None) -> dict | None:
    if not value:
        return None
    try:
        return _serializer.loads(value)
    except BadSignature:
        return None


def login_redirect_url(state: str) -> str:
    params = {
        "client_id": client_id(),
        "redirect_uri": f"{base_url()}/auth/callback",
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def exchange_code(code: str) -> dict:
    """Trade the authorization code for the user's email and name."""
    with httpx.Client(timeout=15) as client:
        token = client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": client_id(),
                "client_secret": _client_secret(),
                "redirect_uri": f"{base_url()}/auth/callback",
                "grant_type": "authorization_code",
            },
        )
        token.raise_for_status()
        access_token = token.json()["access_token"]
        info = client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        info.raise_for_status()
        return info.json()  # keys: email, name, picture, ...
