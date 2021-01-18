


# Tutorial: RESTful service, Docker and Kubernetes(K8s)

Speaker: dr. [Zhiming Zhao](mailto: z.zhao@uva.nl), Support: dr. [Spiros Koulouzis](mailto: S.Koulouzis@uva.nl), 

University of Amsterdam, Amsterdam, NL

LifeWatch ERIC, vLab & Innovation Center, Amsterdam, NL

The tutorial is part of the webinar [“an introduction to Cloud computing](https://www.lifewatch.eu/web/guest/towards-envri-winter-school-programme-and-speakers)”, in [the ENVRI community winter school 2020](https://www.lifewatch.eu/all-news/-/asset_publisher/BU9HdfPGXPaK/content/towards-the-envri-community-winter-school/10194). In this tutorial, you will learn how to define a simple REST service using OpenAPI. You will also learn how to use Ansible and Kubernetes, a.k.a K8s to deploy the RESTful Web Service on a VM in Cloud environments. 

We sincerely thank mr. Giuseppe Larocca and mr. Andrea Manzi from EGI to provide the testbed via the EGI training platform. The tutorial is supported by the [EOSC early adopter program](https://confluence.egi.eu/display/EOSC/EOSC+DevOps+framework+and+virtual+infrastructure+for+ENVRI-FAIR+common+FAIR+data+services?show-miniview) via [ENVRI-FAIR](http://www.envri-fair.eu/) project, and [LifeWatch-ERIC](https://www.lifewatch.eu/). The testbed will be accessible after the webinar for 10 days; during those days we will also provide support for all technical questions.  



## Before you Begin


### Install Ansible on a local machine (laptop)

You will need Ansible for the assignment. Please install it on your local computer based on the following instructions:[ https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)


### Request a VM for experiment

Fill in the form at [https://forms.gle/Qo8y1Gsiaqo5D2pu9](https://forms.gle/Qo8y1Gsiaqo5D2pu9) to request a VM. All information will only be used in the scope of the webinar. All information will be destroyed after the completion of the webinar


### Configure the VM

Please follow the link to request a virtual machine for your experiment.

You will access a VM via ssh.

Log in to your assigned VM using the keys you have received:


```
ssh USERNAME@VM_IP
```


Try a sudo command:


```
sudo apt update
```
Install git:
```
sudo apt install git
```

## Install microk8s

If you install microk8s you do not need to do the next step to install Kubernetes
```
sudo snap install microk8s --classic 
```
Check your cluster. On the master node type:


```
microk8s kubectl get nodes
```


## Install Kubernetes
If you installed microk8s you do not need execute this step to install Kubernetes
```

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

If you installed microk8s you'll need to include microk8s before every command 
This is a basic Kubernetes deployment of Nginx. On the master node create an Nginx deployment:


```
(microk8s) kubectl create deployment nginx --image=nginx
```


You may check your Nginx deployment by typing:


```
(microk8s) kubectl get all
```


The output should look like this:


```
NAME                         READY   STATUS              RESTARTS   AGE
pod/nginx-6799fc88d8-wttct   0/1     ContainerCreating   0          6s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   134d

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   0/1     1            0           7s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-6799fc88d8   1         1         0       7s
```


You will notice in the first line 'ContainerCreating'. This means that the K8s cluster is downloading and starting the 
Nginx container. After some minutes if you run again:

```bash
(microk8s) kubectl get all
```
The output should look like this:


```
NAME                         READY   STATUS    RESTARTS   AGE
pod/nginx-6799fc88d8-wttct   1/1     Running   0          39s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   134d

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   1/1     1            1           40s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-6799fc88d8   1         1         1       40s
```


At this point Nginx is running on the K8s cluster, however it is only accessible from within the cluster. To expose 
Nginx to the outside world we should type:


```
(microk8s) kubectl create service nodeport nginx --tcp=80:80
```


To check your Nginx deployment type:


```
(microk8s) kubectl get all
```


You should see the among others the line:


```
service/nginx        NodePort    10.98.203.181   <none>        80:30155/TCP   6s
```


This means that port 80 is mapped on port 30155 of each node in the K8s cluster. Note that the mapped port will be 
different on your deployment. Now we can access Nginx from http://&lt;VM_PUBLIC_IP>:NODE_PORT.

You may now delete the Nginx service by using:
```
(microk8s) kubectl delete service/nginx 
(microk8s) kubectl delete deployment.apps/nginx
```

## Deploy RESTful Web Service on K8s Cluster

To deploy a RESTful Web Service on the K8s Cluster clone the git repository:
```bash
git clone -b  winter-school-21 https://github.com/QCDIS/DevOpsTutorial.git
```
Go in to the K8s folder. In that folder there should be the following files:

```
.
├── my-temp-deployment.yaml
└── my-temp-service.yaml
0 directories, 4 files
```

my-temp-deployment.yaml and my-temp-service.yaml are used for deploying the RESTful Web Service created previously.

Open the 'my-temp-deployment.yaml' file and edit the following line:

```YAML
  image: REPOSITORY/DOCKER
```
Replace 'REPO' with your docker hub username and in the 'NAME' put the name of your FAIR-Cells service.
If for example your Docker username is 'cloudcells' and the service name is 'classifiers' the  'my-temp-deployment.yaml' 
should look like this:
```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    kompose.cmd: kompose convert
    kompose.version: 1.16.0 (0c01309)
  creationTimestamp: null
  labels:
    io.kompose.service:  fair-cell-service
  name:  fair-cell-service
spec:
  selector:
    matchLabels:
      io.kompose.service:  fair-cell-service
  replicas: 1
  strategy:
        type: RollingUpdate
        rollingUpdate:
            maxSurge: 50%
            maxUnavailable: 50%
  minReadySeconds: 10
  revisionHistoryLimit: 3
  template:
    metadata:
      creationTimestamp: null
      labels:
        io.kompose.service:  fair-cell-service
    spec:
      containers:
        image: cloudcells/classifiers
        name:  fair-cell-service
        imagePullPolicy: Always
        ports:
        - containerPort: 8082
        resources: {}
      restartPolicy: Always
status: {}
```

To create all the deployments and services type in the K8s folder:


```
(microk8s) kubectl create -f .
```


This should create the my-temp-service deployments and services. To see what is running on the cluster 
type:

```
(microk8s) kubectl get all
```


You should see something like this:


```
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/fair-cell-service   NodePort    10.102.118.62   <none>        8888:31783/TCP   78s
service/kubernetes          ClusterIP   10.96.0.1       <none>        443/TCP          133d

NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/fair-cell-service   0/1     1            0           11s

NAME                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/fair-cell-service-7f5bbfb44d   1         1         0       11s
```


Note that in this output 'service/my-temp-service' is mapped to 31783 node port. In your case it may be a different 
number. Now your service should be aveline on http://&lt;VM_PUBLIC_IP>:&lt;NODE_PORT>/

To delete all deployed resources simply type on the master K8s node:


```
(microk8s) kubectl delete -f ./K8s
```

Now we can benchmark the service. To do that, install apache2-utils:
```bash
sudo apt-get install apache2-utils
```
More information about the tool can be found here: https://www.tutorialspoint.com/apache_bench/index.htm 


Run the benchmark:
```
ab -n 5 -r -c 5 -g out.data -s 1000 http://&lt;VM_PUBLIC_IP>:NODE_PORT
```
The output will look like this:
```
Document Path:          /
Document Length:        0 bytes

Concurrency Level:      5
Time taken for tests:   347.545 seconds
Complete requests:      5
Failed requests:        0
Total transferred:      905 bytes
HTML transferred:       0 bytes
Requests per second:    0.01 [#/sec] (mean)
Time per request:       347545.008 [ms] (mean)
Time per request:       69509.002 [ms] (mean, across all concurrent requests)
Transfer rate:          0.00 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        3    3   0.1      3       3
Processing: 57942 204803 114178.1 242193  347542
Waiting:    57942 204802 114178.0 242192  347542
Total:      57945 204806 114178.1 242196  347545

Percentage of the requests served within a certain time (ms)
  50%  207447
  66%  276945
  75%  276945
  80%  347545
  90%  347545
  95%  347545
  98%  347545
  99%  347545
 100%  347545 (longest request)

```

## Enable Service Autoscaling

To be able to set the minimum and maximum utilization levels (for CPU, mem. etc.) that will trigger autoscaling you'll 
need to install the Kubernetes Metrics Server. To install go to folder 'metrics_server' and deploy the Metrics Server:

```bash
(microk8s) kubectl apply -f .
```

When the Metrics Server is installed on the master, test if metrics are gathered by typing:
```bash
kubectl top nodes
```
and
```bash
kubectl -n kube-system top pods
```
If you don't get any results you may wait for several minutes for the server to deploy.


Enable autoscaling with 10 % cpu utilization and max 10 pods:
```bash
(microk8s) kubectl autoscale deployment.apps/fair-cell-service --cpu-percent=10 --min=1 --max=10
```
Check that the horizontal pod autoscaler (hpa) is running:
```bash
(microk8s) kubectl describe hpa fair-cell-service
````

You should see something like this:
```bash
Name:                                                  fair-cell-service
Namespace:                                             default
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Mon, 11 Jan 2021 17:08:07 +0100
Reference:                                             Deployment/fair-cell-service
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  <unknown> / 70%
Min replicas:                                          1
Max replicas:                                          5
Deployment pods:                                       0 current / 0 desired
Events:                                                <none>
```

More details about limits and requests can be found here: 
https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/


Now the service should automatically scale (i.e. create more pods) as the cpu load increases. To be able to see the pods
increase open a new terminal and type:
```bash
watch kubectl get all
```

On a separate shell re-run the benchmark:
```bash
ab -n 5 -r -c 5 -g out.data -s 1000 http://&lt;VM_PUBLIC_IP>:NODE_PORT
```




### Questions
*   How much time did it take for the second benchmark ?  
*   If we set the '--cpu-percent' to 50 % what will be the impact on the number of pods, and the total execution time 
    of the benchmark and why? Note: If you run the benchmark again make sure to redeploy the service so that the pods 
    number is rest to one. 
*   Currently, the RESTful Web Service runs over plain http meaning that the communication between any client and 
    the RESTful Web Service is unsecured. How would you enable SSL encryption, meaning that the RESTful Web Service 
    will run from https without modifying the service's source code?


## Appendix: Technologies Short Background

### GitHub

GitHub is a web-based hosting service for version control using Git. Version control helps keep track of changes in a project and allows for collaboration between many developers.


### Docker

Docker performs operating-system-level virtualization, also known as "containerization". Docker uses the resource isolation features of the Linux kernel to allow independent "containers" to run within a Linux instance.


### kubernetes

Kubernetes is an open-source container-orchestration system for automating computer application deployment, scaling, and management.


### Python Virtualenv

Virtualenv is a tool to create isolated Python environments. The basic problem being addressed is one of dependencies and versions. Virtualenv creates an environment that has its own installation directories, that doesn't share libraries with other virtualenv environments.
