"""
Authentication API
Simple app-password gate using signed tokens.
"""

import hmac
from functools import wraps

from flask import Blueprint, request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from ..config import Config
from ..utils.logger import get_logger

logger = get_logger('mirofish.auth')

auth_bp = Blueprint('auth', __name__)

PUBLIC_PATHS = frozenset({'/health', '/api/auth/login'})


def _get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def _auth_enabled() -> bool:
    return bool(Config.APP_PASSWORD)


def verify_token(token: str) -> bool:
    if not token:
        return False
    try:
        _get_serializer().loads(token, max_age=Config.AUTH_TOKEN_MAX_AGE)
        return True
    except (SignatureExpired, BadSignature):
        return False


def require_auth(f):
    """Decorator for individual routes that need auth."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not _auth_enabled():
            return f(*args, **kwargs)
        token = request.headers.get('Authorization', '').removeprefix('Bearer ')
        if not verify_token(token):
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


def auth_middleware():
    """Before-request hook that gates all /api/* routes."""
    if not _auth_enabled():
        return None

    if request.path in PUBLIC_PATHS:
        return None

    if not request.path.startswith('/api/'):
        return None

    token = request.headers.get('Authorization', '').removeprefix('Bearer ')
    if not verify_token(token):
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    return None


@auth_bp.route('/login', methods=['POST'])
def login():
    if not _auth_enabled():
        return jsonify({"success": True, "token": "no-auth", "message": "Auth disabled"})

    data = request.get_json(silent=True) or {}
    password = data.get('password', '')

    if not hmac.compare_digest(password, Config.APP_PASSWORD):
        logger.warning(f"Failed login attempt from {request.remote_addr}")
        return jsonify({"success": False, "error": "Wrong password"}), 401

    token = _get_serializer().dumps({"auth": "ok"})
    logger.info(f"Successful login from {request.remote_addr}")
    return jsonify({"success": True, "token": token})
