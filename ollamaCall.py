import ollama
import json
from RAGLoader import getTodaysTitles

models = ollama.list()['models']
models = {
    'LLama3':"llama3:latest",
    'Gemma2':"gemma2:latest",
    'Mistral':"mistral:latest",
    'Mistral-Nemo':"mistral-nemo:latest"
}

path = "./todays.json"
batchSize = 5
titleBatches = getTodaysTitles(path,batchSize)

def constructUserPrompt(prompt, data):
    outputStr = prompt + "\n"
    for item in data:
        outputStr += json.dumps(item)+"\n"
    return outputStr

systemPrompt = """
You are a helpful AI Research assistant.
Your job is to read the titles of a research paper and evaluate their relvance to a researcher. The user will
tell you what they study, and what they are interested in. They will then give you a list of article IDs and titles.
Analyse the following list, and give a Rating of its relevance to the reader, and a justification.
Do not put ANYTHING in the response that is not in the JSON.

The response should be in the following format:

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ArticleID": {
            "type": "string",
            "description": "A unique identifier for the article"
          },
          "Justification": {
            "type": "string",
            "description": "An explanation of why the article is is not relevant to the user's interests"
          },
          "Rating": {
            "type": "number",
            "format": "float",
            "description": "A rating for the article, between 0 and 1, where 1 is the highest rating"
          }
        },
        "required": ["ArticleID", "Justification", "Rating"]
      }
    }
  },
  "required": ["items"]
}
"""

userPromptPrepend = """
I am an optical engineer working in Free Space Optical Communication (FSOC).
I am interested in Adaptive Optics, optical communication,photonic lanters,atmospheric turbulence and monitoring,
wavefront sensing and control, phase control and laser communication.
"""

for i in range(len(titleBatches)):
    print(f"Batch {i+1} of {len(titleBatches)}")
    userPrompt = constructUserPrompt(userPromptPrepend, titleBatches[i])
    messages = [
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": userPrompt }
    ]
    response = ollama.chat(model=models['Mistral-Nemo'],
        messages=messages
    )
    # print(response['message']['content'])
    # Save the response to text file
    with open(f'./ollamaResponse/response{i:02d}.json', 'w') as f:
        f.write(response['message']['content'])
