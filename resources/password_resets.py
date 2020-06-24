from flask_restful import Resource, reqparse
from flask import g, request
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
        action = request.args.get('action')

        if action is None:
            return {'message':'action to be carried out is unknown'}, 400
        
        if action == 'mail':
            return self.mail()

        if action == 'verify':
            return self.verify()

        return {'message':'action to be carried out is unknown'}, 400
        
    def mail(self):
        self.parser.add_argument('email', type=email, required=True, help='email is required')
        args = self.parser.parse_args()

        user = User.query.filter((User.email == args['email'])).first()

        if user is None:
            return {'message':'User does not exist'}, 404

        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 100)).lower()
        expiry = datetime.now() + timedelta(minutes=30)

        reset = PwReset(user_id=user.id, token=token, expires_at=expiry)
        send_password_reset_mail(user, reset)
        db.session.add(reset)
        db.session.commit()

        return {'data':{'message':'password reset email sent successfully'}}

    def verify(self):
        self.parser.add_argument('token', type=str, required=True, help='reset token is required')
        args = self.parser.parse_args()

        reset = PwReset.query.filter((PwReset.token == args['token'])).first()

        if reset is None:
            return {'message':'invalid password reset token'}, 400

        if datetime.now() > reset.expires_at:
            db.session.delete(reset)
            return {'message':'expired password reset token'}, 400

        db.session.commit()
        return {'data':{'message':'valid password reset token'}}



    

        
        

