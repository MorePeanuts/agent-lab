from deepsearch_demo.utils import now
from pathlib import Path
from deepsearch_demo.agents import DeepSearchAgent
from typing import Annotated
from typer import Typer, Argument, Option
from datetime import datetime


app = Typer(name='DeepSearchAgent-Demo', help='')


@app.command()
def research(
    query: Annotated[str, Argument(help='')],
    save_dir: Annotated[str | None, Argument(help='')] = None,
    max_reflections: Annotated[int, Option(help='')] = 3,
):
    if save_dir is None:
        path = Path(__file__).parents[2] / f'output/{now()}'
    else:
        path = Path(save_dir)
    path.mkdir(parents=True, exist_ok=True)
    agent = DeepSearchAgent(path, max_reflections)
    agent.research(query)


@app.command()
def plot_graph(path: Annotated[str | None, Argument(help='')] = None):
    agent = DeepSearchAgent()
    if path is None:
        agent.plot_graph(Path(__file__).parents[2] / 'graph.png')
    else:
        agent.plot_graph(Path(path))


def main():
    print('Hello from DeepSearchAgent-Demo!')
    app()
