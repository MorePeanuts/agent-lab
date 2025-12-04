from langchain.tools import tool
from rich.console import Console
from langchain.chat_models import init_chat_model

model = init_chat_model(model='deepseek-reasoner')
console = Console()


@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city"""
    return f"It's always sunny in {city}"


model = model.bind_tools([get_weather_for_location])

for chunk in model.stream('what is the weather in sf?'):
    for block in chunk.content_blocks:
        if block['type'] == 'reasoning' and (reasoning := block.get('reasoning')):
            console.print(reasoning, style='blue', end='')
        elif block['type'] == 'tool_call_chunk':
            console.print(block, style='red', end='')
        elif block['type'] == 'text':
            console.print(block['text'], end='')
