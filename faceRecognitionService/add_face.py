import json
import boto3 as boto
import requests
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
    except Exception as e:
        print ("Following error was raised:")
        print (e)
        print ("----------------------------")
        response = None

    if (response is not None):
        if (not response['FaceDetails']):
            face_detected = False
        else:
            face_detected = True

    return face_detected, response

def collection_exists(client, collection_name):
    value = True
    response = client.list_collections()
    collections = response['CollectionIds']
    try:
        collections.index(collection_name)
    except ValueError:
        value = False
    return value

def add_face_to_collection(client, file, collection, label):
    face_added = False
    image_bytes = get_bytes(file)
    response = client.index_faces(CollectionId=collection,
                                            Image={'Bytes': image_bytes},
                                            ExternalImageId=label,
                                            DetectionAttributes=['ALL'])

    if (response['FaceRecords'][0]['Face']['ExternalImageId'] == label):
        face_added = True

    return face_added

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def process(event, context):
    sns_record = event['Records'][0]
    sns_message = sns_record['Sns']['Message']
    sns_message_json = json.loads(sns_message)
    image_url = sns_message_json['image_url']
    collection_name = sns_message_json['collection_name']
    label = sns_message_json['label']
    received_from = sns_message_json['from_number']
    send_to = sns_message_json['to_number']
    message = "No faces in given image or invalid image format"

    client = get_rekog_client()

    # First: Find a face in the given image
    result, resp = detect_face(client, image_url)

    # Second: Find if the given collection exists
    valid_collection = collection_exists(client, collection_name)

    # If face is detected in the image but the collection does not exist
    if (result and not valid_collection):
        message = "Given collection {0} does not exist in your account".format(collection_name)

    # If face is not detected and the collection does not exist
    if (result is False and not valid_collection):
        message = "No faces in given image and given collection {0} does not exist in your account".format(collection_name)

    # Finally: If there is a face and the collection exists, add the face to the given collection and associate with
    # the given label (name)
    if (result and valid_collection):
        print("Face detected!")
        add_face_response = add_face_to_collection(client,
                                                    image_url,
                                                    collection_name,
                                                    label)
        message = "Picture of {0} added to Collection {1}".format(label, collection_name)

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
    parser = ArgumentParser(description='Add a face in a given image to a Collection in AWS Image Rekognition and associate it with a Name. Note: Concatenate the first name and last name with a underscore _. For instance, enter: python add_face.py -c celebs -i https://goo.gl/cvE4s -n Sean_Connery')
    parser.add_argument('-c', '--collection', required=True)
    parser.add_argument('-i', '--image', required=True)
    parser.add_argument('-n', '--name', required=True)
    return parser.parse_args()

def main():
    args = get_args()
    test_message = "{\"collection_name\": \""+args.collection+"\", \"label\": \""+args.name+"\", \"from_number\": \"18007001234\", \"to_number\": \"18779991234\", \"image_url\": \""+args.image+"\"}"
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
