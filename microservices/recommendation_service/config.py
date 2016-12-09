import boto3

aws_region = 'us-west-2'

max_queue_messages = 10
sqs = boto3.resource('sqs', region_name=aws_region)

recommendation_queue_name = 'duclos-app-recommendation-queue'

dynamodb = boto3.resource('dynamodb', region_name=aws_region)

similarity_queue_name = 'duclos-app-similarity-queue'
similar_users_dynamodb_table_name = 'duclos-app-similar-users'
similar_users_dynamodb_table = dynamodb.Table(similar_users_dynamodb_table_name)
similar_users_pkey = 'user-id'
similarity_index_map_attribute = 'similarity-index-map'
