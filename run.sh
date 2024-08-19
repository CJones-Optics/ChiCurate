#!/bin/bash

# bash script to run each subcomponent of the pipeline

# Enter python environment
source ./.venv/bin/activate

# Run the first element, if exit code is not 0, exit
echo "Starting the data collection"
python3 ./main.py
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

echo "Report generated, Opening in browser"
xdg-open ./report.html
