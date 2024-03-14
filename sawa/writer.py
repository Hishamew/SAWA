"""
@Description :   Write
@Author      :   hisham 
@Time        :   2024/02/27 09:00:05
"""
import pandas as pd

from .llm import build_llm_from_config
from .retrieval import build_retrieval
from .prompt import RedBookEditorPrompt,WritePrompt
from .utils import print_log,get_root_logger

import time

class Writer:
    def __init__(self,
                 user_query,
                 openai_config_path = 'config\openai\openai.yaml',
                 dataset_path = 'data/sawa_data_1.csv',
                 embeddings_path = 'data/sawa_data_1.npy',
                 mode = None
                 ):
        self.llm = build_llm_from_config(openai_config_path, sys_prompter=RedBookEditorPrompt("请协助我完成一系列任务从而完成一篇小红书文案。"))
        self.retrieval = build_retrieval(user_query,embeddings_path,dataset_path,self.llm)
        self.dataset_path = dataset_path
        self.user_query = user_query
        self.mode = mode
        self.logger = get_root_logger()

    def retrieve(self):
        print_log("Doing semantic retrieval.",logger=self.logger,mode = self.mode)
        return self.retrieval.semantic_retrieval()
    
    def write(self):

        t0 = time.time()

        info = self.retrieve()

        t1 = time.time()
        print_log(t1-t0,logger=self.logger,)
        
        prompter = WritePrompt()
        prompt = prompter(**info)
        
        print_log("Writing article.",logger=self.logger,mode = self.mode)
        article = self.llm(prompt)

        t2 = time.time()
        print_log(t2-t1,logger=self.logger,)

        print_log("total : {}".format(t2-t0),logger=self.logger)

        return prompt,article
    
def build_writer(user_query,
                 openai_config_path,
                 dataset_path,
                 embeddings_path,
                 mode=None,):
    return Writer(user_query=user_query,
                  openai_config_path=openai_config_path,
                  dataset_path=dataset_path,
                  embeddings_path=embeddings_path,
                  mode=mode)