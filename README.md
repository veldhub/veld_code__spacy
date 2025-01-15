# veld_code__spacy

This repo contains several code velds encapsulating usage of [spaCy](https://spacy.io/).

## requirements

- git
- docker compose (note: older docker compose versions require running `docker-compose` instead of 
  `docker compose`)

## how to use

A code veld may be integrated into a chain veld, or used directly by adapting the configuration 
within its yaml file and using the template folders provided in this repo. Open the respective veld 
yaml file for more information.

Run a veld with:
```
docker compose -f <VELD_NAME>.yaml up
```

## contained code velds

**[./veld_convert.yaml](./veld_convert.yaml)**

Converts data to spacy docbin 

```
docker compose -f veld_convert.yaml up
```

**[./veld_create_config.yaml](./veld_create_config.yaml)**

Creates a spacy training configuration

```
docker compose -f veld_create_config.yaml up
```

**[./veld_train.yaml](./veld_train.yaml)**

Training setup

```
docker compose -f veld_train.yaml up
```

**[./veld_publish_to_hf.yaml](./veld_publish_to_hf.yaml)**

Publishes to huggingface

```
docker compose -f veld_publish_to_hf.yaml up
```

