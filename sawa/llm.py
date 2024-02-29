import yaml

from openai import OpenAI


class LLM:
    def __init__(self,api_base = None ,
                 api_key = None,
                 model = "gpt-4-1106-preview",
                 temperature = 1,
                 stream = True,
                 sys_prompt = "你是一个私人助理，请你根据指令帮助我完成我的工作。\n\n",
                 ):

        self.client = OpenAI(api_key=api_key,
                            base_url=api_base
        )
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.sys_prompt = sys_prompt
        self.history = []

    def __call__(self,user_prompt,count_history = True,use_history = True):

        ''' call function to get gpt response
        Args:
            user_prompt (str) : phrase or prompt to get results.
        
        Return:
            str : gpt response
        
        '''

        results = self.call_openai_api(user_prompt,use_history)
        if count_history:
            self.history.extend([{
                'role' : 'user',
                'content' : user_prompt,
            },
            {
                'role' : 'assistant',
                'content': results,
            }])
        return results
    
    def call_openai_api(self, user_prompt, use_history) -> dict:
        message = self.make_message(user_prompt,use_history)
        try:
            # print('Calling openai api.')
            response = self.client.chat.completions.create(model="gpt-4-1106-preview",
                messages=message,
                stream=self.stream,
                temperature=self.temperature)
            final = ''
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    final += chunk.choices[0].delta.content
            return final
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def make_message(self,user_prompt,use_history):
        message=[{
                    'role': 'system',
                    'content':self.sys_prompt
                }]
        if use_history :
            message.extend(self.history)

        message.append({
            'role' : 'user',
            'content': user_prompt,
        })
        return message
    
    def get_embeddings(self,text,model = "text-embedding-3-small"):
        text = text.replace("\n", " ")
        embeddings = self.client.embeddings.create(input = [text], model=model).data[0].embedding
        return embeddings
    
    @property
    def dialogue(self):
        return self.history


def build_llm_from_config(config,sys_prompter):
    with open(config,'r') as f:
        cfg = yaml.safe_load(f)
    sys_prompt = sys_prompter()
    llm = LLM(**cfg,sys_prompt=sys_prompt)
    return llm
    

            
if __name__ == "__main__":

    
    llm = build_llm_from_config(config='config/openai.yaml',
                                sys_prompt="你是一个私人助理，请你根据指令帮助我完成我的工作。\n\n")

    response = llm("请用法语翻译以下这段话，尽量做到用书面语：我想请问是否仅需要参加考试，还是需要出席课堂和做作业呢？")
    print(response)
    