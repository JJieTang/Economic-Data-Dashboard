#!/bin/bash

# direct all output (stdout and stderr) to the log file
exec >> /var/log/cron.log 2>&1

cd /Economic-Data-Dashboard

echo 'Starting daily data collection at $(date)'

echo 'Running FRED data retrieval...'
python scripts/fred_data_retrieval.py 

echo 'Daily data collection completed at $(date)'