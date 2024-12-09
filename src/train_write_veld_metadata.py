import os
import json

import yaml


SPACY_METADATA_FILE = "/veld/output/model-best/meta.json"
VELD_METADATA_FILE = "/veld/output/model-best/veld.yaml"


with open(SPACY_METADATA_FILE, "r") as f:
    spacy_metadata = json.load(f)
spacy_metadata = {"performance": spacy_metadata["performance"]}
veld_metadata = {
    "x-veld": {
        "data": {
            "file_type": "spacy model",
            "contents": [
                "spacy model",
                "NLP model"
                "NER model"
            ],
            "additional": spacy_metadata
        }
    }
}
with open(VELD_METADATA_FILE, "w") as f:
    yaml.dump(veld_metadata, f, sort_keys=False)

