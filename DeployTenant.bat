@setlocal enableextensions enabledelayedexpansion
@echo off
call DeployApplication.bat %1 %2 313 1
set "tenant="
set "funnel="
set "appname="
set "dashboardkey=%2"
set /a "line = 0"
if not defined dashboardkey set /p dashboardkey="Enter Dashboard Key: "
if exist ./\%dashboardkey%.cfg (
for /f "tokens=*" %%a in (./\%dashboardkey%.cfg) do (
    set /a "line = line + 1"
    if !line!==1 set tenant=%%a
    if !line!==3 set funnel=%%a
    if !line!==4 set appname=%%a))
REM Update Key Store dashboard
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform/KeyStore.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '##  ') {(Get-Content $_ | ForEach {$_ -replace '##  ', '## %dashboardkey% Tenant Created with !appname! Application and !funnel! Funnel\n##  '}) | Set-Content $_ -encoding UTF8}}"
REM Upload Tenant dashboard
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/fbe8d3b1-ccb9-480c-9e5d-0e1b8b4da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\TenantOverview.json
REM Upload Key Store Dashboard
curl -X PUT "https://%tenant%/api/config/v1/dashboards/d4db8e38-000f-42df-85a9-d491d34da000" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\KeyStore.json
echo .
echo *********                             *********
echo ********* Welcome to Dynatrace BizOps *********
echo *********                             *********
