from llama_index.core import GPTVectorStoreIndex, StorageContext, PromptHelper, load_index_from_storage
from llama_index.core import SimpleDirectoryReader
from llama_index.legacy.llm_predictor.base import LLMPredictor
from langchain_community.llms import OpenAI
import sys
import os

openai_api_key = os.environ["OPENAI_API_KEY"]
openai_api_url = os.environ["OPENAI_API_BASE"]

#Generate json from gpt3.5
def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600
    
    prompt_helper = PromptHelper(max_input_size, num_outputs, chunk_overlap_ratio=0.1, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTVectorStoreIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index.storage_context.persist(persist_dir='index')
    print('generate over')
    return index

#chatbot function
def chatbot(input_text):
    storage_context = StorageContext.from_defaults(persist_dir="index")
    index = load_index_from_storage(storage_context)
    #index = GPTVectorStoreIndex.load_from_disk('index.json')
    response = index.as_query_engine(response_mode="compact").query(input_text)
    return response.response

index = construct_index("docs")

#msg=input('请输入：')
#print(chatbot(msg))