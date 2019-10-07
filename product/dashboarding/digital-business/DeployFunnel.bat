@setlocal enableextensions enabledelayedexpansion
@echo off
copy .\*.json .\Transform\
set "posnum="
set "tenant="
set "owner="
set "funnel="
set "appname="
set "revflag=True"
set "revenue="
set "laststep="
set "lasturlstep="
set "f1step="
set "f2step="
set "f3step="
set "f4step="
set "f5step="
set "f6step="
set "f7step="
set "f8step="
set "f9step="
set "f10step="
set "f11step="
set "f12step="
set "f1headerstep="
set "f2headerstep="
set "f3headerstep="
set "f4headerstep="
set "f5headerstep="
set "f6headerstep="
set "f7headerstep="
set "f8headerstep="
set "f9headerstep="
set "f10headerstep="
set "f11headerstep="
set "f12headerstep="
set "f1urlstep="
set "f2urlstep="
set "f3urlstep="
set "f4urlstep="
set "f5urlstep="
set "f6urlstep="
set "f7urlstep="
set "f8urlstep="
set "f9urlstep="
set "f10urlstep="
set "f11urlstep="
set "f12urlstep="
set "stepcount=3"
set /a "line = 0"
set "dashboardkey="
set "overviewkey="
set "dashboardkey=%2"
if not defined dashboardkey set /p dashboardkey="Enter Dashboard Key: "
set "overviewkey=%3"
if not defined overviewkey set /p overviewkey="Enter Overview Dashboard Key: "
set "posnum=%4"
if not defined posnum set /p posnum="Enter Position (2-11): "
if exist ./\%dashboardkey%.cfg (
for /f "tokens=*" %%a in (./\%dashboardkey%.cfg) do (
    set /a "line = line + 1"
    if !line!==1 set tenant=%%a
    if !line!==2 set owner=%%a
    if !line!==3 set funnel=%%a
    if !line!==4 set appname=%%a
    if !line!==5 set revenue=%%a
    if !line!==6 (set f1step=%%a
set f1urlstep=%%a
set f1step=!f1step:"=\\""\\""""!
set f1urlstep=!f1urlstep: =%%20!
set f1urlstep=!f1urlstep:#=%%23!
set f1urlstep=!f1urlstep:"=\\""\\""""!
)
    if !line!==7 set f1headerstep=%%a
    if !line!==8 (set f2step=%%a
set f2urlstep=%%a
set f2step=!f2step:"=\\""\\""""!
set f2urlstep=!f2urlstep: =%%20!
set f2urlstep=!f2urlstep:#=%%23!
set f2urlstep=!f2urlstep:"=\\""\\""""!
)
    if !line!==9 set f2headerstep=%%a
    if !line!==10 (set f3step=%%a
set laststep=%%a
set f3urlstep=%%a
set f3step=!f3step:"=\\""\\""""!
set f3urlstep=!f3urlstep: =%%20!
set f3urlstep=!f3urlstep:#=%%23!
set f3urlstep=!f3urlstep:"=\\""\\""""!
)
    if !line!==11 set f3headerstep=%%a
    if !line!==12 (set f4step=%%a
set laststep=%%a
set f4urlstep=%%a
set f4step=!f4step:"=\\""\\""""!
set f4urlstep=!f4urlstep: =%%20!
set f4urlstep=!f4urlstep:#=%%23!
set f4urlstep=!f4urlstep:"=\\""\\""""!
)
    if !line!==13 set f4headerstep=%%a
    if !line!==14 (set f5step=%%a
set laststep=%%a
set f5urlstep=%%a
set f5step=!f5step:"=\\""\\""""!
set f5urlstep=!f5urlstep: =%%20!
set f5urlstep=!f5urlstep:#=%%23!
set f5urlstep=!f5urlstep:"=\\""\\""""!
)
    if !line!==15 set f5headerstep=%%a
    if !line!==16 (set f6step=%%a
set laststep=%%a
set f6urlstep=%%a
set f6step=!f6step:"=\\""\\""""!
set f6urlstep=!f6urlstep: =%%20!
set f6urlstep=!f6urlstep:#=%%23!
set f6urlstep=!f6urlstep:"=\\""\\""""!
)
    if !line!==17 set f6headerstep=%%a
    if !line!==18 (set f7step=%%a
set laststep=%%a
set f7urlstep=%%a
set f7step=!f7step:"=\\""\\""""!
set f7urlstep=!f7urlstep: =%%20!
set f7urlstep=!f7urlstep:#=%%23!
set f7urlstep=!f7urlstep:"=\\""\\""""!
)
    if !line!==19 set f7headerstep=%%a
    if !line!==20 (set f8step=%%a
set laststep=%%a
set f8urlstep=%%a
set f8step=!f8step:"=\\""\\""""!
set f8urlstep=!f8urlstep: =%%20!
set f8urlstep=!f8urlstep:#=%%23!
set f8urlstep=!f8urlstep:"=\\""\\""""!
)
    if !line!==21 set f8headerstep=%%a
    if !line!==22 (set f9step=%%a
set laststep=%%a
set f9urlstep=%%a
set f9step=!f9step:"=\\""\\""""!
set f9urlstep=!f9urlstep: =%%20!
set f9urlstep=!f9urlstep:#=%%23!
set f9urlstep=!f9urlstep:"=\\""\\""""!
)
    if !line!==23 set f9headerstep=%%a
    if !line!==24 (set f10step=%%a
set laststep=%%a
set f10urlstep=%%a
set f10step=!f10step:"=\\""\\""""!
set f10urlstep=!f10urlstep: =%%20!
set f10urlstep=!f10urlstep:#=%%23!
set f10urlstep=!f10urlstep:"=\\""\\""""!
)
    if !line!==25 set f10headerstep=%%a
    if !line!==26 (set f11step=%%a
set laststep=%%a
set f11urlstep=%%a
set f11step=!f11step:"=\\""\\""""!
set f11urlstep=!f11urlstep: =%%20!
set f11urlstep=!f11urlstep:#=%%23!
set f11urlstep=!f11urlstep:"=\\""\\""""!
)
    if !line!==27 set f11headerstep=%%a
    if !line!==28 (set f12step=%%a
set laststep=%%a
set f12urlstep=%%a
set f12step=!f12step:"=\\""\\""""!
set f12urlstep=!f12urlstep: =%%20!
set f12urlstep=!f12urlstep:#=%%23!
set f12urlstep=!f12urlstep:"=\\""\\""""!
)
    if !line!==29 set f12headerstep=%%a
)
if !revenue! == NOREVENUE (set "revflag=False")
set /a "stepcount = (line - 5)/2"
set laststep=!laststep:"=\\""\\""""!
echo | set/p=Transforming Dashboards...
REM Replace all tenant names
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'da313') {(Get-Content $_ | ForEach {$_ -replace 'da313', 'da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyTenant') {(Get-Content $_ | ForEach {$_ -replace 'MyTenant', '!tenant!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all owner names
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyEmail') {(Get-Content $_ | ForEach {$_ -replace 'MyEmail', '!owner!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all funnel names
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyFunnel') {(Get-Content $_ | ForEach {$_ -replace 'MyFunnel', '!funnel!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyCompareFunnel') {(Get-Content $_ | ForEach {$_ -replace 'MyCompareFunnel', '!funnel!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all timeframes
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyTime') {(Get-Content $_ | ForEach {$_ -replace 'MyTime', '2'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyCompareTime') {(Get-Content $_ | ForEach {$_ -replace 'MyCompareTime', '4'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace all appname names
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'MyApp') {(Get-Content $_ | ForEach {$_ -replace 'MyApp', '!appname!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace promotional marketing names
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'PromHeaderStep') {(Get-Content $_ | ForEach {$_ -replace 'PromHeaderStep', 'No Active'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
REM Replace revenue system property name
if !revenue! NEQ NOREVENUE (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'comparerevenueproperty') {(Get-Content $_ | ForEach {$_ -replace 'comparerevenueproperty', '!revenue!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'revenueproperty') {(Get-Content $_ | ForEach {$_ -replace 'revenueproperty', '!revenue!'}) | Set-Content $_ -encoding UTF8}}")
echo | set /p=.
REM Replace Funnel step names
if defined f10step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step10') {(Get-Content $_ | ForEach {$_ -replace '22Step10', '22!f10urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step10') {(Get-Content $_ | ForEach {$_ -replace 'Step10', '!f10step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader10') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader10', '!f10headerstep!'}) | Set-Content $_ -encoding UTF8}}")
if defined f11step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step11') {(Get-Content $_ | ForEach {$_ -replace '22Step11', '22!f11urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step11') {(Get-Content $_ | ForEach {$_ -replace 'Step11', '!f11step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader11') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader11', '!f11headerstep!'}) | Set-Content $_ -encoding UTF8}}")
if defined f12step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step12') {(Get-Content $_ | ForEach {$_ -replace 'Step12', '!f12step!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader12') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader12', '!f12headerstep!'}) | Set-Content $_ -encoding UTF8}}")
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step1') {(Get-Content $_ | ForEach {$_ -replace '22Step1', '22!f1urlstep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step2') {(Get-Content $_ | ForEach {$_ -replace '22Step2', '22!f2urlstep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step3') {(Get-Content $_ | ForEach {$_ -replace '22Step3', '22!f3urlstep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader1') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader1', '!f1headerstep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader2') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader2', '!f2headerstep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader3') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader3', '!f3headerstep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'CompareStep1') {(Get-Content $_ | ForEach {$_ -replace 'CompareStep1', '!f1step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step1') {(Get-Content $_ | ForEach {$_ -replace 'Step1', '!f1step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step2') {(Get-Content $_ | ForEach {$_ -replace 'Step2', '!f2step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step3') {(Get-Content $_ | ForEach {$_ -replace 'Step3', '!f3step!'}) | Set-Content $_ -encoding UTF8}}"
if defined f4step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step4') {(Get-Content $_ | ForEach {$_ -replace '22Step4', '22!f4urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step4') {(Get-Content $_ | ForEach {$_ -replace 'Step4', '!f4step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader4') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader4', '!f4headerstep!'}) | Set-Content $_ -encoding UTF8}}")
if defined f5step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step5') {(Get-Content $_ | ForEach {$_ -replace '22Step5', '22!f5urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step5') {(Get-Content $_ | ForEach {$_ -replace 'Step5', '!f5step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader5') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader5', '!f5headerstep!'}) | Set-Content $_ -encoding UTF8}}")
if defined f6step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step6') {(Get-Content $_ | ForEach {$_ -replace '22Step6', '22!f6urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step6') {(Get-Content $_ | ForEach {$_ -replace 'Step6', '!f6step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader6') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader6', '!f6headerstep!'}) | Set-Content $_ -encoding UTF8}}")
if defined f7step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step7') {(Get-Content $_ | ForEach {$_ -replace '22Step7', '22!f7urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step7') {(Get-Content $_ | ForEach {$_ -replace 'Step7', '!f7step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader7') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader7', '!f7headerstep!'}) | Set-Content $_ -encoding UTF8}}")
if defined f8step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step8') {(Get-Content $_ | ForEach {$_ -replace '22Step8', '22!f8urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step8') {(Get-Content $_ | ForEach {$_ -replace 'Step8', '!f8step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader8') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader8', '!f8headerstep!'}) | Set-Content $_ -encoding UTF8}}")
if defined f9step (powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22Step9') {(Get-Content $_ | ForEach {$_ -replace '22Step9', '22!f9urlstep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'Step9') {(Get-Content $_ | ForEach {$_ -replace 'Step9', '!f9step!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'StepHeader9') {(Get-Content $_ | ForEach {$_ -replace 'StepHeader9', '!f9headerstep!'}) | Set-Content $_ -encoding UTF8}}")
set lasturlstep=!laststep: =%%20!
set lasturlstep=!lasturlstep:#=%%23!
set lasturlstep=!lasturlstep:/=%%2F!
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '22LastStep') {(Get-Content $_ | ForEach {$_ -replace '22LastStep', '22!lasturlstep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'CompareLastStep') {(Get-Content $_ | ForEach {$_ -replace 'CompareLastStep', '!laststep!'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\*.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'LastStep') {(Get-Content $_ | ForEach {$_ -replace 'LastStep', '!laststep!'}) | Set-Content $_ -encoding UTF8}}"
echo | set /p=.
powershell -Command "Get-ChildItem -Path ./Transform\Overview!revflag!.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'dashboard;id=fbe8d3b1-ccb9-480c-9e5d-0e1b8b3da%dashboardkey%') {(Get-Content $_ | ForEach {$_ -replace 'dashboard;id=fbe8d3b1-ccb9-480c-9e5d-0e1b8b3da%dashboardkey%', 'dashboard;id=fbe8d3b1-ccb9-480c-9e5d-0e1b8b3da%overviewkey%'}) | Set-Content $_ -encoding UTF8}}"
echo .
echo | set /p=Uploading Dashboards...
@echo off
REM Upload dashboards
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/65312f05-ca6c-4896-b2b4-1bc8ce3da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\Funnel!stepcount!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/0d81ee7c-f7ba-4626-a087-60b76ecda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ConversionAnalysisF!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/c16cb11a-22be-41ab-a336-412369ada%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\DuratioinAnalysis!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7afde609-dbbe-486f-b2c0-0bde4c4da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\AbandonsAnalysis!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/8a487b1b-c491-41f7-adf2-7460165da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ErrorAnalysis!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/ba9ecfe5-e7ec-451d-a187-060a724da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ConversionAnalysisO!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7eb2b38c-bae4-46c5-8955-c3eabb9da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\RageAnalysis!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f063e1f-e142-44f1-81a0-523f7e5da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\NonEngagedAnalysis!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\Overview!revflag!.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/6e481cc8-bea9-46ba-b1f8-23ebdd1da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelOverview!revflag!Compare.json
echo | set /p=.
if !revenue! NEQ NOREVENUE (curl -X PUT "https://!tenant!/api/config/v1/dashboards/f8c73b94-d5ef-4cbf-bcb8-d866c91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\RevenueAnalysis.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/834e194e-a9bc-406a-9696-40afcc0da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\RiskRevenueAnalysis.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/361e6756-3227-43bb-9fdd-69305feda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\LostRevenueAnalysis.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/3aa5be20-8833-4af1-a847-2f84cb5da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ExecutiveOverview1True.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/21a04cb8-804b-4755-b530-d4c40feda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ExecutiveOverview2True.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/dbd5f52f-bd79-45fd-b45c-7f1b171da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ExecutiveOverview3True.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/934b0dce-bbf4-443d-b0f0-e370faeda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview1True.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/21e4da5e-d4c7-4816-9d31-6698719da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview2True.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/0149758a-c29a-4e3b-96ed-b073438da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview3True.json)
echo | set /p=.
if !revenue! EQU NOREVENUE (curl -X PUT "https://!tenant!/api/config/v1/dashboards/3aa5be20-8833-4af1-a847-2f84cb5da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ExecutiveOverview1False.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/dbd5f52f-bd79-45fd-b45c-7f1b171da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\ExecutiveOverview2False.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/934b0dce-bbf4-443d-b0f0-e370faeda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview1False.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/935b0dce-bbf4-443d-b0f0-e370faeda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\MarketingOverview2False.json)
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/1fc1af04-a855-43cb-855c-c32f4ecda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep1.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/2662ddb8-dd6a-4345-a1bc-7ff069eda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep2.json
echo | set /p=.
if defined f4step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json)
echo | set /p=.
if defined f5step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json)
echo | set /p=.
if defined f6step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac15-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep5.json)
echo | set /p=.
if defined f7step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac15-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep5.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac06-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep6.json)
echo | set /p=.
if defined f8step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac15-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep5.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac06-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep6.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac07-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep7.json)
echo | set /p=.
if defined f9step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac15-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep5.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac06-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep6.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac07-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep7.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac08-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep8.json)
echo | set /p=.
if defined f10step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac15-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep5.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac06-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep6.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac07-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep7.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac08-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep8.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac09-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep9.json)
echo | set /p=.
if defined f11step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac15-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep5.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac06-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep6.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac07-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep7.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac08-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep8.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac09-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep9.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac10-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep10.json)
echo | set /p=.
if defined f12step (curl -X PUT "https://!tenant!/api/config/v1/dashboards/10a69069-74c2-4eba-b18a-6856d91da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep3.json
curl -X PUT "https://!tenant!/api/config/v1/dashboards/7f64e3ef-239c-416a-b3a4-66b99beda%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep4.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac15-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep5.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac06-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep6.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac07-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep7.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac08-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep8.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac09-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep9.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac10-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep10.json
echo | set /p=.
curl -X PUT "https://!tenant!/api/config/v1/dashboards/a7340848-3f03-4155-ac11-d8ea4a7da%dashboardkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\FunnelAnalysisStep11.json)
REM Get App Overview Dashboard
echo .
curl -X GET "https://%tenant%/api/config/v1/dashboards/fbe8d3b1-ccb9-480c-9e5d-0e1b8b3da%overviewkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" > ./Transform/TempOverview.json
REM Update Overview Dashboard
if %posnum% EQU 2 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '2 Logs') {(Get-Content $_ | ForEach {$_ -replace '2 Logs', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'logmonitoring') {(Get-Content $_ | ForEach {$_ -replace 'logmonitoring', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 3 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '3 Smartscape') {(Get-Content $_ | ForEach {$_ -replace '3 Smartscape', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'smartscape') {(Get-Content $_ | ForEach {$_ -replace 'smartscape', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 4 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '4 Diagnostics') {(Get-Content $_ | ForEach {$_ -replace '4 Diagnostics', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'diagnostictools') {(Get-Content $_ | ForEach {$_ -replace 'diagnostictools', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 5 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '5 Services') {(Get-Content $_ | ForEach {$_ -replace '5 Services', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'newservices') {(Get-Content $_ | ForEach {$_ -replace 'newservices', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 6 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '6 Databases') {(Get-Content $_ | ForEach {$_ -replace '6 Databases', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'newdatabases') {(Get-Content $_ | ForEach {$_ -replace 'newdatabases', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 7 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '7 Hosts') {(Get-Content $_ | ForEach {$_ -replace '7 Hosts', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'newhosts') {(Get-Content $_ | ForEach {$_ -replace 'newhosts', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 8 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '8 Technologies') {(Get-Content $_ | ForEach {$_ -replace '8 Technologies', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'newprocessessummary') {(Get-Content $_ | ForEach {$_ -replace 'newprocessessummary', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 9 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '9 Deploy') {(Get-Content $_ | ForEach {$_ -replace '9 Deploy', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'deploy') {(Get-Content $_ | ForEach {$_ -replace 'deploy', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 10 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '10 Applications') {(Get-Content $_ | ForEach {$_ -replace '10 Applications', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'uemapplications') {(Get-Content $_ | ForEach {$_ -replace 'uemapplications', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
if %posnum% EQU 11 (powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '11 Sessions') {(Get-Content $_ | ForEach {$_ -replace '11 Sessions', '%funnel% Overview'}) | Set-Content $_ -encoding UTF8}}"
powershell -Command "Get-ChildItem -Path ./Transform\TempOverview.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern 'usersearchoverview') {(Get-Content $_ | ForEach {$_ -replace 'usersearchoverview', 'dashboard;id=6e481cc8-bea9-46ba-b1f8-23ebcc1da%dashboardkey%'}) | Set-Content $_ -encoding UTF8}}")
REM Upload Overview Dashboard
curl -X PUT "https://%tenant%/api/config/v1/dashboards/fbe8d3b1-ccb9-480c-9e5d-0e1b8b3da%overviewkey%" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\TempOverview.json
REM Get Key Store Dashboard
curl -X GET "https://%tenant%/api/config/v1/dashboards/d4db8e38-000f-42df-85a9-d491d34da000" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" > ./Transform/KeyStore.json
REM Update Key Store Dashboard
powershell -Command "Get-ChildItem -Path ./Transform/KeyStore.json -recurse | ForEach {If (Get-Content $_.FullName | Select-String -Pattern '##  ') {(Get-Content $_ | ForEach {$_ -replace '##  ', '## %dashboardkey% !funnel! Funnel Added to %overviewkey% at Position %posnum%\n##  '}) | Set-Content $_ -encoding UTF8}}"
REM Upload Key Store Dashboard
curl -X PUT "https://%tenant%/api/config/v1/dashboards/d4db8e38-000f-42df-85a9-d491d34da000" -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token %1" -H "Content-Type: application/json; charset=utf-8" -d @./Transform\KeyStore.json
if !posnum! NEQ 1 (echo .
echo *********                *********
echo ********* Funnel Created *********
echo *********                *********)
)
if not exist ./\%dashboardkey%.cfg (
echo Config file missing
)






