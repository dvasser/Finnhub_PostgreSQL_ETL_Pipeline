#!/usr/bin/env python
# coding: utf-8

# In[1]:


from FinnhubConnector import FinnhubConnector
import psycopg2
import datetime as dt


# In[2]:


#Import API Connector and establish the object variable
connector = FinnhubConnector(api_key = 'YOUR_API_KEY')


# In[3]:


#Helper function to convert datetime objects to UNIX timestamps
def convert_to_unix(datetime) -> int:
    formated_date = dt.datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S")
    return int(dt.datetime.timestamp(formated_date))


# In[4]:


# How to use the postgres_load_candles function below:
# 1. Specify a symbol from which you'd like to get candles. F.e 'MSFT'
# 2. Specify the frequency or resolution of candles. Supported resolution includes [1, 5, 15, 30, 60, D, W, M].
# Some timeframes might not be available depending on the exchange.

# 3. Specify the date in the following format:  yyyy-mm-dd  -time is an optional argument set to default 00:00:00.
# Make sure you speficy all the arguments in the same exact order they are below.

# 4. Specify the title of the file. I recommend the title to be as short as possible such as: tsla5min. The only
# allowed characters in a title string are lowercase letters and underscores.

# 5. Specify your connection credentials. Once you download pgAdmin4 it will ask you to create a password. If you
# decide to make it anything other than '1234', change it in the code below. The other parameters are default
# and should work right off the bat.

def postgres_load_candles(symbol, frequency, start_date, end_date, title,
                          start_time= '00:00:00', end_time= '00:00:00',
                          host = 'localhost',
                          dbname = 'postgres',
                          user= 'postgres',
                          password='1234',
                          port= 5432):
    
    # Create a data frame with desired candles using our FinnhubConnector object. Convert the datetime column
    # to unix timestamps.
    df = connector.get_stock_candles(symbol, frequency, start_date, end_date, start_time, end_time)
    df.insert(0, 'Datetime', df.index)
    df['Datetime'] = df['Datetime'].apply(lambda x: convert_to_unix(x))
    df.drop(['Status'], axis=1, inplace=True)
    
    # Establish the connection to your PostgreSQL database as well as the cursor and connector variables.
    # All the parameters are set to default. 
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
    cur = conn.cursor()
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {title}(
        unix_datetime BIGINT PRIMARY KEY,
        close FLOAT,
        high FLOAT,
        low FLOAT,
        open FLOAT,
        volume BIGINT
    );
    ''')

    #Iterate through our data frame and add each row in the form of an SQL tuple.
    for i in range(len(df)):
        cur.execute(f'''INSERT INTO {title} (unix_datetime, close, high, low, open, volume) VALUES
        {tuple(df.iloc[i])};
        ''')

    #Commit changes and print a success statement.
    conn.commit()
    cur.close()
    conn.close()
    print('Successfully loaded candles to PostgreSQL!')
    


# In[5]:


# Examples:

# postgres_load_candles('META', 'D', '2021-04-07', '2023-03-30', 'meta21_4_7to23_3_30daily')

# postgres_load_candles('TSLA', '5', '2022-10-30', '2022-11-16', 'tsla5min')

