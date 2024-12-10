#!/bin/bash

set -e

python -m spacy train /veld/input/config/"$in_spacy_config" \
  --paths.train /veld/input/docbin/"$in_train_docbin_file" \
  --paths.dev /veld/input/docbin/"$in_dev_docbin_file" \
  --output /veld/output/ \
  |& tee /veld/output/"$out_train_log_file"

python -m spacy evaluate \
  /veld/output/model-best/ \
  /veld/input/docbin/"$in_eval_docbin_file" \
  |& tee /veld/output/"$out_eval_log_file"

python /veld/code/train_write_veld_metadata.py

