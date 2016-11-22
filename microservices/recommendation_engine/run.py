import sys, getopt
import config

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

if __name__ == "__main__":
    main()
    

