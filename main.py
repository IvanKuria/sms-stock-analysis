import requests
from twilio.rest import Client

'''
Stock api information

'''
tsla_api_key = "AYCRJKGY3G75VRTI"
AA_Endpoint = "https://www.alphavantage.co/query"

tesla_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": tsla_api_key

}

response = requests.get(AA_Endpoint, params=tesla_params)
data = response.json()

time_series = data["Time Series (Daily)"]
dates = list(time_series.keys())

# Sort dates in descending order (most recent first)
dates.sort(reverse=True)

# Get the closing prices for the most recent two dates
yesterday_close = float(time_series[dates[0]]["4. close"])
day_before_yesterday_close = float(time_series[dates[1]]["4. close"])

'''
News api information
'''

news_api_key = "44703c14a03b4e6c8bda63ceb883c958"
News_Endpoint = "https://newsapi.org/v2/everything"

news_params = {
    "q": "Tesla",
    "from": dates[0],
    "to": dates[0],
    "sortBy": "popularity",
    "apiKey": news_api_key,
}

'''
Twilio api information
'''

account_sid = "AC831194dde523017fd46efd68454717aa"
auth_token = "f7492e386c376ed0abc17ccc8461ab3a"

news_response = requests.get(News_Endpoint, params=news_params)
news_data = news_response.json()

# Calculates the percentage change
percentage_change = ((yesterday_close - day_before_yesterday_close) / day_before_yesterday_close) * 100


for i in range(3):
    title = news_data['articles'][i]['title']
    description = news_data['articles'][i]['description']
    if percentage_change < 0:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Tesla: 📉 {percentage_change}%\nArticle {i + 1}:\nTitle: {title}\nDescription: {description}",
            from_="+18777804236",
            to="+16692780383",
        )
        print(message.status)
    else:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Tesla: 📈 {percentage_change}%\nArticle {i + 1}:\nTitle: {title}\nDescription: {description}",
            from_="+18777804236",
            to="+16692780383",
        )
        print(message.status)