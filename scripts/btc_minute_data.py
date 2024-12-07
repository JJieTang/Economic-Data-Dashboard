import os
from sqlalchemy import create_engine, text
import argparse
import time
import yfinance as yf
from datetime import datetime
import traceback
import pandas as pd



# Directory to save data
DATA_DIR = 'data'

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# SQLite database path
DB_PATH = os.path.join(DATA_DIR, 'economics_data.db')

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DB_PATH}')

def get_latest_timestamp():
    '''Get the latest timestamp from the db'''
    try:
        with engine.begin() as conn:
            latest = conn.execute(text('SELECT MAX(Datetime) FROM btc_minute')).scalar()

            if latest:
                # convert to UTC timezone-aware timestamp
                return pd.to_datetime(latest).tz_localize('UTC')
            
            print("No data available in the 'btc_minute' table.")
            return None
    except Exception as e:
        print(f'Error getting latest timestamp: {e}')
        return None


def setup_database():
    '''create the database table if it doesn't exist'''
    create_table_sql = text('''
    CREATE TABLE IF NOT EXISTS btc_minute (
        Datetime TIMESTAMP PRIMARY KEY,
        Open REAL,
        High REAL,
        Low REAL,
        Close REAL,
        Volume REAL,
        Adj_Close REAL,
        fetch_timestamp TIMESTAMP
    )
    ''')

    try:
        with engine.begin() as conn: # ensure transaction are committed or rolled back automatically
            conn.execute(create_table_sql)
    except Exception as e:
        print(f'Error setting up the database: {e}')



def get_btc_minute_date():
    '''Get minute-level data'''
    try:
        # get the latest timestamp
        latest_timestamp = get_latest_timestamp()
        if latest_timestamp:
            print(f'Latest timestamp in database: {latest_timestamp}')

        # download data using yf.download with 1d period and 1m interval
        df = yf.download(
            tickers='BTC-USD',
            interval='1m',
            period='1d'
        )

        if df.empty:
            print('No data received.')
            return None
        
        # filter for only new data if we have existing data
        if latest_timestamp:
            df = df[df.index.tz_localize(None).tz_localize('UTC') > latest_timestamp]
            if df.empty:
                print('No data received.')
                return None   
            print(f'New data shape after filtering: {df.shape}')

        new_df = df.copy()
        new_df.columns = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
        new_df['fetch_timestamp'] = datetime.now()
        new_df.index = new_df.index.tz_localize(None) # convert index to timezone-naive for SQLite storage

        # Append to SQLite with unique index to avoid duplicates
        try:
            new_df.to_sql('btc_minute', engine, if_exists='append', index=True, index_label='Datetime')

            with engine.begin() as conn:
                total_record = conn.execute(text('SELECT COUNT(*) FROM btc_minute')).scalar()

        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                print('Duplicate data point - skipping')
            else:
                print(f'Error saving to database: {e}')

        return df
    
    except Exception as e:
        print(f'Error fetching data: {e}')
        print(f'Traceback: {traceback.format_exc()}')
        return None


def continuous_fetch(interval_seconds=60):
    '''Continuously fetch BTC minute data at specific intervals'''
    try:
        while True:
            try:
                get_btc_minute_date()
            except Exception as e:
                print(f'Error fetching data: {e}')
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print('Stopping data collection')


def main():
    parser = argparse.ArgumentParser(
        description='BTC Minute Data Collection',
        formatter_class=argparse.RawTextHelpFormatter
    )

    mode_choices = ['continuous', 'once']

    parser.add_argument(
        '--mode',
        type=str,
        choices=mode_choices,
        default='once',
        metavar='MODE',
        help='Execution mode:\n'
            '   continuous - Keep running and fetch data at regular intervals\n'
            '   once - Single fetch and exit (default)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default='60',
        metavar='SECONDS',
        help='Interval in seconds between fetches in continuous mode (default: 60)'
    )

    args = parser.parse_args()
    
    # set up database
    setup_database()

    # execute based on mode
    if args.mode == 'continuous':
        continuous_fetch(args.interval)
    else:
        get_btc_minute_date()


if __name__=='__main__':
    main()