@echo off
set /p wvs_path=please input wvs path,eg: [D:\Program Files (x86)\Web Vulnerability Scanner 10]::
for /f %%i in (result.txt) do (
set pp=%%i
echo running   %%i ......
"%wvs_path%\wvs_console.exe" /scan %%i /Profile default /SaveFolder d:\wwwscanresult\%pp%\ /save /Verbose --EnablePortScanning=true --UseCSA=true --RobotsTxt=true --CaseInsensitivePaths=true
)