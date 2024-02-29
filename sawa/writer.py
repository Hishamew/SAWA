"""
@Description :   Write
@Author      :   hisham 
@Time        :   2024/02/27 09:00:05
"""
import pandas as pd

from .llm import build_llm_from_config
from .retrieval import build_retrieval
from .prompt import RedBookEditorPrompt,WritePrompt

class Writer:
    def __init__(self,
                 openai_config_path,
                 dataset_path,
                 embeddings_path,
                 user_query):
        self.llm = build_llm_from_config(openai_config_path,sys_prompter=RedBookEditorPrompt("请协助我完成一系列任务从而完成一篇小红书文案。"))
        self.retrieval = build_retrieval(user_query,embeddings_path,self.llm)
        self.dataset_path = dataset_path
        self.user_query = user_query

    def retrieve(self):
        print("Doing semantic retrieval.")
        return self.retrieval.semantic_retrieval()
    
    def write(self):

        f = pd.read_csv(self.dataset_path)
        info = self.retrieve()
        index = info.pop('most_similar_document_index')
        
        for item in f.columns:
            info[item] = f[item][index]

        info['user_query'] = self.user_query

        prompter = WritePrompt()
        prompt = prompter(**info)
        
        print("Writing article.")
        article = self.llm(prompt)

        return article
    
def build_writer(openai_config_path,dataset_path,embeddings_path,user_query):
    return Writer(openai_config_path,
                  dataset_path,
                  embeddings_path,
                  user_query
                  )
        

