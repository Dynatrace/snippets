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

### [Azure App Configuration](AppConfiguration.json)
![AppConfiguration.png](AppConfiguration.png)

### [Azure App Service Deployment Slots](AppServiceDeploymentSlots.json)
![AppServiceDeploymentSlots.png](AppServiceDeploymentSlots.png)

### [App Service Function Deployment Slots.json](AppServiceFunctionDeploymentSlots.json)
![AppServiceFunctionDeploymentSlots.png](AppServiceFunctionDeploymentSlots.png)

### [Azure App Service Environment](AppServiceEnvironment.json)
![AppServiceEnvironment.png](AppServiceEnvironment.png)

### [Azure App Service Plan](AppServicePlan.json)
![AppServicePlan.png](AppServicePlan.png)

### [Azure Application Insights](ApplicationInsights.json)
![ApplicationInsights1.png](ApplicationInsights1.png)


![ApplicationInsights2.png](ApplicationInsights2.png)


![ApplicationInsights3.png](ApplicationInsights3.png)

### [Azure Automation Account](AutomationAccount.json)
![AutomationAccount.png](AutomationAccount.png)

### [Azure Batch Accounts](BatchAccounts.json)
![BatchAccounts.png](BatchAccounts.png)

### [Azure Blockchain](Blockchain.json)
![Blockchain.png](Blockchain.png)

### [Azure CDN WAF Policy](CdnWafPolicy.json)
![CdnWafPolicy.png](CdnWafPolicy.png)

### [Azure Cognitive Services](CognitiveServices.json)
![CognitiveServices.png](CognitiveServices.png)

### [Azure Connection Monitors](ConnectionMonitors.json)
![ConnectionMonitors.png](ConnectionMonitors.png)

### [Azure Connection Monitors Preview](ConnectionMonitorsPreview.json)
![ConnectionMonitorsPreview.png](ConnectionMonitorsPreview.png)

### [Azure Container Instances](ContainerInstances.json)
![ContainerInstances.png](ContainerInstances.png)

### [Azure Container Registries](ContainerRegistries.json)
![ContainerRegistries.png](ContainerRegistries.png)

### [Azure Data Explorer Clusters](DataExplorerClusters.json)
![DataExplorerClusters.png](DataExplorerClusters.png)

### [Azure Data Factory V1](DataFactoryV1.json)
![DataFactoryV1.png](DataFactoryV1.png)

### [Azure Data Factory V2](DataFactoryV2.json)
![DataFactoryV2.png](DataFactoryV2.png)

### [Azure Data Lake Analytics](DataLakeAnalytics.json)
![DataLakeAnalytics.png](DataLakeAnalytics.png)

### [Azure Data Lake Storage](DataLakeStorage.json)
![DataLakeStorage.png](DataLakeStorage.png)

### [Azure Data Share](DataShare.json)
![DataShare.png](DataShare.png)

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

### [Azure Device Provisioning Services](DeviceProvisioningServices.json)
![DeviceProvisioningServices.png](DeviceProvisioningServices.png)

### [Azure DNS Zones](DnsZones.json)
![DnsZones.png](DnsZones.png)

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

### [Azure IoT Central Applications](IotCentralApplications.json)
![IotCentralApplications.png](IotCentralApplications.png)

### [Azure Key Vault](KeyVault.json)
![KeyVault.png](KeyVault.png)

### [Azure Kubernetes Service](KubernetesService.json)
![KubernetesService.png](KubernetesService.png)

### [Azure Logic Apps](LogicApps.json)
![LogicApps.png](LogicApps.png)

### [Azure Machine Learning](MachineLearning.json)
![MachineLearning1.png](MachineLearning1.png)

![MachineLearning2.png](MachineLearning2.png)

### [Azure Maps Accounts](MapsAccounts.json)
![MapsAccounts.png](MapsAccounts.png)

### [Azure Media Services (and Media Service Streaming Endpoint)](MediaServices.json)
![MediaServices.png](MediaServices.png)

### [Azure Mesh Applications](MeshApplications.json)
![MeshApplications.png](MeshApplications.png)

### [Azure NetApp Capacity Volume](NetAppCapacityVolume.json)
![NetAppCapacityVolume.png](NetAppCapacityVolume.png)

### [Azure Network Interface](NetworkInterface.json)
![NetworkInterface.png](NetworkInterface.png)

### [Azure Notification Hubs](NotificationHubs.json)
![NotificationHubs.png](NotificationHubs.png)

### [Azure PowerBI](PowerBi.json)
![PowerBi.png](PowerBi.png)

### [Azure Private DNS Zones](PrivateDnsZones.json)
![PrivateDnsZones.png](PrivateDnsZones.png)

### [Azure Public IP](PublicIp.json)
![PublicIp.png](PublicIp.png)

### [Azure Relay](Relay.json)
![Relay.png](Relay.png)

### [Azure Search Services](SearchServices.json)
![SearchServices.png](SearchServices.png)

### [Azure SignalR](SignalR.json)
![SignalR.png](SignalR.png)

### [Azure Spring Cloud](SpringCloud.json)
![SpringCloud.png](SpringCloud.png)

### [Azure SQL Managed Instance](SqlManagedInstances.json)
- database clients have to be instrumented with [OneAgent](https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/) 

![SqlManagedInstances.png](SqlManagedInstances.png)

### [Azure Storage Account Classic](StorageAccountClassic.json)
![StorageAccountClassic.png](StorageAccountClassic.png)

### [Azure Storage Account Classic (Blob)](StorageAccountClassicBlob.json)
![StorageAccountClassicBlob.png](StorageAccountClassicBlob.png)

### [Azure Storage Account Classic (File)](StorageAccountClassicFile.json)

### [Azure Storage Account Classic (Queue)](StorageAccountClassicQueue.json)

### [Azure Storage Account Classic (Table)](StorageAccountClassicTable.json)
![StorageAccountClassicTable.png](StorageAccountClassicTable.png)

### [Azure Storage Sync Services](StorageSyncServices.json)
![StorageSyncServices.png](StorageSyncServices.png)

### [Azure Stream Analytics Jobs](StreamAnalyticsJobs.json)
![StreamAnalyticsJobs.png](StreamAnalyticsJobs.png)

### [Azure Synapse Workspace (and Apache Spark Pool and SQL Pool)](SynapseWorkspace.json)
![SynapseWorkspace.png](SynapseWorkspace.png)

### [Azure Time Series Insights Environment](TimeSeriesInsightsEnvironment.json)
![TimeSeriesInsightsEnvironment.png](TimeSeriesInsightsEnvironment.png)

### [Azure Time Series Insights Event Sources](TimeSeriesInsightsEventSources.json)
![TimeSeriesInsightsEventSources.png](TimeSeriesInsightsEventSources.png)

### [Azure Traffic Manager](TrafficManager.json)
![TrafficManager.png](TrafficManager.png)

### [Azure Virtual Machine Classic](VirtualMachineClassic.json)
![VirtualMachineClassic.png](VirtualMachineClassic.png)

### [Azure Virtual Network Gateway](VirtualNetworkGateway.json)
![VirtualNetworkGateway.png](VirtualNetworkGateway.png)
