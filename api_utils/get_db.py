
import os
from google.cloud import storage

def get_gcp_bucket():
  gcp = storage.Client()
  return gcp.get_bucket(os.environ.get('PATCH_BUCKET'))