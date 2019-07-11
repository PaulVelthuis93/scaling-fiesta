import requests
import pandas as pd

entrypoint = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=TR675ZR80ZC1RK86&datatype=csv'


response = requests.get(entrypoint)
if response.status_code != 200:
  raise Exception("error occured")
else:
  try:
    df = pd.read_csv(entrypoint)
    # save the csv file
    df.to_csv("out.csv")
  except:
    print("we could not obtain the data")     
  # average price start monday, ends sunday
  # the date is in the second row as timestamp
  # we first create a copy of the dataframe, so that we can use the raw dataframe for other calculations as well
  avg_df=df
  avg_df['timestamp']=pd.to_datetime(avg_df['timestamp'])
  #  create empty column for week
  avg_df['Week_Number'] = avg_df['timestamp'].dt.week 
  avg_df['year'] = avg_df['timestamp'].dt.year
  #  calculate the close price average for the BTC on each week
  avg_df = avg_df.groupby(['year','Week_Number'])['close (USD)'].mean()
  avg_df.to_csv("close_price_btc_week.csv",header=True)  
  # function to build relative_span = (max(price) - min(price)) / min(price)
  # max(price) 
  relative_span_max=df.groupby(['year','Week_Number'])['year','Week_Number','close (USD)'].transform(max).groupby(['year','Week_Number']).last()
  # min(price)
  relative_span_min=df.groupby(['year','Week_Number'])['year','Week_Number','close (USD)'].transform(min).groupby(['year','Week_Number']).last()
  try:
    relative_span_df= (relative_span_max - relative_span_min) / relative_span_min
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # make sure all the rows are printed
      print(relative_span_df)
  except ZeroDivisionError:
    print("divide by zero") 
