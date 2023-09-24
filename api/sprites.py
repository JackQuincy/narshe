from flask import Blueprint, Response
import sys

bp = Blueprint('sprites', __name__, url_prefix="/api")

@bp.route("/sprites", methods=["GET"])
def get_sprites_web():
    sys.path.append("WorldsCollide")
    
    from WorldsCollide.api.get_sprites import get_sprites
    from WorldsCollide.api.get_portraits import get_portraits
    from WorldsCollide.api.get_palettes import get_palettes_with_colors
    
    sprites = get_sprites()
    palettes = get_palettes_with_colors()
    portraits = get_portraits()
    
    result = { 
        'sprites': sprites,
        'palettes': palettes,
        'portraits': portraits
    }

    import json
    return Response(
        response = json.dumps(result).encode(),
        status = 200,
        mimetype='application/json'
    )