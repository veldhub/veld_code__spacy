#!/bin/bash

python -m spacy init config -F /tmp/base_config.cfg --lang "$model_base" --pipeline ner,textcat --optimize accuracy

python -m spacy init fill-config /tmp/base_config.cfg /veld/output/"$out_config_file" --pretraining

