import requests
from keys_api import HUGGINGFACEHUB_API_TOKEN

def query(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

model_id = "google/flan-t5-xxl"
api_token = HUGGINGFACEHUB_API_TOKEN # get yours at hf.co/settings/tokens
data = query("""Given the following context. Generate 4 queries that could be asked to an LLM.
	     Return only the queries and nothing else,  queries should  end with a question mark. 


Context:


2023 ICD-10-CM Diagnosis Code A01.2
 
Paratyphoid fever B

Approximate Synonyms

 Paratyphoid b fever 

ICD-10-CM  A01.2  is grouped within Diagnostic Related Group(s) (MS-DRG  v 40.0):

 867  Other infectious and parasitic diseases diagnoses with mcc 
 868  Other infectious and parasitic diseases diagnoses with cc 
 869  Other infectious and parasitic diseases diagnoses without cc/mcc""", model_id, api_token)

print(data)