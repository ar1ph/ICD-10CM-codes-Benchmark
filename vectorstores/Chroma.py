
import sys, os
from typing import Any
from base import BaseVectorstore
from tqdm import tqdm
from uuid import uuid1
from chromadb import Client
from chromadb.config import Settings
sys.path.append('..')
from embeddings.base import BaseEmbedding
from embeddings.HuggingFaceEmbedding import HuggingFaceEmbedding



class Chroma(BaseVectorstore):

    SEARCH_STRATEGIES = {'ip',
                         'cosine',
                         'l2'}

    def __init__(self,
                 embedding,
                 strategy
                 ) -> None:
        
        _DATABASE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 
                                           "database")
        self.embedding = embedding
        self.strategy = strategy
        _emb_model_name = embedding.get_name()
        self.persist_directory = os.path.join(_DATABASE_DIRECTORY,
                                              f"{_emb_model_name}__Chroma")
        self._client = Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory= self.persist_directory
        ))
        self._add_collection()
        super().__init__()


    def _collection_exist(self,
                         name : str) -> bool:
        try:
            collection = self._client.get_collection(name)
            return True
        except:
            return False



    def __setattr__(self, 
                    __name: str, 
                    __value: Any
                    ) -> None:
        
        if __name == "embedding":
            if not isinstance(__value, BaseEmbedding):
                error_msg = "Embedding must be of BaseEmbedding type"
                raise ValueError(error_msg)
        elif __name == "strategy":
            if not __value in Chroma.SEARCH_STRATEGIES:
                error_msg = f"{__value} search strategy is not supported"
                raise ValueError(error_msg)
            
        return super().__setattr__(__name, __value)
    

    def _add_collection(self):

        name = 'chroma_collection'
        metadata = {'hnsw:space':self.strategy,
                    'hnsw:construction_ef':4096,
                    'hnsw:search_ef':4096,
                    'hnsw:M':100}
        func = self.embedding.get_function()
        if self._collection_exist(name): self._client.reset()
        print(self._client.list_collections())
        self._collection = self._client.create_collection(name,
                                                          metadata,
                                                          func)
        
    

    def add_data(self, 
                 data_directory: str) -> None:
        
        try:
            docs = super().process_documents(data_directory=data_directory)
            with tqdm(total=len(docs), 
                      desc="Adding documents", 
                      ncols=80) as pbar:
                for doc in docs:
                    # embedding = self.embedding.from_text(doc.page_content)
                    self._collection.add(ids=[str(uuid1())],
                                        # embeddings=[embedding],
                                        metadatas=[doc.metadata],
                                        documents=[doc.page_content]
                                        )
                    pbar.update()
            self._client.persist()
            return True
        except Exception as e:
            print("Error occured while adding documents" + str(e))
            return False
        
    def query(self, 
              query_text: str, 
              n_results: int,
              inclue: list[str]):
        if n_results == -1:
            return self._collection.query(query_texts=query_text,
                                          n_results=self.get_max_n(),
                                          include=inclue)
        return self._collection.query(query_text=query_text,
                                      n_results=n_results,
                                      include=inclue)
        
    def get_available_strategies(self) -> list[str]:
        return Chroma.SEARCH_STRATEGIES
    
    def get_max_n(self) -> int:
        return self._collection.count()

    


def main():
    embedding = HuggingFaceEmbedding(model_name='all-MiniLM-L6-v2')
    chroma = Chroma(embedding=embedding,
                    strategy='ip')
    data_directory = os.path.join(os.path.abspath(os.curdir),
                                  'data_temp')
    chroma.add_data(data_directory=data_directory)
    print(chroma.query(query_text='Describe the ICD-10 Code A01.2',
                       n_results=-1))


if __name__ == "__main__": main()