import re
import json

def extract_and_clean_json(input_string):
    """
    Runs some regex to conver the possibly malformed JSON-like
    objects in the input string to valid JSON objects.
    Args:
        input_string (str): The input string containing JSON-like objects.
    Returns:
        list: A list of dictionaries, where each dictionary represents an item.
    """
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
