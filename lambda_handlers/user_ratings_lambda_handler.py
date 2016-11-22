import boto3
import json
import os

print('Loading function')

user_ratings_dynamo_table_name = os.environ['user_ratings_dynamo_table_name']
recommend_queue_name = os.environ['recommend_queue_name']
user_ratings_dynamo_pkey = os.environ['user_ratings_dynamo_pkey']
user_ratings_dynamo_skey = os.environ['user_ratings_dynamo_skey']

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(Key=
            {
                user_ratings_dynamo_pkey : x[user_ratings_dynamo_pkey],
                user_ratings_dynamo_skey : x[user_ratings_dynamo_skey]
            }),
        'GET': lambda dynamo, x: dynamo.scan(Item=x),
        'POST': lambda dynamo, x: dynamo.put_item(Item=x),
        'PUT': lambda dynamo, x: dynamo.update_item(Item=x),
    }
    
    operation = event['httpMethod']
    
    if operation in operations:
        
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        dynamo = boto3.resource('dynamodb').Table(user_ratings_dynamo_table_name)
        operations[operation](dynamo, payload)
        
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=recommend_queue_name)
        response = queue.send_message(MessageBody=json.dumps(event))
        
        return respond(None, response)
        
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))