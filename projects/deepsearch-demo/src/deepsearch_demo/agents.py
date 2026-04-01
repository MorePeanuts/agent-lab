import json
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from loguru import logger
from .state import State, Paragraph
from .schema import ReportStructure
from .tools import tavily_search
from .utils import truncate_content


class DeepSearchAgent:
    def __init__(self):
        self.llm = init_chat_model('deepseek-chat')
        self.max_reflections = 3
        self.agent = (
            StateGraph(State)
            .add_node('generate_report_structure', self.generate_report_structure)
            .add_node('first_search', self.first_search)
            .add_node('first_summary', self.first_summary)
            .add_edge(START, 'generate_report_structure')
            .compile()
        )

    def research(self, query: str, save_report: bool = True) -> str:
        logger.info(f'Start research: {query}')
        self.state = State(query=query)
        response = self.agent.invoke(self.state)
        return AIMessage(response['final_report']).pretty_repr()

    def generate_report_structure(self, state: State) -> Command:
        logger.info('Generating the report structure based on the following query:')

        prompt = """
You are a deep research assistant. Given a query, you need to plan the structure of a report and the paragraphs it contains. Up to five paragraphs.

Ensure the paragraphs are logically and sequentially ordered.

Once the outline is created, you will be provided with tools to search the web and reflect on each section separately.
"""
        llm_with_structure = self.llm.with_structured_output(ReportStructure)
        try:
            report_structure = llm_with_structure.invoke(
                [
                    SystemMessage(prompt),
                    HumanMessage(state.query),
                ]
            )
            assert isinstance(report_structure, ReportStructure)
        except Exception:
            logger.exception('Exception occurred while generating the report structure.')
            raise

        report_title = f'Deep Research Report on {state.query}'
        paragraphs = []
        for idx, item in enumerate(report_structure.items):
            paragraphs.append(Paragraph(item.title, item.content, order=idx))

        logger.info(
            f'The report structure has been generated, consisting of {len(paragraphs)} paragraphs.'
        )
        for idx, paragraph in enumerate(paragraphs, 1):
            logger.info(f'\t{idx}. {paragraph["title"]}')

        return Command(
            update={
                'report_title': report_title,
                'paragraphs': paragraphs,
                'paragraph_index': 0,
            },
            goto='first_search',
        )

    def first_search(self, state: State) -> Command:
        prompt = """
You are an in-depth research assistant. You will be given the title and expected content of a paragraph from a report.

You can use a web search tool that accepts 'search_query' as a parameter.

Your task is to think about this topic and provide the best web search query to enrich your current knowledge.
"""
        llm_with_tools = self.llm.bind_tools([tavily_search], tool_choice='tavily_search')

        paragraph_index = state.paragraph_index
        paragraphs = state.paragraphs
        paragraph = paragraphs[paragraph_index]
        logger.info(f'Processing paragraph {paragraph_index}, performing first search.')

        user_prompt = f"""
Title: {paragraph.title}
Expected content: {paragraph.content}
"""
        ai_msg = llm_with_tools.invoke(
            [
                SystemMessage(prompt),
                HumanMessage(user_prompt),
            ]
        )
        search_results = []
        for tool_call in ai_msg.tool_calls:
            tool_results = tavily_search.invoke(tool_call['args'])
            search_results.append(tool_results)

        logger.info(f'A total of {len(search_results)} search results found')
        paragraph.research.search_history.extend(search_results)

        return Command(update={'paragraphs': paragraphs}, goto='first_summary')

    def first_summary(self, state: State) -> Command:
        prompt = """
"""

        paragraph_index = state.paragraph_index
        paragraphs = state.paragraphs
        paragraph = paragraphs[paragraph_index]
        search_history = paragraph.research.search_history
        logger.info(f'Processing paragraph {paragraph_index}, performing first summary.')

        user_prompt = f"""
Title: {paragraph.title}
Expected content: {paragraph.content}

"""
        if len(search_history) > 0:
            user_prompt += f'Search query: {search_history[0].search_query}\n'
        for idx, search_result in enumerate(search_history):
            user_prompt += f'\tSearch result {idx}: {truncate_content(search_result.content)}'
        response = self.llm.invoke(
            [
                SystemMessage(prompt),
                HumanMessage(user_prompt),
            ]
        )
        paragraph.research.latest_summary = response.pretty_repr()
        logger.info(
            f'First summary for paragraph {paragraph_index}: {truncate_content(paragraph.research.latest_summary, 100)}'
        )

        return Command(update={'paragraphs': paragraphs}, goto='reflection')

    def reflection(self, state: State) -> Command:
        raise NotImplementedError()
