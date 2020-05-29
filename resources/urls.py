from flask_restful import Resource, marshal, fields, reqparse
from flask import g
from utilities.validators import url as url_validator, url_group
from utilities.middlewares import authenticate
from models import db, Url
import random
import string

class Urls(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser();
        self.urlField = {
            'id':fields.Integer(attribute='id'),
            'group_name':fields.String(attribute='group_name', default=None),
            'path':fields.String(attribute='path'),
            'short_path':fields.String(attribute='short_path'),
            'num_redirects':fields.Integer(attribute='num_redirects', default=0),
            'created_at':fields.String(attribute='created_time')
        }
        self.method_decorators = [authenticate]

    def post(self):
        self.parser.add_argument('url', type=url_validator, required=True, 
        help='url is invalid')
        self.parser.add_argument('length', type=int, required=True,
        help='specify a valid length between 6-10')
        self.parser.add_argument('group', type=url_group, required=True,
        help='invalid group id', dest='group_id')

        args = self.parser.parse_args()

        url = Url(group_id=args['group_id'], user_id=g.user.id,
        path=args['url'], short_path=self.shorten(args['length']))
        db.session.add(url)
        db.session.commit()

        return marshal(url, self.urlField, envelope='data'), 201

    def get(self):
        urls = Url.query.filter((Url.user_id == g.user.id)).all()

        for url in urls:
            url.num_redirects = len(url.redirects)
            url.created_time = url.created_at.strftime('%B %d, %Y %H:%M')

        return marshal(urls, self.urlField, envelope='data')

    def shorten(self, length=6):
        characters = string.ascii_letters + string.digits
        short_path = ''.join(random.sample(characters, length))
        return short_path

        
    