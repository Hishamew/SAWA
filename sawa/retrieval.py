# Update by zyg
# 2024.1.25 Version 2: load toy_dataset and keyword retrieval
# 2024.1.18 version 1: 实现简单的语义搜索，返回相似度最高的文本。需要与数据集格式匹配

# Author: zht
# 2024.2.27 v0.0.2 
# For semantic retrieval, we need download BERT models: “bert-base-uncased”/“bert-large-uncased” from huggingface
import torch
from sklearn.metrics.pairwise import cosine_similarity

from .llm import build_llm_from_config
from prompt import RedBookEditorPrompt,WriteOutlinePrompt

def argmax(list,key = None):
    max_value = max(list,key = key)
    return [index for index,_ in enumerate(list) if list[index] == max_value]
    

class Retrieval():
    '''
    Input:
    reading little red book texts dataset or connect to net and crawler

    Output:
    data

    '''
    def __init__(self, user_query, embeddings_path,config
                 ):
        self.user_query = user_query
        self.embeddings = torch.load(embeddings_path)
        self.llm = build_llm_from_config(config,sys_prompt=RedBookEditorPrompt("现在需要你帮忙根据要求撰写一篇小红书的大纲。"))


    def semantic_retrieval(self):

        outline = self.write_outlines()

        user_embeddings = self.llm.get_embeddings(outline)
        user_embeddings = torch.tensor(user_embeddings).unsqueeze(0)
        document_embeddings = self.read_embeddings()
        # 计算用户查询与所有文档之间的余弦相似度
        similarities = cosine_similarity(user_embeddings, document_embeddings)
        # 查找最相似文档的索引
        most_similar_document_index = similarities.argmax()

        embeddings_map_list = list(self.embeddings.items())

        outline_matched = embeddings_map_list[most_similar_document_index][0]
        
        return outline_matched,most_similar_document_index,outline

    def write_outlines(self):
        
        prompter = WriteOutlinePrompt()
        outline = self.llm(prompter(self.user_query))

        return outline
        

    def read_embeddings(self):
        embeddings_map = self.embeddings
        embeddings = []
        for value in embeddings_map.values():
            embeddings.append(value)
        
        return torch.cat(embeddings)
 
def build_retrieval(user_query, embeddings_path,config):
    return Retrieval(user_query, embeddings_path,config)

# def test_retireval():
#     key_word = "留学"
#     data_path = "data/toy_dataset.json"
#     retrieval = Retrieval(key_word, data_path)
#     content = retrieval.keyword_retrieval()
#     print(content)

# if  __name__ == "__main__":
#     test_retireval()
