# DevOpsTutorial
Define a simple REST API with OpenAPI and Swagger, develop the application logic and dockerize it


## Use IaaS (EOSC) 
The European Open Science Cloud (EOSC) brings together multiple service providers to create a single contact point for researchers and innovators to discover, access, and use Cloud resources. EOSC providers use OpenStack which is an open standard cloud computing platform, mostly deployed as infrastructure-as-a-service (IaaS) in both public and private clouds. 


### Usage of OpenStack on EOSC
Open the EOSCs providers  OpenStack dashboard on this URL: https://fedcloud-osservices.egi.cesga.es/project/

1. You will need to log in with via EGI SSO	
2. On the dashboard go to instances and select "Launch Instance"
3. Fill in the requiered fialds. Note depanding on the provider there may be small variations. Important! create and save the generated key
4. Change the permitions to the downloaded key 
5. ssh into the newly vreated VM 
6. Try a sudo command e.g. sudo apt update. Notice you do not need a pasword to run commands using sudo 
