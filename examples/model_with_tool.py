from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

model = init_chat_model('deepseek-chat')


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


# Bind (potentially multiple) tools to the model
model_with_tools = model.bind_tools([get_weather])

# Step 1: Model generates tool calls
messages = [HumanMessage("What's the weather in Boston?")]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)  # type: ignore

# Step 2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    # Execute the tool with the generated arguments
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)

# Step 3: Pass results back to model for final response
final_response = model_with_tools.invoke(messages)
print(final_response.text)
