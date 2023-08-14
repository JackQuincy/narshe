from flask import Blueprint, Response
import sys

bp = Blueprint('sprite', __name__, url_prefix="/api")

@bp.route("/sprite/<sprite_id>/<palette_id>/<pose_id>", methods=["GET"])
def get_sprite(sprite_id, palette_id, pose_id):
    sys.path.append("WorldsCollide")

    sprite_id = int(sprite_id)
    palette_id = int(palette_id)
    pose_id = int(pose_id)
    
    from WorldsCollide.api.get_sprite_palette_bytes import get_sprite_palette_bytes
    (sprite_bytes, palette_bytes) = get_sprite_palette_bytes(sprite_id, palette_id, pose_id)

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


@bp.route("/sprite/random", methods=["GET"])
def get_random_sprite():
    sys.path.append("WorldsCollide")
    
    from WorldsCollide.api.get_random_sprite_pose import get_random_sprite_pose
    (sprite, palette, pose) = get_random_sprite_pose()
    
    result = { 
      'sprite_id': sprite,
      'palette_id': palette,
      'pose_id': pose
    }

    import json 
    return Response(
        response = json.dumps(result).encode(),
        status = 200,
        mimetype='application/json'
    )
