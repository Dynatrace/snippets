# Dynatrace AWS Monitoring Helm Chart

The Dynatrace AWS Monitoring Helm Chart is a snippet that automates installation of AWS monitoring (based on ActiveGate) and CloudWatch integration.

This Helm Chart requires Helm 3.

# Usage 

# Prerequisites
* Helm 3 client
* kubectl
* generate Dynatrace [PaaS token](https://www.dynatrace.com/support/help/shortlink/token#paas-token-) in Your Dynatrace environment
* check Your K8S API url 

for example with:
```sh
kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " "
```

## Quick Start

Create Dynatrace namespace (if doesn't exist)
```sh
$ kubectl create namespace dynatrace
```

Clone snippets repository to get Helm chart
```sh
git clone https://github.com/Dynatrace/snippets.git
```


Install Helm chart, replace the `ENVIRONMENTID`, the `PLATFORM_AS_A_SERVICE_TOKEN` and `K8_SERVER_URL` in command and execute it 
```sh
$ helm install dynatrace-awsmon ./snippets/technologies/aws/awsmon-helm-chart -n dynatrace --set dynatrace.host="ENVIRONMENTID.live.dynatrace.com",dynatrace.environment="ENVIRONMENTID",dynatrace.paasToken="PLATFORM_AS_A_SERVICE_TOKEN",k8s.server="K8_SERVER_URL"
```

## Uninstall 

```sh
$ helm uninstall dynatrace-awsmon -n dynatrace
```