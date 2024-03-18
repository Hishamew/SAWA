# Update by zyg
# 2024.1.25 Version 2: load toy_dataset and keyword retrieval
# 2024.1.18 version 1: 实现简单的语义搜索，返回相似度最高的文本。需要与数据集格式匹配

# Author: zht
# 2024.2.27 v0.0.2 : Now use openai as embeddings_transformers
import numpy as np
import pandas as pd
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
                 dataset_path,
                 llm,
                 ):
        self.user_query = user_query
        self.embeddings_path = embeddings_path
        self.dataset_path = dataset_path
        self.llm = llm


    def semantic_retrieval(self):

        user_embeddings = self.llm.get_embeddings(self.user_query)
        user_embeddings = np.expand_dims(np.array(user_embeddings),axis=0)
        document_embeddings = self.read_embeddings()
        # 计算用户查询与所有文档之间的余弦相似度
        similarities = cosine_similarity(user_embeddings, document_embeddings)
        # 查找最相似文档的索引
        most_similar_document_index = similarities.argmax()

        for dataset_index,dataset_size in enumerate(self.dataset_len):
            if most_similar_document_index+1 <= dataset_size:
                break
            most_similar_document_index -= dataset_size

        embeddings_key_list = list(self.embeddings_maps[dataset_index].keys())

        outline_matched = embeddings_key_list[most_similar_document_index]

        results = dict(matched_outline = outline_matched,most_similar_document_index = most_similar_document_index,dataset_index = dataset_index)

        results = self.find_all_needed_info(results)
        
        return results
        

    def read_embeddings(self):

        self.embeddings_maps = [np.load(embedding_path,allow_pickle = True).item() for embedding_path in self.embeddings_path]
        self.dataset_len = [len(embeddings_map) for embeddings_map in self.embeddings_maps]

        embeddings = []
        for embeddings_map in self.embeddings_maps:
            for value in embeddings_map.values():
                embeddings.append(np.expand_dims(value,axis=0))
        
        return np.concatenate(embeddings)
    
    def find_all_needed_info(self,semantic_results):

        results = semantic_results
        most_similar_document_index = semantic_results.pop('most_similar_document_index')
        dataset_index = semantic_results.pop('dataset_index')

        f = pd.read_csv(self.dataset_path[dataset_index])

        for item in f.columns:
            results[item] = f[item][most_similar_document_index]
        
        results['user_query'] = self.user_query

        return results


        


 
def build_retrieval(user_query, embeddings_path, dataset_path,llm):
    return Retrieval(user_query=user_query,
                     embeddings_path=embeddings_path,
                     dataset_path=dataset_path,
                     llm=llm)
