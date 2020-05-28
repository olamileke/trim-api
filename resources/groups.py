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
            'id':fields.Integer(attribute='id'),
            'name':fields.String(attribute='name'),
            'url':fields.String(attribute='path'),
            'num_urls':fields.Integer(default=0),
            'created_at':fields.String(default=None, attribute='created_time')
        }

    def get(self):
        groups = Group.query.filter((Group.user_id == g.user.id)).all()

        for group in groups:
            group.num_urls = len(group.urls)
            group.created_time = group.created_at.strftime('%B %d, %Y %H:%M')
        
        return marshal(groups, self.group, envelope='data')
    
    def post(self):
        self.parser.add_argument('name', type=group_name,
        required=True, help='name must be at least 5 characters')
        self.parser.add_argument('url', type=url, required=True,
        help='url is invalid')

        args = self.parser.parse_args()

        group = Group(name=args['name'], path=args['url'], user_id=g.user.id)
        db.session.add(group)
        db.session.commit()

        return marshal(group, self.group, envelope='data'), 201
