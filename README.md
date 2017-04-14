# **CelebritySleuth**
A celebrity face recognition service built with [Serverless Framework](https://serverless.com/framework/) using [Twilio](https://www.twilio.com/), [Amazon Rekognition](https://aws.amazon.com/rekognition) and [IMDbPy API](http://imdbpy.sourceforge.net/).

This project provides an overview of *Serverless* computing and drills the concept down by helping build a compelling example of *Shazam for Celebrities* dubbed ***CelebritySleuth*** using the Serverless Framework. 

# Audience
You are a Developer or Solutions Architect wanting to learn the Serverless Framework and how to use it for developing your own auto-scaling, pay-per-execution, event-driven applications. You want to build applications that matters to business instead of spending time configuring, deploying and maintaining infrastructure. The boost in efficiency that the Serverless architecture promises is very compelling for you to ignore.

# The *CelebritySleuth* Application
The *CelebritySleuth* application is an event-driven application taking advantage of the user's mobile SMS/MMS for the presentation tier, Twilio in the middle-tier to bridge the SMS world and AWS Gateway and a set of AWS Lambda functions written in Python making use of AWS Rekogniton for image processing and IMDB for gathering information on the celebrities.

In a typical usage, the user snaps a picture of an celebrity using his/her phone camera and sends the image along with the instructions to a certain phone number hosted on Twilio. The system validates the instructions and responds immediately if there is an error in the instruction set or with a message to await the actual response if the validation passes. Momentarily, the user gets a response with the name and biography of the celebrity.

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
Update the *setTwilio.sh* in the repository with your credentials from Twilio and setup your environment.

    $ vi setTwilio.sh
    $ source ./setTwilio.sh

### Install node.js and Serverless framework
Serverless framework is a node.js application. To use Serverless framework and run the CelebritySleuth application you need to install node.js. Follow the [instructions](https://serverless.com/framework/docs/providers/aws/guide/installation/) from Serverless website to install both node.js and the Serverless framework and ensure your Serverless framework is operational using the following:

    $ serverless --version

### Amazon AWS Setup
1. Sign into your AWS account or [sign-up](https://console.aws.amazon.com/console/home?region=us-east-1) for one.
2. Setup your AWS credentials by following the instructions from [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/).


**Serverless Architecture vs. Serverless Framework**
====================================================
Per Gartner, by 2022 most cloud architectures will evolve to a fundamentally serverless model rendering the cloud platform architectures dominating in 2017 as legacy architectures. 

Serverless architecture reflects the core-promise of cloud-computing by offering agility and capability on demand at a value price. It will be at your best interest to understand this technology, the evolving eco-system and how to harness it as it provides high productivity at low cost.

Separating the Wheat from the Chaff
-----------------------------------

Serverless computing model is an emerging trend and quite often misunderstood because of the hype and build-up surrounding the topic. 

The term *[Serverless](https://martinfowler.com/articles/serverless.html)* refers to building applications without having to configure or maintain infrastructure required for running your applications. In reality, servers are still involved, though they are owned and controlled by the platform providers. On the other hand there are frameworks used for exploiting the serverless architecture uninspiringly named *[Serverless Framework](https://serverless.com/)* increasing the confusion.
 

Serverless Architectures
------------------------
 Serverless Architectures are those where the applications logic provided by the Developer is run on stateless, compute containers that are provisioned and managed by a provider. Typically these compute instances are ephemeral (short-lived for the duration of the request-response cycle) and triggered through an event. Due to the on-demand provisioning nature of this architecture, the systems built using Serverless technologies are inherently scaleable and highly responsive under load. 

**FaaS vs PaaS**

Some people in the industry refer to the technique of building applications using Serverless architecture as FaaS (Function as a Service). The reason becomes clear when you contrast FaaS applications with the traditionally built applications or PaaS (Platform as a Service) where there is a perpetual process running on a server waiting for HTTP requests or API calls. In FaaS there is no perpetual process (for the most part) but an event mechanism that triggers the execution of a piece of code, usually just a function. You still need a perpetual gateway that will field your API calls to start the events to cascade.  

The other key operational difference between FaaS and PaaS is scaling. With most PaaS solutions you still need to worry about scale. With FaaS the compute resources are provisioned at a request level. You cannot get the same level of granularity with PaaS applications even if you set it to auto-scale. As a result of this, FaaS applications are extremely efficient when it comes to managing cost.

> **Limitations of FaaS**
> 
> *State* Due to the ephemeral nature of the FaaS architecture, the state of your application should be managed externally from the FaaS
> infrastructure or off-loaded to a cache or data-base. This could be
> very limiting for certain type of applications running on thin clients
> or untrusted devices where the application orchestration has to extend
> through multiple request-response cycles.
> 
> *Duration* Because of the on-demand provisioning and low-cost nature of the FaaS solution there is a restriction on how long your functions
> are allowed to run.  To keep the price low - as you are billed by
> minutes of usage, some providers such as Amazon AWS and Microsoft
> Azure restrict the duration of time a function is allowed to process a
> request.  
> 
> *Deployment & Resource Limits* Some providers such as AWS have [deployment
> limits](http://docs.aws.amazon.com/lambda/latest/dg/limits.html) on
> the size of the deployment package, size of the code and libraries
> that can be deployed in the package. This could be severely limiting
> for some applications such as image processing functions that depend
> on large libraries that have to be packaged along with the code.
> Additionally, there are limits on the number of concurrent function
> executions, ephemeral disk capacity (temp space) etc. While some of
> these limits are soft limits and can be reconfigured per function by
> working with the providers, others are hard limits and will force you
> to reevaluate the choice of your design.
> 
> *Latency*  Due to the on-demand provisioning nature of the FaaS infrastructure, applications that uses languages such as Java/Scala
> that require a long start time to spin up JVMs may encounter longer
> runtime. Having said that, providers optimize the infrastructure
> spin-ups based on the usage patterns of the functions. Due to the
> interpreted nature of Python and Javascript, functions written in
> these languages may not see a significant difference in latency
> between a PaaS and FaaS offering.

**The Players**

While there are new providers entering the market to exploit the Serverless wave, the dominant players are Amazon with its AWS Lambda, Microsoft with its Azure Functions, Google with its Google Functions and Apache with its Openwhisk rule the roost with AWS Lambda being the dominant player.

Serverless Framework
--------------------
While the Serverless architecture unbinds you the Developer from having to provision and manage the resources for the bulk of your compute needs you are still bound to idiosyncrasies of the provider when it comes to their FaaS offering. Not only do you have to learn the different terminologies used by the various providers, you will have to learn how to use their offerings on their respective consoles or CLI (Command Line Interface).

To avoid vendor lock-in and allow to deploy your FaaS solutions to various providers, [Serverless Framework](https://serverless.com/) comes to your rescue. The Serverless Framework allows you to deploy auto-scaling, pay-per-execution, event-driven functions to any cloud. They currently support [AWS Lambda](https://aws.amazon.com/lambda), [IBM Bluemix OpenWhisk](https://developer.ibm.com/openwhisk/), [Microsoft Azure](https://azure.microsoft.com/en-us/services/functions), and are expanding to support other cloud providers.

The Serverless Framework allows you to provision and deploy a REST API, data pipe-line, or other uses cases by providing you a CLI to manage and build a serverless architecture by abstracting away provider-level complexity. 

The Serverless Framework is an MIT open-source project, actively maintained by a vibrant and engaged community of developers.


----------


