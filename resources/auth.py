from flask_restful import reqparse, Resource, fields, marshal
from models import db, User
from utilities.validators import email, password
from werkzeug.security import check_password_hash
from utilities.token import generate_token

class Auth(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.field = {
            'token':fields.String(attribute='token'),
            'user':{
                'name':fields.String(attribute='user.name'),
                'email':fields.String(attribute='user.email'),
                'avatar':fields.String(attribute='user.avatar')
            }
        }

    def post(self):
        self.parser.add_argument('email', type=email, required=True, help='valid email is required')
        self.parser.add_argument('password', type=password, required=True, help='password must be at least 8 characters')
        args = self.parser.parse_args()

        user = User.query.filter((User.email == args['email'])).first()

        if user is None or user.activation_token is not None:
            return {'message':'Incorrect email or password'}, 404
        
        if check_password_hash(user.password, args['password']) == False:
            return {'message':'Incorrect email or password'}, 404

        data = {'token':generate_token(user.id), 'user':user}

        return marshal(data, self.field, envelope='data')
            
        
