import streamlit as st
from utils import create_figure, get_chart_layout, load_data


def show():
    st.header('Currency Markets')

    try:

        #Dollar Index
        dollar_query = '''
        SELECT *
        FROM dtwexbgs
        ORDER BY date
        '''
        dollar_index = load_data(dollar_query)
        dollar_traces = [
            {'data':dollar_index, 'column':'DTWEXBGS', 'name':'Dollar Index', 'line':{'color':'#FFBA08', 'width':2}}
        ]
        fig_dollar = create_figure(dollar_traces)
        layout = get_chart_layout('Trade Weighted U.S. Dollar Index')
        fig_dollar.update_layout(layout)
        st.plotly_chart(fig_dollar, use_container_width=True)
        st.markdown("""
        * **Market Measure**: The Trade Weighted Dollar Index shows the U.S. dollar's strength against major world currencies. A rising index indicates dollar strengthening, falling means weakening.
        * **Economic Impact**: A stronger dollar makes U.S. exports more expensive but imports cheaper, affecting trade balance and inflation.
        * **Global Context**: Dollar strength often reflects relative economic performance and interest rate differences between the U.S. and other countries.
        * **Retail Investor**: During strong dollar periods, consider U.S. companies focused on domestic market or importers. When dollar weakens, look at U.S. exporters and international stocks that benefit from currency translation gains.
        """)

        # EUR/USD
        eurusd_query = '''
        SELECT *
        FROM dexuseu
        ORDER BY date
        '''
        eurusd = load_data(eurusd_query)
        eurusd_traces = [
            {'data':eurusd, 'column':'DEXUSEU', 'name':'EUR/USD', 'line':{'color':'#FFBA08', 'width':2}}
        ]
        fig_eurusd = create_figure(eurusd_traces)
        layout = get_chart_layout('EUR/USD Exchange Rate')
        fig_eurusd.update_layout(layout)
        st.plotly_chart(fig_eurusd, use_container_width=True)
        st.markdown("""
        * **Exchange Rate**: EUR/USD shows how many dollars one euro can buy. Higher rate means stronger euro/weaker dollar, lower rate means weaker euro/stronger dollar.
        * **Policy Impact**: The rate reflects differences in monetary policy between the Federal Reserve and European Central Bank, as well as relative economic strength.
        * **Trade Effects**: A stronger euro benefits U.S. exporters to Europe but makes European goods more expensive for U.S. consumers, and vice versa.
        * **Retail Investor**: Consider European stocks when EUR/USD is low (European exporters benefit), and U.S. stocks when EUR/USD is high (U.S. exporters benefit). For travelers, a high EUR/USD means expensive European trips, while low rates make European travel more affordable.
        """)

    except Exception as e:
        st.error(f'Error in Currency Market: {e}')
