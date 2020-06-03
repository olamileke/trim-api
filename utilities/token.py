from flask import current_app
from datetime import datetime, timedelta
import jwt

def generate_token(id):
    payload = {
        'iat':datetime.now(),
        'exp':datetime.now() + timedelta(days=14),
        'sub':id
    }

    return jwt.encode(payload, current_app.config['SECRET_KEY'],
    algorithm='HS256').decode('utf-8')
