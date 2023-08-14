from api_utils.generate_handler import GenerateHandler
from flask import Blueprint, request

bp = Blueprint('generate', __name__, url_prefix="/api")

@bp.route("/generate", methods=["POST"])
def post_generate():
    handler = GenerateHandler(True, True, "recaptcha")
    return handler.do_POST(request)