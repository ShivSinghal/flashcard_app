from flask import Flask
from flask_restful import Resource, Api
from application.config import LocalDevelopmentConfig
from application.database import db
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.logger.info("Staring Local Development.")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    app.logger.info("App setup complete")
    return app

app = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

# # Add all restful controllers
# from application.api import *
# api.add_resource(DeckAPI, "/api/deck/<int:user_id>")


if __name__ == '__main__':
  # Run the Flask app
  app.secret_key = 'abc'
  app.run(
    # debug= True
  )
