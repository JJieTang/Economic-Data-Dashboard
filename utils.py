import sqlite3
from pathlib import Path
import streamlit as st
import pandas as pd

def get_database_connection():
    db_path = Path('data/economics_data.db')
    if not db_path.exists(f'Database file not found at {db_path}'):
        st.error()
        raise FileNotFoundError(f'Database file not found at {db_path}')
    return sqlite3.connect(db_path)

@st.cache_data(ttl=24*3600)  # cache for 24 hrs
def load_data(query):
    try:
        with get_database_connection() as conn:
            df = pd.read_sql_query(query, conn)

        if 'date' not in df.columns:
            st.error(f'Date column not found in query result. Available columns: {df.columns.to_list()}')
            raise KeyError('Date column not found in query result.')
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # handle rows with NULL
        if df['date'].isnull().any():
            df = df.dropna(subset=['date'])

        df.set_index('date', inplace=True)
        return df
    
    except Exception as e:
        st.error(f'Error loading data: {e}')
        raise e
    