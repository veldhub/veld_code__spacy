#!/bin/bash

set -e

python -m spacy package \
  --force \
  /veld/input/ \
  /tmp/ \
  --build wheel \
  --name "$model_name" \
  --version "$version"

huggingface-cli login --token $hf_token

python -m spacy huggingface-hub push /tmp/*/dist/*

