import os
import importlib 
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'data')
DATABASE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'database')

# Gets the embeddings and location of the vectorstore
# Retrieves it if possible
def get_vectorstore(embedding, persist_directory):
    try: 
        if (not os.path.exists(persist_directory)): 
            raise Exception("Directory doesn't exist.")

        if not (os.path.exists(os.path.join(persist_directory, 'index'))) :
            raise Exception("Index directory doesn't exist") 
        # db = DBModule(embedding_function=embedding, persist_directory=persist_directory)
        # if (len(db.get()['metadatas']) == 0):
        #     db = None
        #     raise Exception("Metadata is empty")
        return True 
    except Exception as e: 
        print(e)
        return None
    
# Given the path to persist directory
# Returns if the vectorstore exist or not
# Applicable only for persisted vectorstore
def vectorstore_exist(persist_directory):
    if not os.path.exists(persist_directory):
        return False
    elif not os.path.exists(os.path.join(persist_directory, 'index')):
        return False
    return True
    
# Gets a list of paths to .txt files
# Loads all the provided files
def load_documents(file_paths):
    loaded_docs = []
    for path in file_paths:
        loaded_docs.extend(TextLoader(file_path=path, autodetect_encoding=True).load())
    return loaded_docs

# Gets the list of files that need to be ignored
# Returns a splitted chunks of the documents in DATA_DIRECTORY
def process_documents(ignored_files = set(), chunk_size=750, chunk_overlap=100):
    
    file_paths = []
    for root, _, files in os.walk(os.path.join(os.pardir, DATA_DIRECTORY)):
        for fl in files:
            if fl not in ignored_files:
                file_paths.append(os.path.join(root, fl))

    # TODO: Remove the ignored files 
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(load_documents(file_paths=file_paths))

# Gets the db
# Returns all the source file names
def get_source_files(db):
    collection = db.get()
    source_files = set()
    for metadata in collection['metadatas']:
        file_name = metadata['source'].split('\\')[-1]
        if file_name not in source_files:
            source_files.add(file_name)
    return source_files


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
    