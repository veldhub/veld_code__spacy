#!/bin/bash
#
# this script is run as docker entrypoint, checking if $model_base var is set (indicating that spacy 
# should base some workload on a pre-trained model provided by spacy). If this var is set, the 
# $PYTHONPATH var is extended to the /tmp/models_base_cache/ volume where models are chached on the
# host. This enables dynamic spacy model loading without needing to bake it into the docker image 
# itself, while still avoiding downloads at each container start-up.

if [[ -n "$model_base" ]]; then
  export PYTHONPATH="/tmp/models_base_cache/:$PYTHONPATH"
  if [ -e /tmp/models_base_cache/"$model_base" ]; then
    echo "found ${model_base} in /tmp/models_base_cache/ , using that."
  else
    echo "could not find ${model_base} in /tmp/models_base_cache/ , downloading."
    python -m spacy download "$model_base"
    cp -r /usr/local/lib/python3.10/site-packages/"$model_base"* /tmp/models_base_cache/
  fi
fi

exec "$@"
