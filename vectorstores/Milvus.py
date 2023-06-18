
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

        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.strategy = strategy

        self._collection_name = f"chroma__collection"
        print(self._collection_name)
        self.collection = self.client.get_or_create_collection(name=self._collection_name,
                                                               embedding_function=self.embedding_model.encode
                                                               )
        # self.collection = self.client.get_collection(name=self._collection_name,
        #                                                        embedding_function=self.embedding_model.encode,
        #                                                        )
        self.collection.modify(metadata={"hnsw:space":strategy})

    def _split_documents(self, data_directory):
        splitter = RecursiveCharacterTextSplitter(chunk_size=750,
                                                chunk_overlap=100)
        file_paths = []
        # print(data_directory)
        # DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "data")
        db_files = set(self.get_source_files())
        for root, _, files in os.walk(data_directory):
            for file in files:
                if file not in db_files: file_paths.append(os.path.join(root, file))
        # Modify here for parallelism or progress ase
        if len(file_paths) > 0:
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
            # print(db_contents)
            self.client.persist()
            return True
        except Exception as e:
            print("Error occured while adding docs: " + str(e))
            return False
        

    def query(self, 
              query_text,
              n_results):
        if n_results == -1:
            print(f"n_results: {self.collection.count()}")
            return self.collection.query(query_texts=query_text,
                                         n_results=self.collection.count())
        return self.collection.query(query_texts=query_text,
                                     n_results=n_results)
    
    def get_available_startegies(): return ['ip','cosine','l2']
    # def get_available_startegies(): return ['cosine', 'ip']
    
    def get_strategy(self): return self.strategy

    def count(self): return self.collection.count()

    def get_source_files(self): 
        metadatas = self.collection.get()['metadatas']
        sources = []
        for metadata in metadatas:
            sources.append(os.path.basename(metadata['source']))
        return sources

    def reset(self): self.client.reset()




def main():

    chroma_obj = Chroma(embedding_model_name='all-MiniLM-L6-v2', strategy='cosine')
    print(chroma_obj.count())
    chroma_obj = Chroma(embedding_model_name='all-MiniLM-L6-v2', strategy='ip')
    print(chroma_obj.count())
    chroma_obj = Chroma(embedding_model_name='all-MiniLM-L6-v2', strategy='l2')
    print(chroma_obj.count())


if __name__ == "__main__": main()

