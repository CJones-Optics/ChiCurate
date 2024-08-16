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

systemPrompt = ""
with open("./systemPrompt.txt", 'r') as f:
    s = f.read()
    systemPrompt = s

# print(systemPrompt)


userPromptPath = "./userPrompt.txt"
# Load the user prompt from a file into a string
userPromptPrepend = ""
with open(userPromptPath, 'r') as f:
    s = f.read()
    userPromptPrepend = s

# print(userPromptPrepend)

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
