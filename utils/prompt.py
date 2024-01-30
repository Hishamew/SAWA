from typing import Any
from retrieval import Retrieval
import os


# 任务：写成封装好可以调用的函数或类，输入是关键词+示例文案，输出是prompt
class Prompt():
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

 
keywords = []  
input_string = input("请依次输入你需求文章的主题，目标人群，期望内容，风格，大致字数，用逗号分隔: ")  


# 调用搜索的例子见utils\retrieval.py的test_retireval()
  
keywords = input_string.split(",")   
  
prompt = "我想让你作为" + keywords[0] + "主题的博客作者，本博客的目标人群是" 
+ keywords[1] + "。提供" + keywords[2] 
+ "的全面概述。在回答问题时，请结合xx文章的写作风格，并且再" 
+ keywords[3] + "一点。请给我多个不同的例子。字数在" + keywords[4] + "左右。"

print(prompt) 
