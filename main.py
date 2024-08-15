import csv
import json
from parseFeed import parse_rss_feed_DF
import pandas as pd



if __name__ == "__main__":
    # create empty DF
    df = pd.DataFrame()
    with open('./feeds.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            items = parse_rss_feed_DF(row[0])
            df = pd.concat([df, items], ignore_index=True)
    df = df.drop_duplicates(subset='id')
    # Save the dataframe to a csv file
    df.to_csv('./todaysFeed.csv', index=False)

    # dump the id,title and abstract to json, one line per entry
    df[['id', 'title','abstract']].to_json('./todays.json', orient='records', lines=True)

    # ollamaCall.py
    # parseOutputs.py
    # htmlReportGenerator.py

    # Shuffle the rows
