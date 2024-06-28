import json
import boto3

def start(region,cluster_name,service):
    ecs_client = boto3.client('ecs', region_name=region)
    desired_count=1
    try:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service,
            desiredCount=desired_count,
            forceNewDeployment=True
        )
        return json.dumps(response, default=str)
        
    except Exception as e:
        print(f"An error occurred: {e}")


def stop(region,cluster_name,service):
    ecs_client = boto3.client('ecs', region_name=region)
    desired_count=0
    try:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service,
            desiredCount=desired_count,
            forceNewDeployment=True
        )
        return json.dumps(response, default=str)
    except Exception as e:
        print(f"An error occurred: {e}")
    

def lambda_handler(event, context):
    with open('cluster.json') as f:
        config = json.load(f)
    environment = event["environment"]
    action = event["action"]
    region = config["region"]
    if (not environment) and (not action):
        return "Environment name and action is required"
    else:
        if action == "start":
            for cluster_config in config[environment]:
                cluster_name = cluster_config["cluster_name"]
                service_names = cluster_config["service_names"]
                for service in service_names:
                    ecs_start=start(region,cluster_name,service)
                    print(ecs_start)
                    #return ecs_start
        if action == "stop":
            for cluster_config in config[environment]:
                cluster_name = cluster_config["cluster_name"]
                service_names = cluster_config["service_names"]
                for service in service_names:
                    ecs_stop=stop(region,cluster_name,service)
                    print(ecs_stop)
                    #return ecs_stop
