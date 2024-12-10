#!/bin/bash

set -e


# main command

command="python -m spacy init config --force /tmp/base_config.cfg"


# 'lang' arg

if ! [[ "$lang" = "" ]]; then
  command+=" --lang ${lang}"
else
  echo "var 'lang' is missing"
  exit 1
fi


# 'pipeline' args

pipeline=""

function build_pipeline_args {
  if [[ "$1" = "true" ]]; then
    if ! [[ "$pipeline" = "" ]]; then
      pipeline+=","
    fi
    pipeline+="$2"
  fi
}

build_pipeline_args "$tagger" "tagger"
build_pipeline_args "$parser" "parser"
build_pipeline_args "$ner" "ner"
build_pipeline_args "$entity_linker" "entity_linker"
build_pipeline_args "$entity_ruler" "entity_ruler"
build_pipeline_args "$textcat" "textcat"
build_pipeline_args "$textcat_multilabel" "textcat_multilabel"
build_pipeline_args "$lemmatizer" "lemmatizer"
build_pipeline_args "$trainable_lemmatizer" "trainable_lemmatizer"
build_pipeline_args "$morphologizer" "morphologizer"
build_pipeline_args "$attribute_ruler" "attribute_ruler"
build_pipeline_args "$senter" "senter"
build_pipeline_args "$sentencizer" "sentencizer"
build_pipeline_args "$tok2vec" "tok2vec"
build_pipeline_args "$transformer" "transformer"

if ! [[ "$pipeline" = "" ]]; then
  command+=" --pipeline ${pipeline}"
else
  echo "no pipeline set"
  exit 1
fi


# 'optimize' arg

if [[ "$optimize_efficiency" = "true" ]] &&[[ "$optimize_accuracy" = "true" ]] ; then
  echo "both 'optimize_efficiency' and 'optimize_accuracy' are set to 'true', but they are mutually exclusive"
  exit 1
else
  if [[ "$optimize_efficiency" = "true" ]]; then
    command+=" --optimize efficiency"
  fi
  if [[ "$optimize_accuracy" = "true" ]]; then
    command+=" --optimize accuracy"
  fi
fi


# 'GPU' arg

if [[ "$gpu" = "true" ]]; then
  command+=" --gpu"
fi


# 'pretraining' arg

if [[ "$pretraining" = "true" ]]; then
  command+=" --pretraining"
fi


# execute

echo "executing:"
echo "$command"
eval "$command"


# fill-config

command="python -m spacy init fill-config /tmp/base_config.cfg /veld/output/${out_config_file}"

echo "executing:"
echo "$command"
eval "$command"

