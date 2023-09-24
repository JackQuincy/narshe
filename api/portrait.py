from flask import Blueprint, Response
from api_utils.seed_storage import SeedStorage
import sys

bp = Blueprint('portrait', __name__, url_prefix="/api")


@bp.route("/portrait/<raw_portrait>", methods=["GET"])
def get_portrait(raw_portrait):
    sys.path.append("WorldsCollide")
    from WorldsCollide.api.get_portrait_bytes import get_portrait_bytes
    import json

    portrait_id = int(raw_portrait)

    (sprite_bytes, palette_bytes) = get_portrait_bytes(portrait_id)

    result = { 
      'sprite': sprite_bytes,
      'palette': palette_bytes 
    }
    import json
    return Response(
        response = json.dumps(result).encode(),
        status = 200,
        mimetype='application/json'
    )
