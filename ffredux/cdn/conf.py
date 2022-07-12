import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = "ff-nwoaffl"
# AWS_S3_ENDPOINT_URL = "https://sfo3.digitaloceanspaces.com"
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
#      "ACL": "public-read"
# }
# AWS_LOCATION = "https://ff-nwoaffl.sfo3.digitaloceanspaces.com"
# DEFAULT_FILE_STORAGE = "ff-nwoaffl.cdn.backends.MediaRootS3BotoStorage"
# STATICFILES_STORAGE = 'ff-nwoaffl.cdn.backends.StaticRootS3BotoStorage'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_LOCATION = 'static'
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# AWS_S3_REGION_NAME='us-east-1'

AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'ff-nwoaffl'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
AWS_LOCATION = 'static'
AWS_S3_REGION_NAME='us-east-1'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'