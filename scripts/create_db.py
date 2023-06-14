from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from lib.process_json import get_dict_from_json, store_dict_in_json
from lib.vectorstore import vectorstore_exist, process_documents
import os
import importlib 


CONFIG_FILE_NAME = os.path.join(os.path.abspath(os.pardir), 'config.json')
DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'data')
DATABASE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'database')

    

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

    embedding_model_name = config['EMBEDDINGS_MODEL_NAME']
    db_module_name = config['DB_MODULE_NAME']
    db_dir_name = f"{embedding_model_name}__{db_module_name}"
    database_directory = os.path.join(os.path.abspath(os.pardir), DATABASE_DIRECTORY)
    persist_directory = os.path.join(database_directory, db_dir_name)

    embeddings = get_embeddings_from_model_name(model_name=embedding_model_name)  
    if (embeddings == None):
        return False
    
    if import_db_module(db_module_name=db_module_name) == False:
        return False

    if not vectorstore_exist(persist_directory=persist_directory):
        print("Vectorstore doesn't exist")
        splitted_docs = process_documents(chunk_size=config["CHUNK_SIZE"],
                                          chunk_overlap=config["CHUNK_OVERLAP"])
        db = DBModule.from_documents(splitted_docs, embedding=embeddings,
                                     persist_directory=persist_directory)
        db.persist() # Only for chroma
    else:
        # print("Vectorstor do exist")
        # db = DBModule(embedding_function=embeddings,
        #               persist_directory=persist_directory)
        # collection = db.get()
        # ignored_files = []
        # db.add_documents(process_documents())
        pass
    

def main():
    
    db_success = []
    db_failed = []

    all_config = get_dict_from_json(CONFIG_FILE_NAME)
    
    # TODO: Roubust checking of config dictionary
    if (all_config == None):
        return None
    
    for db_key in all_config:
        try:
            build_db(all_config[db_key])
            db_success.append(db_key)
        except:
            db_failed.append(db_key)

    print("Successful vectorstores:")
    for db in db_success:
        print(db)

    print("Failed vectorstores:")
    for db in db_failed:
        print(db)
 
    



if __name__ == '__main__':
    main()