import gradio as gr
import yaml
import pandas as pd
from sawa import Retrieval, WritePrompt, RedBookEditorPrompt, build_llm_from_config

title = "小红书文案生成器"
description = "请输入您想生成小红书文案的话题"
examples = [
    ["法国留学攻略，详细介绍需要注意的事项"],
    ["心理咨询师和心理医生的区别"]
    ]
article = "感兴趣的小伙伴可以阅读github项目"

config_path = 'config\sawa.yaml'
with open(config_path,'r') as file:
    cfg = yaml.safe_load(file)

def xhs_writer(user_query):
    data = pd.read_csv(cfg['dataset_path'])
    llm = build_llm_from_config(cfg['openai_config_path'], 
                                sys_prompter=RedBookEditorPrompt(""))
    retriever = Retrieval(user_query, cfg['embeddings_path'], llm)
    info = retriever.semantic_retrieval()
    index = info.pop('most_similar_document_index')
    
    for item in data.columns:
        info[item] = data[item][index]

    info['user_query'] = user_query

    prompter = WritePrompt()
    prompt = prompter(**info)
    
    article = llm(prompt)

    return prompt, article

interface = gr.Interface(
    fn = xhs_writer, 
    inputs = gr.Textbox(label="请输入或使用下面的examples"), 
    outputs=[gr.Textbox(label="prompt"),
            gr.Textbox(label="结果")], 
    title=title, description=description, examples=examples, article=article)

interface.launch()