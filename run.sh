#!/bin/bash

# bash script to run each subcomponent of the pipeline

# Enter python environment
source ./.venv/bin/activate

# Run the first element, if exit code is not 0, exit
echo "Starting the data collection"
python3 ./pullFeeds.py
exit_code=$?

if [ $exit_code -eq 1 ]; then
  echo "No articles from today. Are you working on the weekend?."
  exit 1
elif [ $exit_code -ne 0 ]; then
  echo "Data collection failed with exit code $exit_code, exiting script."
  exit $exit_code
fi

# Start the inference
echo "Starting inference"
python3 ./ollamaCall.py
echo "Inference complete, generating report"
python3 ./parseOutputs.py
python3 ./htmlReportGenerator.py

echo "Report generated"

if grep -q "^os:" config.yaml && [ "$(awk '/^os:/ {print $2}' config.yaml | tr -d '"' | tr -d "'")" = "windows" ]; then
    echo "OS is set to Windows"
    echo "saving to path"
    # Read the path from config.yaml
    path=$(awk '/^path:/ {print $2}' config.yaml | tr -d '"' | tr -d "'")
    # Add the mnt point to it
    path="/mnt/c/$path"
    mv ./report.html $path
else
    echo "OS is not set to Windows, opening report in browser"
    xdg-open ./report.html
fi
