Write-Output " ==============  Start syncing highcharts =================== "
Robocopy.exe "highcharts" "../../ccn/highcharts" /E /NDL /XF *.json *.svg
Write-Output " --------------          Done!            ------------------- "