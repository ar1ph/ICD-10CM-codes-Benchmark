import os
import csv
import sys
sys.path.append("..")
import statistics
from lib.util import *


BENCHMARK_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "benchmark")
BENCHMARK_FILE = os.path.join(BENCHMARK_DIRECTORY, "benchmark.csv")  
ASSETS_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "assets")
QUERY_FILE = os.path.join(ASSETS_DIRECTORY, "queries.json")
CONFIG_FILE_NAME = os.path.join(ASSETS_DIRECTORY, 'config.json')

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
           str(report['Average k']),
           str(report['Sigma'])]
    with open(file=file_path, mode='a') as fn:
        fn.write("\n")
        fn.write(", ".join(row))

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
    if len(db.get()["metadatas"]) == 0:
        return False
    return db

# TODO: Function that takes db and query returns k value
# def get_k(query, db)

# Based on DATA_DIRECTORY generates a dictionary of following format
# qa = {file_name: [med_code, med_desc]}
def generate_qa():
    qa = dict()
    contents = get_contents_from_json(src_file=QUERY_FILE)
    for qa_collection in contents:
        query = qa_collection['query']
        var_dict = qa_collection['variables']
        variables = list(var_dict.keys())
        answers = qa_collection['answers']
        num_of_instances = len(var_dict[variables[0]])
        for idx in range(num_of_instances):
            instance = dict()
            for var in variables:
                instance[var] = var_dict[var][idx]
            question = query.format(**instance)
            qa[question] = answers[idx]
    return qa


# Returns the list of query formats
def generate_query_types(): 
    try:
        with open(file=QUERY_FILE,mode='r') as q:
            query_types = q.read().strip().split('\n') 
        return query_types
    except Exception as e:
        print('Error occured while retrieving the queries: ' + str(e))
        return None


# gets query, database, strategy
# Returns k
def get_k(query, db, ans, strg="Cosine similarity"):
    max_k = len(db.get()['metadatas'])

    # Needs to consider the startegy
    search_res = db.similarity_search(query, k=max_k)
    for idx, doc in enumerate(search_res):
        source = doc.metadata['source']
        if ans in source: return idx + 1
    return -1


# Gets database configuration, qa dictionary, strategy
# Return a report dictionary
def generate_report(db_config, all_qa, strg='Cosine similarity'):
    db = get_db(db_config)
    if not db: return None
    all_k = []
    for ques in all_qa:
        ans = all_qa[ques] 
        k = get_k(query=ques, db=db, ans=ans)
        if k == -1 : return None
        all_k.append(k)

    avg = round(sum(all_k) / len(all_k))
    sigma = round(statistics.stdev(all_k), 2)
    report = {'Embedding Model': db_config["EMBEDDINGS_MODEL_NAME"],
              'DB Type': db_config["DB_MODULE_NAME"],
              'Strategy': strg,
              'Average k': avg,
              'Sigma': sigma}
    return report


def main():
    initialize_benchmark()
    # print(all_disease)
    # TODO: generate_queries function
    # all_queries = generate_queries(all_codes, all_disease)
    all_db_configs = get_dict_from_json(src_file=CONFIG_FILE_NAME)
    all_qa = generate_qa()
    report = dict()
    # add_report(report=report)
    failed_configs = []
    for db_key in all_db_configs:
        db_config = all_db_configs[db_key]
        report = generate_report(db_config=db_config, all_qa=all_qa)
        print(report)
    add_report(report=report)


if __name__ == "__main__":
    main()


