from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage
from langgraph.types import Command
from loguru import logger
from .state import State
from .schema import ReportStructure


class DeepSearchAgent:
    def __init__(self):
        self.llm = init_chat_model('deepseek-chat')

    def research(self, query: str, save_report: bool = True) -> str:
        logger.info(f'Start research: {query}')
        self.state = {'query': query}

        return ''

    def generate_report_structure(self, state: State) -> Command:
        logger.info('Step1: Generate report structure.')
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
                    HumanMessage(state['query']),
                ]
            )
            assert isinstance(report_structure, ReportStructure)
        except Exception:
            logger.exception('Exception occurred while generating the report structure.')
            raise

        report_title = f'Deep Research Report on {state["query"]}'
        paragraphs = []
        for idx, item in enumerate(report_structure.items):
            paragraphs.append(
                {
                    'title': item.title,
                    'content': item.content,
                    'order': idx,
                }
            )

        logger.info(
            f'The report structure has been generated, consisting of {len(paragraphs)} paragraphs.'
        )
        for idx, paragraph in enumerate(paragraphs, 1):
            logger.info(f'\t{idx}. {paragraph["title"]}')

        return Command(
            update={
                'report_title': report_title,
                'paragraphs': paragraphs,
            }
        )
