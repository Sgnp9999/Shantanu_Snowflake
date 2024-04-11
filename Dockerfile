ARG BASE_IMAGE=python:3.10-slim-buster
FROM $BASE_IMAGE
COPY . ./
RUN pip install --upgrade pip && \
    pip install flask snowflake-connector-python langchain sentence_transformers chromadb
CMD ["python3", "echo_service.py"]

