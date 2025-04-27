import asyncio
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr, BaseModel
from typing import List
from browser_use import Agent,Controller
import json
load_dotenv()

class Web_Data(BaseModel):
    WebSite_url:str
    UserName:str
    Password:str
    output:str
    loginStatus:str
    status: str
    timestamp: str


class Web_Datas(BaseModel):
    webdatas: List[Web_Data]

controller = Controller(output_model=Web_Datas)


api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEN API KEY IS NOT SET')
    print("THE ERROR IS DUE TO API")


llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp',api_key=SecretStr(api_key))

def save_test_result(test_data: dict):
    filename = 'test_results.jsaon'

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    existing_data.append(test_data)

    with open(filename,'w') as file:
        json.dump(existing_data,file,indent =4)


async def run_search():
    agent = Agent(
        task = 'go to website utl=https://www.farmley.com  and applt five different passwor and username to login',
        llm = llm,
        max_actions_per_step =4,
        controller=controller,
    )
    
    history = await agent.run(max_steps=25)

    result = history.final_result()

    if result:
        parsed: Web_Datas.model_validate_json(result)
        for post in parsed.webdatas:
            print('\n--------------------------------')
            print(f'WebSite_url:            {post.WebSite_url}')
            print(f'UserName:              {post.UserName}')
            print(f'Password:             {post.Password}')
            print(f'output:               {post.output}')
            print(f'loginStatus:          {post.loginStatus}')
    else:
        print('No result')


    


if __name__ == '__main__':
    asyncio.run(run_search())