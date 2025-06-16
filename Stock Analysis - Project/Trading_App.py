import streamlit as st

st.set_page_config(
    page_title="Trading App",
    page_icon=":chart_with_downwards_trend:",
    layout="wide"
)

st.title("Trading Guide App :bar_chart:")

st.header("We provide the greatest platform for you to collect all information prior to investing in stocks.")

# Enlarging the image to full width using st.image
st.image("stock.jpg", use_column_width=True)

st.markdown("## We Provide the following services:")

st.markdown("#### :one: Stock Information")
st.write("Through this page you can see all the information about stock.")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models.")

st.markdown("#### :three: CAPM Return")
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks based on its risk.")

st.markdown("#### :four: CAPM Beta")
st.write("Calculates Beta and Expected Return for Individual Stocks.")



