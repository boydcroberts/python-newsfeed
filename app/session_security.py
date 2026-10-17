import os
import secrets


def session_secret():
    """Use a private deployment key, or an unpredictable development key."""
    configured = os.environ.get('SECRET_KEY')
    if configured is None:
        return secrets.token_hex(32)
    if len(configured.encode('utf-8')) < 32:
        raise ValueError('SECRET_KEY must contain at least 32 bytes.')
    return configured
