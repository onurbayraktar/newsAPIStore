import requests
import pandas as pd
import numpy as np
import xlrd
import sqlite3 as sql
from datetime import date
from pandas import ExcelWriter, ExcelFile
from requests.exceptions import HTTPError
from openpyxl import Workbook

articles = {}  # Dictionary that will keep the articles, will be fed below

class Article():
    def __init__(self, source_id, source_name, author, title, desc, url, published_at, content):
        self.source_id = source_id
        self.source_name = source_name
        self.author = author
        self.title = title
        self.desc = desc
        self.url = url
        self.published_at = published_at
        self.content = content

# Function to fetch breaking news
def fetchBreakingNews(country):
    url = ('https://newsapi.org/v2/top-headlines?'
       'country='+country+'&'
       'apiKey=a538a0a2c2ab435fb68c17ef2ab56934')
    try:
        response = requests.get(url)
        # If the response was successful, no exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP Error Occured: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
        return response.json()

# Function to save news to a excel file.
def storeNews(news, noOfItems):
    numOfNews = 0
    for article in news['articles']:
        # Get the necessary informations
        source_id = article['source']['id']
        source_name = article['source']['name']
        author = article['author']
        title = article['title']
        desc = article['description']
        url = article['url']
        published_at = article['publishedAt']
        content = article['content']

        # Creation of article and add to article dict
        articles[numOfNews] = [source_id, source_name, author, title, desc, url, published_at, content]
        numOfNews = numOfNews + 1

        # Create the dataframe, and save it to a excel file
        news = pd.DataFrame.from_dict(articles, orient='index')
        print(news)
        writer = ExcelWriter('Breaking.xlsx')
        news.to_excel(writer, 'Sheet1', index=False, startrow=noOfItems)
        writer.save()


# Function to store the news in database
def storeInDatabase(news):
    # Create, or connect to the database
    my_db = sql.connect('news.sqlite')  # Connect to database
    cur = my_db.cursor()
    CREATE_QUERY = """CREATE TABLE IF NOT EXISTS news(source_id, source_name, author, title, desc, url, published_at, content)"""
    cur.execute(CREATE_QUERY)

    # Iterate over the items(articles) that returned from api.
    for article in news['articles']:
        # Get the necessary informations
        source_id = article['source']['id']
        source_name = article['source']['name']
        author = article['author']
        title = article['title']
        desc = article['description']
        url = article['url']
        published_at = article['publishedAt']
        content = article['content']

        # Create an article object and append it to the array
        articleObject = [source_id, source_name, author, title, desc, url, published_at, content]
        cur.execute("""INSERT INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", articleObject)
        my_db.commit()

def main():
    print("1: Fetch top breaking news in a country.")
    print("2: Fetch the news from specific date.")
    print("3: Fetch the news from specific date by specify a keyword.")
    option = input("Please enter 1, 2 or 3:")

    if option == '1':         # We need to fetch today's news
        country = input("Enter a country code: ")
        news = fetchBreakingNews(country)
        storeInDatabase(news)
    elif option == 2:       # We need to fetch news with specific date
        #TODO
        pass
    elif option == 3:       # We need to fetch news with date and keyword
        #TODO
        pass


if __name__ == '__main__':
    main()
