from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'nwoaffl'
    location = 'media'

class StaticStorage(S3Boto3Storage):
    bucket_name = 'nwoaffl'
    location = 'static'