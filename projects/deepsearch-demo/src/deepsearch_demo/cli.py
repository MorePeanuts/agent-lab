from deepsearch_demo.utils import now
from pathlib import Path
from deepsearch_demo.agents import DeepSearchAgent
from typing import Annotated
from typer import Typer, Argument, Option
from datetime import datetime


app = Typer(name='DeepSearchAgent-Demo', help='A deep research agent that performs web searches and generates comprehensive reports.')


@app.command()
def research(
    query: Annotated[str, Argument(help='The research query to investigate')],
    save_dir: Annotated[str | None, Argument(help='Directory to save research outputs (default: output/<timestamp>)')] = None,
    max_reflections: Annotated[int, Option(help='Maximum number of reflection iterations per paragraph')] = 3,
):
    """
    Perform deep research on a given query.

    This command initiates a comprehensive research process that includes:
    - Generating a report structure with multiple paragraphs
    - Searching the web for relevant information
    - Summarizing findings
    - Reflecting on and improving the content
    - Generating a final report

    Results are saved to the specified directory or a timestamped output folder.
    """
    if save_dir is None:
        path = Path(__file__).parents[2] / f'output/{now()}'
    else:
        path = Path(save_dir)
    path.mkdir(parents=True, exist_ok=True)
    agent = DeepSearchAgent(path, max_reflections)
    agent.research(query)


@app.command()
def plot_graph(path: Annotated[str | None, Argument(help='Path to save the graph PNG file (default: graph.png)')] = None):
    """
    Plot the state graph of the research agent.

    Generates a visual representation of the agent's workflow showing all
    nodes and edges in the state machine. This helps understand the research
    process flow.
    """
    agent = DeepSearchAgent()
    if path is None:
        agent.plot_graph(Path(__file__).parents[2] / 'graph.png')
    else:
        agent.plot_graph(Path(path))


def main():
    """Entry point for the DeepSearchAgent-Demo CLI."""
    print('Hello from DeepSearchAgent-Demo!')
    app()
