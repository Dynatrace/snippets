# Automatically monitor newly created accounts with Dynatrace via Control Tower integration 

The Dynatrace integrated solution for Control Tower provides the easiest way to automate Dynatrace monitoring for multi-account AWS environments by automating this configuration process when new AWS accounts are created.  The result for customers is a complete end-to-end picture of their cloud environment that is combining workload insights with CloudWatch service metrics with the governance and automation that Control Tower provides.

After deploying CloudFormation template following resources are added to Control Tower Master Account: 
- StackSet for creating IAM Dynatrace monitoring role in managed accounts 
- Event Rule for capturing CreateManagedAccount Control Tower event 
- Lambda that handles CreateManagedAccount event – creates StackSet instance and configure AWS monitoring settings in Dynatrace via API 
- Secret (in Secrets Manager) to store Dynatrace API url and token

![](control-tower-solution-architecture.png)

Solution is triggered by Control Tower event (CreateManagedAccount). This event is triggered by Control Tower when creating new Managed Account. 

Solution will automatically create IAM role for Dynatrace monitoring in Managed Account and trigger Dynatrace configuration API call to configure monitoring.

Configuration: 
- Log into the Dynatrace web UI 
- Generate API Token (Settings > Integration > Dynatrace API). **Token needs to have API v1 “Read configuration” and “Write configuration” permissions.** 
- Download the CloudFormation template code from here 
- Login in to MASTER account in AWS Control Tower as  user with AdministratorAccess and deploy the solution –  create CloudFormation Stack using downloaded template. 
- Specify template parameters:  
  * DynatraceUrl - URL to Dynatrace tenant endpoint, e.g. https://abc12345.live.dynatrace.com 
  * DynatraceApiKey – the API token that was created
- Verify that stack was created successfully  
