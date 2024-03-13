import gradio as gr
import yaml
import pandas as pd
from sawa import build_writer


class Interface:
    CONFIGPATH = 'config\sawa.yaml'

    def __init__(self,
                 title='',
                 description='',
                 examples=[],
                 article=''):
        self.title = "小红书文案生成器"
        self.description = "请输入您想生成小红书文案的话题"
        self.examples = [
            ["法国留学攻略，详细介绍需要注意的事项"],
            ["心理咨询师和心理医生的区别"]
            ]
        self.article = "感兴趣的小伙伴可以阅读github项目"

    def launch(self):
        with open(self.CONFIGPATH,'r') as file:
            cfg = yaml.safe_load(file)

        def xhs_writer(user_query):
            writer = build_writer(user_query=user_query,**cfg,mode = 'gradio')
            prompt, article = writer.write()

            return prompt,article

        interface = gr.Interface(
            fn = xhs_writer, 
            inputs = gr.Textbox(label="请输入或使用下面的examples"), 
            outputs=[gr.Textbox(label="prompt"),
                    gr.Textbox(label="结果")], 
            title=self.title, description=self.description, examples=self.examples, article=self.article)

        interface.launch()

if __name__ == "__main__":
    title = "小红书文案生成器"
    description = "请输入您想生成小红书文案的话题"
    examples = [
            ["法国留学攻略，详细介绍需要注意的事项"],
            ["心理咨询师和心理医生的区别"],
            ]
    article = "感兴趣的小伙伴可以阅读github项目"
    interface = Interface(title,
                          description,
                          examples,
                          article,)
    interface.launch()