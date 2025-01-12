# veld_code__spacy

This repo contains several code velds encapsulating usage of [spaCy](https://spacy.io/).

## requirements

- git
- docker compose

## how to use

The following code velds can either be integrated into chain velds or used on their own. More
information can be found within their respective veld yaml file:

- [./veld_convert.yaml](./veld_convert.yaml) : converts data to spacy docbin 
- [./veld_create_config.yaml](./veld_create_config.yaml) : creates a spacy training configuration
- [./veld_publish_to_hf.yaml](./veld_publish_to_hf.yaml) : publishes to huggingface
- [./veld_train.yaml](./veld_train.yaml) : training setup

