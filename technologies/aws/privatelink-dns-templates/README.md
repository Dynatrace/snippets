# PrivateLink integration

Dynatrace SaaS supports integration with AWS PrivateLink. You can use PrivateLink to connect your OneAgents and ActiveGates running in your VPC directly to Dynatrace SaaS VPC.  While traffic send to Dynatrace is always encrypted, PrivateLink provides additional security layer by ensuring the traffic never AWS network.

More information about Dynatrace integration with AWS PrivateLink can be found [here](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/amazon-web-services/configuration/connect-to-dynatrace-using-aws-privatelink/)

Key part of the integration is an override of DNS so that your Dynatrace environment URL points to your VPC Endpoint (i.e. resolves to private IP addresses).
This approach is called split-horizon DNS - while the domain `<environment_id>.live.dynatrace.com` is public, it will resolve differently from within your VPC.

Easy way of creating such override is provided by the CloudFormation template in this repo. 
It creates private hosted zone in Route 53 and an alias record pointing to your VPC Endpoint.
