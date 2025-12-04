from langchain.agents import create_agent
from pprint import pprint


def get_weather(city: str) -> str:
    """Get weather for a given city"""
    return f"It's always sunny in {city}"


agent = create_agent(
    model='deepseek-chat',
    tools=[get_weather],
    system_prompt='You are a helpful assistant',
)

output = agent.invoke({'messages': [{'role': 'user', 'content': 'what is the weather in sf'}]})
pprint(output)
