# The output of the model can be a little unpredicatable
# since I cannot guarantee that the model will always return a valid JSON string.
# Instead, I will use a regex to extract the JSON string from the output.

import json
import pandas as pd
import os
from RAGLoader import getTodaysArticles
from regexJSONCleaner import extract_and_clean_json

def loadAllResponses(responseDir):
    # Walk through the directory and load all the response .json files
    responseList = []
    for root, dirs, files in os.walk(responseDir):
        for file in files:
            # Open the the file as plain text
            with open(os.path.join(root, file), 'r') as f:
                rawText = f.read()
                cleanedList = extract_and_clean_json(rawText)
                responseList.extend(cleanedList)
    return responseList

def createDataframe(responseList):
    # Column Headings
    columns = ['ArticleID', 'Justification', 'Rating']
    # Create Dataframe with the column headings
    df = pd.DataFrame(columns=columns)
    for i in range(len(responseList)):
        print(f"Processing response {i} of {len(responseList)}")
        # Create a dictionary for each item
        try:
            articleID = responseList[i]['ArticleID']
            justification = responseList[i]['Justification']
            rating = responseList[i]['Rating']
            df.loc[len(df)] = [articleID, justification, rating]
        except:
            print(f"Error at index {i}")
            continue
    return df

def main():
    responseDir = "./ollamaResponse"
    responseList = loadAllResponses(responseDir)
    responseDF = createDataframe(responseList)
    # Re-order the columns based on the rating value
    responseDF = responseDF.sort_values(by='Rating', ascending=False)
    # Get today's articles
    articlePath = "todaysFeed.csv"
    articleDF = pd.read_csv(articlePath)
    # Merge the two dataframes on the ArticleID
    mergedDF = pd.merge(responseDF, articleDF, left_on='ArticleID', right_on='id')
    # Save the merged dataframe to a json file for report generation
    articlesDict = mergedDF.to_dict(orient='records')
    path = "ratedArticles.json"
    # Save to a file with indentation for better readability
    with open(path, 'w') as f:
        json.dump(articlesDict, f, indent=2)

if __name__ == "__main__":
    main()
