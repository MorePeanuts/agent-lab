from enum import Enum
from langchain.chat_models import init_chat_model


class ModelRegistry(Enum):
    DEEPSEEK_V4_FLASH = {
        'model': 'deepseek-v4-flash',
        'model_provider': 'deepseek',
        'extra_body': {'thinking': {'type': 'disabled'}},
    }
    DEEPSEEK_V4_FLASH_THINKING = {
        'model': 'deepseek-v4-flash',
        'model_provider': 'deepseek',
        'reasoning_effort': 'high',
        'extra_body': {'thinking': {'type': 'enabled'}},
    }
    DEEPSEEK_V4_PRO = {
        'model': 'deepseek-v4-pro',
        'model_provider': 'deepseek',
        'extra_body': {'thinking': {'type': 'disabled'}},
    }
    DEEPSEEK_V4_PRO_THINKING = {
        'model': 'deepseek-v4-pro',
        'model_provider': 'deepseek',
        'reasoning_effort': 'high',
        'extra_body': {'thinking': {'type': 'enabled'}},
    }
    DEEPSEEK_V4_PRO_MAX = {
        'model': 'deepseek-v4-pro',
        'model_provider': 'deepseek',
        'reasoning_effort': 'max',
        'extra_body': {'thinking': {'type': 'enabled'}},
    }


def get_chat_model(model: ModelRegistry):
    return init_chat_model(**model.value)  # type: ignore
