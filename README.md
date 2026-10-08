# dev-environment-vs-code

A basic Python LangGraph chatbot. Its graph follows `START → agent → END`,
using message state and an OpenAI chat model. The offline demo uses a fake model
with a fixed response; it exercises the same graph without network access or keys.

## Develop in a container

1. Install Docker and the **Dev Containers** extension in VS Code.
2. Open this repository and select **Dev Containers: Reopen in Container**.
3. The container uses `ghcr.io/ryanwirt/python-ai-ubuntu-24.04:main` and installs
   the project into `.venv` automatically.
4. In the container terminal, run:

   ```sh
   .venv/bin/langgraph-agent --demo
   ```

The image must be accessible to your Docker installation. If it is private,
authenticate to GHCR with `docker login ghcr.io` before reopening the container.

## Run with an LLM

Set `OPENAI_API_KEY` in your terminal environment, then run:

```sh
.venv/bin/langgraph-agent "Explain state graphs in one sentence"
```

The default model is `gpt-4o-mini`. Override it with `--model` or `OPENAI_MODEL`.
API calls require network access and may incur charges. Do not commit API keys;
`.env` files are ignored, but are not loaded automatically.

## Run locally

Python 3.12 or newer is required:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/langgraph-agent --demo
```

To extend the agent, add nodes or routing in `src/langgraph_agent/__init__.py`.
`build_agent(model)` accepts a chat model so graph behavior can also be exercised
with a fake model.