from flask_restful import Resource, fields, marshal, reqparse
from flask import g, current_app
from utilities.middlewares import authenticate
from utilities.validators import group_name, url as url_validator
from models import db, Group as GroupModel, Url

class UrlField(fields.Raw):
    def format(self, urls):
        response = []
        for url in urls:
            data = {}
            data['id'] = url.id
            data['path'] = url.path
            data['short_path'] = url.short_path
            data['created_at'] = url.created_at.strftime('%B %d, %Y %H:%M')
            data['num_redirects'] = len(url.redirects)

            response.append(data)

        return response

class RedirectsField(fields.Raw):
    def format(self, redirects):
        response = []

        for redirect in redirects:
            data = {}
            data['url'] = redirect.url.short_path
            data['created_at'] = redirect.created_at.strftime('%B %d, %Y %H:%M')

            response.append(data)

        return response

class Group(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.method_decorators = [authenticate]
        self.group_all_field = {
            'id':fields.Integer(attribute='group.id'),
            'name':fields.String(attribute='group.name'),
            'url':fields.String(attribute='group.path'),
            'redirects':RedirectsField(attribute='redirects'),
            'created_at':fields.String(default=None, attribute='group.created_time'),
            'urls':UrlField(attribute='urls'),
            'num_urls':fields.Integer(attribute='total_urls'),
            'num_redirects':fields.Integer(attribute='total_redirects')
        }
        self.group_field = {
            'id':fields.Integer(attribute='group.id'),
            'name':fields.String(attribute='group.name'),
            'url':fields.String(attribute='group.path'),
            # 'num_urls':fields.Integer(attribute='total_urls'),
            # 'num_redirects':fields.Integer(attribute='total_redirects'),
            'created_at':fields.String(default=None, attribute='group.created_time')
        }

    def get(self, group_id):
        group = GroupModel.query.filter((GroupModel.id == group_id)
        & (GroupModel.user_id == g.user.id)).first()

        if group is None:
            return {'error':{'message':'group does not exist'}}, 404

        stop = current_app.config['PER_PAGE']
        urls = group.urls
        redirects = group.redirects

        data = {'group':group,'urls':urls[0:stop] ,'redirects':redirects[0:stop], 'total_urls':len(urls),
        'total_redirects':len(redirects)}
        
        return marshal(data, self.group_all_field, envelope='data')

    def patch(self, group_id):
        self.parser.add_argument('name', type=group_name, required=True, help='name must be at least 5 characters')
        self.parser.add_argument('url', type=url_validator, required=True, help='url is invalid')

        args = self.parser.parse_args() 
        group = GroupModel.query.filter((GroupModel.id == group_id) & (GroupModel.user_id == g.user.id)).first()

        if group is None:
            return {'error':{'message':'group does not exist'}}, 404

        old_group_path = group.path
        group.name = args['name']
        group.path = args['url']

        for url in group.urls:
            url.path = url.path.replace(old_group_path, args['url'])

        db.session.commit()
        group.created_time = group.created_at.strftime('%B %d, %Y %H:%M')
        data = {'group':group}

        return marshal(data, self.group_field, envelope='data')


    def delete(self, group_id):
        group = GroupModel.query.filter((GroupModel.id == group_id)
        & (GroupModel.user_id == g.user.id)).first()

        if group is None:
            return {'error':{'message':'group does not exist'}}, 404

        db.session.delete(group)
        db.session.commit()

        return {'data':{'message':'group deleted successfully'}}, 204 