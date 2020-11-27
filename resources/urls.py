from flask_restful import Resource, marshal, fields, reqparse
from flask import g, current_app, request
from utilities.validators import url as url_validator, url_group, short_url
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

    def get(self):
        page = request.args.get('page')
        group_id = request.args.get('group_id')

        if page is None:
            page = 1

        per_page = current_app.config['PER_PAGE']
        start = (int(page) - 1) * per_page
        stop = int(page) * per_page

        if group_id is not None:
            urls = Url.query.filter((Url.user_id == g.user.id) & (Url.group_id == group_id)).order_by(Url.created_at.desc())[start:stop]
        else:
            urls = Url.query.filter((Url.user_id == g.user.id)).order_by(Url.created_at.desc())[start:stop]

        total_urls = Url.query.filter((Url.user_id == g.user.id)).count()

        for url in urls:
            url.num_redirects = len(url.redirects)
            url.created_time = url.created_at.strftime('%B %d, %Y %H:%M')

        urls_data = marshal(urls, self.urlField)
        data = {'total_urls':total_urls, 'urls':urls_data}

        return {'data':data}

    def post(self):
        self.parser.add_argument('url', type=url_validator, required=True, help='url is invalid')
        self.parser.add_argument('group', type=url_group, required=True, help='invalid group id', dest='group_id')
        self.parser.add_argument('short_url', type=short_url, help='short url must be at least 3 characters in length')

        args = self.parser.parse_args()

        url = Url.query.filter((Url.path == args['url']) & (Url.user_id == g.user.id)).first()

        if url is not None:
            message = '{0} has been shortened'.format(args['url'])
            return {'message':message}, 403

        length = random.randint(4, 8)
        custom = False

        if args['short_url'] == '':
            short_path = self.shorten(length, g.user.id)
        else:
            short_path = args['short_url']
            url = Url.query.filter((Url.short_path == short_path)).first()

            if url is not None:
                message = '{0} is not available'.format(short_path)
                return {'message':message}, 403
            
            custom = True

        url = Url(group_id=args['group_id'], user_id=g.user.id, path=args['url'], short_path=short_path, custom=custom)
        db.session.add(url)
        db.session.commit()

        return marshal(url, self.urlField, envelope='data'), 201

    def shorten(self, length, user_id):
        i = 0

        while i < 1:
            characters = string.ascii_letters + string.digits
            short_path = ''.join(random.sample(characters, length))

            url = Url.query.filter((Url.short_path == short_path)).first()
            if url is None:
                i = i + 1

        return short_path        


        
    