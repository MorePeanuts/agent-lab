from agent_lab.model_hub import ChatModelRegistry
from langchain.chat_models import init_chat_model, BaseChatModel
from ..tools.builtin import get_builtin_tool_list

_chat_models = {}


class ChatModelFactory:
    @staticmethod
    def get(model_name: str) -> BaseChatModel:
        for item in ChatModelRegistry:
            if item.name == model_name:
                chat_model = item
        builtin_tools = get_builtin_tool_list()
        if model_name not in _chat_models:
            _chat_models[model_name] = init_chat_model(**chat_model).bind_tools(builtin_tools)
        return _chat_models[model_name]
