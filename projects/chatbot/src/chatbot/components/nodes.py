from langchain.messages import AIMessage, ToolMessage, HumanMessage
from .state import ChatBotState
from .models import ChatModelFactory
from ..utils.commands import CommandParser
from ..tools.builtin import get_builtin_tool
from langgraph.types import interrupt, Command
from typing import Literal


def user_input(state: ChatBotState) -> Command[Literal['chat_model_call', 'command_parse']]:
    user_prompt: str = interrupt(
        {
            'action': 'user_input',
            'message': '> ',
        }
    )
    is_command = CommandParser.is_command(user_prompt)
    goto = 'chat_model_call'
    if is_command:
        goto = 'command_parse'
    else:
        pass
        # TODO: User data security verification
    return Command(
        update={
            'messages': [HumanMessage(user_prompt)],
            'user_last_prompt': user_prompt,
        },
        goto=goto,
    )


async def chat_model_call(state: ChatBotState) -> Command[Literal['builtin_tools', 'user_input']]:
    chat_model = ChatModelFactory.get(state['chat_model'])
    ai_msg = await chat_model.ainvoke(state['messages'])

    if hasattr(ai_msg, 'tool_calls') and len(ai_msg.tool_calls) > 0:
        goto = 'builtin_tools'
    else:
        goto = 'user_input'

    return Command(
        update={
            'messages': [ai_msg],
            'model_last_response': ai_msg.content,
        },
        goto=goto,
    )


def command_parse(state: ChatBotState) -> Command[Literal['user_input', '__end__']]:
    if state['user_last_prompt'] == '/exit':
        return Command(goto='__end__')
    # TODO: More command parsing
    else:
        # TODO: If the command parsing fails, an error message
        # must be output and fall back to the user input.
        return Command(goto='user_input')


async def builtin_tools(state: ChatBotState) -> Command[Literal['chat_model_call']]:
    ai_msg = state['messages'][-1]
    assert isinstance(ai_msg, AIMessage), (
        'The last message entering the tool call node does not come from AI.'
    )
    tool_msgs = []
    for tool_call in ai_msg.tool_calls:
        user_response = interrupt(
            {
                'action': 'builtin_tools',
                'message': (
                    f'ChatBot wants to use builtin tool {tool_call["name"]}.\n'
                    f'Args:\n\t{tool_call["args"]}'
                    'Do you allow this operation? (y/n)'
                ),
            }
        )
        if user_response == 'y':
            tool_msg = await get_builtin_tool(tool_call['name']).ainvoke(tool_call)
            tool_msgs.append(tool_msg)
        else:
            tool_msgs.append(
                ToolMessage(
                    content='The tool call was rejected by the user.',
                    tool_call_id=tool_call['id'],
                )
            )
    return Command(update={'messages': tool_msgs}, goto='chat_model_call')
