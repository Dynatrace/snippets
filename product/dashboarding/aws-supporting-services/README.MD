# AWS Supporting Services Dashboards

This repository contains custom dashboards for AWS Supporting Services. 

## How to use

To use AWS Supporting Services Dashboards, you have to upload them via Dashboards API. First you need to create the API token as described in [Dynatrace API - Authentication](https://www.dynatrace.com/support/help/dynatrace-api/basics/dynatrace-api-authentication/). Uploading the dashboard requires `Write configuration` permission, you have to check it when creating the token.

Example cURL command to upload the dashboard:

```shell script
curl --location --request POST 'http://{DYNATRACE_HOST}/e/{DYNATRACE_TENANT}/api/config/v1/dashboards' \
--header 'Authorization: Api-Token {TOKEN}' \
--header 'Content-Type: application/json' \
--data-binary '{PATH_TO_DASHBOARD}'
```

See [Dashboards API - POST a dashboard](https://www.dynatrace.com/support/help/dynatrace-api/configuration-api/dashboards-api/post-dashboard/#expand-540authentication) to for further details/API changes. 

## How to setup Management Zone

Some dashboards require you to set up the management zone, you can find the instruction of how to create Management Zone in [Set up management zones](https://www.dynatrace.com/support/help/how-to-use-dynatrace/management-zones/set-up-management-zones/).
The rules should be created to match relevant entities. Dashboards which require Management Zone have description of required rules setup. 

See [Dashboard timeframe and management zone](https://www.dynatrace.com/support/help/how-to-use-dynatrace/dashboards-and-charts/dashboards/dashboard-timeframe/?new-selector%3C-%3Eold-selector=new-selector) article to learn how to select management zone for imported dashboard.

## Dashboards

### [Amazon Elastic Kubernetes Service](AmazonElasticKubernetesService.json)
![AmazonElasticKubernetesService.png](AmazonElasticKubernetesService.png)

### [Amazon Elastic Transcoder](AmazonElasticTranscoder.json)
![AmazonElasticTranscoder.png](AmazonElasticTranscoder.png)

### [Amazon EventBridge](AmazonEventBridge.json)
![AmazonEventBridge.png](AmazonEventBridge.png)

### [Amazon Polly](AmazonPolly.json)
![AmazonPolly.png](AmazonPolly.png)

### [Amazon QLDB](AmazonQLDB.json)
![AmazonQLDB.png](AmazonQLDB.png)

### [AWS RoboMaker](AWSRoboMaker.json)
![AWSRoboMaker.png](AWSRoboMaker.png)

### [AWS VPN](AWSVPN.json)
![AWSVPN.png](AWSVPN.png)

### [Amazon Connect](AmazonConnect.json)

### [Amazon EC2 Auto Scaling](AmazonEC2AutoScaling.json)
![AmazonEC2AutoScaling.png](AmazonEC2AutoScaling.png)

### [AmazonFSx](AmazonFSx.json)
![AmazonFSx.png](AmazonFSx.png)

### [Amazon Transfer](AmazonTransfer.json)
![AmazonTransfer.png](AmazonTransfer.png)

### [Amazon WAF](AmazonWAF.json)
![AmazonWAF.png](AmazonWAF.png)

### [AWS App Sync](AWSAppSync.json)
![AWSAppSync.png](AWSAppSync.png)

### [AWS Cloud HSM](AWSCloudHSM.json)
![AWSCloudHSM.png](AWSCloudHSM.png)

### [AWS Dax](AWSDax.json)
![AWSDax.png](AWSDax.png)

### [AWS DMS](AWSDMS.json)
![AWSDMS.png](AWSDMS.png)

### [AWS Elastic Inference](AWSElasticInference.json)
![AWSElasticInference.png](AWSElasticInference.png)

### [AWS Media Connect](AWSMediaConnect.json)
![AWSMediaConnect.png](AWSMediaConnect.png)

### [AWS Media Tailor](AWSMediaTailor.json)
![AWSMediaTailor.png](AWSMediaTailor.png)

### [AWS Neptune](AWSNeptune.json)
![AWSNeptune.png](AWSNeptune.png)

### [AWS Rekognition](AWSRekognition.json)
![AWSRekognition.png](AWSRekognition.png)

### [AWS Step Functions](AWSStepFunctions.json)
![AWSStepFunctions.png](AWSStepFunctions.png)

### [AWS Storage Gateway](AWSStorageGateway.json)
![AWSStorageGateway.png](AWSStorageGateway.png)

### [AWS Work Mail](AWSWorkMail.json)
![AWSWorkMail.png](AWSWorkMail.png)

### [AWS Work Spaces](AWSWorkSpaces.json)
![AWSWorkSpaces.png](AWSWorkSpaces.png)