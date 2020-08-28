from flask_restful import Resource, reqparse, fields, marshal
from flask import current_app, request, g
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from models import db, User, PasswordReset
from utilities.validators import email, password
from utilities.middlewares import authenticate
from utilities.mail import send_activate_mail
from datetime import datetime
from os import path
import random
import string
import time
import boto3


class Users(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.user_field = {
            'user':{
                'name':fields.String(attribute='user.name'),
                'email':fields.String(attribute='user.email'),
                'avatar':fields.String(attribute='user.avatar')
            }
        }
        self.allowed_extensions = ['jpg', 'jpeg', 'png']
        
    def post(self):
        self.parser.add_argument('name', type=str, required=True, help='name is required')
        self.parser.add_argument('email', type=email, required=True, help='valid email is required')
        self.parser.add_argument('password', type=password, required=True, help='password must be at least 8 characters')
        args = self.parser.parse_args()

        user = User.query.filter((User.email == args['email'])).first()

        if user:
            return {'message':'User with email exists'}, 403

        avatar_path = current_app.config['S3_BUCKET_LINK'] + 'users/unknown.png'; 
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 100)).lower()
        new_user = User(name=args['name'], email=args['email'], password=generate_password_hash(args['password']),
        avatar=avatar_path, activation_token=token)

        send_activate_mail(new_user)
        db.session.add(new_user)
        db.session.commit()
        data = {'user':new_user}
        return marshal(data, self.user_field, envelope='data'), 201

    def patch(self):
        field = request.args.get('field')
        if field is None:
            return {'message':'patch operation to be carried out is unknown'}, 400

        if field == 'avatar':
            return self.change_avatar()

        if field == 'activation_token':
            return self.activate()

        if field == 'password':
            return self.change_password()

        return {'message':'patch operation to be carried out is unknown'}, 400

    @authenticate
    def change_avatar(self):
        self.parser.add_argument('avatar', location='files', required=True, help='image avatar is required')
        args = self.parser.parse_args()
        avatar = request.files.get('avatar')
        filename = secure_filename(avatar.filename)

        ext = filename.rsplit('.')[1].lower()

        if ext not in self.allowed_extensions:
            return {'message':'unsupported file extension'}, 400

        filename = 'users' + '/' + str(time.time()) + filename

        user = User.query.get(g.user.id)
        user.avatar = self.upload_to_s3(user, filename, avatar)

        db.session.commit()
        data = {'user':user}

        return marshal(data, self.user_field, envelope='data')

    def upload_to_s3(self, user, filename, avatar):
        s3_resource = boto3.resource('s3', 
        aws_access_key_id=current_app.config['S3_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['S3_SECRET_KEY'])

        default_avatar = current_app.config['S3_BUCKET_LINK'] + 'users/unknown.png'
        bucket = s3_resource.Bucket(current_app.config['S3_BUCKET'])

        if user.avatar != default_avatar:
            key = user.avatar.split(current_app.config['S3_BUCKET_LINK'])[1]
            bucket.Object(key).delete()

        bucket.Object(filename).put(ACL='public-read', Body=avatar)
        file_path = current_app.config['S3_BUCKET_LINK'] + filename

        return file_path

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

        data = {'user':user}
        return marshal(data, self.user_field, envelope='data')


