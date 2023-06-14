import importlib
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import json

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
        DBModule = getattr(package, db_module_name)
        globals()['DBModule'] = DBModule
        return DBModule
    except Exception as e:
        print('Error occured while loading db module: ' + str(e))
        return None
    

# Gets the path of the src_file (.json) 
# Return the contents in dictionary format
def get_dict_from_json(src_file):
    try:  
        with open(file=src_file, mode='r') as contents: 
            return json.load(contents)
    except Exception as e:
        print('Error occured while reading config file: ' + str(e))
        return None
    
# Gets the path of the dest_file (.json) and dictionary
# Writes the contents of the dictionary in that file
def store_dict_in_json(dest_file, contents):
    try:
        with open(file=dest_file, mode='w') as json_file:
            json.dump(contents, json_file)
            return True
    except Exception as e:
        print('Error occured while reading config file: ' + str(e))
        return False
    