# Automate setup Dynatrace Site-Extension for Monitoring Azure App-Service

The powershell script is a blueprint to automate the [Setup to monitor Azure App-Services with OneAgent using the Dynatrace Site-Extension](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/microsoft-azure/azure-services/app-service/deploy-oneagent-on-azure-app-service/). 

## The basic workflow of the script
* Use Azure CLI to retrieve the publishing profile to get the credentials required to access the [Kudu](https://github.com/projectkudu/kudu/wiki) Rest-API, which is used to install the Site-Extension

* Install the Dynatrace Site-Extension via the [Kudu Rest-API](https://github.com/projectkudu/kudu/wiki/REST-API#siteextensions)

* Configure Dynatrace's Site-Extension via the extensions [REST-API](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/microsoft-azure/azure-services/app-service/update-oneagent-on-azure-app-service/?azure-portal%3C-%3Erest-api=rest-api)


## How-To Guide

### Prerequisites 
* Powershell 3.0 or higher
* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)

Before executing the script, make sure you are signed-in with Azure CLI. For more details see [Sign in with Azure CLI](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest)

### Script Parameter
| Parameter | Mandatory | Value |
| ----- | ----- | ----- |
| subscription | yes | Subscription-ID or -name the targeted App-Service is in. |
| resourceGroup | yes | Resourcegroup of the App-Service |
| appName | yes | Name of the App-Service |
| environmentId | yes | Dynatrace Environment-ID. For more details see [Dynatrace Help](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/microsoft-azure/azure-services/app-service/deploy-oneagent-on-azure-app-service/) |
| apiToken | yes | Dynatrace API Token. For more details see [Dynatrace Help](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/microsoft-azure/azure-services/app-service/deploy-oneagent-on-azure-app-service/) |
| apiUrl | no | Dynatrace API Token. For more details see [Dynatrace Help](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/microsoft-azure/azure-services/app-service/deploy-oneagent-on-azure-app-service/) |
| sslMode | no | Dynatrace ssl-mode. For more details see [Dynatrace Help](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/microsoft-azure/azure-services/app-service/deploy-oneagent-on-azure-app-service/) |


### Example 

``` 
./automate-siteextension.ps1 -subscription "Demo" -resourceGroup "MyAppServiceGroup" -appName "MyApp" -environmentId "XXXXXX" -apiToken "XXXX"
``` 


## License
This project is licensed under [Apache 2.0 license](LICENSE).