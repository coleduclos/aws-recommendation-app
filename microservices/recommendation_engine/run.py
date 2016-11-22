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
    user_ratings = dynamodb_client.get_all_ratings_by_user_id(rating['user-id'])
    restaurant_ratings = dynamodb_client.get_all_ratings_by_restaurant_id(rating['restaurant-id'])
    for item in restaurant_ratings['Items']:
        print item

if __name__ == "__main__":
    main()
