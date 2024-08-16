import ollama
import json
from RAGLoader import getTodaysTitles

models = {
    'LLama3':"llama3:latest",
    'Gemma2':"gemma2:latest",
    'Mistral':"mistral:latest",
    'Mistral-Nemo':"mistral-nemo:latest"
}


def constructUserPrompt(prompt, data):
    outputStr = prompt + "\n"
    for item in data:
        outputStr += json.dumps(item)+"\n"
    return outputStr


def main():
    path = "./todays.json"
    batchSize = 5
    titleBatches = getTodaysTitles(path,batchSize)

    with open("./systemPrompt.txt", 'r') as f:
        systemPrompt = f.read()

    userPromptPath = "./userPrompt.txt"
    # Load the user prompt from a file into a string
    with open(userPromptPath, 'r') as f:
        userPromptPrepend = f.read()

    for i in range(len(titleBatches)):
        print(f"Batch {i+1} of {len(titleBatches)}")
        userPrompt = constructUserPrompt(userPromptPrepend, titleBatches[i])
        messages = [
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userPrompt }
        ]

        # This is the part which calls the LLM
        response = ollama.chat(model=models['Mistral-Nemo'],
            messages=messages
        )

        # Save the response to text file
        with open(f'./ollamaResponse/response{i:02d}.json', 'w') as f:
            f.write(response['message']['content'])

if __name__=="__main__":
    main()
