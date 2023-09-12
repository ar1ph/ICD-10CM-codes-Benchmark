from langchain import PromptTemplate, LLMChain, HuggingFaceHub
from langchain.llms import OpenAI
from getpass import getpass
import os
from keys_api import HUGGINGFACEHUB_API_TOKEN

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN 

template = """
Generate a query from the context. Should end in a question mark
Context:
{context}
"""

prompt = PromptTemplate.from_template(template)

file = open("../data_temp/A01.2.txt")
context = file.read()
file.close()


models = ["google/flan-t5-xxl", "google/flan-t5-base", "google/flan-t5-large", "google/flan-t5-xl"]
repo_id = models[3]
llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64, "repetition_penalty": 99}, cache=False, verbose=True, task="text2text-generation")

# prompt = PromptTemplate.from_template("Hello. Please tell me a story")
llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

print(llm_chain.run(context=context))






