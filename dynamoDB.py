# dynamoDB.py Update data/legalbot-FAQ.json into AWS DynamoDB 

# import AWS DynamoDB
import boto3
from botocore.exceptions import ClientError
import json
from decimal import Decimal


# DynamoDB connection
dynamodb = boto3.resource('dynamodb',
                     aws_access_key_id = os.environ.get('aws_access_key_id') or 'AKIAI3SH5HX2JF3HEHTQ',
                     aws_secret_access_key = os.environ.get('aws_secret_access_key') or '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',
                     region_name = "eu-central-1")

table_name = 'legalbot-FAQ'

def load_json_data(data_list):
    table = dynamodb.Table(table_name)
    for item in data_list:
        Question = item['Question']
        Answer = item['Answer']
        print("Adding Question: "+ Question)
        table.put_item(Item=item)


if __name__ == '__main__':
    with open("data/legalbot-FAQ.json") as json_file:
        data_list = json.load(json_file, parse_float=Decimal)
    load_json_data(data_list)
