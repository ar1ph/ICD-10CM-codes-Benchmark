import os
import csv

BENCHMARK_FILE = 'benchmark.csv'


def add_report(report):
    benchmark_directory = os.path.join(os.path.abspath(os.pardir), "benchmark")
    file_path = os.path.join(benchmark_directory, BENCHMARK_FILE) 
    row = [report['Embedding Model'],
           report['DB Type'],
           report['Strategy'],
           report['Average k'],
           report['Sigma']]
    with open(file=file_path, mode='a') as fn:
        csv_writter = csv.writer(fn, delimiter=' ', lineterminator='\n')
        csv_writter.writerow(row)

def initialize_benchmark():
    benchmark_directory = os.path.join(os.path.abspath(os.pardir), "benchmark")
    file_path = os.path.join(benchmark_directory, BENCHMARK_FILE) 
    row = ['Embedding Model',
           'DB Type',
           'Strategy',
           'Average k',
           'Sigma']
    with open(file=file_path, mode='w') as fn:
        csv_writter = csv.writer(fn, delimiter=' ', lineterminator='\n')
        csv_writter.writerow(row)

def main():
    initialize_benchmark()
    report = {'Embedding Model': 'all_mini',
              'DB Type': 'Chroma',
              'Strategy': 'Cosine similarity',
              'Average k': 5,
              'Sigma': 0.1}
    add_report(report=report)


if __name__ == "__main__":
    main()


