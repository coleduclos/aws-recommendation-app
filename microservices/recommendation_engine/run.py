import sys, getopt
import json
import config
import dynamodb_client

def main():
    sqs_queue_name = ''
    usage_str = "run.py -q <sqs_queue_name>"

    try:
        # Read command line args
        opts, args = getopt.getopt(sys.argv[1:],"h:q:")
    except getopt.GetoptError:
        print usage_str 
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage_str
            sys.exit()
        elif opt == '-q':
            sqs_queue_name = arg
    if sqs_queue_name == '':
        print "Please specify the sqs_queue_name with -q option"
        sys.exit()

    sqs_queue = config.sqs.get_queue_by_name(QueueName=sqs_queue_name)
    process_messages(sqs_queue)

def process_messages(sqs_queue):
    for message in sqs_queue.receive_messages(MaxNumberOfMessages=config.max_queue_messages):
        # print("SQS Message: {}".format(message.body))
        event = json.loads(message.body)
        rating = json.loads(event['body'])
        update_similar_users(rating)
        # message.delete()
        
def update_similar_users(rating):
    compared_user_list = [] 
    user_ratings_map = {}

    # Get all ratings by the user
    user_ratings = dynamodb_client.get_all_ratings_by_user_id(rating['user-id'])['Items']

    # For each user rating get a unique set of users who have also rated the same restaurants
    for u_rating in user_ratings:
        user_ratings_map[u_rating['restaurant-id']] = u_rating['rating-value'] 
        compared_user_list += \
            dynamodb_client.get_ratings_attribute_by_restaurant_id(u_rating['restaurant-id'],'user-id')['Items']
    compared_user_set = set([x['user-id'] for x in compared_user_list])
    compared_user_set.discard(rating['user-id'])

    # For each comparing user compute the similarity index
    for compared_user in compared_user_set:
        compared_user_ratings_map = {}
        similarity_idx_numerator = 0

        # Get the ratings of the compared user
        compared_user_ratings = dynamodb_client.get_all_ratings_by_user_id(compared_user)['Items']

        # Find the intersection and union of the user and compared user rating set to 
        # compute the similarity index
        for compared_user_rating in compared_user_ratings:
            compared_user_ratings_map[compared_user_rating['restaurant-id']] = compared_user_rating['rating-value']
        intersecting_restaurants = set(user_ratings_map.keys()) & set(compared_user_ratings_map.keys()) 
        similarity_idx_demoninator = len(set(user_ratings_map.keys()) | set(compared_user_ratings_map.keys()))
        for r in intersecting_restaurants:
             if user_ratings_map[r] == compared_user_ratings_map[r]:
                 similarity_idx_numerator += 1 
             else:
                 similarity_idx_numerator -= 1
        similarity_idx = float(similarity_idx_numerator) / float(similarity_idx_demoninator)

if __name__ == "__main__":
    main()
