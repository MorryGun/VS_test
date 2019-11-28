"""
The flask application package.
"""

from flask import Flask, Blueprint
from flask_restplus import Api, Resource

app = Flask(__name__, template_folder="templates")

import NerdAPI.views

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/')

app.register_blueprint(blueprint)

name_space = api.namespace('nerds', description='Nerds\' API')

@name_space.route("/")
class MainClass(Resource):
	def get(self):
		return { 
			"nerd_name": 0
		   }
	def post(self):
		return {
			"status": "Posted new data"
		}