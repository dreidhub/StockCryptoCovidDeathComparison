import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import pandas_datareader.data as web
from sklearn import preprocessing
import streamlit as st
from urllib.request import Request, urlopen
from sodapy import Socrata

st.write("""
#Stock Market Web Application
**Visually** show data of stocks and cryptos for 2020
""")

st.sidebar.header('User Input')

# Define time period
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2020, 12, 1)


# Pull covid case data from API
def pull_covid_data():
    # API KEY: https://data.cdc.gov/resource/vbim-akqf.json
    client = Socrata("https://data.cdc.gov/resource/vbim-akqf.json", "None", username="fakeuser@somedomain.com",
                     password="mypassword")
    # client.get()


# pull_covid_data()

# Get users date range input
def get_user_input():
    start_date = st.sidebar.text_input("Start Date", "2020-01-01")
    end_date = st.sidebar.text_input("End Date", "2020-12-01")
    #symbol
    st.sidebar.text_input("Stock Symbol", "AMZN")


# DEFINE DATAFRAMES
# Bitcoin dataframe
btc_df = web.DataReader('BTC-USD', 'yahoo', start, end)
# ETH dataframe
eth_df = web.DataReader('ETH-USD', 'yahoo', start, end)
# TSLA dataframe
tsla_df = web.DataReader('TSLA', 'yahoo', start, end)
# AMZN dataframe
amzn_df = web.DataReader('AMZN', 'yahoo', start, end)

# complete Dataframe
df = pd.DataFrame({'BTC': btc_df['Adj Close'],
                    'ETH': eth_df['Adj Close']})
                   # 'TSLA': tsla_df['Adj Close'],
                   # 'AMZN': amzn_df['Adj Close']
                   # })

#df = pd.DataFrame({'TSLA': tsla_df['Adj Close']})

# Plot combined Dataframe
# print(df.head())
# print(df.describe())
df.plot()
#df2.plot()

# print first 10 results from data
# print(btc_df.head(10))

# save dataframe as csv
# df.to_csv('tsla.csv')

# df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
# print(df.head())


df_dict = {}


# Plot ADJ CLOSE only
btc_df['Adj Close'].plot(label='Bitcoin')
tsla_df['Adj Close'].plot(label='Tesla')
amzn_df['Adj Close'].plot(label='Amazon')
eth_df['Adj Close'].plot(label='Ethereum')

# Define data labels
btc_patch = mpatches.Patch(color="red", label="Bitcoin")
tsla_patch = mpatches.Patch(color="blue", label="Tesla")
eth_patch = mpatches.Patch(color="purple", label="Ethereum")
amzn_patch = mpatches.Patch(color="green", label="Amazon")
# Assign data labels
# plt.legend(handles=[btc_patch, tsla_patch, eth_patch])

# Assign axis labels
# plt.ylabel("Price (USD)")
# plt.xlabel("Date")

# plt.title("Price of Cryptos vs Tesla")
# plt.style.use('ggplot')

# Show graph
# plt.show()

# SCALE THE DATA
mix_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 100))
scale = mix_max_scaler.fit_transform(df)
# print(scale)

# convert scaled data into Dataframe
df_scaled = pd.DataFrame(scale, columns=df.columns)

# Display scaled dataframe
my_data = df_scaled
plt.figure(figsize=(12.4, 4.5))
for c in my_data.columns.values:
    plt.plot(my_data[c], label=c)

plt.title('Scaled Data')
plt.xlabel('Days')
plt.ylabel('Scaled Price (USD)')
plt.legend(my_data.columns.values, loc="upper left")
plt.show()
