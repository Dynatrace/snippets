# Dynatrace Azure Monitoring Helm Chart

The Dynatrace Azure Monitoring Helm Chart is a snippet that automates installation of Azure monitoring (Active Gate).

This Helm Chart requires Helm 3.

# Usage 

## Quick Start

Create dynatrace namespace (if not exists)
```sh
$ kubectl create namespace dynatrace
```

Clone Snippets repository to get helm chart
```sh
git clone https://github.com/Dynatrace/snippets.git
```

Install helm chart
```sh
$ helm install dynatrace-azuremon ./snippets/technologies/azure/azuremon-helm-chart  -n dynatrace --set dynatrace.host="ENVIRONMENTID.live.dynatrace.com",dynatrace.environment="ENVIRONMENTID",dynatrace.paasToken="PLATFORM_AS_A_SERVICE_TOKEN"
```

## Uninstall 

```sh
$ helm uninstall dynatrace-azuremon -n dynatrace
```