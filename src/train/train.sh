#!/bin/bash


in_train_docbin_file="/veld/input/${in_train_docbin_file}"
in_dev_docbin_file="/veld/input/${in_dev_docbin_file}"
in_eval_docbin_file="/veld/input/${in_eval_docbin_file}"
out_model_folder="/veld/output/${out_model_folder}"
out_train_log_file="/veld/output/${out_train_log_file}"
out_eval_log_file="/veld/output/${out_eval_log_file}"


python -m spacy train /veld/code/config2.cfg \
  --paths.train "$in_train_docbin_file" \
  --paths.dev "$in_dev_docbin_file" \
  --output "$out_model_folder" \
  |& tee "$out_train_log_file"

python -m spacy evaluate \
  "${out_model_folder}/model-best/" \
  "$in_eval_docbin_file" \
  |& tee "$out_eval_log_file"

