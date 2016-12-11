import sys, getopt
import json
from decimal import *
import config
import dynamodb_client

def main():
    recommendation_queue = config.sqs.get_queue_by_name(QueueName=config.recommendation_queue_name)
    process_messages(recommendation_queue)

def process_messages(recommendation_queue):
    for message in recommendation_queue.receive_messages(MaxNumberOfMessages=config.max_queue_messages):
        # print("SQS Message: {}".format(message.body))
        user_id = message.body
        update_recommendations(user_id)
        # message.delete()
        
def update_recommendations(user_id):
    print('Updating recommendations for user: {}'.format(user_id))
    user_ratings_restaurant_id_list = []
    near_restaurant_id_list = []
    # Get similar users
    user_similarity_index_map = dynamodb_client.get_similarity_index_map_by_user_id(user_id)['Items']
    if len(user_similarity_index_map) > 0:
        user_similarity_index_map = user_similarity_index_map[0]['similarity-index-map']
    user_ratings = dynamodb_client.get_all_ratings_by_user_id(user_id)['Items']
    for u_rating in user_ratings:
        user_ratings_restaurant_id_list.append(u_rating['restaurant-id'])

    near_restaurants = dynamodb_client.get_all_restaurants_by_zip_code('94109')['Items']
    for restaurant in near_restaurants:
        near_restaurant_id_list.append(restaurant['restaurant-id'])
    restaurants_not_rated = set(user_ratings_restaurant_id_list)^set(near_restaurant_id_list)
    for restaurant_id in restaurants_not_rated:
        print restaurant_id

if __name__ == "__main__":
    main()
