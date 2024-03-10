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
                 user_query,
                 openai_config_path = 'config\openai\openai.yaml',
                 dataset_path = 'data/sawa_data_1.csv',
                 embeddings_path = 'data/sawa_data_1.npy',
                 ):
        self.llm = build_llm_from_config(openai_config_path, sys_prompter=RedBookEditorPrompt("请协助我完成一系列任务从而完成一篇小红书文案。"))
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

        most_similar_article = info['content']

        prompter = WritePrompt()
        prompt = prompter(**info)
        
        print("Writing article.")
        article = self.llm(prompt)

        return most_similar_article,article
    
def build_writer(user_query,
                 openai_config_path,
                 dataset_path,
                 embeddings_path):
    return Writer(user_query=user_query,
                  openai_config_path=openai_config_path,
                  dataset_path=dataset_path,
                  embeddings_path=embeddings_path)