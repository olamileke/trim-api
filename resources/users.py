from flask_restful import Resource, reqparse, fields, marshal
from flask import current_app, request, g
from werkzeug.security import generate_password_hash
from models import db, User, PasswordReset
from utilities.validators import email, password
from utilities.middlewares import authenticate
from utilities.mail import send_activate_mail
from datetime import datetime
from os import path
import random
import string

user = {}
user['name'] = fields.String(attribute='name')
user['email'] = fields.String(attribute='email')
user['avatar'] = fields.String(attribute='avatar', default=None)

user_field = {
    'user':user
}

class Users(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.method_decorators = {'patch':[authenticate]}

    def post(self):
        self.parser.add_argument('name', type=str, required=True, help='name is required')
        self.parser.add_argument('email', type=email, required=True, help='valid email is required')
        self.parser.add_argument('password', type=password, required=True, help='password must be at least 8 characters')
        args = self.parser.parse_args()

        user = User.query.filter((User.email == args['email'])).first()

        if user:
            return {'error':{'message':'User with email exists'}}, 403

        avatar_path = self.generate_default_user_image()
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 100)).lower()
        new_user = User(name=args['name'], email=args['email'], password=generate_password_hash(args['password']),
        avatar=avatar_path, activation_token=token)

        send_activate_mail(new_user)
        db.session.add(new_user)
        db.session.commit()
        return marshal(new_user, user_field, envelope='data'), 201


    def patch(self):
        field = request.args.get('field')
        if field is None:
            return {'error':{'message':'patch operation to be carried out is unknown'}}, 400

        if field == 'activation_token':
            return self.activate()

        if field == 'password':
            return self.change_password()

            
    def change_password(self):
        self.parser.add_argument('password', type=password, required=True, help='password must be at least 8 characters')
        self.parser.add_argument('token', type=str, required=True, help='password reset token is required')
        args = self.parser.parse_args()

        reset = PasswordReset.query.filter((PasswordReset.token == args['token'])).first()

        if reset is None:
            return {'error':{'message':'invalid reset token'}}, 400
        
        if datetime.now() > reset.expires_at:
            return {'error':{'message':'expired reset token'}}, 400

        user = User.query.filter((User.id == reset.user_id)).first()
        user.password = generate_password_hash(args['password'])
        db.session.delete(reset)
        db.session.commit()

        return {'data':{'message':'password changed successfully'}}

    
    def activate(self):
        self.parser.add_argument('token', type=str, required=True, help='activation token is required')
        args = self.parser.parse_args()
        user = User.query.filter((User.activation_token == args['token'])).first()

        if user is None:
            return {'error':{'message':'invalid activation token'}}, 400

        user.activation_token = None
        db.session.commit()

        return marshal(user, user_field, envelope='data')


    def generate_default_user_image(self):
        avatar_path = path.join(current_app.config['BASE_DIR'], 'images', 'users', 'anon.png')

        return avatar_path


