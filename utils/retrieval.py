# Update by zyg
# 2024.1.25 Version 2: load toy_dataset and keyword retrieval
# 2024.1.18 version 1: 实现简单的语义搜索，返回相似度最高的文本。需要与数据集格式匹配
# For semantic retrieval, we need download BERT models: “bert-base-uncased”/“bert-large-uncased” from huggingface
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel

class Retrieval():
    '''
    Input:
    reading little red book texts dataset or connect to net and crawler

    Output:
    data

    '''
    def __init__(self, user_query, data_path
                 ):
        self.user_query = user_query
        self.data_path = data_path

    def semantic_retrieval(self):
        tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        model = BertModel.from_pretrained("bert-base-chinese")
        user_query = self.user_query
        user_query_inputs = tokenizer(user_query, return_tensors="pt", padding=True, truncation=True)
        user_query_outputs = model(**user_query_inputs)
        user_query_embedding = user_query_outputs.last_hidden_state.mean(dim=1)
        document_embeddings = self.data_to_vect()
        # 计算用户查询与所有文档之间的余弦相似度
        similarities = cosine_similarity(user_query_embedding, document_embeddings)
        # 查找最相似文档的索引
        most_similar_document_index = similarities.argmax()
        most_similar_document = self.data[most_similar_document_index]
        print("最相似的文档:", most_similar_document)

    def keyword_retrieval(self):
        '''
        Input: 
        user_query: 中文关键词字符串
        data_path: 本地数据集路径
        Output:
        note_content
        '''
        max_likes_content = None
        max_likes = 0

        with open(self.data_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            for thing in data:
                if thing['note_keyword'] == self.user_query:
                    likes = int(thing['likes'])
                    if likes > max_likes:
                        max_likes = likes
                        max_likes_content = thing['note_content']
            if max_likes == 0:
                print('I cannot find contents about this word')
                return None

        return max_likes_content


    def data_to_vect(self):
        # Tokenize and encode the originel data documents
        data = self.data
        document_embeddings = []
        for document in data:
            inputs = self.tokenizer(document, return_tensors="pt", padding=True, truncation=True)
            outputs = self.model(**inputs)
            document_embedding = outputs.last_hidden_state.mean(dim=1)  # Average over tokens
            document_embeddings.append(document_embedding)

        return torch.cat(document_embeddings)


def test_retireval():
    key_word = "留学"
    data_path = "data/toy_dataset.json"
    retrieval = Retrieval(key_word, data_path)
    content = retrieval.keyword_retrieval()
    print(content)

if  __name__ == "__main__":
    test_retireval()
