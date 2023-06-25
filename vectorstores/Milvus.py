
import sys, os
from typing import Any
# from base import BaseVectorstore
from .base import BaseVectorstore
from tqdm import tqdm
from uuid import uuid1
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
sys.path.append('..')
from embeddings.base import BaseEmbedding
from embeddings.HuggingFaceEmbedding import HuggingFaceEmbedding



class Milvus(BaseVectorstore):

    SEARCH_STRATEGIES = {'ip',
                         'l2'}

    def __init__(self,
                 embedding,
                 strategy,
                 host="localhost",
                 port="19530",
                 ) -> None:
        
        super().__init__(embedding=embedding,
                         strategy=strategy)
        self.name = 'Milvus'
        emb_model_name = embedding.get_name()
        self.emb_model_name = emb_model_name
        connections.connect("default",
                            host=host,
                            port=port)
        self._add_collection()


    def _collection_exist(self,
                         name : str) -> bool:
        return utility.has_collection(name)


    def __setattr__(self, 
                    __name: str, 
                    __value: Any
                    ) -> None:
        
        if __name == "embedding":
            if not isinstance(__value, BaseEmbedding):
                error_msg = "Embedding must be of BaseEmbedding type"
                raise ValueError(error_msg)
        elif __name == "strategy":
            if not __value in Milvus.SEARCH_STRATEGIES:
                error_msg = f"{__value} search strategy is not supported"
                raise ValueError(error_msg)
            
        return super().__setattr__(__name, __value)
    

    def _add_collection(self):

        name = 'milvus_collection'
        if self._collection_exist(name): 
            utility.drop_collection(name)
            # self._collection = Collection(name)
            # print("Collection exist, " , self._collection.num_entities)
            # return
        id_field = FieldSchema(
            name="ids",
            dtype=DataType.VARCHAR,
            is_primary=True, 
            auto_id=False, 
            max_length=64
        )
        metadata_field = FieldSchema(
            name="source",
            dtype=DataType.VARCHAR,
            max_length=512

        )
        embed_field = FieldSchema(
            name="embeddings",
            dtype=DataType.FLOAT_VECTOR,
            dim=self.embedding.get_dimension()
        )
        doc_field = FieldSchema(
            name="documents",
            dtype=DataType.VARCHAR,
            max_length=65535
        )

        fields = [id_field, metadata_field, embed_field,  doc_field]
        schema = CollectionSchema(fields, "Milvus collection")
        self._collection = Collection(name, schema, consistency_level="Strong")
        print(self._collection.description)
        
    

    def add_data(self, data_directory: str) -> None:
        
        docs = super().process_documents(data_directory=data_directory)
        datas = [[], [], [], []]
        with tqdm(total=len(docs), 
                    desc="Extracting datas", 
                    ncols=80) as pbar:
            for doc in docs:
                # embedding = self.embedding.from_text(doc.page_content)
                # self._collection.add(ids=[str(uuid1())],
                #                     # embeddings=[embedding],
                #                     metadatas=[doc.metadata],
                #                     documents=[doc.page_content]
                #                     )
                datas[0].append(str(uuid1()))
                datas[1].append(doc.metadata['source'])
                datas[2].append(self.embedding.from_text(doc.page_content))
                datas[3].append(doc.page_content)
                pbar.update()

        # data = [
        #     [str(uuid1())],
        #     [docs[0].metadata['source']],
        #     [self.embedding.from_text(docs[0].page_content)],
        #     [docs[0].page_content]
        # ]
        self._collection.insert(datas)
        self._collection.flush()
        # print(self._collection.num_entities)
        # Creating indexes for the embeddings field
        field_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "nlist": 4096,
            "m": 100
        }
        self._collection.create_index("embeddings", field_params)
        self._collection.load()

    def _process_output(self,
                        output,
                        include):
        all_fields = {
            "ids":[],
            "distances":[],
            "metadatas":[[]],
            "documents":[]
        }
        for row in output[0]:
            row_dict = row.to_dict()
            all_fields['ids'].append(row_dict['id'])
            all_fields['distances'].append(row_dict['distance'])
            all_fields['metadatas'][0].append({'source':row_dict['entity']['source']})
            all_fields['documents'].append(row_dict['entity']['documents'])
        
        new_output = dict()
        for field in include : new_output[field] = all_fields[field] 
        return new_output
        
    def query(self, 
              query_text: str, 
              n_results: int,
              include: list[str]):

        query_vector = self.embedding.from_text(query_text)
        limit = self._collection.num_entities if n_results == -1 else n_results
        param = {
            "metric_type": "L2",
            "limit": limit,
            # "nlist": 4096,
            # "m":100
        }
        output = self._collection.search(data=[query_vector],
                                         anns_field="embeddings",
                                         param=param,
                                         output_fields=['source',
                                                        'documents'],
                                         limit=limit)
        # print("check ", output[0][0].to_dict())
        # self._process_output(output, include)
        return self._process_output(output=output,
                                    include=include)
        
        
    def get_available_strategies(self) -> list[str]:
        return Milvus.SEARCH_STRATEGIES
    
    def get_max_n(self) -> int:
        return self._collection.num_entities
    
    def __call__(self, 
                 embedding, 
                 strategy, 
                 data_directory: str
                 ) -> None:
        raise NotImplementedError()

    


def main():
    # embedding = HuggingFaceEmbedding(model_name='emilyalsentzer/Bio_ClinicalBERT')
    embedding = HuggingFaceEmbedding(model_name='all-MiniLM-L6-v2')
    
    milvus = Milvus(embedding=embedding, strategy='ip')
    milvus.add_data(os.path.join(os.path.abspath(os.pardir), 'data_temp'))
    # milvus.query("Describe the ICD-10 CM Code A01.2", n_results=-1, include=["metadatas"])
    print(milvus.query("Describe the ICD-10 CM Code A01.2", n_results=-1, include=["metadatas"]))


if __name__ == "__main__": main()