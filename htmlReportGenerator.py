# Read the list of items in ofInterest.json and create an HTML report of the items.

import json
import pandas as pd
import html


stylePath = "style.css"
style = ""
with open(stylePath, 'r') as f:
    s = f.read()
    style = s

# print(style)


"""
/* CSS Variables */
:root {
    --body-bg-color: #24273a;
    --font-color: #cad3f5;
    --item-box-border-color: #c6a0f6;
    --item-box-bg-color: #363a4f;
    --button-bg-color: #b7bdf8;
    --button-hover-bg-color: #c6a0f6;
    --button-text-color: #181926;
    --rating-bar-bg-color: #1e2030;
    --rating-bar-filled-color: #a6da95;
}

body {
    background-color: var(--body-bg-color);
    color: var(--font-color);
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    line-height: 1.6;
}

.item-box {
    border: 2px solid var(--item-box-border-color); /* Pale blue border */
    padding: 15px; /* Space inside the box */
    margin-bottom: 20px; /* Space below each box */
    border-radius: 8px; /* Rounded corners */
    background-color: var(--item-box-bg-color); /* Light background color */
}

.button {
    display: inline-block;
    padding: 10px 15px;
    margin: 5px;
    background-color: var(--button-bg-color);
    color: var(--button-text-color);
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.button:hover {
    background-color: var(--button-hover-bg-color);
}

.rating-bar-container {
    width: 100%;
    background-color: var(--rating-bar-bg-color); /* Light grey background */
    border-radius: 5px; /* Rounded corners */
    overflow: hidden;
    height: 20px; /* Fixed height for the bar */
    margin-bottom: 10px; /* Space below the bar */
}

.rating-bar {
    height: 100%;
    background-color: var(
        --rating-bar-filled-color
    ); /* Green color for the filled part */
    width: 0%; /* Initial width */
    transition: width 0.3s ease; /* Smooth transition */
}
"""

def load_articles_from_json(file_path):
    """
    Load articles from a JSON file and return them as a list of dictionaries.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    list: A list of dictionaries, where each dictionary represents an article.
    """
    try:
        with open(file_path, 'r') as file:
            articles = json.load(file)

        if not isinstance(articles, list):
            raise ValueError("JSON file does not contain a list of articles")

        return articles
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not valid JSON.")
        return []
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return []


if __name__=="__main__":
    # Read the list of items in ofInterest.json
    items = load_articles_from_json('./ratedArticles.json')
    # with open('./ratedArticles.json', 'r') as file:
    #     for line in file:
    #         items.append(json.loads(line))
    #         print(f"Read item: {items[-1]['title']}")

    # Create an HTML report of the items
    # html_report = "<html><head><title>Daily ArXive Report</title></head><body>"
    html_report =f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily ArXiv Roundup</title>

        <style>
        {style}
        </style>

    </head>
"""

    for index, item in enumerate(items):
        html_report += "<div class='item-box'>"
        html_report += f"<h2>{index+1}. {item['title']}</h2>"
        html_report += f"<p><strong>Abstract: </strong>{item['abstract']}</p>"
        html_report += f"<a href='{item['link']}' class='button'>Read More</a>"
        html_report += f"<a href='{item['pdf']}' class='button'>PDF</a>"
        html_report += "<div class='rating-bar-container'>"
        html_report += f"<div class='rating-bar' style='width: {item['Rating']*100}%'></div>"
        html_report += "</div>"
        html_report += f"<p><strong>Rating: </strong>{item['Rating']}</p>"
        html_report += f"<p><strong>Justification: </strong>{item['Justification']}</p>"
        html_report += "</div>"
    html_report += "</main></html>"
    # Save the HTML report to a file
    with open('./report.html', 'w') as file:
        file.write(html_report)
    print("HTML report generated successfully!")
