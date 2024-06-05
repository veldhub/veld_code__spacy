#!/bin/bash

python -m spacy train /veld/input/config.cfg \
  --paths.train /veld/input/train.spacy \
  --paths.dev /veld/input/dev.spacy \
  --output /veld/output/model/ \
  |& tee /veld/output/train.log

python -m spacy evaluate /veld/output/model/model-best/ /veld/input/eval.spacy |& tee /veld/output/eval.log

