
from chromadb import Client
from chromadb.config import Settings
import os
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from uuid import uuid1


class Chroma(object):

    def __init__(self,
                 embedding_model_name,
                 strategy) -> None:
        
        _DATABASE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 
                                           "database")
        self.persist_directory = os.path.join(_DATABASE_DIRECTORY,
                                              f"{embedding_model_name}__Chroma")
        self.client = Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory= self.persist_directory
        ))

        self._collection_name = f"{strategy}__collection"
        self.collection = self.client.get_or_create_collection(self._collection_name)

        self.embedding_model = SentenceTransformer(embedding_model_name)


    def _split_documents(data_directory):
        splitter = RecursiveCharacterTextSplitter(chunk_size=750,
                                                chunk_overlap=100)
        file_paths = []
        DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "data")
        for root, _, files in os.walk(DATA_DIRECTORY):
            for file in files:
                file_paths.append(os.path.join(root, file))
        # Modify here for parallelism or progress ase
        docs = TextLoader(file_path=file_paths[0], encoding='utf-8').load()
        for path in file_paths:
            docs.extend(TextLoader(file_path=path, encoding='utf-8').load())
        splitted_docs = splitter.split_documents(docs)
        return splitted_docs
    
    def _initialize_contents(self, 
                             docs):
        metadatas = []
        documents = []
        for doc in docs:
            documents.append(doc.page_content)
            metadatas.append(doc.metadata)
        ids = [str(uuid1()) for _ in range(len(documents))]
        db_contents = {'ids': ids,
                       'metadatas': metadatas,
                       'documents': documents}
        
        return db_contents

    def add_data(self, 
                 data_directory):

        try:
            splitted_docs = self._split_documents(data_directory)
            db_contents = self._initialize_contents(splitted_docs)
            self.collection.add(**db_contents)
            self.client.persist()
            return True
        except Exception as e:
            print("Error occured while adding docs: " + str(e))
            return False
        

    def query(self, 
              query_text,
              n_results):
        return self.collection.query(query_texts=query_text,
                                     n_results=n_results)
    
    def get_available_startegies():
        return ['ip','cosine','l2']

