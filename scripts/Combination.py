import statistics
import os, sys
from tabulate import tabulate
from tqdm import tqdm

sys.path.append('..')
from embeddings.HuggingFaceEmbedding import HuggingFaceEmbedding
from vectorstores.Chroma import Chroma
from vectorstores.Milvus import Milvus

class Combination(object):

    def __init__(self,
                 db_model,
                 queries_path : str
                 ) -> None:
        
        self.db_model = db_model
        self.queries_path = queries_path


    def get_query_source_map(self):
        qa = dict()
        contents = None
        import json
        with open(file=self.queries_path, mode='r') as fn:
            contents = json.load(fn)
        for qa_collection in contents:
            query = qa_collection['query']
            var_dict = qa_collection['variables']
            variables = list(var_dict.keys())
            sources = qa_collection['sources']
            num_of_instances = len(var_dict[variables[0]])
            for idx in range(num_of_instances):
                instance = dict()
                for var in variables:
                    instance[var] = var_dict[var][idx]
                question = query.format(**instance)
                qa[question] = sources[idx]
        return qa

    
    def get_sources(self,
                    query):
        db = self.db_model
        # output = db.query(query, 
        #                   -1,
        #                   include=['metadatas'])
        output = db.query(query, 
                          -1,
                          include=['metadatas',
                                   'distances'])
        # print(output['metadatas'])
        metadatas = output['metadatas'][0] 
        sources = []
        for metadata in metadatas:
            sources.append(os.path.basename(metadata['source']))
        # print(sources)
        return sources
    
    def get_k(self, 
              query, 
              sources, 
              matches):
        
        output_sources = self.get_sources(query=query)
        given_sources = set(sources) 
        for idx, src in enumerate(output_sources):
            if src in given_sources:
                matches -= 1
                if matches == 0: return idx + 1
        raise Exception(f"Number of unique sources doesn't match the number of matches: {query}")
        
    
    def get_report(self,
                   matches):
        all_k = []
        query_srcs_map = self.get_query_source_map()
        with tqdm(total=len(query_srcs_map.items()),
                  desc="Getting the values of k: ",
                  ncols=100) as pbar_k:
            for query, sources in query_srcs_map.items():
                # print(query, sources)
                all_k.append(self.get_k(query=query,
                                        sources=sources,
                                        matches=matches))
                pbar_k.update()


        avg = round(sum(all_k) / len(all_k))
        sigma = round(statistics.stdev(all_k), 2)
        report = {'Embedding Model': self.db_model.emb_model_name,
                  'DB Type': self.db_model.name,
                  'Strategy': self.db_model.strategy,
                  'Average k': avg,
                  'Sigma': sigma}
        return report
    

    def save_reports(self, 
                     all_reports,
                     file_path):
        row = ['Embedding Model',
                'DB Type',
                'Strategy',
                'Average k',
                'Sigma']
        if not os.path.exists(file_path):
            with open(file=file_path, mode='w') as fn: 
                fn.write(' '.join(row))
                fn.write('\n\n')
        with open(file_path, "r") as file:
            lines = file.readlines()
            data = [row]
            for line in (lines[2:]):
                row = [word.strip() for word in line.strip().split('|') if len(word.strip()) > 0]
                data.append(row)
        for report in all_reports: data.append(list(report.values()))
            # print(data)
        table = tabulate(data, headers="firstrow", tablefmt="pipe")
        with open(file_path, "w") as file: file.write(table)



def main():
    emb_model = HuggingFaceEmbedding("allenai/scibert_scivocab_uncased")
    # db_model = Chroma(embedding=emb_model,
    #                   strategy="ip")
    db_model = Milvus(embedding=emb_model,
                      strategy="ip")
    data_directory = os.path.join(os.path.abspath(os.pardir),
                                  'data')
    db_model.add_data(data_directory=data_directory)
    assets_directory = os.path.join(os.path.abspath(os.pardir),
                                    "assets")
    queries_path = os.path.join(assets_directory, 'queries.json')
    combination = Combination(db_model=db_model,
                              queries_path=queries_path)
    # qa = combination.get_query_source_map()
    # print(combination.get_sources('Describe the ICD-10 CM code A01.2'))
    # query = list(qa.keys())[0]
    # print(combination.get_k(query=query,
    #                         sources=qa[query],
    #                         matches=1))
    print(combination.get_report(matches=1))    
    
        


if __name__ ==  "__main__": main()