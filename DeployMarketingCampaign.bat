@setlocal enableextensions enabledelayedexpansion
@echo off
copy .\Marketing*.json .\Transform\
set "tenant="
set "owner="
set "appname="
set "campaign="
set "revflag=True"
set "revenue="
set "laststep="
set "promstep="
set /a "line = 0"
set "dashboardkey="
set "overviewkey="
set "dashboardkey=%2"
if not defined dashboardkey set /p dashboardkey="Enter Dashboard Key: "
set "overviewkey=%3"
if not defined overviewkey set /p overviewkey="Enter Overview Dashboard Key: "
if exist ./\%dashboardkey%.cfg (
for /f "tokens=*" %%a in (./\%dashboardkey%.cfg) do (
    set /a "line = line + 1"
    if !line!==1 set tenant=%%a
    if !line!==2 set owner=%%a
    if !line!==3 set appname=%%a
    if !line!==4 set campaign=%%a
    if !line!==5 set revenue=%%a
    if !line!==6 set promstep=%%a
    if !line!==7 set laststep=%%a
)
if !revenue! == NOREVENUE (set "revflag=False")
set promstep=!promstep:"=\\""\\""""!
set laststep=!laststep:"=\\""\\""""!
echo | set /p=Transforming Marketing Dashboard...
REM Replace all tenant names
powershell -Command "Get-ChildItem -Path ./Transform\Marketing*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'da313') {(Get-Content $_ | ForEach {$_ -replace 'da313', 'da%overviewkey%'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all owner names
powershell -Command "Get-ChildItem -Path ./Transform\Marketing*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyEmail') {(Get-Content $_ | ForEach {$_ -replace 'MyEmail', '!owner!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all appname names
powershell -Command "Get-ChildItem -Path ./Transform\Marketing*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyApp') {(Get-Content $_ | ForEach {$_ -replace 'MyApp', '!appname!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace promotional marketing names
powershell -Command "Get-ChildItem -Path ./Transform\Marketing*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'PromHeaderStep') {(Get-Content $_ | ForEach {$_ -replace 'PromHeaderStep', '!campaign!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace revenue system property name
if !revenue! NEQ NOREVENUE (powershell -Command "Get-ChildItem -Path ./Transform\Marketing*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'revenueproperty') {(Get-Content $_ | ForEach {$_ -replace 'revenueproperty', '!revenue!'}) | Set-Content $_ -encoding UTF8}}")
echo | set /p=.
REM Replace Funnel step names
powershell -Command "Get-ChildItem -Path ./Transform\Marketing*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step1') {(Get-Content $_ | ForEach {$_ -replace 'Step1', '!promstep!'}) | Set-Content $_ -encoding UTF8}}"
echo .
powershell -Command "Get-ChildItem -Path ./Transform\Marketing*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'LastStep') {(Get-Content $_ | ForEach {$_ -replace 'LastStep', '!laststep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=Uploading Marketing Dashboard...
@echo off
REM Upload dashboards
echo | set /p=.
if !revenue! NEQ NOREVENUE (curl -X PUT "https://!tenant!/api/config/v1/dashboards/934b0dce-bbf4-443d-b0f0-e370faeda%overviewkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview1True.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/21e4da5e-d4c7-4816-9d31-6698719da%overviewkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview2True.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/0149758a-c29a-4e3b-96ed-b073438da%overviewkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview3True.json)
echo | set /p=.
if !revenue! EQU NOREVENUE (curl -X PUT "https://!tenant!/api/config/v1/dashboards/934b0dce-bbf4-443d-b0f0-e370faeda%overviewkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview1False.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/935b0dce-bbf4-443d-b0f0-e370faeda%overviewkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview2False.json)
REM Get Key Store Dashboard
echo .
curl -X GET "https://!tenant!/api/config/v1/dashboards/d4db8e38-000f-42df-85a9-d491d34da000" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" > ./Transform/KeyStore.json
REM Update Key Store Dashboard
powershell -Command "Get-ChildItem -Path ./Transform/KeyStore.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '##  ') {(Get-Content $_ | ForEach {$_ -replace '##  ', '## %dashboardkey% !campaign! Campaign Added to %overviewkey%\n##  '}) | Set-Content $_ -encoding UTF8}}"
REM Upload Key Store Dashboard
curl -X PUT "https://!tenant!/api/config/v1/dashboards/d4db8e38-000f-42df-85a9-d491d34da000" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\KeyStore.json
echo *********                             *********
echo ********* Marketing Campaign Deployed *********
echo *********                             *********
)

if not exist ./\%dashboardkey%.cfg (
echo Config file missing
)





