import boto3
import json
import os
from twilio.rest import TwilioRestClient
import boto3 as boto

def getTwilioCredentials():
    SID = os.environ['TWILIO_ACCOUNT_SID']
    TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    return SID,TOKEN

ACCOUNT_SID, AUTH_TOKEN = getTwilioCredentials()
twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
sns_client = boto.client("sns")

VALID_OPERATORS = ["match", "addcol", "addimg"]
SNS_TOPICS = {'match':'match_face_request', 'addcol':'create_collection_request', 'addimg': 'add_face_request'}

def getTopicArn(topic):
    topicArn = None
    topics = sns_client.list_topics()["Topics"]
    for t in topics:
        if topic in json.dumps(t):
            topicArn = t["TopicArn"]
    return topicArn

def getTwilioFromTo():
    fromNumber = os.environ['TWILIO_FROM_NUMBER']
    toNumber = os.environ['TWILIO_TO_NUMBER']
    return fromNumber,toNumber

def sendMessage(toNum, fromNum, msgBody, media):
    twilio_client.messages.create(
        to = toNum,
        from_= fromNum,
        body= msgBody,
        media_url=media
    )
    return None

def sendMessage(toNum, fromNum, msgBody):
    twilio_client.messages.create(
        to = toNum,
        from_= fromNum,
        body= msgBody
    )
    return None

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def process(event, context):
    print("Received event:")
    print(json.dumps(event))
    print("----End of event----")

    command_line = event['body']
    from_number = event['fromNumber']
    to_number = event['toNumber']
    image_url = event['image']
    num_media = event['numMedia']

    print("Extracted values are: -------------------------------------")
    print("Body: {} ".format(command_line) )
    print("From: {} ".format(from_number) )
    print("To: {} ".format(to_number) )
    print("image_url: {} ".format(image_url) )

    commands = command_line.split()
    message = "All good. You should receive your response momentarily!"
    process_command = True
    service = ""
    operation = ""
    collection_name = ""
    label = ""
    topicArn = ""
    payload = ""
    publish_response = {}
    length = len(commands)
    if length<3 or length>4:
        message = "Usage: face match (collection-name)| face addimg (collection-name) (first-name)_(last-name) | addcol (collection-name). For match|addimg include an image attachment."
        process_command = False

    if process_command:
        service = commands[0].lower()
        print("Service is {}".format(service))

    if process_command and service != "face":
        print ("Not a valid service")
        message = "I only understand service 'face' right now."
        process_command = False

    if process_command:
        operation = commands[1].lower()

    if process_command and operation not in VALID_OPERATORS:
        message = "Valid operators for service 'face' is 'match|addcol|addimg'."
        process_command = False

    if process_command and operation == "addimg" and length <> 4:
        message = "Syntax for adding an image to a collection is: face addimg (collection-name) (first-name)_(last-name)"
        process_command = False

    if process_command and operation == "addimg" and length == 4:
        label = commands[3].lower()

    if process_command and operation in ["addimg","match"] and len(image_url) == 0:
        message = "Attach an image to 'match' or 'addimg' operations"
        process_command = False

    if process_command:
        collection_name = commands[2].lower()
        print("Will send message to SNS topic {}".format(SNS_TOPICS[operation]))
        topicArn = getTopicArn(SNS_TOPICS[operation])
        payload_json = { "operation": operation,
                            "image_url": image_url,
                            "collection_name": collection_name,
                            "from_number": from_number,
                            "to_number": to_number,
                            "label": label }
        payload = json.dumps({'default':json.dumps(payload_json)})
        publish_response = sns_client.publish(TopicArn=topicArn, Message=payload, MessageStructure='json' )

    print("Debug message: -------------------------------------")
    print("Service: {} ".format(service) )
    print("Operation: {} ".format(operation) )
    print("Collection: {} ".format(collection_name) )
    print("Publish Response: {}".format(json.dumps(publish_response)))
    print("Final message: {}".format(message))
    print("topicArn: {}".format(topicArn))
    print("SNS Payload: {}".format(payload))
    return message

def main():

    fromNum,toNum = getTwilioFromTo()
    # request = {
    #         "body": "face addimg celebs mel_gibson",
    #         "fromNumber": toNum,
    #         "toNumber" : fromNum,
    #         "image": "https://goo.gl/6QA0xK",
    #         "numMedia": "1"
    #     }
    request = {
            "body": "face addcol friends",
            "fromNumber": toNum,
            "toNumber" : fromNum,
            "image": "",
            "numMedia": "0"
        }
    context = None
    print(process(request, context))
    print("All done!")

if __name__ == '__main__':
    main()
