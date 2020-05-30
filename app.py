from flask_restful import Api, Resource
from flask import Flask
from flask_migrate import Migrate
from models import db
from resources.users import Users
from resources.auth import Auth
from resources.groups import Groups
from resources.urls import Urls
from resources.url import Url
from resources.group import Group
from resources.redirects import Redirects
import config
import os

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/{3}'.format(app.config['DB_USER'],
app.config['DB_PASSWORD'], app.config['DB_PORT'], app.config['DB_NAME'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enabling CORS on the response
@app.after_request
def enable_cors(response):
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accepts, Authorization')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')

    return response

migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(Auth, '/authenticate')
api.add_resource(Groups, '/groups')
api.add_resource(Group, '/groups/<int:group_id>')
api.add_resource(Urls, '/urls')
api.add_resource(Url, '/urls/<int:url_id>')
api.add_resource(Redirects, '/redirects')

if __name__ == '__main__':
    app.run()