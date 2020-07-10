## Background
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

### Install Ansible 
You may follow these instructions depending your OS: 
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

<!--
## Usage of OpenStack on EOSC
Open the EOSCs providers OpenStack dashboard on this URL: https://stack-server.ct.infn.it/dashboard/project/. 
You will need to log in with via EGI SSO. 
-->
On the dashboard go to instances and select "Launch Instance" and fill in the required fields. 
<!--
Note depending on the provider there may be small variations. 
Important! create and save the generated key
Change the permissions to the downloaded key: 
```Bash
chmod 400 demo.pem
```
ssh into the newly created VM:
```Bash
ssh ubuntu@<IP> -i demo.pem
``` 
Try a sudo command: 
```Bash
sudo apt update
```
Notice you do not need a password to run commands using sudo
-->

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
Got to your own Dockerhub at https://hub.docker.com/
1. Create a new repository and name it 'my-temp-service'. Make sure your 
repository is public.
2. On the section 'Build Settings (optional)' select the Github icon
3. On 'Select Organization' add your connected github account name
4. Select the 'DevOpsTutorial' repository
5. Select 'BUILD RULES' on the 'Source' replace 'master' with 'summer_school'
6. In 'Build Context' add '/api_server'
7. Finally select 'Create and Build'

  
## Deploy RESTful Web Service on a VM
### Ansible 
Start 1 VM with Ubuntu 18.04, 1 VCPUS 2 GB RAM and 20 GB disk
. Make sure that the VM has port 8082 open in the appropriate security 
group 

Got to DevOpsTutorial/playbooks folder 

Edit the inventory_my-temp-service.yaml file and replace the line 
'VM_IP' with the actual public IP of your newly created VM  

Run the deploy-my-temp-service.yaml playbook by typing: 
```Bash
ansible-playbook -i inventory_my-temp-service.yaml --key-file PATH_TO_VM_PRIVATE_KEY deploy-my-temp-service.yaml
```

Got to http://<VM_PUBLIC_IP>:8082/my-temp-service/0.0.1/ui/ and test your service. 
If everthing is working properly you may terminate the VM

### Install Kubernetes 

Start 2 VMs with Ubuntu 18.04, 1 VCPUS 2 GB RAM and 20 GB disk

On both VMs install Docker using these instructions: 
https://linoxide.com/containers/install-docker-ubuntu-20-04/

On both VMs install Kubernetes (K8s). Download and add the key for K8s: 
```Bash
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add 
```
Install Kubernetes:
```Bash
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```

Choose on VM to be the master node. On the master node initialize K8s:
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

Since we have a small cluster (2 VMs) we want the master to also tun 
containers. To do that type:
```Bash
kubectl taint nodes --all node-role.kubernetes.io/master-  
```    

To be able to add workers to the cluster we need to get some keys. To
do that type:
```Bash
sudo kubeadm token create --print-join-command
```   
Join the worker VM on the K8s cluster. On the VM chosen as worker type:
```Bash
sudo swapoff -a
```   
Copy the output of 'sudo kubeadm token create --print-join-command' from the master to 
the worker. It should look like this:

```Bash
sudo kubeadm join 212.189.145.45:6443 --token ijg5iy.kso5ifgarxge9884     --discovery-token-ca-cert-hash sha256:081c4d0c2c56d19672ebb527e70fe58d3e2914108e907b226383649d183a155'
```  

Check your cluster. On the master node type:
```Bash
kubectl get nodes
```
You should see something like this:
```Bash
NAME   STATUS   ROLES    AGE     VERSION
vm1    Ready    master   32m     v1.18.5
vm2    Ready    <none>   2m23s   v1.18.5
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
NAME                        READY   STATUS    RESTARTS   AGE
pod/nginx-f89759699-blzk7   1/1     Running   0          50s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   146m

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   1/1     1            1           50s

NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-f89759699   1         1         1       50s
```


At this point Nginx is running on the K8s cluster, however it is only accessible from
within the cluster. To expose Nginx to the outside world we should type:
 ```Bash
kubectl create service nodeport nginx --tcp=443:443
```
To check your Nginx deployment type:
 ```Bash
kubectl get all
```
You should see the among others the line: 
 ```Bash
service/nginx        NodePort    10.104.65.224   <none>        443:30115/TCP   5m48s
```
This means that port 443 is mapped on port 30115 of each node in the K8s cluster. 
Now we can access Nginx from  https://<VM_PUBLIC_IP>
