import importlib
import statistics
import os 
from tabulate import tabulate

class Combination(object):

    def __init__(self,
                 db_name,
                 embedding_model_name) -> None:
        self.DBModule = self._import_db_module(db_name)
        self.embedding_model_name = embedding_model_name
        self.db_name = db_name
        self.db_objs = self._generate_db_objs()

    def get_strategies(self):
        return self.DBModule.get_available_startegies()

    def _generate_db_objs(self):
        all_strategies = self.DBModule.get_available_startegies()
        db_objs = dict()
        for strategy in all_strategies:
            db_objs[strategy] = self.DBModule(self.embedding_model_name,
                                              strategy)
        return db_objs
    
    def _get_sources(self,
                     query,
                     db):
        output = db.query(query, -1)
        metadatas = output['metadatas'][0]
        # distances = output['distances']
        # print(distances)
        sources = []
        for metadata in metadatas:
            sources.append(os.path.basename(metadata['source']))
        return sources
    
    def _get_k(self, 
              query, 
              sources, 
              matches,
              db):
        output_sources = self._get_sources(query=query,
                                           db=db)
        given_sources = set(sources)
        # print(output_sources)
        for idx, src in enumerate(output_sources):
            if src in given_sources:
                matches -= 1
                if matches == 0:
                    return idx + 1
        raise Exception(f"Number of unique sources doesn't match the number of matches: {query}")
        
    
    def _report_for_one(self, 
                        query_srcs_map,
                        db_obj,
                        matches):
        all_k = []
        for query, sources in query_srcs_map.items():
            # print(query, sources)
            all_k.append(self._get_k(query=query,
                                     sources=sources,
                                     matches=matches,
                                     db=db_obj))


        avg = round(sum(all_k) / len(all_k))
        sigma = round(statistics.stdev(all_k), 2)
        report = {'Embedding Model': self.embedding_model_name,
                  'DB Type': self.db_name,
                  'Strategy': db_obj.get_strategy(),
                  'Average k': avg,
                  'Sigma': sigma}
        return report
    # query_src_map: query : str -> src : str
    def generate_benchmark(self,
                           query_srcs_map,
                           matches,
                           print_reports=False):
        db_objs = self.db_objs
        # for query in query_srcs_map:
    
        all_reports = []
        for db_obj in db_objs:
            report = self._report_for_one(query_srcs_map=query_srcs_map,
                                          matches=matches,
                                          db_obj=db_objs[db_obj])
            all_reports.append(report)

        if print_reports:
            print(all_reports)

        return all_reports
    

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



    def _import_db_module(self, 
                          db_module_name):
        try:
            package = importlib.import_module(name=db_module_name)
            DBModule = getattr(package, db_module_name)
            # DBModule = importlib.import_module(name=db_module_name)
            # globals()['DBModule'] = DBModule
            return DBModule
        except Exception as e:
            print('Error occured while loading db module: ' + str(e))
            return None
        

    def add_data(self, 
                 data_directory):
        # print((self.db_objs))
        for db_obj in list(self.db_objs.values()):
            db_obj.add_data(data_directory)

        # print(db_obj.count())

    def get_collection_data(self):
        frequency = self.db_objs['ip'].get_source_files()
        print(frequency)
        # print(f'Frequency of ip: {frequency}')
        # frequency = self.db_objs['l2'].count()
        # print(f'Frequency of l2: {frequency}')
        # frequency = self.db_objs['cosine'].count()
        # print(f'Frequency of cosine: {frequency}')
        # return metadatas
        

    
def generate_qa():
    qa = dict()
    ASSETS_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "assets")
    QUERY_FILE = os.path.join(ASSETS_DIRECTORY, "queries.json")
    contents = None
    import json
    with open(file=QUERY_FILE, mode='r') as fn:
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

def main():
    embedding_models = ['all-MiniLM-L6-v2',
                        'emilyalsentzer/Bio_ClinicalBERT',
                        'google/bert_uncased_L-12_H-768_A-12',
                        'allenai/scibert_scivocab_uncased']
    all_qa = generate_qa()
    for model in embedding_models[3:]:
        combination = Combination(db_name='Chroma',
                                embedding_model_name=model)
        # combination.get_collection_data()
        data_directory = os.path.join(os.path.abspath(os.pardir), 'data')
        combination.add_data(data_directory)
        all_reports = combination.generate_benchmark(query_srcs_map=all_qa,
                                                matches=1,
                                                print_reports=True)
        BENCHMARK_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'benchmark')
        BENCHMARK_FILE = os.path.join(BENCHMARK_DIRECTORY, 'benchmark.txt')


        # combination.get_collection_data()
        combination.save_reports(all_reports=all_reports,
                                file_path=BENCHMARK_FILE)
        


if __name__ ==  "__main__": main()