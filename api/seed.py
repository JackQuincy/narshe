import sys
from flask import Blueprint, Response, request, make_response
from api_utils.generate_handler import GenerateHandler

bp = Blueprint('seed', __name__, url_prefix="/api")

# curl -d '{"key":"ff6wc", "flags":"-open"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/seed
@bp.route("/seed", methods=["POST"])
def post_generate():
    handler = GenerateHandler(False, False, "api_key")
    return handler.do_POST(request)

# http://localhost:5000/api/seed/ff6wc/poraozdq5svg
@bp.route("/seed/<raw_key>/<seed_id>", methods=["GET"])
def get_seed_with_key(raw_key, seed_id):
    import json
    from api_utils.get_api_key import get_api_key
    
    api_key = get_api_key(raw_key)

    if api_key is None:
        return Response(
            response = json.dumps({
            'errors': ['Invalid api key'],
            'success': False
            }).encode(),
            status = 403,
            mimetype='application/json'
        )
  
    from api_utils.seed_storage import SeedStorage
    seed = SeedStorage.get_seed(seed_id)

    if not seed:
        return Response(
            response = json.dumps({
            'errors': [f'Seed {seed_id} not found'],
            'success': False
            }).encode(),
            status = 404,
            mimetype='application/json'
        )

    log = SeedStorage.get_spoiler_log(seed_id)
    patch = SeedStorage.get_patch(seed_id)
    
    from api_utils.get_seed_payload import get_seed_payload
    from api_utils.get_seed_filename import get_seed_filename
    from api_utils.get_seed_url import get_seed_url
    
    filename = get_seed_filename(seed_id, seed['type'])

    website_url = get_seed_url(seed_id)
    payload = get_seed_payload(seed, log['log'], patch, website_url=website_url, filename=filename)

    return Response (
        response = json.dumps(payload).encode(),
        status = 200,
        mimetype='application/json',
    )