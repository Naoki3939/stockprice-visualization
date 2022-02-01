import pandas as pd
import yfinance as yf
import streamlit as st
import altair as alt

st.title("Stock Price Visualization")

st.sidebar.write("""
    # Stock Price
    Adjust the period length and the price range.
""")

st.sidebar.write("""
    ## Displaying period length
    """)

days = st.sidebar.slider('days', 1, 50, 20)

st.write(f"""
### Stock Price Changes over the past {days} days
""")

@st.cache(suppress_st_warning=True)
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        hist
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ## Price Range
    """)

    ymin, ymax = st.sidebar.slider(
        'dollars',
        0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        'select companies:',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple'] 
    )

    if not companies:
        st.error('choose at least one.')

    else: 
        data = df.loc[companies]
        st.write("### Stock Prices(USD)", data.sort_index())
        data = data.T.reset_index()
        data=pd.melt(data, id_vars=['Date']).rename(
            columns={'value':'Stock Prices(USD)'})
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q",stack=None, scale=alt.Scale(domain=[ymin,ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error('Oops. Something went wrong.')