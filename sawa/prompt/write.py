from .base import Prompt

class WritePrompt(Prompt):
    def __init__(self):
        super().__init__()

    def format(self,keyword,title,contents,likes,matched_outline,user_query,user_outline):
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


        prompt = "我想让你作为" + prompt_keyword + "主题的小红书内容作者，为小红书用户用户创作一篇文案。"
        prompt += "文案的大纲如下： " + user_outline + "请在这篇大纲的基础上进行创作，创作的文章请至少包括大纲上的所有内容。"
        prompt += "在回答问题时，请仿照后面文章的写作风格，如果有相关内容的话，写作内容也可以以示例文章作为补充。请给我多个不同的例子。示例文章如下：" + prompt_contents

        return prompt