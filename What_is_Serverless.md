


**Serverless Architecture vs. Serverless Framework**
====================================================
Per Gartner, by 2022 most cloud architectures will evolve to a fundamentally serverless model rendering the cloud platform architectures dominating in 2017 as legacy architectures.
 
Serverless is a cloud-native platform model and reflects the core-promise of cloud-computing by offering agility and capability on demand at a value price. 

The introduction of function PaaS (fPaaS) as Lambda by Amazon in re:Invent, Nov 2014 (and out of beta in late 2015) created a momentum for "serverless" platform architecture. AWS Lambda was soon followed by most major cloud platform vendors, including IBM, Microsoft, Google and, more recently, Oracle.  

    Amazon started the trend with Lambda

Separating the Wheat from the Chaff
-----------------------------------

Serverless computing model is an emerging trend and quite often misunderstood because of the hype and build-up surrounding the topic. 

The term *[Serverless](https://martinfowler.com/articles/serverless.html)* refers to building applications without having to configure or maintain infrastructure required for running your applications. In reality, servers are still involved, though they are owned and controlled by the platform providers. On the other hand there are frameworks used for exploiting the serverless architecture uninspiringly named *[Serverless Framework](https://serverless.com/)* increasing the confusion.
 

    Serverless - No need to configure or maintain infrastructure

Serverless Architectures
------------------------
Serverless Architectures are based on models where the applications logic provided by the Developer is run on stateless, compute containers that are provisioned and managed by a provider. Typically these compute instances are ephemeral (short-lived for the duration of the request-response cycle) and triggered through an event. Due to the on-demand provisioning nature of this architecture, the systems built using Serverless technologies are inherently scaleable and highly responsive under load. 


**FaaS - Function as a Service **

The technique of building applications using Serverless architecture.

![enter image description here](https://github.com/skarlekar/faces/blob/master/Faas.png)

>- **Pay-per-execution** - Pay per execution model is most efficient at managing costs.
> - **Ephemeral** – Short-lived process triggered via event.
> - **Auto-scaling** – Compute resources are provisioned granularly per request.
> - **Event-driven** – Functions respond to events such as http, file drop, alerts, timer, topics etc
> - **Microservices** – Modules built to satisfy a specific goal and uses a simple, well-defined interface. 

    FaaS – Applications Built with Serverless Architecture

**FaaS vs PaaS**

Some people in the industry refer to the technique of building applications using Serverless architecture as FaaS (Function as a Service). The reason becomes clear when you contrast FaaS applications with the traditionally built applications or PaaS (Platform as a Service) where there is a perpetual process running on a server waiting for HTTP requests or API calls. In FaaS there is no perpetual process (for the most part) but an event mechanism that triggers the execution of a piece of code, usually just a function. You still need a perpetual gateway that will field your API calls to start the events to cascade.  

The other key operational difference between FaaS and PaaS is scaling. With most PaaS solutions you still need to worry about scale. With FaaS the compute resources are provisioned at a request level. You cannot get the same level of granularity with PaaS applications even if you set it to auto-scale. As a result of this, FaaS applications are extremely efficient when it comes to managing cost.

 **Limitations of FaaS**
 
***State*** Due to the ephemeral nature of the FaaS architecture, the state of your application should be managed externally from the FaaS
 infrastructure or off-loaded to a cache or data-base. This could be
 very limiting for certain type of applications running on thin clients
 or untrusted devices where the application orchestration has to extend
 through multiple request-response cycles.
 

    State between Requests must be maintained outside of FaaS

 ***Duration*** Because of the on-demand provisioning and low-cost nature of the FaaS solution there is a restriction on how long your functions
 are allowed to run.  To keep the price low - as you are billed by
 minutes of usage, some providers such as Amazon AWS and Microsoft
 Azure restrict the duration of time a function is allowed to process a
 request.  
 

     Duration of time a function is allowed to run is restricted

 ***Deployment & Resource Limits*** Some providers such as AWS have [deployment
 limits](http://docs.aws.amazon.com/lambda/latest/dg/limits.html) on
 the size of the deployment package, size of the code and libraries
 that can be deployed in the package. This could be severely limiting
 for some applications such as image processing functions that depend
 on large libraries that have to be packaged along with the code.
 Additionally, there are limits on the number of concurrent function
 executions, ephemeral disk capacity (temp space) etc. While some of
 these limits are soft limits and can be reconfigured per function by
 working with the providers, others are hard limits and will force you
 to reevaluate the choice of your design.

    Resources are limited - Use wisely

 ***Latency***  Due to the on-demand provisioning nature of the FaaS infrastructure, applications that uses languages such as Java/Scala
 that require a long start time to spin up JVMs may encounter longer
 runtime. Having said that, providers optimize the infrastructure
 spin-ups based on the usage patterns of the functions. Due to the
 interpreted nature of Python and Javascript, functions written in
 these languages may not see a significant difference in latency
 between a PaaS and FaaS offering.

    Test the performance of your applications thoroughly

**The Players**

While there are new providers entering the market to exploit the Serverless wave, the significant players are Amazon with its AWS Lambda, Microsoft with its Azure Functions, Google with its Google Functions and IBM with its Openwhisk rule the roost with AWS Lambda being the dominant player.

    Amazon's AWS Lambda is the dominant player

Serverless Framework
--------------------
While not having to manage infrastructure by using serverless functions is nice, having to deal with hundreds of functions in a project between multiple providers, managing buckets, messaging and permissions becomes an issue in itself. Additionally, organizations want to diversify risk and hence do not want to be bound to a single provider. 

Add to this mix the idiosyncrasies of the provider when it comes to their FaaS offering. Not only do you have to learn the different terminologies used by the various providers, you will have to learn how to use their offerings on their respective consoles or CLI (Command Line Interface).

To avoid vendor lock-in and allow to deploy your FaaS solutions to various providers, [Serverless Framework](https://serverless.com/) comes to your rescue. The Serverless Framework allows you to deploy auto-scaling, pay-per-execution, event-driven functions to any cloud. They currently support [AWS Lambda](https://aws.amazon.com/lambda), [IBM Bluemix OpenWhisk](https://developer.ibm.com/openwhisk/), [Microsoft Azure](https://azure.microsoft.com/en-us/services/functions), and are expanding to support other cloud providers.

The Serverless Framework is an MIT open-source project, actively maintained by a vibrant and engaged community of developers and provides robust plugins for various FaaS providers and allows to extend it when needed.

The Serverless Framework allows you to provision and deploy REST APIs, backend services, data pipe-lines, and other uses cases by providing a framework and CLI to build serverless services across many providers by abstracting away provider-level complexity.

The Serverless Framework is different than other application frameworks because:
- It manages your code as well as your infrastructure
- It supports multiple languages (Node.js, Python, Java, and more)

    Serverless framework allows choice of FaaS providers across a single project


**Core concepts of Serverless Framework**
Serverless Framework consists of the following core concepts:

- Service
- Function
- Events
- Resources 
- Plugins

**Service**
A Service in the Serverless Framework is the unit of organization. It's where you define your Functions, the Events that trigger them, and the Resources your Functions use, all in one file titled *serverless.yml*. More information at: https://goo.gl/9SKBvx

An application can have multiple services and hence multiple *serverless.yml* files.

![enter image description here](https://github.com/skarlekar/faces/blob/master/images/service-yml.png)

**Functions**
A Function is an independent unit of deployment or microservice. It manifests itself as a Lambda or Azure Function depending upon the provider.  It's merely code, deployed in the cloud, that is most often written to perform a single job such as:

- Saving a user to the database
- Processing a file in a database
- Performing a scheduled task

![enter image description here](https://github.com/skarlekar/faces/blob/master/images/function-yml.png)

**Events**
Anything that triggers an Function to execute is regarded by the Framework as an Event. 
Events on AWS are:

- An AWS API Gateway HTTP endpoint request (e.g., for a REST API)
- An AWS S3 bucket upload (e.g., for an image)
- A CloudWatch timer (e.g., run every 5 minutes)
- An AWS SNS topic (e.g., a message)
- A CloudWatch Alert (e.g., something happened)

When you define an event for your functions in the Serverless Framework, the Framework will automatically create any infrastructure necessary for that event (e.g., an API Gateway endpoint) and configure your Functions to listen to it.

Simply put, events are the things that trigger your functions to run. If you are using AWS as your provider, all events in the service are anything in AWS that can trigger an AWS Lambda function, like an S3 bucket upload, an SNS topic, and HTTP endpoints created via API Gateway.

Upon deployment, the framework will deploy any infrastructure required for an event (e.g., an API Gateway endpoint) and configure your function to listen to it.

![enter image description here](https://github.com/skarlekar/faces/blob/master/images/event-yml.png)

**Resources**
Resources are infrastructure components which your Functions uses. 
If you use AWS as you provider, then resources are:

 - An AWS DynamoDB Table (e.g., for saving Users/Posts/Comments data) 
 - An AWS S3 Bucket (e.g., for saving images or files) 
 - An AWS SNS Topic (e.g., for sending messages asynchronously)

Anything that can be defined in CloudFormation is supported by the Serverless Framework. The Serverless Framework not only deploys your Functions and the Events that trigger them, but it also deploys the infrastructure components your Functions depend upon.

![enter image description here](https://github.com/skarlekar/faces/blob/master/images/resource-yml.png)

**Credentials**
Serverless Framework needs access to your cloud provider account credentials to deploy resources on your behalf.  For AWS you can use AWS CLI (aws configure).  Azure is more involved. 

Following links provide excellent guidance on setting up the credentials for various providers currently supported on the Serverless Framework.

- AWS - https://serverless.com/framework/docs/providers/aws/guide/credentials/
- Azure -https://serverless.com/framework/docs/providers/azure/guide/credentials/
- Openwhisk - https://serverless.com/framework/docs/providers/openwhisk/guide/credentials/

**Deployment**
Serverless Framework translates the service declaration in the serverless.yml file into a Cloud Formation or Resource Manager template depending upon the provider you choose.

To deploy your service,  all the functions and provision the resources, enter:

    serverless deploy --verbose

To deploy a single function after making changes to it, enter:

    serverless deploy function --function <myfunction> --verbose

**Invoking**
Serverless Framework translates the service declaration in the serverless.yml file into a Cloud Formation or Resource Manager template depending upon the provider you choose.

To deploy your service,  all the functions and provision the resources, enter:

    serverless deploy --verbose

To deploy a single function after making changes to it, enter:

    serverless deploy function --function <myfunction> --verbose

CelebritySleuth - A Sample Usecase
---------------

CelebritySleuth is a celebrity face recognition service built using Serverless Framework, Twilio, Amazon Rekognition and IMDbPy API.

The CelebritySleuth application is an event-driven application taking advantage of:
The user's mobile SMS/MMS for the presentation tier, 
Twilio in the middle-tier to bridge the SMS world and 
AWS Gateway and a set of AWS Lambda functions written in Python making use of AWS Rekogniton for image processing and IMDB for gathering information on the celebrities.

CelebritySleuth code repository, installation guide and usage at:
https://github.com/skarlekar/faces

**How it works**
To begin with you have to train the application to recognize the faces by building a collection of celebrities. You do this by sending a random sample of celebrity pictures (image URLs) and their corresponding names. The more pictures of a celebrity, the more accurate the recognition will be.
The CelebritySleuth application consists of two services:

 - Twilio Communication Service 
 - Face Recognition Service

The services are decoupled to allow for using different presentation tiers in future.

**Architecture**
![enter image description here](https://github.com/skarlekar/faces/blob/master/CelebritySleuthArchitecture.png)

