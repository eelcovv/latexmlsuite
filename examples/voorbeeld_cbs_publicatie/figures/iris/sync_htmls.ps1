Write-Output " ==============  Start syncing highcharts =================== "
Robocopy.exe "highcharts" "../../ccn/highcharts" /E /NDL /XF *.json
Write-Output " --------------          Done!            ------------------- "