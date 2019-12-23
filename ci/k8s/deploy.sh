#!/bin/bash
set -e

command=$1

PROJECT="video-python" 
CLUSTER_NAME="robo-car"
ZONE="europe-west1-b"
NAMESPACE="default"

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

function delete_cluster(){
    gcloud container clusters delete $CLUSTER_NAME 
}

function connect_to_cluster() {
    gcloud container clusters get-credentials $CLUSTER_NAME \
        --zone $ZONE \
        --project $PROJECT
}

function deploy_to_cluster (){
    NAMESPACE="default"
    
    # we talk with the cluster using kubectl CLI
    kubectl apply -f ./mysql-initdb-config.yaml -n $NAMESPACE
    kubectl apply -f ./mysql.yaml -n $NAMESPACE 

    kubectl apply -f ./node-red.yaml -n $NAMESPACE 
}

function get_info(){
    NAMESPACE="default"

    echo "Cluster's Nodes"
    echo "------------------------------"
    kubectl get nodes

    echo ""
    get_node_ip_addresses

    echo ""
    echo "Namespaces"
    echo "------------------------------"
    kubectl get ns

    echo ""
    echo "Services"
    echo "------------------------------"
    kubectl get svc -n $NAMESPACE

    echo ""
    echo "Deployments"
    echo "------------------------------"
    kubectl get deployments -n $NAMESPACE

    echo ""
    echo "Pods"
    echo "------------------------------"
    kubectl get pods -n $NAMESPACE
}

function get_node_ip_addresses(){
    # cluster's node name
    INSTANCE_NAME="gke-robo-car-default-pool-ecd0e422-zkbd"
    echo "Getting the internal and external IP address of '$CLUSTER_NAME' cluster"

    INTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
                    --format='get(networkInterfaces[0].networkIP)' \
                    --zone $ZONE)
    echo "INTERNAL IP ADDRESS: $INTERNAL_IP"

    EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
                    --format='get(networkInterfaces[0].accessConfigs[0].natIP)' \
                    --zone $ZONE)

    echo "EXTERNAL IP ADDRESS: $EXTERNAL_IP"  
}

function exec_to_node_red(){
    NODE_RED_POD=$(kubectl get pods -n $NAMESPACE --no-headers | grep node-red | awk '{print $1}')

    kubectl exec -it $NODE_RED_POD bash
}

function log_to_node_red(){
    NODE_RED_POD=$(kubectl get pods -n $NAMESPACE --no-headers | grep node-red | awk '{print $1}')

    kubectl logs $NODE_RED_POD
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
    "info" )
        get_info
        ;;
    "node_ip" )
        get_node_ip_addresses
        ;;
    "exec-node-red" )
        exec_to_node_red
        ;;
    "log-node-red" )
        log_to_node_red
        ;;
esac

