from flask_restful import Resource, reqparse, fields, marshal
from flask import current_app
from werkzeug.security import generate_password_hash
from models import db, User
from utilities.validators import email, password

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

        new_user = User(name=args['name'], email=args['email'], password=generate_password_hash(args['password']))
        db.session.add(new_user)
        db.session.commit()
        return marshal(new_user, user_field, envelope='data'), 201

