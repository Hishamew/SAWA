from openai import OpenAI
import httpx

class LLM:
    def __init__(self,api_base,
                 api_key,
                 model = "gpt-4-1106-preview",
                 temperature = 1,
                 stream = True):

        self.client = OpenAI(api_key=api_key,
                            base_url=api_base, 
                            http_client=httpx.Client(
                            base_url="https://vip-hk-s1.zeabur.app/v1",
                            follow_redirects=True,),
        )
        self.model = model
        self.temperature = temperature
        self.stream = stream

    def __call__(self,msgs=None,roles=['user'],*args):
        assert msgs is not None or len(args)!=0, "You must input msg-role pair in form of str or list of dict."
        if msgs is not None and len(args) != 0:
            raise RuntimeError("One form of input at a time.")
        if msgs is not None :
            if isinstance(msgs,str):
                msgs = [msgs]
            assert len(msgs) == len(roles),"Your message and role doesn't have a same size"
            messages = [dict(role=role,message=message) for role,message in zip(roles,msgs)]
        else:
            self.check_args_input(args)

        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=self.temperature,stream=self.stream)

        lines = []
        for chunk in response:
            line = chunk.choice[0].data.content
            lines.append(line)
        results = ''.join(lines)
        return results,len(results)
    
    def check_args_input(self,args):
        for message in args:
            if 'role' not in message or 'message' not in message:
                raise RuntimeError("Invalid input form")
            
if __name__ == "__main__":
    llm = LLM(api_key="sk-jIX3lMObPh1Rbu44Bb2dEeD7347a4998A2E095Ee208cA108",api_base = "https://vip-hk-s1.zeabur.app/v1")
    response,_ = llm("hello")
    print(response)