from flask_restful import Resource, reqparse
from flask import g
from utilities.validators import email
from utilities.mail import send_password_reset_mail
from models import db, User , PasswordReset as PwReset
from datetime import datetime, timedelta
import random
import string

class PasswordResets(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('email', type=email, required=True, help='email is required')
        args = self.parser.parse_args()

        user = User.query.filter((User.email == args['email'])).first()

        if user is None:
            return {'error':{'message':'User does not exist'}}, 404

        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 100)).lower()
        expiry = datetime.now() + timedelta(minutes=30)

        reset = PwReset(user_id=user.id, token=token, expires_at=expiry)
        send_password_reset_mail(user, reset)
        db.session.add(reset)
        db.session.commit()

        return {'data':{'message':'password reset email sent successfully'}}
        

