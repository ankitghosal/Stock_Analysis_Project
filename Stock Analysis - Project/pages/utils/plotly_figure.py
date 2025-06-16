import plotly.graph_objects as go
import dateutil
import datetime
import pandas as pd
import pandas_ta as pta





def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'
    
    # Create the table figure
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Index</b>"] + ["<b>" + str(col)[:10] + "</b>" for col in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[["<b>" + str(idx) + "</b>" for idx in dataframe.index]] + [dataframe[col].tolist() for col in dataframe.columns],
            fill_color=[[rowOddColor if i % 2 == 0 else rowEvenColor for i in range(len(dataframe.index))]],
            align='left',
            line_color='white',
            font=dict(color='black', size=15),
            height=30
        )
    )])
    
    # Update layout
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig



def filter_data(dataframe, num_period):
    df = dataframe.reset_index()  # reset index once
    last_date = df['Date'].iloc[-1]

    if num_period == '1mo':
        date = last_date - dateutil.relativedelta.relativedelta(months=1)
    elif num_period == '5d':
        date = last_date - datetime.timedelta(days=5)
    elif num_period == '6mo':
        date = last_date - dateutil.relativedelta.relativedelta(months=6)
    elif num_period == '1y':
        date = last_date - dateutil.relativedelta.relativedelta(years=1)
    elif num_period == '5y':
        date = last_date - dateutil.relativedelta.relativedelta(years=5)
    elif num_period == 'ytd':
        date = datetime.datetime(last_date.year, 1, 1)
    else:
        date = df['Date'].iloc[0]

    filtered_df = df[df['Date'] > date]
    return filtered_df



def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines',
                             name='High', line=dict(width=2, color="#0077ff")))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines',
                             name='Low', line=dict(width=2, color='red')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',  # fixed the color code here
        legend=dict(
            yanchor="top",
            xanchor="right"
        )
    )
    return fig



def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe.index,
                                 open=dataframe['Open'],
                                 high=dataframe['High'],
                                 low=dataframe['Low'],
                                 close=dataframe['Close']))
    
    fig.update_layout(showlegend=False, height=500,
                      margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig


def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=dataframe['RSI'], name='RSI', marker_color='orange', line=dict(width=2, color='orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=[70]*len(dataframe), name='Overbought', marker_color='red', line=dict(width=2, color='red', dash='dash'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=[30]*len(dataframe), fill='tonexty', name='Oversold', marker_color='#79da84', line=dict(width=2, color='#79da84', dash='dash')
    ))
    fig.update_layout(yaxis_range=[0, 100],
                      height=200, plot_bgcolor='white', paper_bgcolor='#e1efff',
                      margin=dict(l=0, r=0, t=0, b=0),
                      legend=dict(orientation='h',
                                  yanchor='top',
                                  y=1.02,
                                  xanchor='right',
                                  x=1))
    return fig


def Moving_average(dataframe, num_period):
    # Ensure the 'Date' column exists and is of datetime type
    if 'Date' not in dataframe.columns:
        dataframe = dataframe.reset_index()
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])

    # Calculate the 50-period Simple Moving Average (SMA)
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], length=50)

    # Filter the dataframe based on the specified period
    dataframe = filter_data(dataframe, num_period)

    # Create the Plotly figure
    fig = go.Figure()

    # Add traces for Open, Close, High, Low, and SMA_50
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines',
                             name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines',
                             name='Low', line=dict(width=2, color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines',
                             name='SMA_50', line=dict(width=2, color='purple')))

    # Update the layout of the figure
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,
                      margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white',
                      paper_bgcolor='#e1efff',
                      legend=dict(yanchor='top',
                                  xanchor='right'))

    return fig

def MACD(dataframe, num_period):
    # Ensure 'Date' column exists and is of datetime type
    if 'Date' not in dataframe.columns:
        dataframe = dataframe.reset_index()
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])

    # Calculate MACD, Signal, and Histogram
    macd_df = pta.macd(dataframe['Close'])
    dataframe['MACD'] = macd_df['MACD_12_26_9']
    dataframe['MACD Signal'] = macd_df['MACDs_12_26_9']
    dataframe['MACD Hist'] = macd_df['MACDh_12_26_9']

    # Filter the dataframe based on the specified period
    dataframe = filter_data(dataframe, num_period)

    # Determine colors for the histogram bars
    colors = ['green' if val >= 0 else 'red' for val in dataframe['MACD Hist']]

    # Create the Plotly figure
    fig = go.Figure()

    # Add MACD line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'],
        name='MACD',
        line=dict(width=2, color='orange')
    ))

    # Add Signal line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'],
        name='Signal',
        line=dict(width=2, color='red', dash='dash')
    ))

    # Add Histogram bars
    fig.add_trace(go.Bar(
        x=dataframe['Date'],
        y=dataframe['MACD Hist'],
        name='Histogram',
        marker_color=colors
    ))

    # Update layout
    fig.update_layout(
        height=300,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation='h', yanchor='top', xanchor='right', x=1)
    )

    return fig

        
def Moving_average_forecast(forecast):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],
                             mode='lines',
                             name='Close Price', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['Close'].iloc[-31:],
                             mode='lines', name='Future Close Price', line=dict(width=2, color='red')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(
            yanchor='top',
            xanchor='right'
        )
    )

    return fig









    