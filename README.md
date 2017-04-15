Table of Contents
-----------------

   * [<strong>CelebritySleuth</strong>](#celebritysleuth)
   * [Audience](#audience)
   * [The <em>CelebritySleuth</em> Application](#the-celebritysleuth-application)
      * [The Architecture](#the-architecture)
      * [Components](#components)
      * [Setup Instructions](#setup-instructions)
         * [Installing Python](#installing-python)
            * [Creating a Python Virtual Environment.](#creating-a-python-virtual-environment)
            * [Initialize your Python Virtual Environment](#initialize-your-python-virtual-environment)
         * [Install Git](#install-git)
         * [Install <em>CelebritySleuth</em>](#install-celebritysleuth)
         * [Twilio Setup](#twilio-setup)
            * [Setup Twilio Environment Variables](#setup-twilio-environment-variables)
            * [Test Twilio Setup](#test-twilio-setup)
         * [Install node.js and Serverless framework](#install-nodejs-and-serverless-framework)
         * [Amazon AWS Setup](#amazon-aws-setup)
         * [Testing your Serverless Setup](#testing-your-serverless-setup)
         * [Twilio Communication Service](#twilio-communication-service)
            * [Deploy Twilio Communication Service](#deploy-twilio-communication-service)
            * [Setup Twilio Messaging Service](#setup-twilio-messaging-service)
         * [Face Recognition Service](#face-recognition-service)
            * [Deploy Face Recognition Service](#deploy-face-recognition-service)
      * [Usage](#usage)



# **CelebritySleuth**
A celebrity face recognition service built with [Serverless Framewor## Heading ##k](https://serverless.com/framework/) using [Twilio](https://www.twilio.com/), [Amazon Rekognition](https://aws.amazon.com/rekognition) and [IMDbPy API](http://imdbpy.sourceforge.net/).

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


----------


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
> 
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

### Twilio Communication Service
The Twilio Communication Service [twilioCommunicationService](https://github.com/skarlekar/faces/tree/master/twilioCommunicationService) bridges Twilio's SMS messaging service with the Face Recognition Service. When the user sends a message to his/her Twilio number, the message is intercepted by Twilio's Messaging service. The Twilio Messaging service will forward the SMS message contents to AWS API Gateway URL. The AWS API Gateway in turn will invoke the  Request Processor (*process_request*) Lambda function in the *twilioCommunicationService*.

See the [Usage](https://github.com/skarlekar/faces#usage) section for the details on how to use this service.

#### Deploy Twilio Communication Service
Assuming your local Serverless setup is complete and the test above to test your Serverless setup passes, follow the instructions below to deploy the *twilioCommunicationService* using the Serverless framework:

Set your Twilio credentials by running the shell script you updated earlier. 

    $ source ./setTwilio.sh

Change directory to the twilioCommunicationService directory and deploy the service by running *sls deploy* as shown below:

    $ cd twilioCommunicationService
    $ sls deploy --verbose

Ensure there are no errors in the deployment process. You can also head on to your [AWS Console](https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis) and verify that the API Gateway has been created. You should see an API Gateway called *dev-twilioCommunication*. 

Also ensure the Lambda functions are created by verifying that the *twilioCommunication-dev-processRequest* and *twilioCommunication-dev-sendResponse* lambda functions is available in the [AWS Lambda console](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions?display=list).

Ensure your Twilio credentials are setup as environment variables by clicking on each of the Lambda functions and verifying that the *TWILIO_AUTH_TOKEN* and *TWILIO_ACCOUNT_SID* have been created with the correct values in the *Environment Variables* section in the *Code* tab.

#### Setup Twilio Messaging Service
Follow the instructions below to setup the Messaging Service in Twilio and associate your Twilio number to the Messaging Service:

1. In the Twilio website, login to your account and head to the [Programmable SMS Dashboard](https://www.twilio.com/console/sms/dashboard).

2. Click on the **+** under Messaging Services with Copilot to add a new Messaging service.

3. Give a name to your service and click on *Create*.

4. Under *Properties* in the *USE CASE* drop-down, select *Chat Bot/Interactive 2-way*.

5. In the *Inbound Settings* section, ensure *PROCESS INBOUND MESSAGES* is checked.

6. Copy and paste the AWS API Gateway URL from your AWS console into the *REQUEST URL* field and select HTTP GET in the drop-down next to the field.

7. Leave rest of the fields to its default value.

8. Head to the [Numbers](https://www.twilio.com/console/phone-numbers/incoming) section in the Twilio console.

9. Click on the number assigned to you. This will take you to the section where you can configure what should happen when an SMS message is sent to your Phone Number.

10. Under the *Messaging* section, select *Messaging Service* under the *CONFIGURE WITH* drop-down.

11. In the *MESSAGING SERVICE*, select the Messaging service that created in steps 2-7 above and click *Save*.

### Face Recognition Service
The Face Recognition Service ([faceRecognitionService](https://github.com/skarlekar/faces/tree/master/faceRecognitionService)) currently supports three functions. They are:

> **createCollection**: To add a collection.
> 
>  **addFace**: To add a face to an existing collection.
>   
>  **matchFace**: To match a face in a collection and look up the biography of the matched person's name in IMDb.

A *collection* is a logical group of face indexes (face vectors) and their corresponding names. When you create a collection using the *createCollection* Lambda function, it is empty. On the back-end, createCollection creates a collection in AWS Rekognition. You can then add new faces to the collection and associate it with a given name. The collection thus created can then be used for searching images for known faces with high degree of confidence.  Physically, the face indexes are stored in a database on a server managed by AWS Rekognition. You do not have direct access to this database.

Once you have created a collection you can add faces to the collection using the *addFace* Lambda function. To add a face to a collection, you have to provide an image, a collection name and name you want to associate with the face. If there are no faces in the given image, or if the collection does not exist an error message is returned. The *addFace* function uses AWS Rekognition to detect faces in the given image, extract features from the face and persist information about facial features detected in the image to AWS Rekognition. The facial features are stored as searchable image vectors.

Once you have some faces indexed using the *addFace* function, you can then provide images of the person indexed using the *matchFace* function. The *matchFace* function requires the 

#### Deploy Face Recognition Service
Change directory to the faceRecognitionService directory and deploy the service by running *sls deploy* as shown below:

    $ cd faceRecognitionService
    $ sls deploy --verbose

Ensure there are no errors in the deployment process. You can also head on to your [AWS Lambda Console](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions?display=list) and verify that the Lambda functions *faceRecognition-dev-addFace*, *faceRecognition-dev-matchFace* and *faceRecogniton-dev-createCollection* has been created.

----------
## Usage
The commands in the SMS body should be of the following format.


----------
### Add Collection

To add a new collection, type the following in the SMS body. You don't have to add any image with this command. Any image added will be ignored.

    face addcol (collection-name)

where *collection-name* is the name of the collection you want to create.

Example:
*face addcol celebs*

![example of adding a collection](https://github.com/skarlekar/faces/blob/master/example-addcol.png)


----------
### Add Image

To add an image to a given collection and associate the face in the image to a name, type the following in the body of the SMS. You should include an image in the same SMS message.

    face addimg (collection-name) (first-name_last-name)

where *collection-name* is the name of an existing collection and first-name_last-name is the full name of the person. Note that the first name and last name should be separated by an underscore. 

Example:
*face addimg celebs Sean_Connery*

![example of adding an image to a collection](https://github.com/skarlekar/faces/blob/master/example-addimg.png)


----------
### Match Face

To match a face in a given collection:

    face match (collection-name)

where *collection-name* is the name of an existing collection. This command must be accompanied with an image in the same SMS message.

Example:
*face match celebs*

![snapshot of matching a celebrity face](https://github.com/skarlekar/faces/blob/master/example-matchface.png)

----------
### Application in Action:

Following is a sample animation of the application in action:

![sample GIF of the application in action](https://github.com/skarlekar/faces/blob/master/mel.gif)