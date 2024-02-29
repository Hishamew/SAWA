from .base import Prompt

class OutlinePrompt(Prompt):
    def __init__(self):
        super().__init__()

    def format(self,title,content, *args):
        ''' format redbook content to a request of its outline
        Args:
            title (str) : redbook article title.
            content (str) : redbook article content.
            args (list[str]) : some keyword to be concerned.
        
        Returns:
            str : formatted prompt.
        '''

        keywords = '，'.join(args)

        prompt = '以下是有关一段小红书文案的信息，请根据内容生成一段字数更少但意思更加明确的大纲。'
        
        prompt += f'这篇小红书的题目是{title}。它的正文内容如下：{content}。另外这是这篇文章相关的关键词或标签：{keywords}。'

        prompt += '仅输出大纲即可，无需给出任何的补充说明。'

        return prompt

class WriteOutlinePrompt(Prompt):
    def __init__(self):
        super().__init__()

    def format(self,requires):
        prompt = "请根据以下要求生成一个小红书的大纲。仅输出大纲即可，无需给出任何的补充说明。"

        prompt += requires

        return prompt
