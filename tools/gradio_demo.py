import gradio as gr
import yaml
from sawa import build_writer

SYSCONFIG = 'config\sawa.yaml'

def interface():
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

    config_path = SYSCONFIG
    with open(config_path,'r') as file:
        cfg = yaml.safe_load(file)

    def xhs_writer(user_query):

        writer = build_writer(user_query=user_query,**cfg)
        article = writer.write()

        return article

    interface = gr.Interface(fn=xhs_writer, 
                inputs=gr.Textbox(label="请输入文章要求："), 
                outputs=gr.Textbox(label="结果"), 
                title=title, description=description, examples=examples, article=article)

    interface.launch()

if __name__ == "__main__":
    interface()