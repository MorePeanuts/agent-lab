from langchain.chat_models import init_chat_model
from rich.console import Console
from langchain.tools import tool


def text_streaming():
    model = init_chat_model('deepseek-chat')
    full = None
    for chunk in model.stream('what color is the sky.'):
        full = chunk if not full else full + chunk
        print(full.text)

    print(full.content_blocks)  # type: ignore


def tool_calls_streaming():
    model = init_chat_model(model='deepseek-reasoner')
    console = Console()

    @tool
    def get_weather_for_location(city: str) -> str:
        """Get weather for a given city"""
        return f"It's always sunny in {city}"

    model = model.bind_tools([get_weather_for_location])

    full = None
    for chunk in model.stream('what is the weather in sf?'):
        for block in chunk.content_blocks:
            if block['type'] == 'reasoning' and (reasoning := block.get('reasoning')):
                console.print(reasoning, style='blue', end='')
            elif block['type'] == 'tool_call_chunk':
                console.print(block, style='red', end='')
            elif block['type'] == 'text':
                console.print(block['text'], end='')
        full = chunk if not full else full + chunk

    print(full.content_blocks)  # type: ignore


if __name__ == '__main__':
    # print('text_streaming:')
    # text_streaming()
    print('tool_calls_streaming:')
    tool_calls_streaming()
