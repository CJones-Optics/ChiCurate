import ollama
import json
from RAGLoader import getTodaysTitles
import yaml
import os

def constructUserPrompt(prompt, data):
    outputStr = prompt + "\n"
    for item in data:
        outputStr += json.dumps(item)+"\n"
    return outputStr

def main():
    path = "./data/todays.json"
    with open("./config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    batchSize = config['batch-size']
    model = config['Model']

    titleBatches = getTodaysTitles(path,batchSize)
    with open("./userData/systemPrompt.txt", 'r') as f:
        systemPrompt = f.read()
    userPromptPath = "./userData/userPrompt.txt"
    # Load the user prompt from a file into a string
    with open(userPromptPath, 'r') as f:
        userPromptPrepend = f.read()
    for i in range(len(titleBatches)):
        print(f"Batch {i+1} of {len(titleBatches)}")
        userPrompt = constructUserPrompt(userPromptPrepend, titleBatches[i])
        messages = [
            {"role": "system", "content": systemPrompt},
            {"role": "user",   "content": userPrompt }
        ]

        # This is the part which calls the LLM
        response = ollama.chat(model=model,messages=messages)

        # Check if ./data/ollamaResponse exists and create it if it doesn't
        if not os.path.exists('./data/ollamaResponse'):
            os.makedirs('./data/ollamaResponse')

        # Save the response to text file
        with open(f'./data/ollamaResponse/response{i:02d}.json', 'w') as f:
            f.write(response['message']['content'])

if __name__=="__main__":
    main()
