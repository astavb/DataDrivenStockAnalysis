# 05_streamlit_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data-Driven Stock Analysis", layout="wide")
st.title("Data-Driven Stock Analysis")

df = pd.read_csv("data/cleaned_csv/all_stocks.csv", parse_dates=['Date'])
symbols = sorted(df['Symbol'].unique())

left, right = st.columns([1,3])
with left:
    selected = st.selectbox("Select Symbol", symbols)
    show_vol = st.checkbox("Show volatility (std of daily returns)", value=True)
    compare = st.multiselect("Compare symbols (optional)", symbols, max_selections=4)

with right:
    sdf = df[df['Symbol']==selected].sort_values('Date').set_index('Date')
    st.subheader(f"{selected} - Price chart")
    st.line_chart(sdf['Close'])
    if 'Daily Return' not in sdf.columns:
        sdf['Daily Return'] = sdf['Close'].pct_change()
    if show_vol:
        st.write("Volatility (std of daily returns):", round(sdf['Daily Return'].std(), 6))

    if compare:
        comp_df = df[df['Symbol'].isin(compare)].pivot_table(index='Date', columns='Symbol', values='Close')
        st.subheader("Comparison chart")
        st.line_chart(comp_df.fillna(method='ffill'))

st.sidebar.header("Top/Bottom by Yearly Return")
yr = df[['Symbol','Yearly Return']].drop_duplicates().dropna()
st.sidebar.write("Top 10")
st.sidebar.dataframe(yr.sort_values('Yearly Return', ascending=False).head(10).reset_index(drop=True))
st.sidebar.write("Bottom 10")
st.sidebar.dataframe(yr.sort_values('Yearly Return', ascending=True).head(10).reset_index(drop=True))
