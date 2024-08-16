import json
import pandas as pd
from parseFeed import parse_rss_feed_DF
import csv

def getTodaysTitles(path,batchSize):
    """
    # Loads the titles from the json file into memory,
    # and splits them into batches.
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
    Loads the titles from the csv file into memory,
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
    """
    Contructs the user prompt by appending the data
    to the prompt.
    Args:
        prompt (str): The prompt to be displayed to the user
        data (list): The data to be appended to the prompt
    Returns:
        str: The user prompt
    """
    outputStr = prompt + "\n"
    for item in data:
        outputStr += json.dumps(item)+"\n"
    return outputStr

if __name__=="__main__":
    # Example usage
    path = "./todays.json"
    batchSize = 10
    titleBatches = getTodaysTitles(path,batchSize)
    print(f"Length of titleBatches: {len(titleBatches)}")
    print(f"Length of titleBatches[0]: {len(titleBatches[0])}")
    prompt = "TESTING prompt creator"
    userPrompt = constructUserPrompt(prompt, titleBatches[0])
    print(userPrompt)
