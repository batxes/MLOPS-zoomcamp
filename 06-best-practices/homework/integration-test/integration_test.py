
from datetime import datetime
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
import os

# Configuration for the S3 connection
s3_endpoint_url = os.getenv('S3_ENDPOINT_URL')
bucket_name = "nyc-duration"
input_file = "nyc_duration.parquet"

s3_client = boto3.client(
    's3',
    endpoint_url=s3_endpoint_url,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='eu-north-1'
)

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)


df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False
)

# Upload the file to the S3 bucket
try:
    s3_client.upload_file(input_file, bucket_name, input_file)
    print(f"File {input_file} uploaded to bucket {bucket_name}.")
except NoCredentialsError:
    print("Credentials not available")

# Clean up local file
#os.remove(input_file)