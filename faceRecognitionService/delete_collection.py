import json
import sys
import boto3 as boto
from argparse import ArgumentParser

def get_rekog_client():
    return boto.client('rekognition')

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def process(event, context):
    collection_name = event['collection_name']
    message = "Deletion of collection {0} failed!".format(collection_name)

    client = get_rekog_client()
    response = {}
    try:
        response = client.delete_collection(CollectionId=collection_name)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            message = "Collection {0} was deleted successfully".format(collection_name)

    except:
        message = "Collection {} does not exist".format(collection_name)

    body = {
        "message": message,
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def get_args():
    parser = ArgumentParser(description='Delete a Collection in AWS Image Rekognition')
    parser.add_argument('-c', '--collection', required=True)
    return parser.parse_args()

def main():
    args = get_args()
    request = {
        "collection_name": args.collection
    }
    context = None
    pp_json(process(request, context))
    print("All done!")

if __name__ == '__main__':
    main()
