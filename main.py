from browser_use import Agent
from dotenv import load_dotenv
import asyncio


load_dotenv()

from config import llm, test_task

async def main():
    agent = Agent(
        task=test_task,
        llm=llm,
    )
    result = await agent.run()
    print("\n✅ Test Result:")
    print(result)

asyncio.run(main())
