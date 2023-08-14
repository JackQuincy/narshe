from flask import Blueprint, Response
import sys

bp = Blueprint('wc', __name__, url_prefix="/api")

@bp.route("/wc", methods=["GET"])
def get_manifest_web():
    sys.path.append("WorldsCollide")
    
    from WorldsCollide.api.get_manifest import get_manifest
    manifest = get_manifest()

    import json
    return Response(
        response = json.dumps(manifest).encode(),
        status = 200,
        mimetype='application/json'
    )