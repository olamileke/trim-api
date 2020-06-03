from flask import current_app, request, g
from models import db, User
from functools import wraps
import jwt

def authenticate(method):
    @wraps(method)
    def middleware(*args, **kwargs):
        token = request.headers.get('Authorization').split(' ')[1]

        print(token)

        if token is None:
            return {'error':{'message':'Authentication failed'}}, 401

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'],
            algorithms='HS256')
            g.user = User.query.get(payload['sub'])

            if g.user is None:
                return {'error':{'message':'Authentication failed'}}, 401

            return method(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return {'error':{'message':'Authentication failed'}}, 401
        except jwt.InvalidTokenError:
            return {'error':{'message':'Authentication failed'}}, 401

    
    return middleware



