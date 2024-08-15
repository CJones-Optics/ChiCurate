import json
import pandas as pd
from parseFeed import parse_rss_feed_DF
import csv

def getTodaysTitles(path,batchSize):
    """
    # Loads the titles from the json file into memory,
    # splits them into batches
    Args:
        path (str): Path to the json file
        batchSize (int): The size of the batches
    Returns:
        list: A list of batches of titles
    """
    titles = []
    with open(path, 'r') as file:
        for line in file:
            article = json.loads(line)
            # drop the abstract
            article.pop('abstract', None)
            titles.append(article)

    return [titles[i:i+batchSize] for i in range(0, len(titles), batchSize)]


def getTodaysArticles(path):
    """
    # Loads the titles from the csv file into memory,
    Args:
        path (str): Path to the json file
    Returns:
        df: A dataframe of articles
    """

    df = pd.DataFrame()
    with open('./feeds.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            items = parse_rss_feed_DF(row[0])
            df = pd.concat([df, items], ignore_index=True)
    df = df.drop_duplicates(subset='id')
    return df


def constructUserPrompt(prompt, data):
    outputStr = prompt + "\n"
    for item in data:
        outputStr += json.dumps(item)+"\n"
    return outputStr

if __name__=="__main__":
    path = "./todays.json"
    batchSize = 10
    titleBatches = getTodaysTitles(path,batchSize)

    print(f"Length of titleBatches: {len(titleBatches)}")
    print(f"Length of titleBatches[0]: {len(titleBatches[0])}")

    # print(f"First batch of titles: {titleBatches[0]}")
    prompt = "TESTING prompt creator"
    userPrompt = constructUserPrompt(prompt, titleBatches[0])
    print(userPrompt)
