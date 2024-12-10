import sqlite3
from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

def get_database_connection():
    db_path = Path('/Economic-Data-Dashboard/data/economics_data.db')
    db_path.parent.mkdir(parents=True, exist_ok=True)    
    if not db_path.exists():
        conn = sqlite3.connect(db_path)
        conn.close()
        st.success(f'Database initialized at {db_path}')
        '''
        st.error(f'Database file not found at {db_path}')
        raise FileNotFoundError(f'Database file not found at {db_path}')        
        '''
    # Return a connection to the database
    try:
        return sqlite3.connect(db_path)
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        raise

@st.cache_data(ttl=24*3600)  # cache for 24 hrs
def load_data(query):
    try:
        with get_database_connection() as conn:
            df = pd.read_sql_query(query, conn)

        if 'date' not in df.columns:
            st.error(f'Date column not found in query result. Available columns: {df.columns.to_list()}')
            raise KeyError('Date column not found in query result.')
        
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df
    
    except Exception as e:
        st.error(f'Error loading data: {e}')
        raise e
    

def load_btc_data():
    try:
        with get_database_connection() as conn:
            query = '''
            SELECT Datetime, Open, High, Low, Close, Volume
            FROM btc_minute
            ORDER BY Datetime DESC
            LIMIT 300            
            '''
            df = pd.read_sql_query(query, conn)
            #conn.close()
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            df.set_index('Datetime', inplace=True)
        return df
    except Exception as e:
        st.error(f'Error loading BTC data: {e}')
        raise e
    

def get_file_update_time(filepath):
    try:
        timestamp = Path(filepath).stat().st_mtime
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return 'File not found'
    

def get_recent_logs():
    try:
        with open('/var/log/cron.log', 'r') as f:
            logs = f.readlines()
            return logs[-10:] if logs else ['No logs available.']
    except:
        return ['Log file not accessible.']


def create_figure(traces):
    try: 
        fig = go.Figure()
        for trace in traces:
            
            fig.add_trace(go.Scatter(
                x=trace['data'].index,
                y=trace['data'][trace['column']],
                name=trace['name'],
                line=trace['line']
            ))
        return fig
    except Exception as e:
        st.error(f'Error create figure: {e}')
        raise e


def get_chart_layout(title):
    return dict(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text=title,
            font=dict(color='#00FFF0', size=20)
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='rgba(26,28,36,0.8)'
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#1a1c24',
            font_size=14,
            font_family='monospace'
        ),
        xaxis=dict(
            gridcolor='#2d3139',
            showgrid=True,
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor='#2d3139',
            showgrid=True,
            gridwidth=1
        )
    )


           
    