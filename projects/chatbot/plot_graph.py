from chatbot.agents import create_agent
from pathlib import Path


if __name__ == '__main__':
    agent, _ = create_agent()
    fig = agent.get_graph(xray=True).draw_mermaid_png()
    path = Path(__file__).parent / 'graph.png'
    with path.open('wb') as f:
        f.write(fig)
