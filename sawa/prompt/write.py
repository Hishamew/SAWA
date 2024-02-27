from .base import Prompt

class WritePrompt(Prompt):
    def __init__():
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
        
        return