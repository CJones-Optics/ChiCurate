import re
import json

def extract_and_clean_json(input_string):
    # Regular expression to match the desired JSON-like objects
    pattern = r'\{\s*"ArticleID"\s*:\s*"[^"]*"\s*,\s*"Justification"\s*:\s*"[^"]*"\s*,\s*"Rating"\s*:\s*\d+(?:\.\d+)?\s*\}'

    # Find all matches in the input string
    matches = re.findall(pattern, input_string)

    # List to store the cleaned items
    cleaned_items = []

    for match in matches:
        try:
            # Try to parse the match as JSON
            item = json.loads(match)
            cleaned_items.append(item)
        except json.JSONDecodeError:
            # If parsing fails, try to clean up the item manually
            cleaned_match = match.replace("'", '"')  # Replace single quotes with double quotes
            cleaned_match = re.sub(r'(\w+):', r'"\1":', cleaned_match)  # Ensure all keys are quoted
            try:
                item = json.loads(cleaned_match)
                cleaned_items.append(item)
            except json.JSONDecodeError:
                # If it still fails, skip this item
                continue

    return cleaned_items

# Function to convert the result to a string
def result_to_string(items):
    return json.dumps(items, indent=2)


# input_string = """
# Some text before
#       {
#         "ArticleID": "oai:arXiv.org:2404.08725v2",
#         "Justification": "Not directly related to optical engineering or FSOC; focuses on data protection for Super-Kamiokande detector.",
#         "Rating": 0.1
#       },
#       {
#         "ArticleID": "oai:arXiv.org:2404.08747v2",
#         "Justification": "Firectly related to optical engineering and FSOC; focuses on data protection for Super-Kamiokande detector.",
#         "Rating": 0.8
#       },
#       {
#         'ArticleID': "oai:arXiv.org:2404.08726v1",
#         'Justification': 'Another example with single quotes',
#         'Rating': 0.5
#       }
# Some text after
# """

# # Extract and clean the JSON items
# cleaned_items = extract_and_clean_json(input_string)

# # Convert the result to a string

# result_string = result_to_string(cleaned_items)

# print(result_string)
