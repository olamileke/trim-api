from flask_restful import Resource, reqparse, fields, marshal
from flask import current_app, request, g
from werkzeug.security import generate_password_hash
from models import db, User
from utilities.validators import email, password
from utilities.middlewares import authenticate
from os import path

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
        self.method_decorators = {'patch':[authenticate]}

    def post(self):
        self.parser.add_argument('name', type=str, required=True,
        help='name is required')
        self.parser.add_argument('email', type=email, required=True,
        help='valid email is required')
        self.parser.add_argument('password', type=password, required=True,
        help='password must be at least 8 characters')

        args = self.parser.parse_args()

        user = User.query.filter((User.email == args['email'])).first()

        if user:
            return {'error':{'message':'User with email exists'}}, 403

        avatar_path = self.generate_default_user_image()
        new_user = User(name=args['name'], email=args['email'], password=generate_password_hash(args['password']),
        avatar=avatar_path)
        db.session.add(new_user)
        db.session.commit()
        return marshal(new_user, user_field, envelope='data'), 201

    def patch(self):
        image = request.files['image']

        if image.filename == '':
            return {'error':{'message':'upload a valid image'}}

        return {'image':image.filename}


    def generate_default_user_image(self):
        avatar_path = path.join(current_app.config['BASE_DIR'], 'images', 'users', 'anon.png')

        return avatar_path


