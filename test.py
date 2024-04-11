k1=0

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# @post
def embedding():
    def write_file(input):
        x.write(input)

    input_rows=[[0, 'Shnatanu is legend!'], [1, 'Shantanu is older than history!'], [2, 'Shantanu is the origin of time!']]
    x=open("1.txt", "w")
    write = [[row[0], write_file(row[1])] for row in input_rows]
    x.close()

def get_echo_response(input, k1):
    if k1==0:
        k1+=1
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

if __name__=='__main__':
    embedding()
    while True:
        result=get_echo_response(input("q: "), k1=k1)
        print(result)

