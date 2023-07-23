FROM python:3.10.12
RUN pip install spacy==3.6.0
RUN pip install de_dep_news_trf@https://github.com/explosion/spacy-models/releases/download/de_dep_news_trf-3.5.0/de_dep_news_trf-3.5.0.tar.gz
RUN useradd -u 1000 docker_user
RUN chown -R docker_user:docker_user /home/
USER docker_user