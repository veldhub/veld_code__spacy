FROM python:3.10.12
RUN pip install spacy==3.8.2
RUN pip install PyYAML==6.0.2
RUN pip install spacy-huggingface-hub==0.0.10
ENTRYPOINT ["/veld/code/load_models_base_cache.sh"]

