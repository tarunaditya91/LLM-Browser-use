from langchain_openai import ChatOpenAI


system_prompt = """
You are an expert QA test automation agent. Your job is to:
1. Take plain English test instructions and a website URL.
2. Convert each instruction into structured actions like:
   {"action": "click", "selector": "button:contains('Sign in')"}
3. Use accurate selectors based on visible text or field attributes.
4. Maintain the order of steps and don’t skip anything.
5. Validate that the expected output is present at the end.

Example:

Steps:
- Click on the 'Sign in' button
- Enter email as 'test@example.com'
- Enter password as 'test123'
- Click on the 'Sign in' button

Expected Output:
User should see 'My account' page

Output:
[
  {"action": "click", "selector": "button:contains('Sign in')"},
  {"action": "type", "selector": "input[type='email']", "value": "test@example.com"},
  {"action": "type", "selector": "input[type='password']", "value": "test123"},
  {"action": "click", "selector": "button:contains('Sign in')"},
  {"action": "assert_text", "selector": "body", "text": "My account"}
]
"""


llm = ChatOpenAI(model="gpt-4o", temperature=0, system_message=system_prompt)


test_task = {
    "url": "https://www.farmley.com/",
    "test_case": {
        "steps": [
            "Click on the 'Sign in' button",
            "Enter email as 'test@example.com'",
            "Enter password as 'test123'",
            "Click on the 'Sign in' button"
        ],
        "expected_output": "User should see 'My account' page"
    }
}
