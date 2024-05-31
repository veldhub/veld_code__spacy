FROM python:3.10.12
RUN pip install spacy==3.6.0
RUN pip install de_dep_news_trf@https://github.com/explosion/spacy-models/releases/download/de_dep_news_trf-3.5.0/de_dep_news_trf-3.5.0.tar.gz
RUN pip install de_core_news_lg@https://github.com/explosion/spacy-models/releases/download/de_core_news_lg-3.6.0/de_core_news_lg-3.6.0-py3-none-any.whl

