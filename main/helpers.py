import hashlib
import logging

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings

s3_signature = {
    'v4': 's3v4',
    'v2': 's3',
}

# See more: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html#Concepts.RegionsAndAvailabilityZones.Availability  # noqa: E501
AWS_DEFAULT_REGION = settings.AWS_DEFAULT_REGION

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME


def hashstring(string, length=10):
    """ Hashes a string using the sha265 algorithm

    Returns a substring of the hash's hexdigest """
    base_hash = hashlib.sha256()
    username_in_bytes = bytes(string, 'utf-8')
    base_hash.update(username_in_bytes)
    return base_hash.hexdigest()[:length]


def create_presigned_s3_url(bucket_key, expiration=3600,
                            signature_version=s3_signature['v4']):
    """ Creates a presigned URL that allows access and expires after 1hr

    See more: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html  # noqa: E501

    Returns the presigned URL"""
    s3_client = boto3.client(
        service_name='s3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version=signature_version),
        region_name=AWS_DEFAULT_REGION,

    )
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_STORAGE_BUCKET_NAME,
                    'Key': bucket_key},
            ExpiresIn=expiration)
        print(s3_client.list_buckets()['Owner'])
        print(s3_client.list_objects(Bucket=AWS_STORAGE_BUCKET_NAME,
                                     Prefix=bucket_key))
        for key in s3_client.list_objects(Bucket=AWS_STORAGE_BUCKET_NAME,
                                          Prefix=bucket_key)['Contents']:
            print("Key: ", key['Key'])
    except ClientError as client_error:
        logging.error(client_error)
        return None
    except KeyError as key_error:
        logging.exception(key_error)
        return None
    # The response contains the presigned URL
    return response
