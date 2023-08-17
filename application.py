from flask import Flask, make_response
from dotenv import load_dotenv
import api.metadata
import api.generate
import api.log
import api.portrait
import api.seed
import api.sprite
import api.sprites
import api.wc

# read in the env variables
load_dotenv('.env')
application = Flask(__name__)

@application.route("/", methods=["GET"])
def hello_world():
    import os
    return f"<p>{os.getenv('HELLO_TEXT')}</p>"

#register the endpoints
application.register_blueprint(api.generate.bp)

application.register_blueprint(api.log.bp)

application.register_blueprint(api.metadata.bp)

@application.route("/api/music/generate", methods=["POST"])
def post_generate_music():
    return make_response("Unsupported", 500)

application.register_blueprint(api.portrait.bp)

application.register_blueprint(api.seed.bp)

application.register_blueprint(api.sprite.bp)

application.register_blueprint(api.sprites.bp)

application.register_blueprint(api.wc.bp)

