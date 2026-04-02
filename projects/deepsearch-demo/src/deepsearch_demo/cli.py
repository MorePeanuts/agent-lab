from pathlib import Path
from deepsearch_demo.agents import DeepSearchAgent
from typing import Annotated
from typer import Typer, Argument, Option


app = Typer(name='DeepSearchAgent-Demo', help='')


@app.command()
def research(
    query: Annotated[str, Argument(help='')],
    save_dir: Annotated[str, Argument(help='')],
    max_reflections: Annotated[int, Option(help='')] = 3,
):
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    agent = DeepSearchAgent(max_reflections, Path(save_dir))
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
