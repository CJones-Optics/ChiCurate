# ArXiv Curator
This is a simple tool to help you curate your arXiv papers.
It is a simple tool which reads the rss feed of ArXiv and
uses an LLM running on Ollama to rank the papers in order of
relevance.

# Requirements

## Operating System
The script is designed to work on Linux. This includes
Windows Subsystem for Linux (WSL), and has been tested.
Read the intstillation documentation. It should work on MacOS,
but I haven't tested it.


- Python >3.12.4
- Ollama
- Local Ollama model:
  - mistral-nemo

# Installation
## Ollama
### Install
NetworkChuck has a good video on how to install Ollama. [VIDEO](https://www.youtube.com/watch?v=Wjrdr0NU4Sk&t=1s)
So does Ollama's website itself. [OLLAMA](https://ollama.com/download)

#### Linux
As of August 2024, the
installation process for linux is:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
#### Windows

1. Install Windows Subsystem for Linux (WSL)
This is a linux environment that runs on Windows.
It is the easiest way to run Ollama on Windows.

```batch
wsl --install
```

This *should* install Ubuntu within WSL automatically.
If it didn't (Like it didnt for me) run
```batch
wsl --install Ubuntu
```

2. Setup Ubuntu VM
You will be prompted to setup a username and password. After this, update the
newly installed Ubuntu VM.
```bash
sudo apt-get update
sudo apt-get upgrade
```
And install `pip` and `python-venv`
```bash
sudo apt-get install python3-pip python3-venv
```

From here you can follow the Linux Instructions.

#### MacOS
There is a dedicated installer for Ollama on MacOS. Download
using that. The other instructions after getting Ollama running
should be the same.

## LLM Model
You have the choice of which model to use. There are tradeoffs
in the model selection. See my blog for details. I have found
mistral-nemo to be the best for my use case.

```bash
ollama pull mistral-nemo
```

You can pull as many models as you like, and try them out by
altering the `conifg.yaml` file.

## Script
If you are using WSL, ensure you run the following commands within the Ubuntu terminal.
### Through Git
- Clone the repo
- Use pip to install the requirements
```bash
git clone
cd ./ArXivCurator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## One line download (BETA)
```bash
curl -L https://github.com/CJones-Optics/ArXivCurator/archive/refs/heads/main.zip -o temp.zip && unzip temp.zip && cd ArXivCurator-main && pip install -r requirements.txt && cd .. && rm temp.zip```
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
This file is used to configure the model used, the batch size of the articles
considered and the colour theme of the output.

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

#### NOTE FOR WINDOWS USERS
If you are using WSL, you will want to move the generated report out of your linux
subsystem and into your windows filesystem. To do this switch `os` to `windows` in the
`config.yaml` file, and set the path to the desired location.

*Note 2* You will need to use the windows path with linux style slashes. For example:
`Users/username/Documents/ArXivCurator/` this might get neatned up in future versions.

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
