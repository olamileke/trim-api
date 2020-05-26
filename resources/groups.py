from flask_restful import Resource, fields, reqparse, marshal
from flask import g
from models import db, Group
from utilities.middlewares import authenticate
from utilities.validators import group_name, url

class Groups(Resource):
    def __init__(self):
        self.method_decorators = [authenticate]
        self.parser = reqparse.RequestParser()
        self.group = {
            'name':fields.String(attribute='name'),
            'url':fields.String(attribute='path')
        }
    
    def post(self):
        self.parser.add_argument('name', type=group_name,
        required=True, help='name must be at least 5 characters')
        self.parser.add_argument('url', type=url, required=True,
        help='invalid url')

        args = self.parser.parse_args()

        group = Group(name=args['name'], path=args['url'], user_id=g.user.id)
        db.session.add(group)
        db.session.commit()

        return marshal(group, self.group, envelope='data'), 201