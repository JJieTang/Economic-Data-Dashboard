#!/bin/bash

# direct all output (stdout and stderr) to the log file
exec >> /var/log/cron.log 2>&1

cd /Economic-Data-Dashboard

echo 'Starting minute data collection at $(date)' 

echo 'Running BTC minute data retrieval...'
python scripts/btc_minute_data.py

echo 'Minute data collection completed at $(date)'