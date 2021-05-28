# Dynatrace Azure Monitoring Helm Chart

The Dynatrace Azure Monitoring Helm Chart is a snippet that automates installation of Azure monitoring (based on ActiveGate).

This Helm Chart requires Helm 3.

# Usage 

# Prerequisites
* Helm 3 client
* kubectl
* generate Dynatrace [PaaS token](https://www.dynatrace.com/support/help/shortlink/token#paas-token-) in Your Dynatrace environment

## Quick Start

Create Dynatrace namespace (if doesn't exists)
```sh
$ kubectl create namespace dynatrace
```

Clone snippets repository to get Helm chart
```sh
git clone https://github.com/Dynatrace/snippets.git
```

Install Helm chart, replace the `ENVIRONMENTID`, the `PLATFORM_AS_A_SERVICE_TOKEN` in command and execute it 
```sh
$ helm install dynatrace-azuremon ./snippets/technologies/azure/azuremon-helm-chart -n dynatrace --set dynatrace.host="ENVIRONMENTID.live.dynatrace.com",dynatrace.environment="ENVIRONMENTID",dynatrace.paasToken="PLATFORM_AS_A_SERVICE_TOKEN"
```

## Uninstall 

```sh
$ helm uninstall dynatrace-azuremon -n dynatrace
```