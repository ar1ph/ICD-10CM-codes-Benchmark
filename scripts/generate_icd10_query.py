import os, json, sys

sys.path.append("..")
from lib.process_codes import *
from lib.process_data import *

ASSETS_DIRECTORY = os.path.join(os.path.abspath(os.pardir),  'assets')
QUERY_FILE_NAME = os.path.join(ASSETS_DIRECTORY, 'queries.json')
DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'data')


def main():
    # Getting code map from data directory
    code_map = get_new_subset_of_codes(full_row=True)
    file_names = get_all_file_names(with_format=True)
    code = get_all_codes()
    condition = [get_medical_desc_from_row(row) for row in list(code_map.values())]
    # print(code_map)
    disease = retrieve_all_diseases(code_map=code_map)
    contents = [
        {
            "query": "Describe the ICD-10 CM code {code}",
            "variables": {
                "code": code
            },
            "answers": file_names
        },
        {
            "query": "What are the ICD-10 CM code that describe the codition {condition}",
            "variables": {
                "condition": condition
            },
            "answers": file_names
        },
        # {
        #     "query": "What are the ICD-10 CM code that describe the disease {disease}",
        #     "variables": {
        #         "disease": disease
        #     },
        #     "answers": file_names
        # }
    ]
    with open(file=QUERY_FILE_NAME, mode='w') as fn:
        fn.write(json.dumps(contents))

    return

if __name__ == "__main__":
    main()



