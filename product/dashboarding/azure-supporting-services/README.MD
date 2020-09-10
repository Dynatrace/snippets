# Azure Supporting Services Dashboards

This repository contains custom dashboards for Azure Supporting Services. 

## How to use

To use Azure Supporting Services Dashboards, you have to upload them via Dashboards API. First you need to create the API token as described in [Dynatrace API - Authentication](https://www.dynatrace.com/support/help/dynatrace-api/basics/dynatrace-api-authentication/). Uploading the dashboard requires `Write configuration` permission, you have to check it when creating the token.

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

### [Azure Automation Account](AutomationAccount.json)
![AutomationAccount.png](AutomationAccount.png)

### [Azure Batch Accounts](BatchAccounts.json)
![BatchAccounts.png](BatchAccounts.png)

### [Azure Container Instances](ContainerInstances.json)
![ContainerInstances.png](ContainerInstances.png)

### [Azure Data Factory V1](DataFactoryV1.json)
![DataFactoryV1.png](DataFactoryV1.png)

### [Azure Data Factory V2](DataFactoryV2.json)
![DataFactoryV2.png](DataFactoryV2.png)

### [Azure Data Lake Analytics](DataLakeAnalytics.json)
![DataLakeAnalytics.png](DataLakeAnalytics.png)

### [Azure Data Lake Storage](DataLakeStorage.json)
![DataLakeStorage.png](DataLakeStorage.png)

### [Azure DB for MariaDB](DbForMariaDb.json)
- database clients have to be instrumented with [One Agent](https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/) 
- Management Zone should be set up to match Azure MariaDB databases, example rules:

![DbForMariaDbManagementZone.png](DbForMariaDbManagementZone.png)

![DbForMariaDb.png](DbForMariaDb.png)

### [Azure DB for MySQL](DbForMySQL.json)
- database clients have to be instrumented with [One Agent](https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/) 
- Management Zone should be set up to match Azure MySQL databases, example rules:

![DbForMySQLManagementZone.png](DbForMySQLManagementZone.png)

![DbForMySQL.png](DbForMySQL.png)

### [Azure DB for PostgreSQL](DbForPostgreSQL.json)
- database clients have to be instrumented with [One Agent](https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/) 
- Management Zone should be set up to match Azure PostgreSQL databases, example rules

![DbForPostgreSQLManagementZone.png](DbForPostgreSQLManagementZone.png)

![DbForPostgreSQL.png](DbForPostgreSQL.png)

### [Azure DB for PostgreSQL - Hyperscale](DbForPostgreSQLHyperscale.json)
- database clients have to be instrumented with [One Agent](https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/) 
- Management Zone should be set up to match Azure PostgreSQL Hyperscale databases, example rules

![DbForPostgreSQLManagementZone.png](DbForPostgreSQLManagementZone.png)

![DbForPostgreSQLHyperscale.png](DbForPostgreSQLHyperscale.png)

### [Azure Event Grid Domains](EventGridDomains.json)
![EventGridDomains.png](EventGridDomains.png)

### [Azure Event Grid System Topics](EventGridSystemTopics.json)
![EventGridSystemTopics.png](EventGridSystemTopics.png)

### [Azure Event Grid Topics](EventGridTopics.json)
![EventGridTopics.png](EventGridTopics.png)

### [Azure Event Hub Clusters](EventHubClusters.json)
![EventHubClusters.png](EventHubClusters.png)

### [Azure Express Route Circuit](ExpressRouteCircuit.json)
![ExpressRouteCircuit.png](ExpressRouteCircuit.png)

### [Azure Firewall](Firewall.json)
![Firewall.png](Firewall.png)

### [Azure Front Door](FrontDoor.json)
![FrontDoor.png](FrontDoor.png)

### [Azure HDInsight Cluster](HDInsight.json)
- Cluster has to be instrumented with OneAgent, you can find the instruction [here](https://github.com/safia-habib/Azure/blob/master/HDInsights/Readme.md)
- Management Zone `hdi-filter` should be set up to match HDI Cluster with hosts, example rules:

![HDInsightManagementZone.png](HDInsightManagementZone.png)

![HDInsight.png](HDInsight.png)

### [Azure Integration Service Environment](IntegrationServiceEnvironment.json)
![IntegrationServiceEnvironment.png](IntegrationServiceEnvironment.png)

### [Azure Integration Service Environment Plus LogicApps](IntegrationServiceEnvironmentPlusLogicApps.json)
![IntegrationServiceEnvironmentPlusLogicApps.png](IntegrationServiceEnvironmentPlusLogicApps.png)

### [Azure Kubernetes Service](KubernetesService.json)
![KubernetesService.png](KubernetesService.png)

### [Azure Logic Workflows](LogicWorkflows.json)
![LogicWorkflows.png](LogicWorkflows.png)

### [Azure Machine Learning](MachineLearning.json)
![MachineLearning.png](MachineLearning.png)

### [Azure Maps Accounts](MapsAccounts.json)
![MapsAccounts.png](MapsAccounts.png)

### [Azure NetApp Capacity Volume](NetAppCapacityVolume.json)
![NetAppCapacityVolume.png](NetAppCapacityVolume.png)

### [Azure Network Interface](NetworkInterface.json)
![NetworkInterface.png](NetworkInterface.png)

### [Azure Private Dns Zones](PrivateDnsZones.json)
![PrivateDnsZones.png](PrivateDnsZones.png)

### [Azure Public Ip](PublicIp.json)
![PublicIp.png](PublicIp.png)

### [Azure Search Services](SearchServices.json)
![SearchServices.png](SearchServices.png)

### [Azure SignalR](SignalR.json)
![SignalR.png](SignalR.png)

### [Azure Spring Cloud](SpringCloud.json)
![SpringCloud.png](SpringCloud.png)

### [Azure SQL Managed Instance](SqlManagedInstances.json)
- database clients have to be instrumented with [OneAgent](https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/) 

![SqlManagedInstances.png](SqlManagedInstances.png)

### [Azure Traffic Manager](TrafficManager.json)
![TrafficManager.png](TrafficManager.png)

### [Azure Virtual Machine Classic](VirtualMachineClassic.json)
![VirtualMachineClassic.png](VirtualMachineClassic.png)

### [Azure Virtual Network Gateway](VirtualNetworkGateway.json)
![VirtualNetworkGateway.png](VirtualNetworkGateway.png)
