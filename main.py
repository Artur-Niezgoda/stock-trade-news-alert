from twilio.rest import Client
import requests
from environs import Env

# Read environment variables from env file
env = Env()
env.read_env()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_url = "https://www.alphavantage.co/query"
news_url = "https://newsapi.org/v2/everything"
perc_alert = 5
stock_api = env("STOCK_API")  # Put your stock api key here
news_api = env("NEWS_API")  # Put your news api key here


def get_daily() -> None:
    """
    Get last two closing stock values from stock api and calculate the change.
    If it is higher than limit value (perc_alert), then call get_news function
    """

    parameters = {"function": "TIME_SERIES_DAILY",
                  "symbol": STOCK,
                  "apikey": stock_api}

    result = requests.get(stock_url, params=parameters)
    data = result.json()["Time Series (Daily)"]

    last_day = list(data.keys())[0]  # get string of the last date in data
    prelast_day = list(data.keys())[1]  # get string of the day before the last date in data

    # get value at closing
    value1 = float(data[last_day]["4. close"])
    value2 = float(data[prelast_day]["4. close"])

    perc_change = round((value1-value2)/value2*100, 2)

    if perc_change > perc_alert or perc_change < -perc_alert:
        get_news(perc_change, last_day, prelast_day)


def get_news(perc_change: float, day1: str, day2: str) -> None:
    """
    Get news on the day when the great change of stock value happened amd send 3 of them via SMS
    :param perc_change: value of how much the stock changed
    :param day1: string corresponding to day of the last available data
    :param day2: string corresponding to day before the last day of available data
    """

    news_parameters = {
                    "q": COMPANY_NAME,
                    "from": day1,
                    "to": day2,
                    "sortBy": "popularity",
                    "language": "en",
                    "pageSize": 3,
                    "page": 1,
                    "apiKey": news_api
                    }

    news_result = requests.get(news_url, params=news_parameters)
    news = (news_result.json()["articles"])
    send_message(news, perc_change)


def send_message(news: list, perc_change: float) -> None:
    """Prepare a message to be sent through Twilio api and send it via SMS
    :param news: list of articles
    :param perc_change: value of how much the stock changed
    """

    account_sid = env("TWILIO_ACC_SID")
    auth_token = env("TWILIO_AUT_TOKEN")
    client = Client(account_sid, auth_token)

    if perc_change < 0:
        change_symbol = "🔻"
    else:
        change_symbol = "🔺"

    for item in news:
        msg = f"{COMPANY_NAME}: {change_symbol}{perc_change}% \n Heading: {item['title']} \n " f"Brief: {item['description']}"
        message = client.messages.create(from_="+16167412561",
                                         body=msg,
                                         to='+34611527372'
                                         )
        print(message.status)


if __name__ == "__main__":
    get_daily()
