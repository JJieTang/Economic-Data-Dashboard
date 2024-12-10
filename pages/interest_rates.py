import streamlit as st
from utils import load_data, create_figure, get_chart_layout

def show():
    st.header('Interest Rates')

    try:

        # Fed Funds Rate
        fedfunds_query = '''
        SELECT date, FEDFUNDS/100 as FEDFUNDS
        FROM fedfunds
        ORDER BY date
        '''
        fedfunds = load_data(fedfunds_query)
        fedfunds_traces = [
            {'data':fedfunds, 'column':'FEDFUNDS', 'name':'Federal Funds Rate', 'line':{'color':'#FFBA08', 'width':2}}
        ]
        fig_fedfunds = create_figure(fedfunds_traces)
        layout = get_chart_layout('Federal Funds Rate')
        layout.update(yaxis=dict(tickformat='.1%'))
        fig_fedfunds.update_layout(layout)
        st.plotly_chart(fig_fedfunds, use_container_width=True)
        st.markdown("""
        * **Policy Rate**: The Federal Funds Rate is the key interest rate that banks charge each other for overnight loans, serving as a benchmark for other interest rates in the economy.
        * **Economic Impact**: When the Fed raises rates, it aims to control inflation by making borrowing more expensive, which can slow economic growth and spending.
        * **Market Effect**: Rate changes affect various markets - higher rates typically strengthen the dollar and can pressure stock valuations, especially for growth companies.
        * **Retail Investor**: When rates are rising, consider increasing allocation to financial sector stocks and short-duration bonds. During rate cuts, growth stocks and longer-duration bonds often perform better.
        """)

        # Treasury Yields
        yields_1y_query = '''
        SELECT date, DGS1/100 as DGS1
        FROM dgs1
        ORDER BY date
        '''
        yields_5y_query = '''
        SELECT date, DGS5/100 as DGS5
        FROM dgs5
        ORDER BY date       
        '''
        yields_10y_query = '''
        SELECT date, DGS10/100 as DGS10
        FROM dgs10
        ORDER BY date       
        '''
        yields_1y = load_data(yields_1y_query)
        yields_5y = load_data(yields_5y_query)
        yields_10y = load_data(yields_10y_query)
        treasury_traces = [
            {'data':yields_1y, 'column':'DGS1', 'name':'1-Year', 'line':{'color':'#FFBA08', 'width':2}},
            {'data':yields_5y, 'column':'DGS5', 'name':'5-Year', 'line':{'color':'#00FFF0', 'width':2}},
            {'data':yields_10y, 'column':'DGS10', 'name':'10-Year', 'line':{'color':'#FF00FF', 'width':2}}   
        ]
        fig_treasury = create_figure(treasury_traces)
        layout = get_chart_layout('Treasury Yields')
        layout.update(yaxis=dict(tickformat='.1%'))
        fig_treasury.update_layout(layout)
        st.plotly_chart(fig_treasury)
        st.markdown("""
        * **Yield Curve**: Treasury yields show interest rates at different maturities. Normally, longer-term yields are higher than shorter-term ones, reflecting greater uncertainty over longer periods.
        * **Economic Signal**: When short-term yields exceed long-term yields (curve inversion), it often signals economic concerns and has historically preceded recessions.
        * **Bond Prices**: Remember that bond prices move inversely to yields - when yields rise, existing bond prices fall, and vice versa.
        * **Retail Investor**: Consider building a "ladder" of bonds with different maturities to manage interest rate risk. During yield curve inversion, it might be prudent to increase cash reserves and focus on high-quality, shorter-duration bonds.
        """)

    except Exception as e:
        st.error(f'Error in Interest Rate: {e}')
