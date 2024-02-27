"""
@Description :   Write
@Author      :   hisham 
@Time        :   2024/02/27 09:00:05
"""
import pandas as pd

from .llm import build_llm_from_config
from .retrieval import build_retrieval
from .prompt import RedBookEditorPrompt

class Writer:
    def __init__(self,
                 openai_config_path,
                 dataset_path,
                 embeddings_path,
                 user_query):
        prompter = RedBookEditorPrompt("请根据提供的信息生成一篇小红书文案。")
        self.llm = build_llm_from_config(openai_config_path,sys_prompt=prompter())
        self.retrieval = build_retrieval(user_query,embeddings_path,openai_config_path)
        self.dataset_path = dataset_path
        self.user_query = user_query

    def retrieve(self):
        return self.retrieval.semantic_retrieval()
    
    def write(self):
        f = pd.read_csv(self.dataset_path)
        matched_outline, index, outline = self.retrieve()
        info = {}
        for item in f.columns:
            info[item] = f[item][index]

        info['matched_outline'] = matched_outline
        info['user_query'] = self.user_query
        info['user_outline'] = outline

        prompter = 
        

