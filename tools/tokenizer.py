# 可以先用这个脚本把所有的文本做成embedding之后存储起来，这样子就不用每次算余弦相似度的时候都要重新算了
# 直接读过来就行了

#v0.2 修改了读取模型和句子编码部分的代码，现在可以运行了。

import tqdm
import argparse
import yaml
import os.path as osp
from typing import Sequence,Union
from collections import OrderedDict

import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel

from sawa.prompt import OutlinePrompt,RedBookEditorPrompt
from sawa import build_llm_from_config

def read_raw_data(path : str):

    f = pd.read_csv(path)
    contents = list(f['contents'])
    keywords = list(f['keyword'])
    titles = list(f['title'])

    return contents,keywords,titles


class tokenizer:
    def __init__(self,config):

        sys_prompt = RedBookEditorPrompt("现在你需要整理一些别人网红笔记的资料，请根据以下有关网红笔记的信息生成它们的大纲。")
        self.llm = build_llm_from_config(config = config, 
                                         sys_prompt= sys_prompt())
    
    def __call__(self,text: Union[Sequence[str],str],keyword : Union[Sequence[str],str],title : Union[Sequence[str],str]):
        '''
        Tokenize text.
        Args:
            text: take str or list of str and return their embeddings
            keyword (str or list[str]): their keyword.
            title (str or list[str]): their title.
        
        Returns:
            numpy.array : their embeddings.
        '''

        print('Generating outlines.')
        outlines = self.get_outline(text,keyword,title)
        self.outlines = outlines

        print('Generating embeddings.')
        if isinstance(outlines,str):

            return self.tokenize(outlines)
        
        else:

            represents = []
            for t in tqdm.tqdm(outlines):
                represent = self.tokenize(t)
                represents.append(represent)
            
            return np.concatenate(represents)
            
    def get_outline(self,text,keyword,title):
        Prompter = OutlinePrompt()
        if isinstance(text,str):
            prompt = Prompter(text,title,keyword)
            return self.llm(prompt,use_history=False)
        else:
            outlines=[]
            for t,k,l in tqdm.tqdm(list(zip(text,keyword,title))):
                prompt = Prompter(t,l,k)
                outlines.append(self.llm(prompt,use_history=False))
            return outlines

    def export_outlines(self):
        return self.outlines



    def tokenize(self,t : str):

        embeddings = self.llm.get_embeddings(t)
        embeddings = np.array(embeddings).expand_dims(0)
        return embeddings
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",type=str,help = "Path to dataset.")

    args = parser.parse_args()

    return args     

def main():

    args = parse_args()


    # with open(args.path, 'r', encoding="utf-8") as file:
    #     data = json.load(file)
    # content = [item['note_content'] for item in data]

    content,keyword,title = read_raw_data(args.path)

    embedding_transformer = tokenizer('config/openai/openai.yaml')
    embeddings = embedding_transformer(content,keyword,title)
    outlines = embedding_transformer.export_outlines()

    root, file_name= osp.split(args.path)

    outline_embeddings_map = OrderedDict()
    for key,value in zip(outlines,embeddings):
        outline_embeddings_map[key] = value

    np.save(osp.join(root,file_name[:-3]+'npy'),outline_embeddings_map)

    

if __name__ == "__main__":
    main()