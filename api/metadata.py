from flask import Blueprint, make_response, Response
import subprocess
import sys
import tempfile
import json

bp = Blueprint('metadata', __name__, url_prefix="/api/metadata")

@bp.route("flag", methods=["GET"])
def get_flag_metadata():
    """ Returns metadata of all wc.py flags """
    sys.path.append("WorldsCollide")
    with tempfile.TemporaryDirectory() as temp_dir:
        in_filename = 'ff3.smc'
        out_filename = temp_dir + "/out-meta.json"
        result = subprocess.Popen(['python', 'WorldsCollide/build-wc-flag-metadata.py', '-i', in_filename, '-o', out_filename]).wait()
        if not result:
          with open(out_filename, "rb") as metadata:
              result = json.load(metadata)
              response = Response(
                  response = json.dumps(result).encode(),
                  status = 200,
                  mimetype='application/json'
              )
              return response
        else:
          return make_response("Failed to build metadata", 500)

@bp.route("objective", methods=["GET"])
def get_objective_metadata():
    """ Returns metadata of all wc.py objectives """
    sys.path.append("WorldsCollide")
    from WorldsCollide.metadata.objective_metadata_writer import ObjectiveMetadataWriter

    result = ObjectiveMetadataWriter().get_objective_metadata()
    response = Response(
        response = json.dumps(result).encode(),
        status = 200,
        mimetype='application/json'
    )
    return response