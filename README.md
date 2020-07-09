## Background
### OpenAPI and Swagger
Swagger is an implementation of OpenAPI. Swagger contains a tool that helps 
developers design, build, document, and consume RESTful Web services. 
Applications implemented based on OpenAPI interface files can automatically 
generate documentation of methods, parameters and models. This helps keep the 
documentation, client libraries, and source code in sync.

### European Open Science Cloud (EOSC)
The European Open Science Cloud (EOSC) brings together multiple service 
providers to create a single contact point for researchers and innovators to 
discover, access, and use Cloud resources. EOSC providers use OpenStack which 
is an open standard cloud computing platform, mostly deployed as 
infrastructure-as-a-service (IaaS) in both public and private clouds.


### GitHub
GitHub is a web-based hosting service for version control using Git. Version 
control helps keep track of changes in a project and allows for collaboration 
between many developers.

### Docker
Docker performs operating-system-level virtualization, also known as 
"containerization". Docker uses the resource isolation features of the Linux 
kernel to allow independent "containers" to run within a Linux instance.


### Python Virtualenv
Virtualenv is a tool to create isolated Python environments. The basic problem 
being addressed is one of dependencies and versions. Virtualenv creates an 
environment that has its own installation directories, that doesn't share 
libraries with other virtualenv environments.


## Preparation
### Setup github
If you don’t have an account already follow these instructions: https://github.com/join. To be able to commit code from your machine to the repository you’ll need to install Git. Follow these instructions to install on your machine: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### Setup Docker Hub
If you don’t have an account already follow these instructions: 
https://hub.docker.com/signup.

### Install Docker
You may follow these instructions depending your OS:
https://docs.docker.com/get-docker/
 

### Install Python3 and Virtualenv
You may follow these instructions depending your OS: 
https://www.python.org/downloads/.
To install virtualenv you can type :
```Bash
pip3 install virtualenv
```

## Usage of OpenStack on EOSC
* Open the EOSCs providers OpenStack dashboard on this URL: https://stack-server.ct.infn.it/dashboard/project/
* You will need to log in with via EGI SSO
* On the dashboard go to instances and select "Launch Instance"
* Fill in the required fields. Note depending on the provider there may be small variations. Important! create and save the generated key
*  Change the permissions to the downloaded key: 
```Bash
chmod 400 demo.pem
```
* ssh into the newly created VM:
```Bash
ssh ubuntu@<IP> -i demo.pem
``` 

* Try a sudo command: 
```Bash
sudo apt update
```
Notice you do not need a password to run commands using sudo

## Develop RESTful Web Service
To get an understanding of Swagger and OpenAPI, you may follow this tutorial up 
to part 5: 
https://apihandyman.io/writing-openapi-swagger-specification-tutorial-part-1-introduction/.

Got to https://github.com/skoulouzis/DevOpsTutorial.git and fork the project 
to your own github repository. You can find instuctions on how to do this here: 
https://docs.github.com/en/github/getting-started-with-github/fork-a-repo

Go to your terminal and check out the sample RESTful Web Service code at:
```Bash
git clone https://github.com/<YOUR-GITHUB>/DevOpsTutorial.git
```
Got to DevOpsTutorial folder and check out the 'summer_school' branch:
```Bash
cd DevOpsTutorial/
git checkout summer_school
``` 
Confirm that you are at the 'summer_school' branch. Type:
```Bash
git branch
```
You should see:
```Bash
  master
* summer_school
```

Go to api_server folder and start Virtualenv:
```Bash
cd api_server
python3 -m venv venv
source venv/bin/activate
```

Now you can follow the instructions at 
[api_server/README.md](api_server/README.md)


## Publish RESTful Web Service on Dockerhub
You will need to connect your Github account with your Dockerhub account. To 
do this follow these infatuations: https://docs.docker.com/docker-hub/builds/link-source/  


To publish your RESTful Web Service on Dockerhub: 
* Got to your own Dockerhub at https://hub.docker.com/
* Create a new repository and name it 'my-temp-service'. Make sure your 
repository is public.
* On the section 'Build Settings (optional)' select the Github icon
* On 'Select Organization' add your connected github account name
* Select the 'DevOpsTutorial' repository
* Select 'BUILD RULES' on the 'Source' replace 'master' with 'summer_school'
* In 'Build Context' add '/api_server'
* Finally select 'Create and Build'

  

