This application will provide Pollen indexes forecasted in an hourly fashion for the location specified in the flask application as latitude and longitude.
The API is provide by api.breezometer.com

## About:
A python flask based web app leveraging on google cloud and kubernetes engine. The app is implements Pollen API lets you request pollen information including types, plants, and indexes for a specific location. The API provides endpoints that let you query. 
1) Current Conditions
2) Daily Forecast

## Running the application:
The following fields have to be edited for the need latitude, longitude, start time, end time, api key

##How To Install and Run the Project :
Install the Dependencies using pip install -r requirements.txt.

Run the project using python pollen.py.

App can be viewed at http://0.0.0.0:8080/

## Overview

Apache Cassandra is a database management system that replicates
large amounts of data across many servers, avoiding a single point of failure
and reducing latency.

[Learn more](https://cassandra.apache.org/).

## About Google Click to Deploy

Popular open stacks on Kubernetes packaged by Google.

### Solution Information

StatefulSet Kubernetes object is used to manage all Cassandra pods within this K8s application. Each pod runs a single instance of Cassandra process.

All pods are behind Service object. Cassandra service is not exposed to the external traffic as this Cassandra K8s application is meant to be an internal database
and access to Cassandra instances is not authenticated by default. Please configure authentication and other layers of protection, like firewalls, before exposing
Cassandra outside K8s cluster.

Cassandra service can be used to discover current number of pods and their addresses.

# Installation

## Quick install with Google Cloud Marketplace

Get up and running with a few clicks! Install this Cassandra app to a
Google Kubernetes Engine cluster using Google Cloud Marketplace. Follow the
[on-screen instructions](https://console.cloud.google.com/marketplace/details/google/cassandra).

## Command line instructions

You can use [Google Cloud Shell](https://cloud.google.com/shell/) or a local workstation in the
further instructions.

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/click-to-deploy&cloudshell_working_dir=k8s/cassandra)

### Prerequisites

#### Set up command-line tools

You'll need the following tools in your development environment:

- [gcloud](https://cloud.google.com/sdk/gcloud/)
- [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/)
- [docker](https://docs.docker.com/install/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [cqlsh](https://pypi.org/project/cqlsh/)

Configure `gcloud` as a Docker credential helper:

```shell
gcloud auth configure-docker
```

#### Create a Google Kubernetes Engine cluster

Create a new cluster from the command line:

```shell
export CLUSTER=cassandra-cluster
gcloud config set compute/zone europe-west2-b

gcloud container clusters create "$CLUSTER" --zone "$ZONE"
```

Configure `kubectl` to connect to the new cluster:

```shell
gcloud container clusters get-credentials "$CLUSTER" --zone "$ZONE"
```
## Export the project using Project ID
export PROJECT_ID="$(gcloud config get-value project -q)"

## pull the project
docker pull cassandra:latest

# Run
docker run --name cassandra-test -d cassandra:latest

## Activate the cqlsh
docker exec -it cassandra-test cqlsh

## After activation create the keyspace
CREATE KEYSPACE pollendata WITH REPLICATION =
{'class' : 'SimpleStrategy', 'replication_factor' : 2};

## Create the table
CREATE TABLE pollendata.pollenvalue (Time float, Grass Boolean, Tree Boolean, Weed Boolean,PRIMARY KEY(Time));

### Now create the c3 nodes cluster named cassandra
gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"

## The first will be a Headless service which will allow peer discovery i.e. the Cassandra pods will be able to find each other and form a ring.The second defines the Cassandra service itself, and the third is a Replication Controller which allows us to scale up and down the number of containers we want. Download these via the following commands:


wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8

## Once these are downloaded we can now run our three components:
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml

## Check that the single container is running correctly:
kubectl get pods -l name=cassandra
## and if so we can can scale up our number of nodes via our replication-controller:
kubectl scale rc cassandra --replicas=3

## Pick one of your containers, we must now check that the ring has been formed between all of the Cassandra instances:
kubectl exec -it cassandra-fwcxr -- nodetool status

## Now activate kubectl 
kubectl exec -it cassandra-fwcxr cqlsh

## Create keyspace with replication
CREATE KEYSPACE pollendata WITH REPLICATION =
{'class' : 'SimpleStrategy', 'replication_factor' : 2};

## Create table inside kubernetes
CREATE TABLE pollendata.pollenvalue (Time float, Grass Boolean, Tree Boolean, Weed Boolean,PRIMARY KEY(Time));

## Now run the following commands

export PROJECT_ID="$(gcloud config get-value project -q)"
docker build -t gcr.io/${PROJECT_ID}/pollen:v1 .
docker push gcr.io/${PROJECT_ID}/pollen:v1
kubectl run pollen --image=gcr.io/${PROJECT_ID}/pollen:v1 --port 8080
kubectl expose deployment pollen --type=LoadBalancer --port 80 --target-port 8080
kubectl get services

### Now we can see the external IP along with Load balance
