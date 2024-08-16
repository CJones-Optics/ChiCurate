# ArXiv Curator
This is a simple tool to help you curate your arXiv papers.
It is a simple tool which reads the rss feed of ArXiv and
uses an LLM running on Ollama to rank the papers in order of
relevance.

# Requirements
- Linux Install
  - It should work on MacOS, but I haven't tested it.
  - It should work in WSL.
- Python >3.12.4
- Ollama
- Local Ollama model:
  - mistral-nemo

# Installation
## Ollama
### Install
NetworkChuck has a good video on how to install Ollama.
So does Ollama's website itself. As of August 2024, the
installation process for linux is:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
## Script
### Through Git
- Clone the repo
- Use pip to install the requirements
```bash
git clone
pip install -r requirements.txt
```

## One line download
```bash

pip install -r requirements.txt
```

# Usage
## Configuration
There are four files for user configuration. They are:
- `config.yaml`
- `./userData/feeds.csv`
- `./userData/userPrompt.txt`
- `./userData/systemPrompt.txt`

The most important to configure is `userPrompt` and `feeds.csv`.

### `feeds.csv`
This csv should contain the rss feeds of the arXiv categories you are interested in.
The ArXiv website contains instructions on how to get the rss feed for a category.

### `userPrompt.txt`
This file is how you customize the ranking of the model. It is a simple text file
where you should describe your research interests. The model will rank papers
based on how well they match your interests.

### `systemPrompt.txt`
This prompt is sent to the LLM before anything else. It describes how the
LLM ought to act, and the schema for the output. You shouldn't need to change
this, but it may be useful to optimise.

### `config.yaml`
This file is used to configure the model used and the batch size of the articles
considered.

#### Choice of Model
The choice of model will have a massive impact on the models performance. Larger
models will take longer to run, but will be more accurate. Small models will run
faster, but has less intelligence to do the ranking. This will depends a lot
on the specifics of model architecture and the data it was trained on. So it is
easiest to just try a few models and see which one works best for you.

In my experiance, the `mistral-nemo` model is the best for my use case.

#### Batch Size
The batch size is the number of articles that are considered at once. It is unlikely
that the entire ArXiv feed can be considered at once since it will fall outside of
the context window of the model.
Larger sizes will cause the model to hallucinate, but may be faster. I hypothesize
that smaller sizes may not be more accurate, since the AI will not have any context
to compare particles against.

A batch size of 5 when using titles only seems to be a good middle ground. It allows the
model to have several articles to compare against each other when doing the rankingm whilst
not being so large that the model hallucinates.

## Running
The entire script can be run with the following command:
```bash
run.sh
```

On my machine it takes about 15 minutes to run using the `mistral-nemo` model.
My machine is a AMD Ryzen™ 5 5600G without any discrete GPU, and 16GB of RAM.

Since it takes a while, but is not time sensitive, so I have a cron job that runs
the script every day at 8am. This way I can wake up to a curated list of papers
every morning.
