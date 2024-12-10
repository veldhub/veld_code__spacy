#!/bin/bash
#
# this script is run as docker entrypoint, ensuring that spacy models are available and cached


if [[ -n "$model_base" ]]; then
  if [ -e /tmp/models_base_cache/"$model_base" ]; then
    echo "found ${model_base} in /tmp/models_base_cache/ , using that."
  else
    echo "could not find ${model_base} in /tmp/models_base_cache/ , downloading."
    python -m spacy download "$model_base"
    cp -r /usr/local/lib/python3.10/site-packages/"$model_base"* /tmp/models_base_cache/
  fi
fi

exec "$@"
