import boto3

user_ratings_dynamodb_table_name = 'duclos-app-user-ratings'
dynamodb = boto3.resource('dynamodb')
sqs = boto3.resource('sqs')
