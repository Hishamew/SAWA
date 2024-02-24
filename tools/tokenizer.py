# 可以先用这个脚本把所有的文本做成embedding之后存储起来，这样子就不用每次算余弦相似度的时候都要重新算了
# 直接读过来就行了

#v0.2 修改了读取模型和句子编码部分的代码，现在可以运行了。

import tqdm
import argparse
from typing import Sequence,Union
import os.path as osp

import pandas as pd
import torch
from transformers import BertTokenizer, BertModel

def read_raw_data(path : str):

    f = pd.read_csv(path)
    contents = list(f['contents'])

    return contents


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",type=str,help = "Path to dataset.")

    args = parser.parse_args()

    return args

class tokenizer:
    def __init__(self):

        self.tokenizer = BertTokenizer.from_pretrained("google-bert/bert-base-chinese")
        self.model = BertModel.from_pretrained("google-bert/bert-base-chinese")
        self.device = "cuda:0" if torch.cuda.is_available() else 'cpu'
        self.tokenizer = self.tokenizer.to(self.device)
        self.model = self.model.to(self.device)
    
    def __call__(self,text: Union[Sequence[str],str]):
        '''
        
        text: take str or list of str and return there

        '''
        
        

        if isinstance(text,str):

            return self.tokenize(text)
        
        else:

            represents = []
            for t in tqdm.tqdm(text):
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


    # with open(args.path, 'r', encoding="utf-8") as file:
    #     data = json.load(file)
    # content = [item['note_content'] for item in data]

    content = read_raw_data(args.path)

    embedding_transformer = tokenizer()
    embeddings = embedding_transformer(content)

    root, file_name= osp.split(args.path)

    torch.save(embeddings,osp.join(root,file_name[:-3]+'pth'))

if __name__ == "__main__":
    main()