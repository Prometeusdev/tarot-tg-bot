import boto3
import csv
import datetime
import os
import pandas as pd

from dotenv import load_dotenv


load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.getenv('AWS_URL')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
KEY_FILE = 'data.csv'

AWS_URL = "https://{}.{}/{}".format(AWS_STORAGE_BUCKET_NAME, AWS_URL, KEY_FILE)

s3 = boto3.resource(
    service_name='s3',
    region_name=AWS_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3_object = s3.Object(AWS_STORAGE_BUCKET_NAME, KEY_FILE)

data_csv = s3_object.get()['Body']
data = datetime.datetime.today().strftime("%Y-%m-%d")
df = pd.read_csv(data_csv, index_col=0, encoding='utf8')
print(df)
new_row = {'data':data, 'id':1, 'command':'f'}
df = df.append(new_row, ignore_index=True)

bucket = AWS_STORAGE_BUCKET_NAME
s3.Object(bucket, 'data.csv').put(Body=df.to_csv(), ACL='public-read')