import config

def get_all_ratings_by_user_id(user_id):
    response = config.user_ratings_dynamodb_table.query(
        IndexName=config.user_id_rating_value_index,
        KeyConditionExpression='#partitionkey = :partitionkeyval',
        ExpressionAttributeNames={
            '#partitionkey' : config.user_id_rating_value_index_pkey 
        },
        ExpressionAttributeValues={
            ':partitionkeyval' : user_id
        }
    )
    return response

def get_all_ratings_by_restaurant_id(restaurant_id):
    response = config.user_ratings_dynamodb_table.query(
        IndexName=config.restaurant_id_rating_value_index,
        KeyConditionExpression='#partitionkey = :partitionkeyval',
        ExpressionAttributeNames={
            '#partitionkey' : config.restaurant_id_rating_value_index_pkey
        },
        ExpressionAttributeValues={
            ':partitionkeyval' : restaurant_id
        }
    )
    return response

def get_ratings_attribute_by_restaurant_id(restaurant_id, attribute):
    response = config.user_ratings_dynamodb_table.query(
        IndexName=config.restaurant_id_rating_value_index,
        KeyConditionExpression='#partitionkey = :partitionkeyval',
        ProjectionExpression='#attribute', 
        ExpressionAttributeNames={
            '#partitionkey' : config.restaurant_id_rating_value_index_pkey,
            '#attribute' : attribute
        },
        ExpressionAttributeValues={
            ':partitionkeyval' : restaurant_id
        }
    )
    return response
