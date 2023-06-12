from langchain.embeddings import HuggingFaceEmbeddings
import json
import os
import importlib


CONFIG_FILE_NAME = 'config.json' 


# Gets the name of the json file 
# Return the contents in dictionary format
def get_dict_from_json(config_file):
    try: 
        file_name = os.path.join(os.path.abspath(os.pardir), config_file)
        print(file_name)
        with open(file=file_name, mode='r') as contents: 
            return json.load(contents)
    except Exception as e:
        print('Error occured while reading config file: ' + str(e))
        return None
    

# Gets the name of the embedding model 
# Returns the embedding function
def get_embeddings_from_model_name(model_name):
    try:
        return HuggingFaceEmbeddings(model_name=model_name)
    except Exception as e:
        print('Error occured while loading embedding model: ' + str(e))
        return None
    

# Gets the name of the module (Available in langchain.vectorstores)
# Imports the module Globally
def import_db_module(db_module_name):
    try:
        package = importlib.import_module(name='langchain.vectorstores')
        globals()['DBModule'] = getattr(package, db_module_name)
        return True
    except Exception as e:
        print('Error occured while loading db module: ' + str(e))
        return False

def main():
    
    config = get_dict_from_json(CONFIG_FILE_NAME)
    
    # TODO: Roubust checking of config dictionary
    if (config == None):
        return None
    
    embeddings = get_embeddings_from_model_name(config['EMBEDDINGS_MODEL_NAME'])

    if (embeddings == None):
        return None
    
    if import_db_module(config['DB_MODULE_NAME']) == False:
        return None
    
    # TODO: create_db()
    



if __name__ == '__main__':
    main()