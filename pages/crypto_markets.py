import streamlit as st
from utils import load_btc_data, create_figure, get_chart_layout
import plotly.graph_objects as go

def show():
    st.header('Cryptocurrency Markets')

    try:
        
        # BTC data
        btc_data = load_btc_data()

        # Price chart
        btc_traces = [
            {'data':'btc_data', 'column':'Close', 'name':'BTC/USD', 'line':{'color':'#FFBA08', 'width':2}}
        ]
        fig_btc = create_figure(btc_traces)
        layout = get_chart_layout('BTC/USD Price')
        fig_btc.update_layout(layout)
        st.plotly_chart(fig_btc, use_container_width=True)
        st.markdown("""
        * **Alternative Asset Class**: Cryptocurrencies represent a distinct asset class that historically has shown lower correlation with traditional investments like stocks and bonds, potentially offering portfolio diversification benefits.
        * **Real-Time Data Pipeline**: This dashboard displays minute-level BTC/USD data that updates with a 2-3 minute lag, demonstrating an automated data pipeline for near real-time market monitoring.
        """)

        # Volume chart
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Bar(x=btc_data['Datetime'], y=btc_data['Volume'], name='Volume', marker_color='#FFBA08'))
        layout = get_chart_layout('BTC/USD Trading Volume')
        fig_volume.update_layout(layout)
        st.plotly_chart(fig_volume, use_container_width=True)

        # Last 5 values table
        st.subheader('Latest BTC/USD Data')
        last_5_data = btc_data.head(5)[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
        last_5_data = last_5_data.round(2)
        st.dataframe(last_5_data)
    
    except Exception as e:
        st.error(f'Error in Crypto Markets: {e}')