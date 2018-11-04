# qlikdemo
A Simple Application that exposes REST API with the below mentioned 4 operations. The API is restricted to use in-memory message store and handles request data only in *application/x-www-form-urlencoded* and *application/json* formats.

The responses from the api is *application/json* and has following fields to provide information about the operations.

*status - Http status of the request made

action - The name of the API function

error - error encountered during the api execution(if any)

info - status of the operation and miscellanious information

response - The message contents(if no errors)*

#### 1. Allows user to post new message
Users can submit new messages to the api URL **/api/message** using HTTP POST method. It accepts all sort of messages from integer and string but not a blank message. The API will label each of the messages with a 10 digit unique ID(derived from a function of time) to avoid duplication. It returns with a unique ID in case the message post succeeds.

#### 2. List All Received Messages
Users can see the all the received messages in the store by sending an HTTP GET request to the api URL **/api/message**. It ignores any request data.

#### 3. Retrieve Specific message and check for palindrome
Users can retrieve specific message from the store by sending a GET request to the api **/api/message/*messageID***, where messageID is the unique ID allotted to the message while adding it to the store. The result of the palindrome is shown along with the *info* field of the response. A *404* message is excepted when the request message ID is not in the store.

#### 4. Delete Specific message
Users can delete a specific message ffrom the store by sending a POST request to the api **api/message/*messageID***, where messageID is the unique ID of the message to be deleted. A *404* message is excepted when the request message ID is not in the store.

### Technical Information
The API is written in python using the flask framework for the web services. The application is currently hosted to a private cloud infrastructure on Openstack. The API is now live on http://qlik.scribblings.in:5000 , A Sample output is given below:

    $ curl http://qlik.scribblings.in:5000/api/message
    {"action":"List All Messages","error":null,"info":"Success","response":[{"id":1111111111,"message":"Welcome to Qlik message store"},{"id":1541368272,"message":"This is a test message"}],"status":200}
    $ curl http://qlik.scribblings.in:5000/api/message/1541368272
    {"action":"List Specific Message","error":null,"info":"Success::Palindrome Check - Failed","response":{"id":1541368272,"message":"This is a test message"},"status":200}

### Deployment
The application stack has been built with two component services *api* and a basic *gui*(in pure html). These services are also configured to run on docker platform. The build process of the application would require git and docker containerization platform preferred on Ubuntu Linux. The installation steps are in the following [documentation](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1)

After installation and verification of the docker platform, the build can be done via the below steps:

    #clone the repository using git tool
    cd /usr/local/src
    git clone https://github.com/jpadmin/qlikdemo.git
    
    #change to the directory "qlikdemo/api" and build the api component
    cd qlikdemo/api
    docker build -t qlikapi .
    
    #run the container on host port 5000
    docker run -d -p 5000:80 qlikapi
    
    #change to the directory "qlikdemo/gui" and build the api component
    cd qlikdemo/gui
    docker build -t qlikgui .
    
    #run the container on host port 8080
    docker run -d -p 8080:80 qlikgui
 
 ### Scope of Improvements
