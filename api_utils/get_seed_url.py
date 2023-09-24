

def get_seed_url(seed_id):
  import os
  return f"{os.getenv('PUBLIC_URL')}/seed/?id={seed_id}"

def get_music_seed_url(seed_id):
  import os
  return f"{os.getenv('PUBLIC_URL')}/music/seed/?id={seed_id}"
  