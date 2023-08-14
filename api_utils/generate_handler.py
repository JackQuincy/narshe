from api_utils.get_seed_payload import get_seed_payload

from api_utils.get_seed_url import get_seed_url
from api_utils.create_seed import create_seed

import xdelta3
import json
import os
import shutil
import subprocess
import sys 
import tempfile
from flask import Response

class GenerateHandler():
  def __init__(self, include_patch, include_log, use_protocol):
    self.include_patch = include_patch
    self.include_log = include_log
    self.use_protocol = use_protocol # to do: make sure it's recapture or api_key

  def get_created_by(self, post_data):
    protocol = self.use_protocol
    if protocol == 'recaptcha':
      return "Website"
    else: 
      from api_utils.get_api_key import get_api_key
      raw_key = post_data['key']
      api_key = get_api_key(raw_key)
      return api_key['name']

  # Return (200, None) if valid, (string, status) if error
  def validate_recaptcha(self, post_data):
    recaptcha_token = post_data['reCAPTCHA']
    secret = os.getenv("RECAPTCHA_SECRET")
    from urllib import request, parse
    data = parse.urlencode({
      "secret": secret,
      "response": recaptcha_token
    }).encode()
    req =  request.Request('https://www.google.com/recaptcha/api/siteverify', data=data)
    resp = request.urlopen(req)

    raw_response = resp.read()
    result = json.loads(raw_response)
    if not result['success']:
      return (403, 'Invalid recaptcha secret')

    return (200, None)
  
  # Return (200, None) if valid, (string, status) if error
  def validate_api_key(self, post_data):
      from api_utils.get_api_key import get_api_key
      raw_key = post_data['key']
      api_key = get_api_key(raw_key)
      if api_key is None:
        return (400, 'Api key is invalid')
      
      return (200, None)
      
  def do_POST(self, request):
    sys.path.append("WorldsCollide")
    with tempfile.TemporaryDirectory() as dir:
      in_filename = dir + "/ff3.smc"
      from api_utils.generate_seed import generate_seed
      seed_id = generate_seed()
      base_filename = f"ff6wc_{seed_id}"
      out_filename = dir + f"/{base_filename}.smc"
      log_filename = dir + f"/{base_filename}.txt"
      manifest_filename = dir + f"/{base_filename}.json"
      website_url = get_seed_url(seed_id)

      post_data = request.data
      data = json.loads(post_data)

      protocol =  self.use_protocol
      print(f'using {protocol} validation protocol')
      (status, error) = self.validate_api_key(data) if protocol == 'api_key' else self.validate_recaptcha(data)
      print(f"{protocol} returned with status {status}")
      if protocol == 'api_key' and status == 403:
        return Response(
          response = json.dumps({
            'errors': ['Invalid api key'],
            'success': False
          }).encode(),
          status = 403,
          mimetype='application/json'
        )
      elif status != 200:
        return Response(
          response = json.dumps({
            'errors': [f'Validation returned with status code {status}: {error}'],
            'success': False
          }).encode(),
          status = 500,
          mimetype='application/json'
        )

      original_flags = data['flags']
      description = data.get('description')
      flags = original_flags +  f' -url {website_url} -manifest {manifest_filename}'
      
      result = self._run_worlds_collide(in_filename, out_filename, manifest_filename, flags)

      if result:
        return Response (
          response = json.dumps({}).encode(),
          status = 400,
          mimetype='application/json',
        )
      else:
        wc_filename = out_filename
        if os.getenv("NEXT_PUBLIC_ENABLE_BETA") == "true":
          wc_filename = dir + f"/{base_filename}-beta.smc"
          print(out_filename, wc_filename)
          self._apply_beta_changes(out_filename, wc_filename)
        with open(in_filename, "rb") as old, open(wc_filename, "rb") as new, open(log_filename, "rb") as logfile, open(manifest_filename, "rb") as manifestfile:
          raw_patch = xdelta3.encode(old.read(), new.read())

          log_bytes = logfile.read()
          log = log_bytes.decode('utf-8')
          
          import base64
          manifest = json.loads(manifestfile.read())
          patch = base64.b64encode(raw_patch).decode('utf-8')
          
          include_log = self.include_log
          include_patch = self.include_patch

          created_by = self.get_created_by(data)

          raw_seed = create_seed(
            seed_id = seed_id, 
            patch = patch, 
            log = log, 
            website_url = website_url, 
            filename = base_filename, 
            flags = manifest['flags'], 
            seed_type = "ff6wc", 
            description = description,
            version = manifest['version'],
            hash = manifest['hash'],
            created_by = created_by
          )
          
          del raw_seed['_id']
          
          seed = get_seed_payload(
            raw_seed, 
            log if include_log else None, 
            patch if include_patch else None,
            website_url=get_seed_url(seed_id),
            filename=base_filename
          )

          return Response (
            response = json.dumps(seed).encode(),
            status = 200,
            mimetype='application/json',
          )

  def _apply_beta_changes(self, wc_filename, new_filename):
    cwd = os.getcwd()  + "/WorldsCollideConfig"

    executable = cwd + "/wc_config.py"

    red_window_arg = '252828.202222.161616.101010.050606.313131.140606'

    args = ['python', executable, '-i', wc_filename, '-o', new_filename, "-bs", '6', "-ms", "1", '-w1', red_window_arg]
    print(f'running command {args}')

    return subprocess.Popen(args, cwd = cwd).wait()

  def _run_worlds_collide(self, in_filename, out_filename, manifest_filename, flags):
    src_file = 'ff3.smc'

    shutil.copyfile(src_file, in_filename)

    cwd = os.getcwd()  + "/WorldsCollide"

    executable = cwd + "/wc.py"

    args = ['python', executable, '-i', in_filename, '-o', out_filename, '-manifest', manifest_filename] + flags.split()
    print(f'running command {args}')

    return subprocess.Popen(args, cwd = cwd).wait()
