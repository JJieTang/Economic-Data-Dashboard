FROM python:3.11-slim

WORKDIR /Economic-Data-Dashboard

# install cron and other required system packages
RUN apt-get update && apt-get install -y cron curl sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt .
RUN pip install -no-cache-dir -r requirements.txt

# copy application files (excluding data directory)
COPY app.py .
COPY utils.py .
COPY scripts/ scripts/
COPY pages/ pages/

# make shell scripts runable
RUN chmod +x scripts/minute_job.sh scripts/daily_job.sh

# set up environment for cron
RUN echo 'SHELL=/bin/bash\n\
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\n\
# Run every minute
* * * * cd /Economic-Data-Dashboard && ./scripts/minute_job.sh >> /var/log/cron.log 2>&1\n\
# Run daily at midnight
0 0 * * cd /Economic-Data-Dashboard && ./scripts/daily_job.sh >> /var/log/cron.log 2>&1' | crontab -

# create log file and set permissions
RUN touch /var/log/cron.log && \
    chmod 0666 /var/log/cron.log

# create data directory
RUN mkdir -p /Economic-Data-Dashboard/data

# create startup script with data check
RUN echo '#!/bin/bash\n\
service cron start\n\
echo "$(date): Starting cron service..." >> /var/log/cron.log\n\
\n\
# Check if database exists and has data\n\
if [ ! -f /Economic-Data-Dashboard/data/economics_data.db ] || [ ! -s /Economic-Data-Dashboard/data/economics_data.db]; then\n\
    echo "$(date): No existing data found. Running initial data collection..." >> /var/log/cron.log\n\
fi\n\
\n\
echo "$(date): Starting Streamlit..." >> /var/log/cron.log\n\
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n\
' > /Economic-Data-Dashboard/start.sh && \
    chmod +x /Economic-Data-Dashboard/start.sh

# Expose Streamlit port
EXPOSE 8501

# Health check using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period= --retries= \ 
    CMD curl --fail http://localhost:8501/_stcore/Health

# Run both cron and Streamlit
CMD ["/Economic-Data-Dashboard/start.sh"]
