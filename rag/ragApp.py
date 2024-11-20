import os
from dotenv import load_dotenv
# initializing the load_dotenv 
load_dotenv(dotenv_path='/home/smarika/Varicon/others/rag/.env')

print("Here!!!")
# Now check the API key
api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     print("API key is missing!")
# else:
#     print(f"API Key Loaded: {api_key}")


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

# convert pdf into documents. this documents create a metadata of the pdf files
documents= SimpleDirectoryReader("data").load_data()
# print(documents)

# converting the documents into index using the vectorstoreindex
# converting the pdf contents into vectors and then store it into index
index= VectorStoreIndex.from_documents(documents, show_progress=True)
print(index)


# creating a query engine --> here it is responsible for retrieving informtion 
query_engine= index.as_query_engine()
query2= 'Give me the table name that has the total number of labours'
response= query_engine.query(query2)
print(response)


print("MULTIPLE RESPONSES BASED ON THE HIGEST SIMILARITY")
# we can also print similar responses 
from llama_index.core.response.pprint_utils import pprint_response
# this not only gives the exact responses, but also the responses that have high similarity index 
pprint_response(response, show_source=True)
print(response)




