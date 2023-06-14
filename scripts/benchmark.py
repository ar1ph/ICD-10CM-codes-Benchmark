import os
import csv
import sys

BENCHMARK_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "benchmark")
BENCHMARK_FILE = os.path.join(BENCHMARK_DIRECTORY, "benchmark.csv")  
DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'data')
DATABASE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'database')
ASSETS_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "assets")
QUERY_FILE = os.path.join(ASSETS_DIRECTORY, "Queries.txt")
CONFIG_FILE = os.path.join(os.path.abspath(os.pardir), 'config.json')

sys.path.append('..')
from lib.process_json import *
from lib.process_codes import *
from lib.process_data import *
from lib.vectorstore import *

# Gets a report dictionary and file path to a csv file
# Inserts a row containing the report
def add_report(report, file_path=BENCHMARK_FILE):
    row = [report['Embedding Model'],
           report['DB Type'],
           report['Strategy'],
           report['Average k'],
           report['Sigma']]
    with open(file=BENCHMARK_FILE, mode='a') as fn:
        csv_writter = csv.writer(fn, delimiter=' ', lineterminator='\n')
        csv_writter.writerow(row)

#   Initializes the benchmark file if not available
def initialize_benchmark(file_path=BENCHMARK_FILE):
    if os.path.exists(file_path):
        return
    row = ['Embedding Model',
           'DB Type',
           'Strategy',
           'Average k',
           'Sigma']
    with open(file=file_path, mode='w') as fn:
        csv_writter = csv.writer(fn, delimiter=',', lineterminator='\n')
        csv_writter.writerow(row)

# Given configuration of a database 
# Returns a report dictionary
def get_db(config):
    embedding_model_name = config['EMBEDDINGS_MODEL_NAME']
    db_module_name = config['DB_MODULE_NAME']
    db_dir_name = f"{embedding_model_name}__{db_module_name}"
    database_directory = os.path.join(os.path.abspath(os.pardir), DATABASE_DIRECTORY)
    persist_directory = os.path.join(database_directory, db_dir_name)
    embeddings = get_embeddings_from_model_name(model_name=embedding_model_name)  
    if (embeddings == None):
        return False
    
    DBModule = import_db_module(db_module_name=db_module_name)
    if DBModule == None:
        return False
    
    db = DBModule(embedding_function=embeddings, persist_directory=persist_directory)
    if len(db.get()["metadatas"] == 0):
        return False
    
    return db

def generate_qa():
    file_names = get_all_file_names(with_format=True) 
    if file_names == None:
        return None
    code_map = get_new_subset_of_codes(full_row=True)
    if code_map == None:
        return None
    if len(code_map) != len(file_names):
        print("Number of codes and files are not same")
        return None
    qa = dict()
    for idx, code in enumerate(code_map):
        row = code_map[code]
        med_condition = get_medical_condition_from_row(row=row)
        qa[file_names[idx]] = med_condition
    return qa



# def generate_queries(all_codes, all_diseases):
#     all_queries = []
#     try:
#         with open(file=QUERY_FILE,mode='r') as q:
#             query_types = q.read().strip().split('\n')
#         # TODO: create actual queries using format
#         queries_type__1 = []
#         for code in all_codes:
#             query = query_types[0].format(code=code)
#             queries_type__1.append(query)
#         for disease
#         return all_queries
#     except Exception as e:
#         print('Error occured while retrieving the queries: ' + str(e))



def main():
    initialize_benchmark()
    all_codes = get_all_codes()
    # print(all_codes)
    code_map = get_new_subset_of_codes(full_row=True)
    # print(code_map)
    all_disease = retrieve_all_diseases(code_map=code_map)
    # print(all_disease)
    # TODO: generate_queries function
    # all_queries = generate_queries(all_codes, all_disease)
    all_db_configs = get_dict_from_json(src_file=CONFIG_FILE)
    # print(all_db)
    # report = {'Embedding Model': 'all_mini',
    #           'DB Type': 'Chroma',
    #           'Strategy': 'Cosine similarity',
    #           'Average k': 5,
    #           'Sigma': 0.1}
    report = dict()
    # add_report(report=report)
    failed_configs = []
    for db_config in all_db_configs:
        db = get_db(db_config)
        if db == None:
            failed_configs.append(db_config)
            # TODO: generate_report function
        # report = generate_report(all_queries)
        if report == None:
            failed_configs.append(db_config)

    


if __name__ == "__main__":
    main()


