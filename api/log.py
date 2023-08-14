from flask import Blueprint, make_response, Response, request
from api_utils.seed_storage import SeedStorage

bp = Blueprint('log', __name__, url_prefix="/api")

# test with curl -d '{"key":"ff6wc", "flags":"-open"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/log/eta9jdw1jt98
@bp.route("/log/<seed_id>", methods=["POST"])
def get_seed_log(seed_id):
    import json

    post_data = request.data
    data = json.loads(post_data)
    key = data['key']

    api_key = SeedStorage.get_api_key(key)
    log = SeedStorage.get_spoiler_log(seed_id)

    if api_key is None:
        response = Response(
          response = json.dumps({
            'errors': ['Invalid api key'],
            'success': False
          }).encode(),
          status = 403,
          mimetype='application/json'
        )
    elif log is None:
        response = make_response(f"Log for seed_id {seed_id} not found", 404)
    else:
        response = Response(
            response = json.dumps(log).encode(),
            status = 200,
            mimetype='application/json'
        )
    return response