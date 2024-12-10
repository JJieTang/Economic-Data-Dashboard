import streamlit as st
from utils import load_data, create_figure, get_chart_layout


def show():
    st.header('Economic Indicators')

    try:
        # GDP data
        gdp_real_query = '''
        SELECT * 
        FROM gdpc1
        ORDER BY date
        '''
        gdp_potential_query = '''
        SELECT * 
        FROM gdppot
        ORDER BY date
        '''
        gdp_real = load_data(gdp_real_query)
        gdp_potential = load_data(gdp_potential_query)
        gdp_traces = [
            {'data': gdp_real, 'column':'gdpc1_us_yoy', 'name':'Real GDP Growth', 'line': {'color':'#FFBA08', 'width':2}},
            {'data': gdp_potential, 'column':'gdppot_us_yoy', 'name':'Potential GDP Growth', 'line': {'color':'#00FFF0', 'width':2}},
        ]
        fig_gdp = create_figure(gdp_traces)
        layout = get_chart_layout('U.S. Real GDP vs Potential GDP Growth (Year-over-Year)')
        layout.update(yaxis=dict(tickformat='.1%'))
        fig_gdp.update_layout(layout)
        st.plotly_chart(fig_gdp, use_container_width=True)
        st.markdown("""
        * **Real vs Potential GDP**: Real GDP represents actual economic output, while Potential GDP indicates the economy's maximum sustainable output. The gap between them helps identify economic cycles and capacity utilization.
        * **Growth Dynamics**: Comparing actual growth to potential growth reveals whether the economy is operating above or below its sustainable capacity, which can signal inflationary pressures or economic slack.
        * **Policy Implications**: Large deviations between real and potential GDP often trigger monetary or fiscal policy responses to help stabilize the economy and maintain sustainable growth.
        * **Retail Investor**: Large gaps between Real and Potential GDP often precede policy changes - if Real GDP is much higher, prepare for potential rate hikes; if much lower, expect stimulus measures. Consider adjusting your portfolio's risk exposure accordingly.
        """)

        # Unemployment Rate
        unemployment_query = '''
        SELECT date, UNRATE/100 as UNRATE
        FROM unrate
        ORDER BY date
        '''
        unemployment = load_data(unemployment_query)
        unemployment_traces = [
            {'data':'unemployment', 'column':'UNRATE', 'name':'Unemployment Rate', 'line':{'color':'#FFBA08', 'width':2}}
        ]
        fig_unemployment = create_figure(unemployment_traces)
        layout = get_chart_layout('U.S. Unemployment Rate')
        layout.update(yaxis=dict(tickformat='.1%'))
        fig_unemployment.update_layout(layout)
        st.plotly_chart(fig_unemployment, use_container_width=True)
        st.markdown("""
        * **Importance**: The U.S. unemployment rate is a vital economic indicator, reflecting labor market health and overall economic performance. It helps shape policies for sustainable growth.
        * **Recent Trend**: Following a sharp spike around 2020 (due to the COVID-19 pandemic), unemployment has declined significantly, stabilizing near historical lows, showcasing labor market resilience.
        * **Role of the Central Bank**: The Federal Reserve aims to maintain maximum employment as part of its dual mandate. By adjusting interest rates and using monetary policy tools, it strives to balance low unemployment with price stability, ensuring sustainable economic growth.
        * **Retail Investor**: Rising unemployment often precedes market downturns - consider increasing cash reserves or defensive positions when unemployment starts trending up. Very low unemployment might signal market peaks, as it often leads to wage inflation and subsequent rate hikes.
        """)

        # US CPI data
        cpi_core_query = '''
        SELECT *
        FROM cpilfesl
        ORDER BY date
        '''
        cpi_all_query = '''
        SELECT *
        FROM cpiaucsl
        ORDER BY date
        '''
        cpi_core = load_data(cpi_core_query)
        cpi_all = load_data(cpi_all_query)
        cpi_traces = [
            {'data':'cpi_core', 'column':'cpi_core_yoy', 'name':'Core CPI', 'line':{'color':'#FFBA08', 'width':2}},
            {'data':'cpi_all', 'column':'cpi_all_yoy', 'name':'All Items CPI', 'line':{'color':'#00FFF0', 'width':2}}
        ]
        fig_cpi = create_figure(cpi_traces)
        layout = get_chart_layout('US Inflation/Consumer Price Index (Year-over-Year Change)')
        layout.update(yaxis=dict(tickformat='.1%'))
        fig_cpi.update_layout(layout)
        st.plotly_chart(fig_cpi, use_container_width=True)
        st.markdown("""
        * **Rising Costs of Living**: High inflation, especially post-2020, reduces household purchasing power, prompting families to reallocate budgets toward essentials like food, energy, and housing.
        * **Planning Ahead for Potential Rate Hikes**: Persistent inflation increases the likelihood of future Federal Reserve rate hikes, which could raise borrowing costs for mortgages, credit cards, and loans, influencing current savings and spending decisions.
        * **Delayed Major Purchases**: Households may postpone big-ticket purchases (like homes or cars) in anticipation of potential increases in financing costs or tighter credit availability.
        * **Retail Investor**: During high inflation periods, consider companies with pricing power and real assets. When inflation trends down, growth stocks and longer-duration bonds typically become more attractive as rate hike pressures ease.
        """)

        # Ireland and Euro Area CPI Data
        ireland_cpi_query = '''
        SELECT *
        FROM ireland_cpi
        ORDER BY date
        '''
        euro_cpi_query = '''
        SELECT *
        FROM euro_cpi
        ORDER BY date
        '''
        ireland_cpi = load_data(ireland_cpi_query)
        euro_cpi = load_data(euro_cpi_query)
        euro_cpi_traces = [
            {'data':'ireland_cpi', 'column':'cpi_ireland_yoy', 'name':'Ireland CPI', 'line':{'color':'#00FF00', 'width':2}},
            {'data':'euro_cpi', 'column':'cpi_euro_yoy', 'name':'Euro Area CPI', 'line':{'color':'#003399', 'width':2}},
            {'data':'cpi_all', 'column':'api_all_yoy', 'name':'US CPI (All Items)', 'line':{'color':'#00FFF0', 'width':2}}
        ]
        fig_euro_cpi = create_figure(euro_cpi_traces)
        layout = get_chart_layout('Ireland vs Euro Area vs. US CPI (Year-over-Year Change)')
        layout.update(yaxis=dict(tickformat='.1%'))
        fig_euro_cpi.update_layout(layout)
        st.plotly_chart(fig_euro_cpi, use_container_width=True)
        st.markdown("""
        * **Household Responses to Inflation Pressure**: High inflation since 2020 has led citizens to prioritize essential spending while delaying or reducing discretionary expenses, such as travel or luxury goods.
        * **Potential Impact of ECB Policy Shifts**: Elevated inflation in the Euro Area raises concerns about future European Central Bank rate hikes, which would increase mortgage and credit costs for households, encouraging higher savings today.
        * **Cross-Regional Impact**: Irish households, being more exposed to energy and housing price volatility, may face unique challenges compared to more stable Euro Area averages, making financial planning more uncertain.
        * **Retail Investor**: Regional inflation differences can create opportunities - consider exposure to markets with lower inflation trends, as they may face less pressure from rate hikes. During high inflation periods across regions, global commodity-related investments might offer protection.
        """)

    except Exception as e:
        st.error(f'Error in Economic Indicators: {e}')

        

