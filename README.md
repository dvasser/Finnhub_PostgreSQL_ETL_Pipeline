## Instructions how to use the ETL pipeline for Finnhub Candles:

1) Get a free Finnhub API key. Refer to https://github.com/dvasser/Finnhub-API-Connector for more details, it will be used to format the candles which will later be loaded into the PostgreSQL database.
2) Download PosgreSQL (I used version 15) and pgAdmin4 (GUI for Postgres). All these resources are free and could easily be downloaded from the internet. You are now ready to load large amounts of candle data to your data base.
3) Download the repository, open an IDE and navigate to the directory with the repo. 
4) ```pip install -r requirements.txt```
5) Run the finn_posgres_etl.py file. You will be prompted to input your API key and other parameters for data such as stock symbol, frequency, dates, title etc. The function has default parameters which should run well locally, however if running on server you may want to make sure the connection between your virtual environment and the database is well established before running the code. Read through the code comments for more details. Enjoy your analyses!
