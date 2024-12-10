#!/bin/bash

# direct all output (stdout and stderr) to the log file
exec >> /var/log/cron.log 2>&1

service cron start
echo "$(date): Starting cron service..."

# Check if database exists and has data
if [ ! -f "/Economic-Data-Dashboard/data/economics_data.db" ] || [ ! -s "/Economic-Data-Dashboard/data/economics_data.db" ]; then
    echo "$(date): No existing data found. Running initial data collection..."
fi

# Start Streamlit
echo "$(date): Starting Streamlit..."
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0