from flask_restful import Resource, reqparse, fields, marshal
from flask import g, current_app, request
from utilities.validators import shortened_link, redirect_source
from utilities.middlewares import authenticate
from models import db, Redirect, Url

class Redirects(Resource):
    def __init__(self):
        self.method_decorators = {'get':[authenticate]}
        self.parser = reqparse.RequestParser()
        self.url_field = {
            'path':fields.String(attribute='path')
        }
        self.redirect_field = {
            'url':fields.String(attribute='url.short_path'),
            'created_at':fields.String(attribute='created_time')
        }

    def get(self):
        page = request.args.get('page')
        group_id = request.args.get('group_id')

        if page is None:
            page = 1
        
        start = (int(page) - 1) * (current_app.config['PER_PAGE'] * 2)
        stop = int(page) * (current_app.config['PER_PAGE'] * 2)

        if group_id is not None:
            redirects = Redirect.query.filter((Redirect.user_id == g.user.id) & (Redirect.group_id == group_id)).order_by(Redirect.created_at.desc())[start:stop]
        else:
            redirects = Redirect.query.filter((Redirect.user_id == g.user.id)).order_by(Redirect.created_at.desc())[start:stop]

        total_redirects = Redirect.query.filter((Redirect.user_id == g.user.id)).count()

        for redirect in redirects:
            redirect.created_time = redirect.created_at.strftime('%B %d, %Y %H:%M')
            # redirect.url = redirect.url.short_path

        redirects_data = marshal(redirects, self.redirect_field)

        data = {'redirects':redirects_data, 'total_redirects':total_redirects}

        return {'data':data}

    def post(self):
        self.parser.add_argument('short_path', required=True, type=str,help='short link must be a string')
        self.parser.add_argument('referrer', required=True, type=str, help='referrer is required');

        args = self.parser.parse_args()

        url = Url.query.filter((Url.short_path == args['short_path'])).first()

        if url is None:
            return {'message':'Short link does not exist'}, 404

        if url.group_id is None:
            group_id = None
        else:
            group_id = url.group_id

        if current_app.config['CLIENT_URL'] not in args['referrer']:
            redirect = Redirect(user_id=url.user.id, url_id=url.id, group_id=group_id)
            db.session.add(redirect)
            db.session.commit()

        return marshal(url, self.url_field, envelope='data'), 201



