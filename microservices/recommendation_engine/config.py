import boto3

aws_region = 'us-west-2'

max_queue_messages = 10
sqs = boto3.resource('sqs', region_name=aws_region)

dynamodb = boto3.resource('dynamodb', region_name=aws_region)
user_ratings_dynamodb_table_name = 'duclos-app-user-ratings'
user_ratings_dynamodb_table = dynamodb.Table(user_ratings_dynamodb_table_name)
user_id_rating_value_index = 'user-id-rating-value-index'
user_id_rating_value_index_pkey = 'user-id'
restaurant_id_rating_value_index = 'restaurant-id-rating-value-index'
restaurant_id_rating_value_index_pkey = 'restaurant-id'
rating_value_index_skey = 'rating-value'
