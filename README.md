## Background
### OpenAPI and Swagger
Swagger is an implementation of OpenAPI. Swagger contains a tool that helps developers design, build, document, and consume RESTful Web services. Applications implemented based on OpenAPI interface files can automatically generate documentation of methods, parameters and models. This helps keep the documentation, client libraries, and source code in sync.

### European Open Science Cloud (EOSC)
The European Open Science Cloud (EOSC) brings together multiple service providers to create a single contact point for researchers and innovators to discover, access, and use Cloud resources. EOSC providers use OpenStack which is an open standard cloud computing platform, mostly deployed as infrastructure-as-a-service (IaaS) in both public and private clouds.


### GitHub
GitHub is a web-based hosting service for version control using Git. Version control helps keep track of changes in a project and allows for collaboration between many developers.

### Docker
Docker performs operating-system-level virtualization, also known as "containerization". Docker uses the resource isolation features of the Linux kernel to allow independent "containers" to run within a Linux instance.

## Preparation
### Setup github
If you don’t have an account already follow these instructions: https://github.com/join. To be able to commit code from your machine to the repository you’ll need to install Git. Follow these instructions to install on your machine: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### Setup Docker Hub
If you don’t have an account already follow these instructions: https://hub.docker.com/signup. 


## Usage of OpenStack on EOSC
1. Open the EOSCs providers OpenStack dashboard on this URL: https://stack-server.ct.infn.it/dashboard/project/
2. You will need to log in with via EGI SSO
3. On the dashboard go to instances and select "Launch Instance"
4. Fill in the required fields. Note depending on the provider there may be small variations. Important! create and save the generated key
5. Change the permissions to the downloaded key 
6. ssh into the newly created VM: ‘ssh ubuntu@<IP> -i’
7. Try a sudo command e.g. sudo apt update. Notice you do not need a password to run commands using sudo
