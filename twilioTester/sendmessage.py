from twilio.rest import TwilioRestClient
import os 
import datetime

def getTwilioCredentials():
    SID = os.environ['TWILIO_ACCOUNT_SID']
    TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    return SID,TOKEN

def getTwilioFromTo():
    fromNumber = os.environ['TWILIO_FROM_NUMBER']
    toNumber = os.environ['TWILIO_TO_NUMBER']
    return fromNumber,toNumber

ACCOUNT_SID, AUTH_TOKEN = getTwilioCredentials()
twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
fromNum, toNum = getTwilioFromTo()
date_time = str(datetime.datetime.now())

twilio_client.messages.create(
    to = toNum,
    from_= fromNum,
    body="This image of Neil Armstrong is the most influential image of our time. A vulnerable human on a distant world - a world that would kill him if he removed so much as a single article of his exceedingly complex clothing. Current time is {}".format(date_time),
    media_url="http://dujye7n3e5wjl.cloudfront.net/photographs/1080-tall/time-100-influential-photos-neil-armstrong-nasa-man-moon-64.jpg",
)
