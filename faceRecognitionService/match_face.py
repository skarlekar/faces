import json
import boto3 as boto
import requests
import sys
from imdb import IMDb
from argparse import ArgumentParser

celebrities = IMDb()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()
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

def get_bytes(image_url):
    req_for_image = requests.get(image_url, stream=True)
    file_object_from_req = req_for_image.raw
    req_data_bytes = file_object_from_req.read()
    return req_data_bytes

def detect_face(client, file):
    face_detected = False

    # An InvalidImageException will be raised if Rekognition does not support the
    # given image type. For instance, animated GIF etc.
    try:
        image_bytes = get_bytes(file)
        response = client.detect_faces(Image={'Bytes': image_bytes})
    except Exception:
        response = None

    if (response is not None):
        if (not response['FaceDetails']):
            face_detected = False
        else:
            face_detected = True

    return face_detected, response

def match_face_in_collection(client, file, collection):
    face_matches = False
    image_bytes = get_bytes(file)
    response = client.search_faces_by_image(CollectionId=collection,
                                            Image={'Bytes': image_bytes},
                                            MaxFaces=1,
                                            FaceMatchThreshold=85)
    if (not response['FaceMatches']):
        face_matches = False
    else:
        face_matches = True
    return face_matches, response

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def celebrity_check(name):
    name = name.replace("_"," ")
    isCelebrity = False
    value = "{} is not a celebrity".format(name)
    results = celebrities.search_person(name)
    if len(results) > 0:
        celebrity = results[0]
        celebrities.update(celebrity)
        value = celebrity.summary().encode(out_encoding, 'replace')
        isCelebrity = True
    return isCelebrity, value

def process(event, context):
    print("Event received is as follows:---------------")
    print(json.dumps(event))
    print("--------------------------------------------")

    sns_record = event['Records'][0]
    sns_message = sns_record['Sns']['Message']
    sns_message_json = json.loads(sns_message)
    #message = sns_message_json['body']['message']
    image_url = sns_message_json['image_url']
    collection_name = sns_message_json['collection_name']
    received_from = sns_message_json['from_number']
    send_to = sns_message_json['to_number']
    message = "No faces in given image, invalid image format or no known face detected"
    body = {}
    client = get_rekog_client()
    isCelebrity = False
    match_face_result = False
    # First: find a face in the given image
    result, resp = detect_face(client, image_url)

    # Second: If there is a face, match the face with the faces in the given collection
    if (result):
        print("Face detected!")
        message = "Face detected, but not a known face"
        match_face_result, match_face_response = match_face_in_collection(client,
                                                    image_url,
                                                    collection_name)

    if (match_face_result):
        name_of_person = match_face_response['FaceMatches'][0]['Face']['ExternalImageId']
        message = "Face matched {0} with {1} similarity and {2} confidence".format(
                    name_of_person.replace("_"," ").title(),
                    round(match_face_response['FaceMatches'][0]['Similarity'], 1),
                    round(match_face_response['FaceMatches'][0]['Face']['Confidence'], 2))
        isCelebrity, bio = celebrity_check(name_of_person)

    body = {
        "Biography": bio if isCelebrity else "",
        "Message": message,
        "From_number": received_from,
        "To_number": send_to,
        "Input": event
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
    parser = ArgumentParser(description='Detect a face in a given image and match it to a name in a Collection stored in AWS Image Rekognition')
    parser.add_argument('-c', '--collection', required=True)
    parser.add_argument('-i', '--image', required=True)
    return parser.parse_args()

def main():
    args = get_args()

    test_message = "{\"collection_name\": \""+args.collection+"\", \"from_number\": \"18007001234\", \"to_number\": \"18779991234\", \"image_url\": \""+args.image+"\"}"
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
