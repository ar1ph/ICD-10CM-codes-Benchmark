from langchain.embeddings import HuggingFaceEmbeddings
import json
import os
import importlib


CONFIG_FILE_NAME = 'config.json'
DATA_DIRECTORY = 'data'
DATABASE_DIRECTORY = 'database'




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

# Gets the configuration of a database
# Builds the database based on the configuration
def build_db(config):

    embeddings = get_embeddings_from_model_name(config['EMBEDDINGS_MODEL_NAME']) 
    if (embeddings == None):
        return False
    
    if import_db_module(config['DB_MODULE_NAME']) == False:
        return False

def main():
    
    db_success = []
    db_failed = []

    all_config = get_dict_from_json(CONFIG_FILE_NAME)
    
    # TODO: Roubust checking of config dictionary
    if (all_config == None):
        return None
    
    for db_key in all_config:
        if build_db(all_config[db_key]) == False:
            print("Failed to build the vectorstore: " + db_key)
            db_failed.append(db_key)
        else:
            db_success.append(db_key)

    print("Successful vectorstores:")
    for db in db_success:
        print(db)

    print("Failed vectorstores")
    for db in db_key:
        print(db)
 
    



if __name__ == '__main__':
    main()