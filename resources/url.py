from flask_restful import Resource, reqparse, fields
from flask import g
from utilities.middlewares import authenticate
from models import db, Url as UrlModel

class Url(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.url = {
            'id':fields.Integer(attribute='id'),
            'group_name':fields.String(attribute='group_name', default=None),
            'path':fields.String(attribute='path'),
            'short_path':fields.String(attribute='short_path'),
            'num_redirects':fields.Integer(attribute='num_redirects', default=0),
            'created_at':fields.String(attribute='created_time')
        }
        self.method_decorators = [authenticate]

    def delete(self, url_id):
        url = UrlModel.query.filter((UrlModel.id == url_id)).first()

        if url is None or url.user_id != g.user.id:
            return {'error':{'message':'shortened url does not exist'}}, 404

        db.session.delete(url)
        db.session.commit()

        return {'data':{'message':'shortened url deleted successfully'}}, 204