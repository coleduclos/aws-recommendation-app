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
    # Get similar users
    user_similarity_index_map = dynamodb_client.get_similarity_index_map_by_user_id(user_id)['Items']
    if len(user_similarity_index_map) > 0:
        user_similarity_index_map = user_similarity_index_map[0]['similarity-index-map']
    print user_similarity_index_map

if __name__ == "__main__":
    main()
