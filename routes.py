from flask import Flask, make_response
import api.metadata

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello_world():
    return "<p>Hello!</p>"

@app.route("/api/generate", methods=["POST"])
def post_generate():
    return make_response("Unsupported", 500)

@app.route("/api/log/<seed_id>", methods=["GET"])
def get_seed_log(seed_id):
    return make_response("Unsupported", 500)

app.register_blueprint(api.metadata.bp)

@app.route("/api/music/generate", methods=["POST"])
def post_generate_music():
    return make_response("Unsupported", 500)

@app.route("/api/portrait/<portrait_id>", methods=["GET"])
def get_portrait(portrait_id):
    return make_response("Unsupported", 500)

@app.route("/api/seed/<api_key>/<seed_id>", methods=["GET"])
def get_seed_with_key(api_key, seed_id):
    return make_response("Unsupported", 500)

@app.route("/api/sprite/<sprite_id>/<palette_id>/<pose_id>", methods=["GET"])
def get_sprite(sprite_id, palette_id, pose_id):
    return make_response("Unsupported", 500)

@app.route("/api/sprite/random", methods=["GET"])
def get_random_sprite():
    return make_response("Unsupported", 500)

@app.route("/api/sprites", methods=["GET"])
def get_sprites():
    return make_response("Unsupported", 500)

@app.route("/api/wc", methods=["GET"])
def get_manifest():
    return make_response("Unsupported", 500)