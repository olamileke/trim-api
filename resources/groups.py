from flask_restful import Resource, fields, reqparse, marshal
from flask import g, current_app, request
from models import db, Group
from utilities.middlewares import authenticate
from utilities.validators import group_name, url as url_validator

class Groups(Resource):
    def __init__(self):
        self.method_decorators = [authenticate]
        self.parser = reqparse.RequestParser()
        self.group_field = {
            'id':fields.Integer(attribute='id'),
            'name':fields.String(attribute='name'),
            'url':fields.String(attribute='path'),
            'num_urls':fields.Integer(default=0),
            'num_redirects':fields.Integer(default=0),
            'created_at':fields.String(default=None, attribute='created_time')
        }

    def get(self):
        page = request.args.get('page')
        fetch_all = request.args.get('fetch_all')

        if page is None:
            page = 1

        start = (int(page) - 1) * current_app.config['PER_PAGE']
        stop = int(page) * current_app.config['PER_PAGE']

        if fetch_all is not None:
            groups = Group.query.filter((Group.user_id == g.user.id)).order_by(Group.created_at.desc()).all()
        else: 
            groups = Group.query.filter((Group.user_id == g.user.id)).order_by(Group.created_at.desc())[start:stop]

        total_groups = Group.query.filter((Group.user_id == g.user.id)).count()

        for group in groups:
            group.num_urls = len(group.urls)
            group.num_redirects = len(group.redirects)
            group.created_time = group.created_at.strftime('%B %d, %Y %H:%M')
        
        groups_data = marshal(groups, self.group_field)
        data = {'groups':groups_data, 'total_groups':total_groups}

        return {'data':data}

    def post(self):
        self.parser.add_argument('name', type=group_name, required=True, help='name must be at least 5 characters')
        self.parser.add_argument('url', type=url_validator, required=True, help='url is invalid')

        args = self.parser.parse_args()
        name = args['name'].lower()
        group = Group.query.filter((Group.name == name) & (Group.user_id == g.user.id)).first()

        if group is not None:
            message = 'group with {0} name exists already'.format(name)
            return {'error':{'message':message}}, 403

        group = Group.query.filter((Group.path == args['url']) & (Group.user_id == g.user.id)).first()

        if group is not None:
            message = 'group with {0} url exists already'.format(args['url'])
            return {'error':{'message':message}}, 403

        group = Group(name=name, path=args['url'], user_id=g.user.id)
        db.session.add(group)
        db.session.commit()

        return marshal(group, self.group_field, envelope='data'), 201

