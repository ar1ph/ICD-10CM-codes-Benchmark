import os
import csv
import sys

BENCHMARK_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "benchmark")
BENCHMARK_FILE = os.path.join(BENCHMARK_DIRECTORY, "benchmark.csv") 
ASSETS_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "assets")
QUERY_FILE = os.path.join(ASSETS_DIRECTORY, "Queries.txt")

sys.path.append('..')
from lib.process_json import *
from lib.process_data import *

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

# 

def main():
    initialize_benchmark()
    all_codes = get_all_codes()
    # print(all_codes)
    code_map = get_new_subset_of_codes(full_row=True)
    # print(code_map)
    all_disease = retrieve_all_diseases(code_map=code_map)
    print(all_disease)
    report = {'Embedding Model': 'all_mini',
              'DB Type': 'Chroma',
              'Strategy': 'Cosine similarity',
              'Average k': 5,
              'Sigma': 0.1}
    add_report(report=report)


if __name__ == "__main__":
    main()


