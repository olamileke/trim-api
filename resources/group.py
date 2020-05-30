from flask_restful import Resource, fields, marshal, reqparse
from flask import g
from utilities.middlewares import authenticate
from utilities.validators import group_name, url as url_validator
from models import db, Group as GroupModel, Url

class UrlField(fields.Raw):
    def format(self, urls):
        response = []
        for url in urls:
            data = {}
            data['path'] = url.path
            data['short_path'] = url.short_path
            data['created_at'] = url.created_at.strftime('%B %d, %Y %H:%M')
            data['num_redirects'] = len(url.redirects)

            response.append(data)

        return response

class Group(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.method_decorators = [authenticate]
        self.groupField = {
            'id':fields.Integer(attribute='id'),
            'name':fields.String(attribute='name'),
            'url':fields.String(attribute='path'),
            'num_urls':fields.Integer(default=0),
            'created_at':fields.String(default=None, attribute='created_time'),
            'urls':UrlField(attribute='urls')
        }

    def get(self, group_id):
        group = GroupModel.query.filter((GroupModel.id == group_id)
        & (GroupModel.user_id == g.user.id)).first()

        if group is None:
            return {'error':{'message':'group does not exist'}}, 404

        data = {'id':group.id, 'name':group.name, 
        'path':group.path, 'num_urls':len(group.urls),
        'created_time':group.created_at.strftime('%B %d, %Y %H:%M'),
        'urls':group.urls}

        return marshal(data, self.groupField, envelope='data')

    def patch(self, group_id):
        self.parser.add_argument('name', type=group_name,
        required=True, help='name must be at least 5 characters')
        self.parser.add_argument('url', type=url_validator, required=True,
        help='url is invalid')

        args = self.parser.parse_args() 
        group = GroupModel.query.filter((GroupModel.id == group_id)
        & (GroupModel.user_id == g.user.id)).first()

        if group is None:
            return {'error':{'message':'group does not exist'}}, 404

        old_group_path = group.path
        group.name = args['name']
        group.path = args['url']

        for url in group.urls:
            url.path = url.path.replace(old_group_path, args['url'])

        db.session.commit()

        return {'data':{'message':'group updated successfully'}}


    def delete(self, group_id):
        group = GroupModel.query.filter((GroupModel.id == group_id)
        & (GroupModel.user_id == g.user.id)).first()

        if group is None:
            return {'error':{'message':'group does not exist'}}, 404

        db.session.delete(group)
        db.session.commit()

        return {'data':{'message':'group deleted successfully'}}, 204 