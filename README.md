# stock-trade-news-alert

The program is checking the closing value of the stock for a chosen  company on the last available day and two days before and calculates the difference.
If it is greater than a given threshold, it requests the news about the company and sends 3 most popular to the user's phone via SMS.

The program uses three APIs:
- https://www.alphavantage.co/query to get the stock data
- https://newsapi.org/v2/everything to get the news
- https://www.twilio.com/ to send the SMS

It is required to register at the abovementioned APIs in order to receive api keys and tokens. 
The credentials should be saved in .env file as below:

* STOCK_API = "your key"
* NEWS_API = "your key"
* TWILIO_ACC_SID = "your acc sid"
* TWILIO_AUT_TOKEN = "your token"

Additionally one should change the phone number on line 11 to the one created by TWILIO, and a number to which the SMS should be sent (line 12).

The fields on lines 8-10 can be changed based on the users preferences. Perc_limit is a threshold which activates news api and then sends the news in SMS.
The two remaining fields are names of the company one is interested in, STOCK for stock shortcut and Company name to fetch the news. 