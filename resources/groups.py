from flask_restful import Resource, fields, reqparse, marshal
from flask import g
from models import db, Group
from utilities.middlewares import authenticate
from utilities.validators import group_name, url as url_validator

class Groups(Resource):
    def __init__(self):
        self.method_decorators = [authenticate]
        self.parser = reqparse.RequestParser()
        self.groupField = {
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
        
        return marshal(groups, self.groupField, envelope='data')
    
    def post(self):
        self.parser.add_argument('name', type=group_name,
        required=True, help='name must be at least 5 characters')
        self.parser.add_argument('url', type=url_validator, required=True,
        help='url is invalid')

        args = self.parser.parse_args()
        name = args['name'].lower()
        group = Group.query.filter((Group.name == name) &
        (Group.user_id == g.user.id)).first()

        if group is not None:
            message = 'group with {0} name exists already'.format(name)
            return {'error':{'message':message}}, 403

        group = Group.query.filter((Group.path == args['url']) &
        (Group.user_id == g.user.id)).first()

        if group is not None:
            message = 'group with {0} url exists already'.format(args['url'])
            return {'error':{'message':message}}, 403

        group = Group(name=name, path=args['url'], user_id=g.user.id)
        db.session.add(group)
        db.session.commit()

        return marshal(group, self.groupField, envelope='data'), 201

