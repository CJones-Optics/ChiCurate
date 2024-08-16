# Read the list of items in ofInterest.json and create an HTML report of the items.
import json
import pandas as pd
import html

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

def main():
    stylePath = "style.css"
    with open(stylePath, 'r') as f:
        style = f.read()
    # Read the list of items in ofInterest.json
    items = load_articles_from_json('./ratedArticles.json')
    # Create an HTML report of the items
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

    # This loops over all the items in the list and creates a div for each item
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

if __name__=="__main__":
    main()
