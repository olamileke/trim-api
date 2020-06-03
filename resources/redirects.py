from flask_restful import Resource, reqparse, fields, marshal
from flask import g, current_app
from utilities.validators import shortened_link, redirect_source
from utilities.middlewares import authenticate
from models import db, Redirect, Url

class Redirects(Resource):
    def __init__(self):
        self.method_decorators = [authenticate]
        self.parser = reqparse.RequestParser()
        self.redirect_field = {
            'path':fields.String(attribute='path')
        }

    def post(self):
        self.parser.add_argument('short_path', required=True, type=str,
        help='short link must be a string')
        self.parser.add_argument('source', required=True, type=redirect_source,
        help='redirect source must be a valid url')

        args = self.parser.parse_args()

        url = Url.query.filter((Url.short_path == args['short_path'])).first()

        if url is None:
            return {'error':{'message':'Short link does not exist'}}, 404

        if url.group_id is None:
            group_id = None
        else:
            group_id = url.group_id

        if args['source'] not in current_app.config['CLIENT_URL']:
            redirect = Redirect(user_id=g.user.id, url_id=url.id, group_id=group_id,
            source=args['source'])

            db.session.add(redirect)
            db.session.commit()

        return marshal(url, self.redirect_field, envelope='data'), 201



