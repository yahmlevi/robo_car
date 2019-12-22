#!/bin/bash
set -e
# source - https://medium.com/google-cloud/running-node-red-on-google-cloud-platform-under-docker-3d4185e97f28

command=$1

if [ "$command" == "" ]; then
    echo "Pleae input the desired command"
    exit 0
fi

PROJECT="video-python"
REGION="europe-west1"
ZONE="europe-west1-b"
CONTAINER_FILE="container_file.yaml" 

NODE_NAME="node-red" 
MACHINE_TYPE="f1-micro"

CONTAINER_IMAGE="nodered/node-red-docker:latest"

function create_vm() {

    exists=$(gcloud compute instances list --format="table(name)" | grep $NODE_NAME)=="$NODE_NAME"
    if [ ! exists ]; then
    
        gcloud beta compute instances create-with-container $NODE_NAME \
            --zone=$ZONE \
            --machine-type=$MACHINE_TYPE \
            --subnet=default \
            --network-tier=PREMIUM \
            --metadata=google-logging-enabled=true \
            --maintenance-policy=MIGRATE \
            --service-account=637334533626-compute@developer.gserviceaccount.com \
            --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
            --tags=http-server,https-server \
            --image=cos-stable-78-12499-89-0 \
            --image-project=cos-cloud \
            --boot-disk-size=10GB \
            --boot-disk-type=pd-standard \
            --boot-disk-device-name=$NODE_NAME \
            --container-image=$CONTAINER_IMAGE \
            --container-restart-policy=always \
            --labels=container-vm=cos-stable-78-12499-89-0 \
            --project=$PROJECT
        fi

        # --reservation-affinity=any \
        create_firewall_rules
        attach_static_ip_address        
}

function attach_static_ip_address(){

    # gcloud compute addresses create $NODE_NAME \
    #     --project=$PROJECT \
    #     --region=$REGION

    # gcloud compute addresses describe $NODE_NAME \
    #     --project=$PROJECT \
    #     --region=$REGION

    ADDRESS=$(gcloud compute addresses describe $NODE_NAME --region $REGION | grep 'address:' | awk '{print $2}')

    gcloud compute instances add-access-config $NODE_NAME \
        --project=$PROJECT \
        --zone=$ZONE \
        --address=$ADDRESS
}

function create_vm_OLD () {
    # Create the Container-Optimized OS VM using the cloud-init file:
    gcloud compute instances create ${NODE_NAME} \
        --image-family=cos-stable \
        --image-project=cos-cloud \
        --metadata-from-file=user-data=./cloud-init.yaml \
        --machine-type=f1-micro \
        --zone=${ZONE} \
        --preemptible \
        --project=${PROJECT} 
}

# we need to open port 1880 for Node-Red
function create_firewall_rules() {
    # RULE_NAME="default-allow-http-https"
    # gcloud compute firewall-rules create $RULE_NAME \
    #     --direction=INGRESS \
    #     --priority=1000 \
    #     --network=default \
    #     --action=ALLOW \
    #     --rules=tcp:80,tcp:443 \
    #     --source-ranges=0.0.0.0/0 \
    #     --target-tags=https-server \
    #     --project=$PROJECT 
    
    RULE_NAME="allow-1880"

    exists=$(gcloud compute firewall-rules list --format="table(name)" | grep $RULE_NAME)=="$RULE_NAME"
    if [ ! exists ]; then
        gcloud compute firewall-rules create $RULE_NAME \
            --direction=INGRESS \
            --priority=1000 \
            --network=default \
            --action=ALLOW \
            --rules=tcp:1880 \
            --source-ranges=0.0.0.0/0 \
            --project=$PROJECT 
    fi
}

function ssh_vm() {
    # Give the image a short amount of time to stabilize to download Node-RED and run the container
     # and then ssh into it
    gcloud compute ssh ${NODE_NAME} \
        --project=${PROJECT} \
        --command="sudo journalctl --unit=node-red --follow" 
}

function curl_endpoint() {
    # curl the Node-RED endpoint remotely
    gcloud compute ssh ${NODE_NAME} \
        --project=${PROJECT} \
        --command="curl localhost:1880"  
}

function update_image() {
    CONTAINER_IMAGE="nodered/node-red-docker:latest"
    gcloud beta compute instances update-container $NODE_NAME \
        --container-image=$CONTAINER_IMAGE \
        --project=${PROJECT} 
    
}

function delete_vm() {
    gcloud compute instances delete ${NODE_NAME} \
        --project=${PROJECT} 
}


case $command in
    "create_vm" )
        create_vm 
        ;;
    "create_firewall_rule" )
        create_firewall_rule
        ;;
    "update_image" )
        update_image 
        ;;

    "ssh_vm" )
        ssh_vm 
        ;;
    "curl_endpoint" )
        curl_endpoint 
        ;;
    "delete_vm" )
        delete_vm 
        ;;
esac
    