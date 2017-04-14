# **CelebritySleuth**
A celebrity face recognition service built with [Serverless Framework](https://serverless.com/framework/) using [Twilio](https://www.twilio.com/), [Amazon Rekognition](https://aws.amazon.com/rekognition) and [IMDbPy API](http://imdbpy.sourceforge.net/).

This project provides an overview of *Serverless* computing and drills the concept down by helping build a compelling example of *Shazam for Celebrities* dubbed ***CelebritySleuth*** using the Serverless Framework. 

For more information on Serverless architecture and Serverless Framework check out this [whitepaper](https://github.com/skarlekar/faces/blob/master/What_is_Serverless.md).

# Audience
You are a Developer or Solutions Architect wanting to learn the Serverless Framework and how to use it for developing your own auto-scaling, pay-per-execution, event-driven applications. You want to build applications that matters to business instead of spending time configuring, deploying and maintaining infrastructure. The boost in efficiency that the Serverless architecture promises is very compelling for you to ignore.

# The *CelebritySleuth* Application
The *CelebritySleuth* application is an event-driven application taking advantage of the user's mobile SMS/MMS for the presentation tier, Twilio in the middle-tier to bridge the SMS world and AWS Gateway and a set of AWS Lambda functions written in Python making use of AWS Rekogniton for image processing and IMDB for gathering information on the celebrities.

In a typical usage, the user snaps a picture of an celebrity (on TV?!) using his/her phone camera and sends the image along with the instructions to a certain phone number hosted on Twilio. The system validates the instructions and responds immediately if there is an error in the instruction set or with a message to await the actual response if the validation passes. Momentarily, the user gets a response with the name and biography of the celebrity.

To begin with you have to train the application to recognize the faces by building a collection of celebrities. You do this by sending a random sample of celebrity pictures (image URLs) and their corresponding names. The more pictures of a celebrity, the more accurate the recognition will be.

The *CelebritySleuth* application consists of two services:
 - [Twilio Communication Service](https://github.com/skarlekar/faces/tree/master/twilioCommunicationService)
 - [Face Recognition Service](https://github.com/skarlekar/faces/tree/master/faceRecognitionService)

The services are decoupled to allow for using different presentation tiers in future.


----------
## Usage:
TO DO: Describe the end-user usage pattern with a snapshots of various commands in use.

----------
## The Architecture
The *CelebritySleuth* application uses Lambda functions for compute needs. As a result the application components are provisioned just before usage and brought down after use resulting in a low-cost, highly-scalable application.

![Celebrity Sleuth Architecture](https://github.com/skarlekar/faces/blob/master/CelebritySleuthArchitecture.png)

The above picture illustrates the high-level architecture of the application. Details are as follows:

1. User sends a picture and commands to add/match face to a collection. Alternatively, the user can create a collection – in which case a picture is not required. The SMS/MMS is sent to a telephone number hosted by Twilio.

2. Twilio intercepts the message and forwards it to an API Gateway based on the user’s Twilio configuration.

3. API Gateway translates TwiML to JSON and calls the Request Processor lambda function.

4. The Request Processor lambda validates the commands and put a message to the appropriate topic on SNS. If the validation fails, it returns the error message to the user via Twilio.

5. When a message arrives in the Create Collection topic, a lambda is triggered which adds the named collection in AWS Rekognition via Boto libraries. A success/error message is put in the Response Processor topic.

6. When a message arrives in Add Face topic, a lambda is triggered which identifies  the most prominent face in the image and adds the metadata for the face to the given collection. If there is no faces identified, it creates an error message and sends the response to the Response Processor topic.

7. When a message arrives in Match Face topic, a lambda is triggered which identifies the most prominent face in the image and matches the metadata for that face with known faces in the collection. If a match is found, the corresponding person’s name is returned. The Lambda then uses IMDB to lookup the biography of the person.

8. The various lambda-based processors drops the response message on the Response Processor topic.

9. The Response Processor picks up the response and constructs a SMS message and calls Twilio’s SMS service.

10. Twilio validates the From number and sends the message to the corresponding To number. 


----------


## Components

The application consists of the following components:
1. Python - Python is a programming language that lets you work quickly
and integrate systems more effectively. We will use Python 2.7 for building the *CelebritySleuth* Application.

2. Twilio - Twilio Messaging Service for having the user communicate with the application through SMS. 

3. AWS Lambda - AWS Lambda lets you run code without provisioning or managing servers. You pay only for the compute time you consume - there is no charge when your code is not running.

4. AWS Rekognition - Amazon Rekognition is a service that makes it easy to add image analysis to your applications. With Rekognition, you can detect objects, scenes, and faces in images. You can also search and compare faces.

5. IMDb - IMDbPY is a Python package useful to retrieve and manage the data of the IMDb movie database about movies, people, characters and companies.

## Setup Instructions
### Installing Python
If you are on a Mac or Linux machine, you probably already have Python installed. On Windows you have to install Python. 

Regardless of your operating system, you are better off using a virtual environment for running Python. [Anaconda](https://www.continuum.io/downloads) or its terse version [Miniconda](https://conda.io/miniconda.html) is a Python virtual environment that allows you to manage various versions and environments of Python. The installers come with Python and the package manager *conda* with it. Follow the instructions [here](https://conda.io/docs/install/quick.html) to install Miniconda. For this project we will use Python 2.7.

#### Creating a Python Virtual Environment.
After installing Python 2.7, create an virtual environment as follows. Note:  I am calling my virtual environment *faces*:
   
    $ conda create -n faces python=2
    
#### Initialize your Python Virtual Environment
To start working in your new Python virtual environment:

    $ source activate faces

### Install Git
Git is a popular code revision control system. To install Git for your respective operating system follow the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

### Install *CelebritySleuth* 
To install CelebritySleuth from Git, follow the instructions below:

    $ mkdir DevFestDC
    $ cd DevFestDC
    $ git clone --recursive https://github.com/skarlekar/faces.git

### Twilio Setup
If you do not already have a Twilio number, [signup](https://www.twilio.com/try-twilio) for Twilio and get a trial phone number with MMS capability. You can use this number for 30-days during the trial period.

#### Setup Twilio Environment Variables
Update the *setTwilio.sh* in the repository with your credentials from Twilio and setup your environment. Instructions on using *vi* is [here](https://www.howtoforge.com/faq/how-to-edit-files-on-the-command-line).

    $ vi setTwilio.sh
    $ source ./setTwilio.sh

#### Test Twilio Setup
To test your Twilio setup, run the Python program *sendmessage.py* under *twilioTester*. This program simply sends a message to your mobile number using your Twilio credentials. *Note: Make sure you are running this in your Python 2.7 environment.*

    $ python twilioTester/sendmessage.py

If you receive a message with an image on your mobile, your Twilio is setup is working.

### Install node.js and Serverless framework
Serverless framework is a node.js application. To use Serverless framework and run the CelebritySleuth application you need to install node.js. Follow the [instructions](https://serverless.com/framework/docs/providers/aws/guide/installation/) from Serverless website to install both node.js and the Serverless framework. 

Ensure your Serverless framework is operational using the following:

    $ serverless --version

### Amazon AWS Setup
1. Sign into your AWS account or [sign-up](https://console.aws.amazon.com/console/home?region=us-east-1) for one.
2. Setup your AWS credentials by following the instructions from [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/).

### Testing your Serverless Setup
Now that you have setup AWS, it is time to test your Serverless setup by creating a mock function using the Serverless framework.

Create a test directory. In the test directory, create a Lambda function from the default template as follows:

    $ sls create --template aws-python --name sls-test
This should create two files in the current directory:
> serverless.yml
> handler.py

The *serverless.yml* declares a sample service and a function. The *handler.py*  returns a message stating that your function executed successfully. 

To deploy the function, simply type:

    $ sls deploy --verbose

This should deploy the function. The verbose option provides extra information.

To test your function, type:

    $ sls invoke --function hello

If you get the following message, your Serverless setup is working.

      WARNING: You are running v1.9.0. v1.10.0 will include the following breaking changes:
        - Some lifecycle events for the deploy plugin will move to a new package plugin. More info -> https://git.io/vy1zC
    
      You can opt-out from these warnings by setting the "SLS_IGNORE_WARNING=*" environment variable.
    
    {
        "body": "{\"input\": {}, \"message\": \"Go Serverless v1.0! Your function executed successfully!\"}",
        "statusCode": 200
    }

## Twilio Communication Service

## Face Recognition Service




