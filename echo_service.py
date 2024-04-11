from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
import logging
import os
import sys
from langchain.vectorstores import Chroma

SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVICE_PORT = os.getenv('SERVER_PORT', 8080)
CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'I')

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2", cache_folder="/emb")

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter(
            '%(name)s [%(asctime)s] [%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    return logger

logger = get_logger('echo-service')
app = Flask(__name__)

@app.get("/healthcheck")
def readiness_probe():
    return "I'm ready!"

@app.post("/echo")
def echo():
    '''
    Main handler for input data sent by Snowflake.
    '''
    message = request.json
    logger.debug(f'Received request: {message}')

    if message is None or not message['data']:
        logger.info('Received empty message')
        return {}

    # input format:
    #   {"data": [
    #     [row_index, column_1_value, column_2_value, ...],
    #     ...
    #   ]}
    input_rows = message['data']
    logger.info(f'Received {len(input_rows)} rows')

    # output format:
    #   {"data": [
    #     [row_index, column_1_value, column_2_value, ...}],
    #     ...
    #   ]}
    output_rows = [[row[0], get_echo_response(row[1])] for row in input_rows]
    logger.info(f'Produced {len(output_rows)} rows')

    response = make_response({"data": output_rows})
    response.headers['Content-type'] = 'application/json'
    logger.debug(f'Sending response: {response.json}')
    return response

@app.post("/embedding")
def embedding():
    '''
    Main handler for input data sent by Snowflake.
    '''
    message = request.json
    logger.debug(f'Received request: {message}')

    if message is None or not message['data']:
        logger.info('Received empty message')
        return {}

    # input format:
    #   {"data": [
    #     [row_index, column_1_value, column_2_value, ...],
    #     ...
    #   ]}
    input_rows = message['data']
    logger.info(f'Received {len(input_rows)} rows')

    # output format:
    #   {"data": [
    #     [row_index, column_1_value, column_2_value, ...}],
    #     ...
    #   ]}
    def write_file(input):
        x.write(input)

    # input_rows=[[0, 'Shnatanu is legend!'], [1, 'Shantanu is older than history!'], [2, 'Shantanu is the origin of time!']]
    x=open("1.txt", "w")
    write = [[row[0], write_file(row[1])] for row in input_rows]
    x.close()
    

    output_rows = [[row[0], embedding_return(row[1])] for row in input_rows]
    logger.info(f'Produced {len(output_rows)} rows')

    response = make_response({"data": output_rows})
    response.headers['Content-type'] = 'application/json'
    logger.debug(f'Sending response: {response.json}')
    return response


@app.route("/ui", methods=["GET", "POST"])
def ui():
    '''
    Main handler for providing a web UI.
    '''
    if request.method == "POST":
        # getting input in HTML form
        input_text = request.form.get("input")
        # display input and output
        return render_template("basic_ui.html",
            echo_input=input_text,
            echo_reponse=get_echo_response(input_text))
    return render_template("basic_ui.html")

def get_echo_response(input):
    from langchain_community.document_loaders import TextLoader
    loader = TextLoader('1.txt')
    documents = loader.load()
    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter (chunk_size=50, chunk_overlap=0)
    texts= text_splitter.split_documents(documents)
    
    from langchain_community.vectorstores import faiss
    db = faiss.FAISS.from_documents(texts, embeddings)
    # retriever = db.as_retriever(search_kwargs={"k": 2})
    context=db.similarity_search(query=input ,fetch_k=2)
    return context

def embedding_return(input):
    return "Done"

if __name__ == '__main__':
    app.run(host=SERVICE_HOST, port=SERVICE_PORT)
