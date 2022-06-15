echo " ==============  Start syncing highcharts =================== "
rsync -arv highcharts/ ../../ccn/highcharts --exclude "*.json"
echo " --------------             Done!         ------------------- "
