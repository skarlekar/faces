import json
import boto3 as boto
from argparse import ArgumentParser

sns_client = boto.client("sns")

def getTopicArn(topic):
    topicArn = None
    topics = sns_client.list_topics()["Topics"]
    for t in topics:
        if topic in json.dumps(t):
            topicArn = t["TopicArn"]
    return topicArn

def get_rekog_client():
    return boto.client('rekognition')

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def collection_exists(client, collection_name):
    value = True
    response = client.list_collections()
    collections = response['CollectionIds']
    try:
        collections.index(collection_name)
    except ValueError:
        value = False
    return value

def process(event, context):
    sns_record = event['Records'][0]
    sns_message = sns_record['Sns']['Message']
    sns_message_json = json.loads(sns_message)
    collection_name = sns_message_json['collection_name']
    received_from = sns_message_json['from_number']
    send_to = sns_message_json['to_number']
    message = "Creation of collection {0} failed!".format(collection_name)

    client = get_rekog_client()

    if (collection_exists(client, collection_name)):
        message = "Collection {} already exists!".format(collection_name)
    else:
        response = client.create_collection(CollectionId=collection_name)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            message = "Collection {0} was created successfully".format(collection_name)

    body = {
        "Message": message,
        "From_number": received_from,
        "To_number": send_to,
        "input": event
    }

    print("Body of message:------------")
    print(json.dumps(body))
    print("----------------------------")

    topicArn = getTopicArn("dispatch_response")
    payload = json.dumps({'default':json.dumps(body)})

    if __name__ <> '__main__':
        publish_response = sns_client.publish(TopicArn=topicArn, Message=payload, MessageStructure='json' )
        print("Publish Response: {}".format(json.dumps(publish_response)))
    else:
        print("If this is not a test, the following response will be published to SNS")
        print("----------------------------------------------------------------------")
        print(payload)
        print("----------------------------------------------------------------------")
    return body


def get_args():
    parser = ArgumentParser(description='Add a new Collection to AWS Image Rekognition')
    parser.add_argument('-c', '--collection', required=True)
    return parser.parse_args()

def main():
    args = get_args()
    args = get_args()
    test_message = "{\"collection_name\": \""+args.collection+"\",  \"from_number\": \"18007001234\", \"to_number\": \"18779991234\"}"
    print ("Test message is: ", test_message)
    request = { "Records":
        [
            {   "Sns": {
                        "Message": test_message
                        }
            }
        ]
    }
    context = None
    pp_json(process(request, context))
    print("All done!")

if __name__ == '__main__':
    main()
