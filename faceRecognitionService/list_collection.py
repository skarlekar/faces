import json
import boto3 as boto


def get_rekog_client():
    return boto.client('rekognition')

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def process(event, context):
    message = {
        "error":
        "Listing of collections failed!" }

    client = get_rekog_client()
    response = client.list_collections()

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        message = response['CollectionIds']
    body = {
        #"message": json.dumps(message),
        "message": message,
        "input": event
    }
    response = {
        "statusCode": 200,
        #"body": json.dumps(body)
        "body": body
    }
    return response

def main():
    request = {
    }
    context = None
    pp_json(process(request, context))
    print("All done!")

if __name__ == '__main__':
    main()
