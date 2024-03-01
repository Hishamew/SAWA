import gradio as gr
import yaml
import pandas as pd
from sawa import Retrieval, WritePrompt, RedBookEditorPrompt, build_llm_from_config

#标题
title = "小红书文案生成器"
#题下的描述，支持md格式
description = "请输入您想生成小红书文案的话题"
#输入样例
examples = [
    ["法国留学攻略，详细介绍需要注意的事项"],
    ["心理咨询师和心理医生的区别"]
    ]
#页面最后的信息，可以选择引用文章，支持md格式
article = "感兴趣的小伙伴可以阅读github项目"

config_path = 'config\sawa.yaml'
with open(config_path,'r') as file:
    cfg = yaml.safe_load(file)

def xhs_writer(user_query):
    data = pd.read_csv(cfg['dataset_path'])
    llm = build_llm_from_config(cfg['openai_config_path'], sys_prompter=RedBookEditorPrompt("请协助我完成一系列任务从而完成一篇小红书文案。"))
    retrieve = Retrieval(user_query, cfg['embeddings_path'], llm)
    info = retrieve.semantic_retrieval()
    index = info.pop('most_similar_document_index')
    
    for item in data.columns:
        info[item] = data[item][index]

    info['user_query'] = user_query

    prompter = WritePrompt()
    prompt = prompter(**info)
    
    article = llm(prompt)

    return article

interface = gr.Interface(fn=xhs_writer, 
             inputs=gr.Textbox(label="请输入或使用下面的examples："), 
             outputs=gr.Textbox(label="结果"), 
             title=title, description=description, examples=examples, article=article)

interface.launch()