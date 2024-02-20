# 可以先用这个脚本把所有的文本做成embedding之后存储起来，这样子就不用每次算余弦相似度的时候都要重新算了
# 直接读过来就行了

import json
import argparse
from typing import Sequence,Union
import os.path as osp

import torch
from transformers import BertTokenizer, BertModel

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",help = "Path to dataset.")

    args = parser.parse_args()

    return args

class tokenizer:
    def __init__(self):

        self.tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        self.model = BertModel.from_pretrained("bert-base-chinese")
    
    def __call__(self,text: Union[Sequence[str],str]):

        if isinstance(text,str):

            return self.tokenize(text)
        
        else:

            represents = []
            for t in text:
                represent = self.tokenize(t)
                represents.append(represent)
            
            return torch.cat(represents)
            

    def tokenize(self,t : str):

        token = self.tokenizer(t,return_tensors='pt',padding=True,truncation=True)
        represents = self.model(**token)
        represents = represents.last_hidden_state.mean(dim=1)    

        return represents   
        

def main():

    args = parse_args()


    with open(args.path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    content = [item['note_content'] for item in data]

    embedding_transformer = tokenizer()
    embeddings = embedding_transformer(content)

    torch.save(embeddings,osp.split(args.path)[0])

if __name__ == "__main__":
    main()