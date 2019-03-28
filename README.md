This application will provide Pollen indexes forecasted in an hourly fashion for the location specified in the flask application as latitude and longitude.
The API is provide by api.breezometer.com

##About:
A python flask based web app leveraging on google cloud and kubernetes engine. The app is implements Pollen API lets you request pollen information including types, plants, and indexes for a specific location. The API provides endpoints that let you query. 
1) Current Conditions
2) Daily Forecast

##Running the application:
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

## Design

![Architecture diagram](resources/cassandra-k8s-app-architecture.png)

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
export ZONE=us-west1-a

gcloud container clusters create "$CLUSTER" --zone "$ZONE"
```

Configure `kubectl` to connect to the new cluster:

```shell
gcloud container clusters get-credentials "$CLUSTER" --zone "$ZONE"
```

#### Clone this repo

Clone this repo and the associated tools repo.

```shell
git clone --recursive https://github.com/GoogleCloudPlatform/click-to-deploy.git
```

#### Install the Application resource definition

An Application resource is a collection of individual Kubernetes components,
such as Services, Deployments, and so on, that you can manage as a group.

To set up your cluster to understand Application resources, run the following command:

```shell
kubectl apply -f "https://raw.githubusercontent.com/GoogleCloudPlatform/marketplace-k8s-app-tools/master/crd/app-crd.yaml"
```

You need to run this command once.

The Application resource is defined by the
[Kubernetes SIG-apps](https://github.com/kubernetes/community/tree/master/sig-apps)
community. The source code can be found on
[github.com/kubernetes-sigs/application](https://github.com/kubernetes-sigs/application).

### Install the Application

Navigate to the `cassandra` directory:

```shell
cd click-to-deploy/k8s/cassandra
```

#### Configure the app with environment variables

Choose an instance name and
[namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
for the app. In most cases, you can use the `default` namespace.

```shell
export APP_INSTANCE_NAME=cassandra-1
export NAMESPACE=default
```

Set the number of replicas for Cassandra:

```shell
# Setting a single node in Cassandra cluster means single point of failure.
# For production environments, consider at least 3 replicas.
export REPLICAS=3
```

Enable Stackdriver Metrics Exporter:

> **NOTE:** Your GCP project should have Stackdriver enabled. For non-GCP clusters, export of metrics to Stackdriver is not supported yet.
By default the integration is disabled. To enable, change the value to `true`.

```shell
export METRICS_EXPORTER_ENABLED=false
```

Configure the container images:

```shell
TAG=3.11
export IMAGE_CASSANDRA="marketplace.gcr.io/google/cassandra:${TAG}"
export IMAGE_METRICS_EXPORTER="marketplace.gcr.io/google/cassandra/prometheus-to-sd:${TAG}"
```

The images above are referenced by
[tag](https://docs.docker.com/engine/reference/commandline/tag). We recommend
that you pin each image to an immutable
[content digest](https://docs.docker.com/registry/spec/api/#content-digests).
This ensures that the installed application always uses the same images,
until you are ready to upgrade. To get the digest for the image, use the
following script:

```shell
for i in "IMAGE_CASSANDRA" "IMAGE_METRICS_EXPORTER"; do
  repo=$(echo ${!i} | cut -d: -f1);
  digest=$(docker pull ${!i} | sed -n -e 's/Digest: //p');
  export $i="$repo@$digest";
  env | grep $i;
done
```

#### Create namespace in your Kubernetes cluster

If you use a different namespace than the `default`, run the command below to create a new namespace:

```shell
kubectl create namespace "$NAMESPACE"
```

#### Expand the manifest template

Use `helm template` to expand the template. We recommend that you save the
expanded manifest file for future updates to the application.

```shell
helm template chart/cassandra \
  --name $APP_INSTANCE_NAME \
  --namespace $NAMESPACE \
  --set cassandra.image=$IMAGE_CASSANDRA \
  --set cassandra.replicas=$REPLICAS \
  --set metrics.image=$IMAGE_METRICS_EXPORTER \
  --set metrics.enabled=$METRICS_EXPORTER_ENABLED > "${APP_INSTANCE_NAME}_manifest.yaml"
```

#### Apply the manifest to your Kubernetes cluster

Use `kubectl` to apply the manifest to your Kubernetes cluster:

```shell
kubectl apply -f "${APP_INSTANCE_NAME}_manifest.yaml" --namespace "${NAMESPACE}"
```

#### View the app in the Google Cloud Console

To get the Console URL for your app, run the following command:

```shell
echo "https://console.cloud.google.com/kubernetes/application/${ZONE}/${CLUSTER}/${NAMESPACE}/${APP_INSTANCE_NAME}"
```

To view your app, open the URL in your browser.

### Check the status of the Cassandra cluster

If your deployment is successful, you can check status of your Cassandra
cluster.

On one of the Cassandra containers, run the `nodetool status` command.
`nodetool` is a Cassandra utility for managing a cluster. It is part of
the Cassandra container image.

```shell
kubectl exec "${APP_INSTANCE_NAME}-cassandra-0" --namespace "${NAMESPACE}" -c cassandra -- nodetool status
```

### Connecting to Cassandra (internal access)

You can connect to the Cassandra service without exposing your cluster
for public access, using the following options:

*  From a container in your Kubernetes cluster, connect using the hostname
  `$APP_INSTANCE_NAME-cassandra-0.$APP_INSTANCE_NAME-cassandra-svc.$NAMESPACE.svc.cluster.local`

* Use port forwarding to access the service. In a separate terminal, run the
  following command:

    ```shell
    kubectl port-forward "${APP_INSTANCE_NAME}-cassandra-0" 9042:9042 --namespace "${NAMESPACE}"
    ```

    Then, in your main terminal, start `cqlsh`:

    ```shell
    cqlsh --cqlversion=3.4.4
    ```

    In the response, you see the Cassandra welcome message:

    ```shell
    Use HELP for help.
    cqlsh>
    ```

### Connecting to Cassandra using an external IP address

By default, the application does not have an external IP address.

If you want to expose your Cassandra cluster using an external IP address,
first [configure access control](https://www.datastax.com/dev/blog/role-based-access-control-in-cassandra).

#### Configuring the Cassandra service

To configure Cassandra as an external service, run the following command:

```shell
envsubst '${APP_INSTANCE_NAME}' < scripts/external.yaml.template > scripts/external.yaml
kubectl apply -f scripts/external.yaml --namespace "${NAMESPACE}"
```

An external IP address is provisioned for the Service. It might take
a few minutes to get the external IP address.

#### Get the IP address of the Service

Get the external IP address of the Cassandra service using the following
command:

```shell
CASSANDRA_IP=$(kubectl get svc $APP_INSTANCE_NAME-cassandra-external-svc \
  --namespace $NAMESPACE \
  --output jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo $CASSANDRA_IP
```

Connect `cqlsh` to the external IP address, using the following command:

```shell
CQLSH_HOST=$CASSANDRA_IP cqlsh --cqlversion=3.4.4


Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
