import json
import boto3 as boto
import requests
from argparse import ArgumentParser

def get_rekog_client():
    return boto.client('rekognition')

def get_bytes(image_url):
    req_for_image = requests.get(image_url, stream=True)
    file_object_from_req = req_for_image.raw
    req_data_bytes = file_object_from_req.read()
    return req_data_bytes

def detect_face(client, file):
    face_detected = False
    image_bytes = get_bytes(file)
    response = client.detect_faces(Image={'Bytes': image_bytes})
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
    image_url = event['image_url']
    collection_name = event['collection_name']
    label = event['label']
    message = "No faces in given image"

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
        "message": message,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def get_args():
    parser = ArgumentParser(description='Add a face in a given image to a Collection in AWS Image Rekognition and associate it with a Name')
    parser.add_argument('-c', '--collection', required=True)
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-n', '--name', required=True)
    return parser.parse_args()

def main():
    args = get_args()
    context = None
    urls = [line.rstrip('\n') for line in open(args.file)]
    for url in urls:
        request = {
            "image_url": url,
            "collection_name": args.collection,
            "label": args.name
        }
        process(request, context)
        print("Image from {} added to collection {}".format(url, args.collection))
    print("All done!")

if __name__ == '__main__':
    main()
