from flask_restful import Api, Resource
from flask import Flask
from flask_migrate import Migrate
from models import db
import config
import os

app = Flask(__name__)
app.config.from_object(os.getenv('APP_CONFIG'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/{3}'.format(app.config['DB_USER'],
app.config['DB_PASSWORD'], app.config['DB_PORT'], app.config['DB_NAME'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)
api = Api(app)

if __name__ == '__main__':
    app.run()