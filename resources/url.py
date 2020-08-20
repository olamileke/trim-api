from flask_restful import Resource, reqparse, fields, marshal
from flask import g
from utilities.middlewares import authenticate
from utilities.validators import url as url_validator, short_url
from models import db, Url as UrlModel

class RedirectsField(fields.Raw):
    def format(self, redirects):
        response = []

        for redirect in redirects:
            data = {}
            data['short_url'] = redirect.url.short_path
            data['url'] = redirect.url.path
            data['created_at'] = redirect.created_at.strftime('%B %d, %Y %H:%M')

            response.append(data)

        return response

class Url(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.url_all_field = {
            'id':fields.Integer(attribute='url.id'),
            'group_name':fields.String(attribute='url.group_name', default=None),
            'group_path':fields.String(attribute='url.group_path', default=None),
            'path':fields.String(attribute='url.path'),
            'short_path':fields.String(attribute='url.short_path'),
            'custom':fields.Boolean(attribute='url.custom'),
            'redirects':RedirectsField(attribute='redirects'),
            'created_at':fields.String(attribute='url.created_time')
        }
        self.url_field = {
            'id':fields.Integer(attribute='url.id'),
            'group_name':fields.String(attribute='url.group_name', default=None),
            'group_path':fields.String(attribute='url.group_path', default=None),
            'path':fields.String(attribute='url.path'),
            'short_path':fields.String(attribute='url.short_path'),
            'custom':fields.Boolean(attribute='url.custom'),
            'created_at':fields.String(attribute='url.created_time')
        }

        self.method_decorators = [authenticate]

    def get(self, url_id):
        url = UrlModel.query.filter((UrlModel.id == url_id) &
        (UrlModel.user_id == g.user.id)).first()
        if url is None:
            return {'message':'shortened url does not exist'}, 404

        url.created_time = url.created_at.strftime('%B %d, %Y %H:%M')
        url.group_name = None

        if url.group_id is not None:
            url.group_name = url.group.name
            url.group_path = url.group.path

        data = {'url':url, 'redirects':url.redirects}

        return marshal(data, self.url_all_field, envelope='data')

    
    def patch(self, url_id):
        self.parser.add_argument('url', type=url_validator, required=True, help='url is invalid')
        self.parser.add_argument('short_url', type=short_url, required=True, help='short link must be at least 3 characters long')
        args = self.parser.parse_args()

        url_to_patch = UrlModel.query.filter((UrlModel.id == url_id) & (UrlModel.user_id == g.user.id)).first()

        if url_to_patch is None:
            return {'message':'shortened url does not exist'}, 404

        url = UrlModel.query.filter((UrlModel.user_id == g.user.id) & (UrlModel.path == args['url'])).first()

        if url is not None and url.id != url_to_patch.id:
            return {'message':'url has been shortened already'}, 403

        if url_to_patch.short_path != args['short_url']:
            url = UrlModel.query.filter((UrlModel.short_path == args['short_url'])).first()

            if url is not None:
                return {'message':'short url is not available'}, 403

        url_to_patch.path = args['url']
        url_to_patch.short_path = args['short_url']
        db.session.commit()
        data = {'url':url_to_patch}
        
        return marshal(data, self.url_field, envelope='data')

    def delete(self, url_id):
        url = UrlModel.query.filter((UrlModel.id == url_id) &
        (UrlModel.user_id == g.user.id)).first()

        if url is None:
            return {'message':'shortened url does not exist'}, 404

        db.session.delete(url)
        db.session.commit()

        return {'data':{'message':'shortened url deleted successfully'}}, 204