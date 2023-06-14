from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os, sys
sys.path.append('..')
from lib.process_data import *
from lib.process_codes import *
from lib.process_json import *
from lib.vectorstore import *

CONFIG_FILE_NAME = os.path.join(os.path.abspath(os.pardir), 'config.json')
DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'data')
DATABASE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'database')

    

    

# Gets the configuration of a database
# Builds the database based on the configuration
# Returns True if successful
def build_db(config):

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

    if not vectorstore_exist(persist_directory=persist_directory):
        print("Vectorstore doesn't exist")
        splitted_docs = process_documents(chunk_size=config["CHUNK_SIZE"],
                                          chunk_overlap=config["CHUNK_OVERLAP"])
        db = DBModule.from_documents(splitted_docs, embedding=embeddings,
                                     persist_directory=persist_directory)
    else:

        print("Vectorstore does exist")
        db = DBModule(embedding_function=embeddings, persist_directory=persist_directory)
        ignored_files = get_source_files(db=db)
        splitted_docs = process_documents(ignored_files=ignored_files,
                                          chunk_size=config["CHUNK_SIZE"],
                                          chunk_overlap=config["CHUNK_OVERLAP"])
        if len(splitted_docs) > 0:
            db.add_documents(splitted_docs)
    db.persist() # Only for chroma
    return True

    

def main():
    
    db_success = []
    db_failed = []

    all_config = get_dict_from_json(CONFIG_FILE_NAME)
    
    # TODO: Roubust checking of config dictionary
    if (all_config == None):
        return None
    
    for db_key in all_config:
        if build_db(all_config[db_key]):
            db_success.append(db_key)
        else:
            db_failed.append(db_key)

    print("Successful vectorstores:")
    for db in db_success:
        print(db)

    print("Failed vectorstores:")
    for db in db_failed:
        print(db)
 
    



if __name__ == '__main__':
    main()