import os
import json
from twilio.rest import TwilioRestClient
import boto3 as boto

def getTwilioCredentials():
    SID = os.environ['TWILIO_ACCOUNT_SID']
    TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    return SID,TOKEN

ACCOUNT_SID, AUTH_TOKEN = getTwilioCredentials()
twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

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

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def process(event, context):
    print("Event received is as follows:---------------")
    print(json.dumps(event))
    print("--------------------------------------------")

    sns_record = event['Records'][0]
    sns_message = sns_record['Sns']['Message']
    sns_message_json = json.loads(sns_message)
    message = sns_message_json['Message']
    try:
        biography = sns_message_json['Biography']
    except KeyError:
        biography = ""
    received_from = sns_message_json['From_number']
    send_to = sns_message_json['To_number']

    print("Debug message:------------------------")
    print("Message: {}".format(message))
    print("Biography: {}".format(biography))
    print("From Number: {}".format(received_from))
    print("---------------------------------------")

    if (len(biography) > 0):
        message = message  + " " + biography

    #fromNum, toNum = getTwilioFromTo()
    print ("Name of program is: {}".format(__name__))
    if __name__ <> '__main__':
        sendMessage(received_from, send_to, message)
    else:
        print("If this is not a test, a message will be sent to {} from {}".format(received_from, send_to))

    return_message = "Response sent to {}".format(received_from)

    response = {
        "statusCode": 200,
        "body": return_message
    }
    return response


def main():
    fromNum, toNum = getTwilioFromTo()
    request = {
    "Records": [
        {
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:219104658389:dispatch_response:43214a04-4b9e-45a0-8846-c2f4c63bc4c2",
            "EventSource": "aws:sns",
            "Sns": {
                "SignatureVersion": "1",
                "Timestamp": "2017-04-09T02:14:01.390Z",
                "Signature": "/zEViFFZY7MQn4UB8+/XDQnpmS+DaCLAbqhcEz+y71ETh1rZv9q4nfRU7eeN0nGMmhxyEUcme3x2IxUPt3Hj+K1T0VteKBsMJM4Zi725wzJmOZP5DCs92XNSRLXRNnCkculddtxfFIOFLLVYbItMR0P4hDlNB+X6FeHxPBYiisRDMTt9MJ88jnvN62aoVtnijWesmDvwFYZU5GAN1B6IPHXaZHjL4JkZGcjc2RuEzkiR1lFmnrlWGp4cuwvBp1Z6aB8Oqv/U+Ij4W4o36ZURIEVE+fQ==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-b95095beb82e8f6a046bf4149a.pem",
                "MessageId": "609128ac-4132-5bf9-90bc-79cfda1b7e34",
                "Message": "{\"Input\": {\"Records\": [{\"EventVersion\": \"1.0\", \"EventSubscriptionArn\": \"arn:aws:sns:us-east-1:219104658389:match_face_request:81c11448-0511-408b-9bc9-f1008b8f7d5f\", \"EventSource\": \"aws:sns\", \"Sns\": {\"SignatureVersion\": \"1\", \"Timestamp\": \"2017-04-09T02:13:52.768Z\", \"Signature\": \"khGxRZPySGY32rmX1mWyRgEuG0yO6CO/EEVW7jA8lr+DZpfetdUcU0zBNTwQD5Lu2DsAgbswiFXXw2kL/vNXjUqWmmn7RhQIK7aA+XDqkBgp3aXYLxNIr3tINirLmcrXYARml9+H0wMG2AUP//+BNsPRHHYtzsr7OryzyxC0R1GAT63hhUlCIeH4addHOEu2b09rRB5fpQVWA1yt8QYj4tdh7WNJM5952Wapmz9TBQSCh7P2zVplEoBSiu0SZEIznR6sZCTTswINtzQ2aJMx+WscNMaYg==\", \"SigningCertUrl\": \"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-b95095beb82e8f6a046b3aafc7f4149a.pem\", \"MessageId\": \"cad80b20-4b98-518e-a624-5a43d0b8a401\", \"Message\": \"{\\\"collection_name\\\": \\\"celebs\\\", \\\"operation\\\": \\\"match\\\", \\\"from_number\\\": \\\"+18007071234\\\", \\\"image_url\\\": \\\"https://api.twilio.com/2010-04-01/Accounts/brt23c14c5a922eac706b13c6189/Messages/MMe9f3b925ba85b64dc2f8e1ce3739269c/Media/MEe7a417b6e95523f0f92d38824cf96e38\\\", \\\"to_number\\\": \\\"+18007071234\\\"}\", \"MessageAttributes\": {}, \"Type\": \"Notification\", \"UnsubscribeUrl\": \"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:219104658389:match_face_request:81c11448-0511-408b-9bc9-f1008b8f7d5f\", \"TopicArn\": \"arn:aws:sns:us-east-1:219104658389:match_face_request\", \"Subject\": null}}]}, \"Message\": \"Face matched Tom Cruise with 93.9 similarity and 100.0 confidence\", \"From_number\": \"+18007071234\", \"To_number\": \"+18007071234\", \"Biography\": \"Person\\n=====\\nName: Cruise, Tom\\nBirth date: 3 July 1962 (Syracuse, New York, USA).\\nLast movies directed: \\\"Fallen Angels\\\" (1993).\\nLast movies acted: M:I 6 - Mission Impossible (2018); American Made (2017); Mummy, The (2017); Luna Park () (????); Top Gun 2 () (????).\\n\"}",
                "MessageAttributes": {},
                "Type": "Notification",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:219104658389:dispatch_response:43214a04-4b9e-45a0-8846-c2f4c63bc4c2",
                "TopicArn": "arn:aws:sns:us-east-1:219104658389:dispatch_response"
            }
        }
    ]
}

    context = None
    pp_json(process(request, context))
    print("All done!")

if __name__ == '__main__':
    main()
