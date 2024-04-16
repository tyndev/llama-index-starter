from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from dotenv import load_dotenv
import logging
import sys
import os
import os.path
import time

logging.basicConfig(stream=sys.stdout, level=logging.INFO) #DEBUG for verbose, otherwise INFO
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# check if storage folder already exist
PERSIST_DIR = "./storage"

start_time = time.time() # Start Timing

if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    logging.info("New index created and persisted.")
else:
    logging.info("Loading existing storage.")
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    logging.info("Existing index loaded.")
    
load_end_time = time.time() # End Timing
logging.info("Index load took %s seconds", load_end_time - start_time)

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)

end_time = time.time() # End Timing
logging.info("Total response time took %s seconds", end_time - start_time)