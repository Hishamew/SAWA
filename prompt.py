from retrieval import Retrieval
import os


# 写成封装好可以调用的函数或类，输入是关键词，输出是prompt

class Prompt():
    def __init__(self) -> None:
        pass

# 创建一个空列表来存储单词  
keywords = []  
  
# 读取用户输入的关键词  
input_string = input("请依次输入你需求文章的主题，目标人群，期望内容，风格，大致字数，用逗号分隔: ")  


#考虑需不需要实现添加一个根据关键词选文章模板的功能（这个得和数据集对接一下）



# 使用split()方法根据逗号分割输入的字符串，并将分割后的单词添加到列表中  
keywords = input_string.split(",")   
  
# 根据关键词生成prompt 
prompt = "我想让你作为" + keywords[0] + "主题的博客作者，本博客的目标人群是" 
+ keywords[1] + "。提供" + keywords[2] 
+ "的全面概述。在回答问题时，请结合xx文章的写作风格，并且再" 
+ keywords[3] + "一点。请给我多个不同的例子。字数在" + keywords[4] + "左右。"

#输出
print(prompt) 
