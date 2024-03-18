from .base import Prompt

class RedBookEditorPrompt(Prompt):
    def __init__(self,completions=''):
        super().__init__()
        self.completions = completions

    def format(self):
        return " 你现在是一个小红书编辑。" + self.completions

