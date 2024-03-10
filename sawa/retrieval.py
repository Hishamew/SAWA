# Update by zyg
# 2024.1.25 Version 2: load toy_dataset and keyword retrieval
# 2024.1.18 version 1: 实现简单的语义搜索，返回相似度最高的文本。需要与数据集格式匹配

# Author: zht
# 2024.2.27 v0.0.2 : Now use openai as embeddings_transformers
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
    def __init__(self, 
                 user_query, 
                 embeddings_path,
                 llm,
                 ):
        self.user_query = user_query
        self.embeddings = np.load(embeddings_path,allow_pickle = True).item()
        self.llm = llm


    def semantic_retrieval(self):

        user_embeddings = self.llm.get_embeddings(self.user_query)
        user_embeddings = np.expand_dims(np.array(user_embeddings),axis=0)
        document_embeddings = self.read_embeddings()
        # 计算用户查询与所有文档之间的余弦相似度
        similarities = cosine_similarity(user_embeddings, document_embeddings)
        # 查找最相似文档的索引
        most_similar_document_index = similarities.argmax()

        embeddings_map_list = list(self.embeddings.items())

        outline_matched = embeddings_map_list[most_similar_document_index][0]

        results = dict(matched_outline = outline_matched,most_similar_document_index = most_similar_document_index)
        
        return results
        

    def read_embeddings(self):
        embeddings_map = self.embeddings
        embeddings = []
        for value in embeddings_map.values():
            embeddings.append(np.expand_dims(value,axis=0))
        
        return np.concatenate(embeddings)
 
def build_retrieval(user_query, embeddings_path, llm):
    return Retrieval(user_query=user_query,
                     embeddings_path=embeddings_path,
                     llm=llm)
