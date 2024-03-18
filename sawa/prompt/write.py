from .base import Prompt

class WritePrompt(Prompt):
    def __init__(self):
        super().__init__()

    def format(self,keyword,title,contents,likes,matched_outline,user_query):
        '''
        Format writing redbook prompt
        Args:
            keyword : matched database keyword
            title : matched database title
            content : matched database content
            likes : matched database likes
            matched_outline : matched database outline
            user_query : user demande
            user_outline : outline generated from user query

        Returns:
            str : prompt to write redbook
        '''
        prompt_keyword = keyword
        prompt_title = title
        prompt_contents = contents
        prompt_demande = user_query


        prompt = '''
        你是小红书爆款写作专家，请你用以下步骤来进行创作，首先产出1个标题（含适当的emoji表情），其次产出1个正文（每一个段落含有适当的emoji表情，文末有合适的tag标签）
        一、在小红书标题方面，你会以下技能:
        1. 采用二极管标题法进行创作 
        2. 你善于利用标题夺人眼球
        3. 你善于使用爆款关键词，写标题时，从这些关键词中随机选1-2个
        4. 你了解小红书平台的标题特性
        5. 你懂得创作的规则

        二、在小红书正文方面，你会以下技能：
        1. 你了解小红书平台的写作风格
        2. 你了解小红书平台的文本结构
        3. 互动引导方法
        4. 一些使文章更具吸引力的小技巧
        5. 善于在文章中加入爆款关键词
        6. 从你生成的稿子中，抽取3-6个seo关键词，生成#标签并放在文章最后
        7. 文章的每句话都尽量口语化、增强文章的可阅读性
        8. 在每段话的开头使用表情符号，在每段话的结尾使用表情符号，在每段话的中间插入表情符号
    
        三、围绕以下主题：“ ''' + prompt_demande + ''' ”，以及你掌握的标题和正文的技巧，产出内容。请按照如下格式输出内容，只需要格式描述的部分，如果产生其他内容则不输出：
        一. 标题
        [标题]
        [换行]
        二. 正文
        [正文]
        标签：[标签]
        
        四、以下是一篇相关领域的爆款小红书文案，你可以参考它的格式但请不要模仿他的具体内容。示例文章如下：
        ''' + prompt_contents

        return prompt