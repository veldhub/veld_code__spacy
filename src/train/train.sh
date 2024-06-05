#!/bin/bash

python -m spacy train /veld/code/config2.cfg \
  --paths.train "$input_spacy_docbin_train" \
  --paths.dev "$input_spacy_docbin_dev" \
  --output "$output_model_path" \
  |& tee "$output_train_log_path"

python -m spacy evaluate \
  "${output_model_path}/model-best/" \
  "$input_spacy_docbin_eval" \
  |& tee "$output_eval_log_path"

