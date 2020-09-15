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

### [AWS AppStream](AppStream.json)
![AppStream.png](AppStream.png)

### [AWS AppSync](AppSync.json)
![AppSync.png](AppSync.png)

### [Amazon Athena](Athena.json)
![Athena.png](Athena.png)

### [AWS Chatbot](Chatbot.json)
![Chatbot.png](Chatbot.png)

### [AWS CloudHSM](CloudHSM.json)
![CloudHSM.png](CloudHSM.png)

### [AWS CloudSearch](CloudSearch.json)
![CloudSearch.png](CloudSearch.png)

### [Amazon CloudWatch Logs](CloudWatchLogs.json)
![CloudWatchLogs.png](CloudWatchLogs.png)

### [AWS API Usage](CloudWatch_Usage.json)
![CloudWatch_Usage.png](CloudWatch_Usage.png)

### [AWS CodeBuild](CodeBuild.json)
![CodeBuild.png](CodeBuild.png)

### [Amazon Connect](Connect.json)
![Connect.png](Connect.png)

### [AWS DataSync](DataSync.json)
![DataSync.png](DataSync.png)

### [AWS DynamoDB Accelerator (DAX)](Dax.json)
![Dax.png](Dax.png)

### [AWS DMS](DMS.json)
![DMS.png](DMS.png)

### [Amazon DocumentDB](DocDB.json)
![DocDB.png](DocDB.png)

### [AWS Direct Connect](DX.json)
![DX.png](DX.png)

### [Amazon EC2 Auto Scaling](EC2AutoScaling.json)
![EC2AutoScaling.png](EC2AutoScaling.png)

### [Amazon EC2 API](EC2_API.json)
![EC2_API.png](EC2_API.png)

### [AWS ECS ContainerInsights](ECS_ContainerInsights.json)
![ECS_ContainerInsights.png](ECS_ContainerInsights.png)

### [AWS Elastic Beanstalk](ElasticBeanstalk.json)
![ElasticBeanstalk.png](ElasticBeanstalk.png)

### [AWS Elastic Inference](ElasticInference.json)
![ElasticInference.png](ElasticInference.png)

### [Amazon Elastic Kubernetes Service (EKS)](ElasticKubernetesService.json)
![ElasticKubernetesService.png](ElasticKubernetesService.png)

### [Amazon Elastic Transcoder](ElasticTranscoder.json)
![ElasticTranscoder.png](ElasticTranscoder.png)

### [Amazon EventBridge](EventBridge.json)
![EventBridge.png](EventBridge.png)

### [Amazon FSx](FSx.json)
![FSx.png](FSx.png)

### [Amazon Gamelift](GameLift.json)
![GameLift.png](GameLift.png)

### [Amazon Inspector](Inspector.json)
![Inspector.png](Inspector.png)

### [AWS IoT Analytics](IoT_Analytics.json)
![IoT_Analytics.png](IoT_Analytics.png)

### [AWS IoT Things Graph](IoT_ThingsGraph.json)
![IoT_ThingsGraph.png](IoT_ThingsGraph.png)

### [Amazon Keyspaces](Keyspaces_Cassandra.json)
![Keyspaces_Cassandra.png](Keyspaces_Cassandra.png)

### [Amazon Lex](Lex.json)
![Lex.png](Lex.png)

### [AWS Elemental MediaConnect](MediaConnect.json)
![MediaConnect.png](MediaConnect.png)

### [AWS MediaConvert](MediaConvert.json)
![MediaConvert.png](MediaConvert.png)

### [Amazon MediaPackage Live](MediaPackage_Live.json)
![MediaPackage_Live.png](MediaPackage_Live.png)

### [AWS CloudSearch](MediaTailor.json)
![MediaTailor.png](MediaTailor.png)

### [Amazon MQ](MQ.json)
![MQ.png](MQ.png)

### [Amazon MSK (Kafka)](MSK_Kafka.json)
![MSK_Kafka.png](MSK_Kafka.png)

### [Amazon Neptune](Neptune.json)
![Neptune.png](Neptune.png)

### [AWS OpsWorks](OpsWorks.json)
![OpsWorks.png](OpsWorks.png)

### [Amazon Polly](Polly.json)
![Polly.png](Polly.png)

### [Amazon QLDB](QLDB.json)
![QLDB.png](QLDB.png)

### [Amazon Rekognition](Rekognition.json)
![Rekognition.png](Rekognition.png)

### [AWS RoboMaker](RoboMaker.json)
![RoboMaker.png](RoboMaker.png)

### [Amazon Route 53](Route53.json)
![Route53.png](Route53.png)

### [AWS Route 53 Resolver](Route53_Resolver.json)
![Route53_Resolver.png](Route53_Resolver.png)

### [AWS Service Catalog](ServiceCatalog.json)
![ServiceCatalog.png](ServiceCatalog.png)

### [AWS Systems Manager - Run Command](SSM_RunCommand.json)
![SSM_RunCommand.png](SSM_RunCommand.png)

### [AWS Step Functions](StepFunctions.json)
![StepFunctions.png](StepFunctions.png)

### [AWS Storage Gateway](StorageGateway.json)
![StorageGateway.png](StorageGateway.png)

### [Amazon SWF](SWF.json)
![SWF.png](SWF.png)

### [Amazon Textract](Textract.json)
![Textract.png](Textract.png)

### [AWS Transfer Family](Transfer.json)
![Transfer.png](Transfer.png)

### [Amazon Transit Gateway](TransitGateway.json)
![TransitGateway.png](TransitGateway.png)

### [Amazon Translate](Translate.json)
![Translate.png](Translate.png)

### [AWS Trusted Advisor](TrustedAdvisor.json)
![TrustedAdvisor.png](TrustedAdvisor.png)

### [AWS Site-to-Site VPN](VPN.json)
![VPN.png](VPN.png)

### [Amazon WAFV2](WAF.json)
![WAF.png](WAF.png)

### [AWS WAF Classic](WAF_Classic.json)
![WAF_Classic.png](WAF_Classic.png)

### [Amazon WorkMail](WorkMail.json)
![WorkMail.png](WorkMail.png)

### [AWS WorkSpaces](WorkSpaces.json)
![WorkSpaces.png](WorkSpaces.png)
