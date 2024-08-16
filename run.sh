#!/bin/bash

# bash script to run each subcomponent of the pipeline


# Enter python environment
source ./.venv/bin/activate

# run the each component
python3 ./main.py

# Start the inference
echo "Starting inference"
python3 ./ollamaCall.py

echo "Inference complete, generating report"
python3 ./parseOutputs.py
python3 ./htmlReportGenerator.py

echo "Report generated, Opening in browser"
xdg-open ./report.html
