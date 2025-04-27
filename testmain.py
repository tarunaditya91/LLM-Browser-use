import asyncio
import os
import json
import random
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr, BaseModel
from typing import List
from browser_use import Agent, Controller
from datetime import datetime


load_dotenv()


class Web_Data(BaseModel):
    WebSite_url: str
    UserName: str
    Password: str
    output: str
    loginStatus: str
    status: str
    timestamp: str

class Web_Datas(BaseModel):
    webdatas: List[Web_Data]

controller = Controller(output_model=Web_Datas)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEN API KEY IS NOT SET')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

def save_test_result(test_data: dict):
    filename = 'test_results.json'

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(test_data)

    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)


def generate_random_password():
    passwords = [
        'pass1234',
        'admin@123',
        'Test@987',
        'Qwerty@2025',
        'Incorrect@123'
    ]
    return random.choice(passwords)


async def run_search():
    
    for i in range(5):
        print(f"\n--- Attempt {i+1} ---\n")

        random_password = generate_random_password()

       
        agent = Agent(
            task=(
                f"Go to website URL=https://www.farmley.com "
                f"Click 'Sign in', enter email 'test@example.com' and password '{random_password}', "
                f"then click 'Sign in' again."
            ),
            llm=llm,
            max_actions_per_step=4,
            controller=controller,
        )

        history = await agent.run(max_steps=25)

        result = history.final_result()

        test_data = {
            "WebSite_url": "https://www.farmley.com",
            "UserName": "test@example.com",
            "Password": random_password,
            "output": result if result else "No output returned",
            "loginStatus": "Pass" if result and "My account" in result else "Fail",
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
        }

        if result:
            result_dict = json.loads(result)
            parsed: Web_Datas = Web_Datas.parse_obj(result_dict)
            for post in parsed.webdatas:
                print('\n--------------------------------')
                print(f'WebSite_url:     {post.WebSite_url}')
                print(f'UserName:        {post.UserName}')
                print(f'Password:        {post.Password}')
                print(f'output:          {post.output}')
                print(f'loginStatus:     {post.loginStatus}')
        else:
            print('No result')

       
        save_test_result(test_data)

if __name__ == '__main__':
    asyncio.run(run_search())
