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

# start via flask --app app run

# read in the env variables
load_dotenv('.env')
app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello_world():
    return "<p>Hello!</p>"

#register the endpoints
app.register_blueprint(api.generate.bp)

app.register_blueprint(api.log.bp)

app.register_blueprint(api.metadata.bp)

@app.route("/api/music/generate", methods=["POST"])
def post_generate_music():
    return make_response("Unsupported", 500)

app.register_blueprint(api.portrait.bp)

app.register_blueprint(api.seed.bp)

app.register_blueprint(api.sprite.bp)

app.register_blueprint(api.sprites.bp)

app.register_blueprint(api.wc.bp)