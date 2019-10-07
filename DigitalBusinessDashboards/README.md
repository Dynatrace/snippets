Digital Business Analytic Dashboard Primer</br>
</br>
Prereqs:

  1. The batch scripts uses Curl and Powershell. 
  2. Add a session property for revenue if it applies for your application (Applications->[Your App]->Edit->Session and User action prop)
  3. Generate a read/write token (Settings->Integration->Dynatrace API->Generate Token)
  
What is Digital Business Analytics?</br>
TBD…</br>
</br>
How do I deploy the dashboards?</br>
1.	Download a zip from this repo
2.	Unzip into any directory
3.	Create a cfg file with a 3-digit prefix (i.e. 313.cfg)
4.	Example: </br>
  a.	abc123.managed-sprint.dynalabs.io/e/1234567890abcdefg</br>
  b.	yourlogin@corp.com</br>
  c.	Book Travel</br>
  d.	www.angular.easytravel.com</br>
  e.	longProperties.income</br>
  f.	Loading of page /easytravel/home</br>
  g.	Home</br>
  h.	/easytravel/rest/login</br>
  i.	Login</br>
  j.	/easytravel/rest/journeys/</br>
  k.	Search</br>
  l.	/easytravel/rest/validate-creditcard</br>
  m.	Finish</br>
5.	The cfg file contains the following fields (Tenant, Owner, Funnel Name, App Name (must match the naming rule for the App), revenue session property (use NOREVENUE if the app is not revenue generating), User Action name for first funnel step (can be the actual name or naming rule name), Header for first funnel step, … repeat for all funnel steps
6.	Note: You need a minimum of 3 funnel steps with a maximum of 12 funnel steps. My example above will create a 3-step funnel
7.	Open windows cmd prompt and CD to the directory where the files were unzipped
8.	Run DeployTennt.bat and pass in the following parameters</br>
  a.	Token</br>
  b.	3-digit prefix you used to create the cfg </br>
9.	For example, DeployTenant.bat 858585dhdh8 313</br>
This will create a Tenant Overview Dashboard, App Overview Dashboard, Funnel Overview Dashboard and many Funnel related Dashboards. This step will also create a Key Store Dashboard that logged the TenantDeploy and all future deployments. This Dashboard can be accessed from the Tenant Overview Dashboard. This info is needed for future updates and keeps track of the 3-digit “keys” used in deployments.</br>
 </br>
How do I deploy a second app to a tenant?</br>
</br>
1.	Create a cfg file just like the tenant cfg above and give it a different 3-digit prefix</br>
2.	Open windows cmd prompt and CD to the directory where the files were unzipped</br>
3.	Run DeployApplication.bat and pass in the following parameters</br>
  a.	Token</br>
  b.	3-digit prefix you used to create the cfg file for the app</br>
  c.	3-digit prefix you used in DeployTenant</br>
  d.	Position number for App Overview link (2-11)</br>
4.	For example, DeployApplication.bat 858585dhdh8 734 313 2</br>
This will create an App Overview Dashboard and link it to the Tenant Overview Dashboard. It will also create a Funnel Overview Dashboard and many Funnel related Dashboards. It will also update the Key Store for the App deployment.</br>
</br>
How do I deploy a second funnel to an app?</br>
</br>
1.	Create a cfg file just like the tenant cfg above and give it a different 3-digit prefix</br>
2.	Open windows cmd prompt and CD to the directory where the files were unzipped</br>
3.	Run DeployFunnel.bat and pass in the following parameters</br>
  a.	Token</br>
  b.	3-digit prefix you used to create the cfg file for the funnel</br>
  c.	3-digit prefix you used in DeployApplication</br>
  d.	Position number for Funnel Overview link (2-11)</br>
4.	For example, DeployFunnel.bat 858585dhdh8 808 734 2</br>
This will create a Funnel Overview Dashboard and link it to the Application Overview Dashboard. It will also create many Funnel related Dashboards. It will also update the Key Store for the Funnel deployment.</br>
</br>
How do I change the time filters in the Comparison Dashboards?</br>
</br>
1.	Open windows cmd prompt and CD to the directory where the files were unzipped</br>
2.	Run UpdateTimeCompareDashboards.bat and pass in the following parameters</br>
  a.	Token</br>
  b.	3-digit prefix you used in DeployTenant/DeployApplication/DeployFunnel</br>
  c.	Compare hours (i.e. 12)</br>
This will update the Compare Dashboards for the Tenant/App/Funnel with a time filter of X in the upper half and X*2 in the bottom half of the Compare Dashboards. My example will filter the top tiles for last 12 hours and the bottom tiles with the previous 12 hours.</br>
</br>
How do I change the application name in the Comparison Dashboards so the top half shows one app and the bottom half shows a different app (i.e. A/B testing)?</br>
</br>
1.	Open windows cmd prompt and CD to the directory where the files were unzipped</br>
2.	Run UpdateAppCompareDashboards.bat and pass in the following parameters</br>
  a.	Token</br>
  b.	3-digit prefix you used in DeployTenant/DeployApplication/DeployFunnel for the primary app (top half of dashboard)</br>
  c.	3-digit prefix you used in DeployTenant/DeployApplication/DeployFunnel for the secondary app (bottom half of dashboard)</br>
This will update the Compare Dashboards for the Tenant/App/Funnel with a time filter of X in the upper half and X*2 in the bottom half of the Compare Dashboards. My example will filter the top tiles for last 12 hours and the bottom tiles with the previous 12 hours.
