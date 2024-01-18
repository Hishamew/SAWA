# Update by zyg， 2024.1.18 version 1: 实现简单的语义搜索，返回相似度最高的文本。需要与数据集
# For semantic retrieval, we need download BERT model ckpt for laod weights
# For exenmple:  “bert-base-uncased”/“bert-large-uncased”from huggingface
# 我认为目前这种”语义搜索“的方法比较慢，因为每次都需要把数据分词、编码，而且每次都要load模型
# 如果可以将数据存储成字典形式，例如：{"id":xxx,"key_word":"xxx","note_content":"xxxx","likes":xxx,"comment":xxx,"stars":xxx}
# 就可以进行关键词搜索，然后根据点赞数或收藏数选取热度最高的例子
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel

class Retrieval():
    '''
    Input:
    reading little red book texts dataset or connect to net and crawler

    Output:
    data

    '''
    def __init__(self, user_query, data
                 ) -> None:
        self.user_query = user_query
        self.data = data
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        self.model = BertModel.from_pretrained("bert-base-chinese")

    def semantic_retrieval(self):
        user_query = self.user_query
        user_query_inputs = self.tokenizer(user_query, return_tensors="pt", padding=True, truncation=True)
        user_query_outputs = self.model(**user_query_inputs)
        user_query_embedding = user_query_outputs.last_hidden_state.mean(dim=1)
        document_embeddings = self.data_to_vect()
        # 计算用户查询与所有文档之间的余弦相似度
        similarities = cosine_similarity(user_query_embedding, document_embeddings)
        # 查找最相似文档的索引
        most_similar_document_index = similarities.argmax()
        most_similar_document = self.data[most_similar_document_index]
        print("最相似的文档:", most_similar_document)

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
