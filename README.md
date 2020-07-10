In this tutorial you will see how a simple REST API is defined with OpenAPI. 
You will use and deploy a RESTful Web Service that makes use of a DB to store and 
retire values. Finally you use two alternatives (Ansible and Kubernetes, a.k.a K8s) to 
deploy the RESTful Web Service on a VM 



## Before you Begin 
This tutorial uses several tools and resources that you will need. 
 
### Setup github
If you don’t have an account already follow these instructions: https://github.com/join. To be able to commit code from your machine to the repository you’ll need to install Git. Follow these instructions to install on your machine: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### Setup Docker Hub
If you don’t have an account already follow these instructions: 
https://hub.docker.com/signup.


### Install Ansible 
You may follow these instructions depending your OS: 
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html


<!--
### Install Docker
You may follow these instructions depending your OS:
https://docs.docker.com/get-docker/
 -->

<!--
### Install Python3 and Virtualenv
You may follow these instructions depending your OS: 
https://www.python.org/downloads/.
To install virtualenv you can type :
```Bash
pip3 install virtualenv
```
 -->

## Tutorial 0: Testbed configuration
In this section you will access a VM via ssh.

Log in to your assigned VM using the keys you have received:
```Bash
ssh ubuntu@VM_IP -i key<N>.pem
```
Try a sudo command: 
```Bash
sudo apt update
```
Notice you do not need a password to run commands using sudo

## Tutorial 1: RESTful Web Service

In this section you will experiment with a simple RESTful Web Service and run it on
 your VM.
 
This RESTful Web Service implements two methods: POST and GET. 
The POST method is used to add and store a temperature value. When the valus is send via 
POST the service creates a timestamp and saves it in MongoDB. 

The GET method is used to retrive the maximum value stored in the MongoDB.

Log in to your assigned VM and clone the github project: 
```Bash
git clone https://github.com/skoulouzis/DevOpsTutorial.git
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

Install Virtualenv:
```Bash
sudo apt install -y python3-venv
```

Go to api_server folder and start Virtualenv:
```Bash
cd api_server
python3 -m venv venv
source venv/bin/activate
```

To run the server, please execute the following from the api_server directory:

```
pip3 install -r requirements.txt
python3 -m openapi_server
```

and open your browser to here:

```
http://VM_IP:8082/my-temp-service/0.0.1/ui/
```

Use the Web UI to add and receive the maximum value. Notice that you wait for some 
time and receive an error. This is because we do not have MongoDB installed yet. 


We will run a MongoDB from a Docker container. To do that install docker using these 
instructions: https://linoxide.com/containers/install-docker-ubuntu-20-04/

Open a new terminal to your VM and type:
```
sudo docker run -it -p 27017:27017 mongo
```
As soon as docker downloads and starts the container try the Web UI at 
http://VM_IP:8082/my-temp-service/0.0.1/ui/ again.

Both terminals shut down the web service and MongoDB docker by typing 'Ctrl+c'

### Questions 

* How can you deploy your RESTful Web Service together with its depending DB on a 
bare metal or virtual cluster ?
* What will happen if a web service and/or DB are already running on ports 8082 and 
27017?  


## Tutorial 2: Deploy the RESTful Web Service with Ansible 

In this section we will automate the deployment of the web service and DB using 
Ansible.

Make sure that the web service and docker MongoDB are not running on your VM and that 
you have installed Ansible on your laptop. 
Download the all files contained in 
https://github.com/skoulouzis/DevOpsTutorial/tree/summer_school/playbooks on your 

Edit the inventory_my-temp-service.yaml file and replace the line 
'VM_IP' with the actual public IP of your  VM  

Run the deploy-my-temp-service.yaml playbook by typing: 
```Bash
ansible-playbook -i inventory_my-temp-service.yaml --key-file PATH_TO_VM_PRIVATE_KEY deploy-my-temp-service.yaml
```

Got to http://<VM_PUBLIC_IP>:8082/my-temp-service/0.0.1/ui/ and test your service. 
If everything is working properly make sure you terminate the service and remove 
MongoDB. To do this type:
```
sudo killall screen
sudo apt remove -y mongodb
```

### Questions 
* Assuming you need to add a new feature to the RESTful Web Service.
 How would you deploy the new version with the minimum possible downtime ?   


<!--
## Tutorial 3: Publish RESTful Web Service on Dockerhub
You will need to connect your Github account with your Dockerhub account. To 
do this follow these infatuations: https://docs.docker.com/docker-hub/builds/link-source/  
To publish your RESTful Web Service on Dockerhub: 
Got to your own Dockerhub at https://hub.docker.com/
1. Create a new repository and name it 'my-temp-service'. Make sure your 
repository is public.
2. On the section 'Build Settings (optional)' select the Github icon
3. On 'Select Organization' add your connected github account name
4. Select the 'DevOpsTutorial' repository
5. Select 'BUILD RULES' on the 'Source' replace 'master' with 'summer_school'
6. In 'Build Context' add '/api_server'
7. Finally select 'Create and Build'
-->
  




### Tutorial 3: Install Kubernetes and Deploy the RESTful Web Service 


Make sure you have terminated the service and removed MongoDB. To do this type:
```
sudo killall screen
sudo apt remove -y mongodb
```

If you haven't already install docker on your VM install it using these instructions: 
https://linoxide.com/containers/install-docker-ubuntu-20-04/

Next, install Kubernetes (K8s) on your VM. Download and add the key for K8s: 
```Bash
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add 
```
Add the kubernetes repository and update:
```Bash
sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
sudo apt-get update
```

Disable swap:
```
sudo swapoff -a
```


Install Kubernetes:
```Bash
sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```

Initialize the master node K8s:
 ```Bash
sudo kubeadm init --ignore-preflight-errors=NumCPU
```

Create the configuration folder 
 ```Bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Enable the bridge-nf-call tables
 ```Bash
sudo sysctl net.bridge.bridge-nf-call-iptables=1
```

Create the Weave Net addon: Weave Net creates a virtual network that 
connects Docker containers across multiple hosts and enables their 
automatic discovery. 
```Bash
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```     

Since we have a one node cluster we want the master to also run containers. 
To do that type:
```Bash
kubectl taint nodes --all node-role.kubernetes.io/master-  
```    

Check your cluster. On the master node type:
```Bash
kubectl get nodes
```

You should see something like this:
```Bash
NAME      STATUS   ROLES    AGE     VERSION
envri15   Ready    master   3m14s   v1.18.5
```


### Test K8s Cluster 
This is a basic Kubernetes deployment of Nginx. On the master node create an Nginx 
deployment:
```Bash
kubectl create deployment nginx --image=nginx
```
You may check your Nginx deployment by typing:
 ```Bash
kubectl get all
```

The output should look like this:
 ```Bash
NAME                        READY   STATUS              RESTARTS   AGE
pod/nginx-f89759699-5cqgg   0/1     ContainerCreating   0          6s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   4m37s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   0/1     1            0           6s

NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-f89759699   1         1         0       6
```

You will notice in the first line 'ContainerCreating'. This means that the K8s cluster
is downloading and staring the Nginx container. After some minutes if you run again:
 ```Bash
kubectl get all
```

The output should look like this:
```
NAME                        READY   STATUS    RESTARTS   AGE
pod/nginx-f89759699-5cqgg   1/1     Running   0          2m1s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   6m32s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   1/1     1            1           2m1s

NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-f89759699   1         1         1       2m1s
```
 

At this point Nginx is running on the K8s cluster, however it is only accessible from
within the cluster. To expose Nginx to the outside world we should type:
 ```Bash
kubectl create service nodeport nginx --tcp=80:80
```
To check your Nginx deployment type:
 ```Bash
kubectl get all
```
You should see the among others the line: 
 ```Bash
service/nginx        NodePort    10.106.12.71   <none>        80:31122/TCP   8s
```
This means that port 80 is mapped on port 31122 of each node in the K8s cluster. 
Note that the mapped port will be different on your deployment. Now we can access 
Nginx from http://<VM_PUBLIC_IP>:NODE_PORT. 


### Deploy RESTful Web Service on K8s Cluster

To deploy your RESTful Web Service on the K8s Cluster go to you VM in the K8s folder. 
In that folder there should be four files:
```Bash
.
├── mongo-deployment.yaml
├── mongo-service.yaml
├── my-temp-deployment.yaml
└── my-temp-service.yaml

0 directories, 4 files
``` 
mongo-deployment.yaml and mongo-service.yaml are used for deploying the MongoDB on the K8s cluster.
my-temp-deployment.yaml and my-temp-service.yaml are used for deploying the RESTful Web
 Service developed on the previous step. 

To create all the deployments and services type in the K8s folder:
```Bash
kubectl create -f .
``` 

This should create the MongoDB and my-temp-service deployments and services. To see 
what is running on the cluster type:
```Bash
kubectl get all
``` 

You should see something like this:
```Bash
NAME                                   READY   STATUS              RESTARTS   AGE
pod/mongo-6d76c566f7-kcjg2             0/1     ContainerCreating   0          7s
pod/my-temp-service-68dccc74f8-7pm8n   0/1     ContainerCreating   0          7s
pod/nginx-f89759699-5cqgg              1/1     Running             0          7m28s

NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          11m
service/mongo             ClusterIP   10.106.24.187    <none>        27017/TCP        7s
service/my-temp-service   NodePort    10.103.250.155   <none>        8082:31400/TCP   6s
service/nginx             NodePort    10.106.12.71     <none>        80:31122/TCP     5m1s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mongo             0/1     1            0           8s
deployment.apps/my-temp-service   0/1     1            0           7s
deployment.apps/nginx             1/1     1            1           7m28s

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/mongo-6d76c566f7             1         1         0       8s
replicaset.apps/my-temp-service-68dccc74f8   1         1         0       7s
replicaset.apps/nginx-f89759699              1         1         1       7m28s
```
Note that in this output 'service/my-temp-service' is mapped to 31400 node port. In 
your case it may be a different number. Now your service should be aveline on 
http://<VM_PUBLIC_IP>:<NODE_PORT>/my-temp-service/0.0.1/ui/

To delete all deployed resources simply type on the master K8s node:
```Bash
kubectl delete -f ./K8s
```


### Questions 
* How dose the RESTful Web Service communicate with the MongoDB if that MongoDB 
is not acceptable externally 
* Currently the RESTful Web Service runs over plain http meaning that the communication
between any client and the RESTful Web Service are unsecured. How would you enable
ssl encryption, meaning that the RESTful Web Service will run from https without 
modifying the service's source code ? 
 


# Appendix 
## Technologies Short Background
### OpenAPI and Swagger
Swagger is an implementation of OpenAPI. Swagger contains a tool that helps 
developers design, build, document, and consume RESTful Web services. 
Applications implemented based on OpenAPI interface files can automatically 
generate documentation of methods, parameters and models. This helps keep the 
documentation, client libraries, and source code in sync.

<!--
### European Open Science Cloud (EOSC)
The European Open Science Cloud (EOSC) brings together multiple service 
providers to create a single contact point for researchers and innovators to 
discover, access, and use Cloud resources. EOSC providers use OpenStack which 
is an open standard cloud computing platform, mostly deployed as 
infrastructure-as-a-service (IaaS) in both public and private clouds.
-->

### GitHub
GitHub is a web-based hosting service for version control using Git. Version 
control helps keep track of changes in a project and allows for collaboration 
between many developers.

### Docker
Docker performs operating-system-level virtualization, also known as 
"containerization". Docker uses the resource isolation features of the Linux 
kernel to allow independent "containers" to run within a Linux instance.

### kubernetes
Kubernetes is an open-source container-orchestration system for 
automating computer application deployment, scaling, and management. 


### Python Virtualenv
Virtualenv is a tool to create isolated Python environments. The basic problem 
being addressed is one of dependencies and versions. Virtualenv creates an 
environment that has its own installation directories, that doesn't share 
libraries with other virtualenv environments.