#!/bin/bash
set -e

command=$1

PROJECT="video-python" 
CLUSTER_NAME="robo-car"
ZONE="europe-west1-b"


function create_cluster(){
    gcloud beta container clusters create $CLUSTER_NAME \
        --zone $ZONE \
        --no-enable-basic-auth \
        --cluster-version "1.13.11-gke.14" \
        --machine-type "n1-standard-2" \
        --image-type "COS" \
        --disk-type "pd-standard" \
        --disk-size "100" \
        --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
        --num-nodes "1" \
        --enable-cloud-logging \
        --enable-cloud-monitoring \
        --enable-ip-alias \
        --network "projects/video-python/global/networks/default" \
        --subnetwork "projects/video-python/regions/europe-west1/subnetworks/default" \
        --default-max-pods-per-node "110" \
        --addons HorizontalPodAutoscaling,HttpLoadBalancing \
        --enable-autoupgrade \
        --enable-autorepair \
        --project $PROJECT
}

function connect_to_cluster() {
    gcloud container clusters get-credentials $CLUSTER_NAME /
        --zone $ZONE /
        --project $PROJECT
}

function deploy_to_cluster (){
    # we talk with the cluster using kubectl CLI
    kubectl apply -f ./mysql.yaml
}

case $command in 
    "create" )
        create_cluster
        ;;
    "connect" )
        connect_to_cluster
        ;;
    "deploy" )
        deploy_to_cluster
        ;;
esac

