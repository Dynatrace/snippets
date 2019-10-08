@setlocal enableextensions enabledelayedexpansion
@echo off
copy .\*Compare.json .\Transform\
set "tenant="
set "owner="
set "funnel="
set "comparefunnel="
set "appname="
set "compareappname="
set "revenue="
set "comparerevenue="
set "revflag=True"
set "internalappname="
set "compareinternalappname="
set "internalname="
set "compareinternalname="
set "internalextractedname="
set "compareinternalextractedname="
set "f1step="
set "comparef1step="
set "laststep="
set "comparelaststep="
set /a "line = 0"
set "dashboardkey=%2"
if not defined dashboardkey set /p dashboardkey="Enter Dashboard Key: "
set "comparekey=%3"
if not defined comparekey set /p comparekey="Enter Compare Dashboard Key: "
if exist ./\%dashboardkey%.cfg (
for /f "tokens=*" %%a in (./\%dashboardkey%.cfg) do (
    set /a "line = line + 1"
    if !line!==1 set tenant=%%a
    if !line!==2 set owner=%%a
    if !line!==3 set funnel=%%a
    if !line!==4 set appname=%%a
    if !line!==5 set revenue=%%a
    if !line!==6 set f1step=%%a
    if !line!==10 set laststep=%%a
    if !line!==12 set laststep=%%a
    if !line!==14 set laststep=%%a
    if !line!==16 set laststep=%%a
    if !line!==18 set laststep=%%a
    if !line!==20 set laststep=%%a
    if !line!==22 set laststep=%%a
    if !line!==24 set laststep=%%a
    if !line!==26 set laststep=%%a
    if !line!==28 set laststep=%%a
)
)
set /a "line = 0"
if exist ./\%comparekey%.cfg (
for /f "tokens=*" %%a in (./\%comparekey%.cfg) do (
    set /a "line = line + 1"
    if !line!==3 set comparefunnel=%%a
    if !line!==4 set compareappname=%%a
    if !line!==5 set comparerevenue=%%a
    if !line!==6 set comparef1step=%%a
    if !line!==10 set comparelaststep=%%a
    if !line!==12 set comparelaststep=%%a
    if !line!==14 set comparelaststep=%%a
    if !line!==16 set comparelaststep=%%a
    if !line!==18 set comparelaststep=%%a
    if !line!==20 set comparelaststep=%%a
    if !line!==22 set comparelaststep=%%a
    if !line!==24 set comparelaststep=%%a
    if !line!==26 set comparelaststep=%%a
    if !line!==28 set comparelaststep=%%a
)
)
if !revenue! == NOREVENUE (set "revflag=False")
set laststep=!laststep:"=\\""\\""""!
set comparelaststep=!comparelaststep:1"=\\""\\""""!
set f1step=!f1step:"=\\""\\""""!
set comparef1step=!comparef1step:"=\\""\\""""!
REM Get Internal APP ID
curl -X GET "https://!tenant!/api/config/v1/applications/web" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" > ./Transform/ApplicationList.json
powershell -Command "Get-ChildItem -Path ./Transform\ApplicationList.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '\{\"values\"\:\[') {(Get-Content $_ | ForEach {$_ -replace '\{\"values\"\:\[', ''}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\ApplicationList.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '\]\}') {(Get-Content $_ | ForEach {$_ -replace '\]\}', ''}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\ApplicationList.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '\{\"id\"\:') {(Get-Content $_ | ForEach {$_ -replace '\{\"id\"\:', ''}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\ApplicationList.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '\"name\"\:') {(Get-Content $_ | ForEach {$_ -replace '\"name\"\:', ''}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\ApplicationList.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '\"id\"\:') {(Get-Content $_ | ForEach {$_ -replace '\"id\"\:', ''}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\ApplicationList.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '\}') {(Get-Content $_ | ForEach {$_ -replace '\}', ''}) | Set-Content $_ -encoding UTF8}}"
set /a line=1
FOR /L %%A IN (3,4,100) DO (
call :getid !line!
set /a line=line+1
call :getname !line!
set /a line=line+1
set internalappname=!internalappname:"=!
set internalname=!internalname:"=!
if !internalname! == !appname! (set "internalextractedname=!internalappname!")
if !internalname! == !compareappname! (set "compareinternalextractedname=!internalappname!")
)
echo top !internalextractedname!
echo botton !compareinternalextractedname!
echo | set /p=Transforming Compare Dashboards...
REM Replace all internal app names
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'InternalAppID') {(Get-Content $_ | ForEach {$_ -replace 'InternalAppID', '!internalextractedname!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'InternalCompareAppID') {(Get-Content $_ | ForEach {$_ -replace 'InternalCompareAppID', '!compareinternalextractedname!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all tenant names
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'da313') {(Get-Content $_ | ForEach {$_ -replace 'da313', 'da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all owner names
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyEmail') {(Get-Content $_ | ForEach {$_ -replace 'MyEmail', '!owner!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all appname names
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyApp') {(Get-Content $_ | ForEach {$_ -replace 'MyApp', '!appname!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all funnel names
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyFunnel') {(Get-Content $_ | ForEach {$_ -replace 'MyFunnel', '!funnel!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyCompareFunnel') {(Get-Content $_ | ForEach {$_ -replace 'MyCompareFunnel', '!comparefunnel!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyCompareApp') {(Get-Content $_ | ForEach {$_ -replace 'MyCompareApp', '!compareappname!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace time filters
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '-MyCompareTimeh to -MyTimeh') {(Get-Content $_ | ForEach {$_ -replace '-MyCompareTimeh to -MyTimeh', ''}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '-MyTimeh') {(Get-Content $_ | ForEach {$_ -replace '-MyTimeh', ''}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace first step
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'CompareStep1') {(Get-Content $_ | ForEach {$_ -replace 'CompareStep1', '!comparef1step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step1') {(Get-Content $_ | ForEach {$_ -replace 'Step1', '!f1step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace last step
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'CompareLastStep') {(Get-Content $_ | ForEach {$_ -replace 'CompareLastStep', '!comparelaststep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'LastStep') {(Get-Content $_ | ForEach {$_ -replace 'LastStep', '!laststep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace revenue
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'comparerevenueproperty') {(Get-Content $_ | ForEach {$_ -replace 'comparerevenueproperty', '!comparerevenue!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'revenueproperty') {(Get-Content $_ | ForEach {$_ -replace 'revenueproperty', '!revenue!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace headers
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Last MyTime Hours') {(Get-Content $_ | ForEach {$_ -replace 'Last MyTime Hours', ''}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*Compare.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Previous MyTime Hours') {(Get-Content $_ | ForEach {$_ -replace 'Previous MyTime Hours', ''}) | Set-Content $_ -encoding UTF8}}"
echo .
echo Uploading Compare Dashboards...
@echo off
REM Upload dashboards
curl -X PUT "https://!tenant!/api/config/v1/dashboards/56d9f8de-c0d1-4b91-8930-6641a73da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\AppOverviewCompare.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/6e481cc8-bea9-46ba-b1f8-23ebdd1da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelOverview!revflag!Compare.json
if !revenue! NEQ NOREVENUE (curl -X PUT "https://!tenant!/api/config/v1/dashboards/b85ba6e4-e575-4cbb-b7b4-7621bbada%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\RevenueCompare.json)
echo *********                             *********
echo ********* Compare Dashboards Deployed *********
echo *********                             *********
)

if not exist ./\%dashboardkey%.cfg (
echo Config file missing
)
if not exist ./\%comparekey%.cfg (
echo Config file missing
)

exit /b

:getid
FOR /f "tokens=%1 delims=:," %%I IN (./Transform/ApplicationList.json) DO (SET "internalappname=%%I")
exit /b

:getname
FOR /f "tokens=%1 delims=:," %%I IN (./Transform/ApplicationList.json) DO (SET "internalname=%%I")
exit /b






