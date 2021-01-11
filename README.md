


# Tutorial: RESTful service, Docker and Kubernetes(K8s)

Speaker: dr. [Zhiming Zhao](mailto: z.zhao@uva.nl), Support: dr. [Spiros Koulouzis](mailto: S.Koulouzis@uva.nl), 

University of Amsterdam, Amsterdam, NL

LifeWatch ERIC, vLab & Innovation Center, Amsterdam, NL

The tutorial is part of the webinar [“an introduction to Cloud computing](https://www.lifewatch.eu/web/guest/towards-envri-winter-school-programme-and-speakers)”, in [the ENVRI community winter school 2020](https://www.lifewatch.eu/all-news/-/asset_publisher/BU9HdfPGXPaK/content/towards-the-envri-community-winter-school/10194). In this tutorial, you will learn how to define a simple REST service using OpenAPI. You will also learn how to use Ansible and Kubernetes, a.k.a K8s to deploy the RESTful Web Service on a VM in Cloud environments. 

We sincerely thank mr. Giuseppe Larocca and mr. Andrea Manzi from EGI to provide the testbed via the EGI training platform. The tutorial is supported by the [EOSC early adopter program](https://confluence.egi.eu/display/EOSC/EOSC+DevOps+framework+and+virtual+infrastructure+for+ENVRI-FAIR+common+FAIR+data+services?show-miniview) via [ENVRI-FAIR](http://www.envri-fair.eu/) project, and [LifeWatch-ERIC](https://www.lifewatch.eu/). The testbed will be accessible after the webinar for 10 days; during those days we will also provide support for all technical questions.  



##Before you Begin


### Install Ansible on a local machine (laptop)

You will need Ansible for the assignment. Please install it on your local computer based on the following instructions:[ https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)


### Request a VM for experiment

Fill in the form at [https://forms.gle/Qo8y1Gsiaqo5D2pu9](https://forms.gle/Qo8y1Gsiaqo5D2pu9) to request a VM. All information will only be used in the scope of the webinar. All information will be destroyed after the completion of the webinar


### Configure the VM

Please follow the link to request a virtual machine for your experiment.

You will access a VM via ssh.

Log in to your assigned VM using the keys you have received:


```
ssh ubuntu@VM_IP -i id_ssh_rsa
```


Try a sudo command:


```
sudo apt update
```


Notice you do not need a password to run commands using sudo



## Install Kubernetes



If you haven't already install docker on your VM install it using these 
instructions:[ https://linoxide.com/containers/install-docker-ubuntu-20-04/](https://linoxide.com/containers/install-docker-ubuntu-20-04/)

Next, install Kubernetes (K8s) on your VM. Download and add the key for K8s:


```
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
```


Add the kubernetes repository and update:


```
sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
sudo apt-get update
```


Disable swap:


```
sudo swapoff -a
```


Install Kubernetes:


```
sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```


Initialize the master node K8s:


```
sudo kubeadm init --ignore-preflight-errors=NumCPU
```


Create the configuration folder


```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


Enable the bridge-nf-call tables


```
sudo sysctl net.bridge.bridge-nf-call-iptables=1
```


Create the Weave Net addon: Weave Net creates a virtual network that connects Docker containers across multiple hosts 
and enables their automatic discovery.


```
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```


Since we have a one node cluster we want the master to also run containers. To do that type:


```
kubectl taint nodes --all node-role.kubernetes.io/master- 
```


Check your cluster. On the master node type:


```
kubectl get nodes
```


You should see something like this:


```
NAME      STATUS   ROLES    AGE     VERSION
envri15   Ready    master   3m14s   v1.18.5
```



### Test K8s Cluster

This is a basic Kubernetes deployment of Nginx. On the master node create an Nginx deployment:


```
kubectl create deployment nginx --image=nginx
```


You may check your Nginx deployment by typing:


```
kubectl get all
```


The output should look like this:


```
NAME                        READY   STATUS              RESTARTS   AGE
pod/nginx-f89759699-5cqgg   0/1     ContainerCreating   0          6s
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   4m37s
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   0/1     1            0           6s
NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-f89759699   1         1         0       6
```


You will notice in the first line 'ContainerCreating'. This means that the K8s cluster is downloading and starting the 
Nginx container. After some minutes if you run again:

```bash
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


At this point Nginx is running on the K8s cluster, however it is only accessible from within the cluster. To expose 
Nginx to the outside world we should type:


```
kubectl create service nodeport nginx --tcp=80:80
```


To check your Nginx deployment type:


```
kubectl get all
```


You should see the among others the line:


```
service/nginx        NodePort    10.106.12.71   <none>        80:31122/TCP   8s
```


This means that port 80 is mapped on port 31122 of each node in the K8s cluster. Note that the mapped port will be 
different on your deployment. Now we can access Nginx from http://&lt;VM_PUBLIC_IP>:NODE_PORT.



## Deploy RESTful Web Service on K8s Cluster

To deploy a RESTful Web Service on the K8s Cluster check out the git repository at 

go to your VM in the K8s folder. In that folder there should be 
four files:

```
.
├── my-temp-deployment.yaml
└── my-temp-service.yaml
0 directories, 4 files
```


my-temp-deployment.yaml and my-temp-service.yaml are used for deploying the RESTful Web Service developed on the previous step.

To create all the deployments and services type in the K8s folder:


```
kubectl create -f .
```


This should create the MongoDB and my-temp-service deployments and services. To see what is running on the cluster type:


```
kubectl get all
```


You should see something like this:


```
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


Note that in this output 'service/my-temp-service' is mapped to 31400 node port. In your case it may be a different number. Now your service should be aveline on http://&lt;VM_PUBLIC_IP>:&lt;NODE_PORT>/my-temp-service/0.0.1/ui/

To delete all deployed resources simply type on the master K8s node:


```
kubectl delete -f ./K8s
```



### Questions



*   How does the RESTful Web Service communicate with the MongoDB if that MongoDB is not accessible externally
*   Currently, the RESTful Web Service runs over plain http meaning that the communication between any client and the RESTful Web Service is unsecured. How would you enable SSL encryption, meaning that the RESTful Web Service will run from https without modifying the service's source code?
*   If the VMs running the K8s cluster fails, how would you make sure all the data saved in the DB are saved?
4. Appendix: technologies Short Background


### OpenAPI and Swagger

Swagger is an implementation of OpenAPI. Swagger contains a tool that helps developers design, build, document, and consume RESTful Web services. Applications implemented based on OpenAPI interface, files can automatically generate documentation of methods, parameters and models. This helps keep the documentation, client libraries, and source code in sync.


### GitHub

GitHub is a web-based hosting service for version control using Git. Version control helps keep track of changes in a project and allows for collaboration between many developers.


### Docker

Docker performs operating-system-level virtualization, also known as "containerization". Docker uses the resource isolation features of the Linux kernel to allow independent "containers" to run within a Linux instance.


### kubernetes

Kubernetes is an open-source container-orchestration system for automating computer application deployment, scaling, and management.


### Python Virtualenv

Virtualenv is a tool to create isolated Python environments. The basic problem being addressed is one of dependencies and versions. Virtualenv creates an environment that has its own installation directories, that doesn't share libraries with other virtualenv environments.
