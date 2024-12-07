import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path
from sqlalchemy import create_engine


# setup database connection
def get_db_path():
    '''get the db path whether running as script or dir'''
    current_file = Path(__file__).resolve() if '__file__' in globals() else Path.cwd()
    if current_file.is_file():
        return current_file.parent.parent / 'data' / 'economic_data.db'
    else:
        return current_file.parent / 'data' / 'economic_data.db'


def create_figure(traces, title, yaxis_title, template='plotly_white', hovermode='x unified', yaxis_format=None):
    fig = go.Figure()
    for trace in traces:
        fig.add_trace(go.Scatter(
            x=trace['data'].index,
            y=trace['data'][trace['column']],
            name=trace['name'],
            line=trace['line']
        ))
    fig.update_layout(
        title=title,
        yaxis_title=yaxis_title,
        template=template,
        hovermode=hovermode
    )
    if yaxis_format:
        fig.update_yaxes(tickformat=yaxis_format)
    return fig
    

db_path = get_db_path()

if db_path.exists():
    engine = create_engine(f'sqlite:///{db_path}')

    # load data from db
    unemployment = pd.read_sql('SELECT * FROM unrate', engine, parse_dates=['date']).set_index('date')
    cpi_core = pd.read_sql('SELECT * FROM cpilfesl', engine, parse_dates=['date']).set_index('date')
    cpi_all = pd.read_sql('SELECT * FROM cpiaucsl', engine, parse_dates=['date']).set_index('date')
    ireland_cpi = pd.read_sql('SELECT * FROM ireland_cpi', engine, parse_dates=['date']).set_index('date')
    euro_cpi = pd.read_sql('SELECT * FROM euro_cpi', engine, parse_dates=['date']).set_index('date')
    gdpc1 = pd.read_sql('SELECT * FROM gdpc1', engine, parse_dates=['date']).set_index('date')
    gdppot = pd.read_sql('SELECT * FROM gdppot', engine, parse_dates=['date']).set_index('date')
    fedfunds = pd.read_sql('SELECT * FROM fedfunds', engine, parse_dates=['date']).set_index('date')
    debt_to_gdp = pd.read_sql('SELECT * FROM gfdegdq188s', engine, parse_dates=['date']).set_index('date')
    dgs1 = pd.read_sql('SELECT * FROM dgs1', engine, parse_dates=['date']).set_index('date')
    dgs5 = pd.read_sql('SELECT * FROM dgs5', engine, parse_dates=['date']).set_index('date')
    dgs10 = pd.read_sql('SELECT * FROM dgs10', engine, parse_dates=['date']).set_index('date')
    dollar_index = pd.read_sql('SELECT * FROM dtwexbgs', engine, parse_dates=['date']).set_index('date')
    enrusd = pd.read_sql('SELECT * FROM dexuseu', engine, parse_dates=['date']).set_index('date')
    vix = pd.read_sql('SELECT * FROM vixcls', engine, parse_dates=['date']).set_index('date')
    sp500 = pd.read_sql('SELECT * FROM sp500', engine, parse_dates=['date']).set_index('date')
    

    # Define trace configurations for each plot
    sp500_traces = [
        {'data': 'sp500', 'column': 'SP500', 'name': 'S&P 500', 'line': {'color': 'blue'}},
        {'data': 'sp500', 'column': 'sp500_ma20', 'name': '20-day MA', 'line': {'color': 'red', 'dash': 'dash'}},
        {'data': 'sp500', 'column': 'sp500_ma50', 'name': '50-day MA', 'line': {'color': 'green', 'dash': 'dash'}},
        {'data': 'sp500', 'column': 'sp500_ma200', 'name': '200-day MA', 'line': {'color': 'purple', 'dash': 'dash'}}
    ]

    sp500_returns_traces = [
        {'data': 'sp500', 'column': 'sp500_returns_yearly', 'name': 'Yearly Returns', 'line': {'color': 'blue'}}
    ]

    unemployment_traces = [
        {'data': 'unemployment', 'column': 'UNRATE', 'name': 'Unemployment Rate', 'line': {'color': 'blue'}},
        {'data': 'unemployment', 'column': 'unrate_ma3', 'name': '3-month MA', 'line': {'color': 'red', 'dash': 'dash'}},
        {'data': 'unemployment', 'column': 'unrate_ma12', 'name': '12-month MA', 'line': {'color': 'green', 'dash': 'dash'}}
    ]

    cpi_comparison_traces = [
        {'data': 'cpi_core', 'column': 'cpi_core_yoy', 'name': 'Core CPI (Less Food & Energy)', 'line': {'color': 'blue'}},
        {'data': 'cpi_all', 'column': 'cpi_all_yoy', 'name': 'All Items CPI', 'line': {'color': 'red'}}
    ]

    euro_cpi_traces = [
        {'data': 'ireland_cpi', 'column': 'cpi_ireland_yoy', 'name': 'Ireland CPI', 'line': {'color': 'green'}},
        {'data': 'euro_cpi', 'column': 'cpi_euro_yoy', 'name': 'Euro Area CPI', 'line': {'color': 'blue'}},
        {'data': 'cpi_all', 'column': 'cpi_all_yoy', 'name': 'US CPI', 'line': {'color': 'red'}}
    ]
    '''
    fig_euro_cpi.add_trace(go.Scatter(
        x=euro_cpi.index,
        y=cpi_all['cpi_all_yoy'],
        name='US CPI',
        line=dict(color='red')
    ))
    '''

    # GDP growth comparison 
    gdp_comparison_traces = [
        {'data': 'gdppot', 'column': 'gdppot_us_yoy', 'name': 'Potential GDP Growth', 'line': {'color': 'blue'}},
        {'data': 'gdpc1', 'column': 'gdpc1_us_yoy', 'name': 'Real GDP Growth', 'line': {'color': 'red'}}
    ]

    # Fed Funds Rate
    fedfunds_traces = [
        {'data': 'fedfunds', 'column': 'FEDFUNDS', 'name': 'Federal Funds Rate', 'line': {'color': 'blue'}}
    ]
    '''
    # Create Fed Funds Rate plot
    fig_fedfunds = px.line(fedfunds, x=fedfunds.index, y='FEDFUNDS',
                           title='Federal Funds Rate')
    fig_fedfunds.update_layout(
        showlegend=False,
        yaxis_title='Rate (%)',
        template='plotly_white'
    )
    fig_fedfunds.show()
    '''

    # Federal Debt to GDP
    debt_gdp_traces = [
        {'data': 'debt_to_gdp', 'column': 'GFDEGDQ188S', 'name': 'Federal Debt to GDP Ratio', 'line': {'color': 'blue'}}
    ]
    '''
    # Create Federal Debt to GDP plot
    fig_debt_gdp = px.line(debt_to_gdp, x=debt_to_gdp.index, y='GFDEGDQ188S',
                           title='Federal Debt to GDP Ratio')
    fig_debt_gdp.update_layout(
        showlegend=False,
        yaxis_title='Ratio (%)',
        template='plotly_white'
    )
    fig_debt_gdp.show()
    '''

    # treasury yields
    treasury_traces = [
        {'data': 'dgs1', 'column': 'DGS1', 'name': '1-Year', 'line': {'color': 'blue'}},
        {'data': 'dgs5', 'column': 'DGS5', 'name': '5-Year', 'line': {'color': 'red'}},
        {'data': 'dgs10', 'column': 'DGS10', 'name': '10-Year', 'line': {'color': 'green'}}
    ]

    # Trade Weighted Dollar Index 
    dollar_traces = [
        {'data': 'dollar_index', 'column': 'DTWEXBGS', 'name': 'Dollar Index', 'line': {'color': 'blue'}},
        {'data': 'dollar_index', 'column': 'dollar_index_ma20', 'name': '20-day MA', 'line': {'color': 'red', 'dash': 'dash'}},
        {'data': 'dollar_index', 'column': 'dollar_index_ma50', 'name': '50-day MA', 'line': {'color': 'green', 'dash': 'dash'}}
    ]

    # EUR/USD Exchange Rate
    eurusd_traces = [
        {'data': 'eurusd', 'column': 'DEXUSEU', 'name': 'EUR/USD', 'line': {'color': 'blue'}},
        {'data': 'eurusd', 'column': 'eurusd_ma20', 'name': '20-day MA', 'line': {'color': 'red', 'dash': 'dash'}},
        {'data': 'eurusd', 'column': 'eurusd_ma50', 'name': '50-day MA', 'line': {'color': 'green', 'dash': 'dash'}}
    ]

    # vix 
    vix_traces = [
        {'data': 'vix', 'column': 'VIXCLS', 'name': 'VIX', 'line': {'color': 'red'}},
        {'data': 'vix', 'column': 'vix_ma20', 'name': '20-day MA', 'line': {'color': 'blue', 'dash': 'dash'}},
        {'data': 'vix', 'column': 'vix_ma50', 'name': '50-day MA', 'line': {'color': 'green', 'dash': 'dash'}}
    ]

    # Create and display plots
    create_figure(sp500_traces, 'S&P 500 Index with Moving Average', 'Index Value').show()
    create_figure(sp500_returns_traces, 'S&P 500 Yearly Return', 'Yearly Returns', yaxis_format='.2%').show()
    create_figure(unemployment_traces, 'U.S. Unemployment Rate with Moving Averages', 'Rate (%)').show()
    create_figure(cpi_comparison_traces, 'Core CPI vs All Items CPI (Year-over-Year Change)', 'Change Rate', yaxis_format='.2%').show()
    create_figure(euro_cpi_traces, 'Ireland vs. Euro Area vs. US CPI (Year-over-Year Change)', 'Change Rate', yaxis_format='.2%').show()
    create_figure(gdp_comparison_traces, 'US GDP Growth Comparison (YoY)', 'Growth Rate (%)', yaxis_format='.1%').show()
    create_figure(fedfunds, 'Federal Funds Rate', 'Rate (%)').show()
    create_figure(debt_to_gdp, 'Federal Debt to GDP Ratio', 'Ratio (%)').show()
    create_figure(treasury_traces, 'Treasury Yields', 'Yield (%)').show()
    create_figure(dollar_traces, 'Trade Weighted U.S. Dollar Index: Broad, Goods', 'Index Value').show()
    create_figure(eurusd_traces, 'U.S. / Euro Foreign Exchange Rate', 'Exchange Rate (USD per EUR)').show()
    create_figure(vix_traces, 'VIX Volatility Index with Moving Averages', 'VIX Value').show()

else:
    print('Error: Database file not found!')
    print(f'Expected location: {db_path}')









