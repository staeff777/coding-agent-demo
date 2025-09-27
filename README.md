# Basic LLM Agent Demo

This is a basic demo of an LLM agent with tool support. The aim of this project is to present coding agents in an 
understandable way.

The most important aspect of this concept is equipping the LLM with the tools it needs to solve problems.
These tools are defined in `agent/prompts.py` and implemented in `core/`. The llm can call these tools via tool calls 
(see agent/tool_call_handler.py).

## Structure

```
src/coding_agent_demo
├── agent
│   ├── chat_session.py             > basic text ui, chat loop with agent  
│   ├── llm.py                      > llm api communication
│   ├── prompts.py                  > very basic agentic prompt and tool definitions
│   └── tool_call_handler.py        > handle tool calls from the agent
├── config
│   └── settings.py                 > configuration of llms and workspace
├── core
│   ├── file_ops.py                 > file operations [provided as tools]
│   ├── merge.py                    > basic llm based merging [provided as tool]
│   ├── sandbox.py                  > simple sandboxing to keep the agent in the workspace
│   └── tree_sitter_utils.py        > exemplary code analysis with tree-sitter [provided as tool]
└── main.py
```

## Configuration
this demo uses an Open AI v1 compatible API with tool support.
### OpenRouter
You can use free models for testing from OpenRouter. Most of them will use your input as training data.
Of couse, model with API costs are also available.

1. Get your OpenRoter API Key.
2. Select a model with tool support:
https://openrouter.ai/models?supported_parameters=tools
3. define key and models in a .env file: 
```
api_key=...
model_primary=deepseek/deepseek-chat-v3.1:free
model_merge=deepseek/deepseek-chat-v3.1:free
```
The model_primary is used for main response generation, the model_merge is used to merge tool results into the final response (can be smaller or cheaper).
4. alternatively the **API_KEY** can also be set as an environment variable.

### Open AI
use your OpenAI API key and models with tool support:

.env file:
```
api_key=...
model_primary=gpt-5-codex
model_merge=gpt-5-mini
api_base=https://api.openai.com/v1
```
## run with uv
1. Install [uv](https://docs.astral.sh/uv/) if not done yet.
2. run `uv run coding-agent`

## AGENTS.md support

The coding-agent reads [AGENTS.md](https://AGENTS.md) from the workspace root.

# Where to go from here?

If you want to build on this example, there are various options available:

- improve the Prompt, see [
system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) for inspiration 
- [Extend the agent architecture](https://www.promptingguide.ai/research/llm-agents)
  - [Reflexion](https://www.promptingguide.ai/techniques/reflexion)
  - [ReAct](https://www.promptingguide.ai/techniques/react)
  - [Subagents](https://docs.claude.com/en/docs/claude-code/sub-agents), see [agent list](https://github.com/wshobson/agents)
  - [Context Window Management](https://factory.ai/news/compressing-context#proactive-memory-curation)
    - Implement a Context Window Management
- Further Tools (e.g. run commands)
- Improve the Treesitter integration
  - allow the llm to search for patterns
  - 
- Tool Policy layer, to allow autated tool calling for specific tools / patterns
- add [MCP support](https://modelcontextprotocol.io/), to allow a broader tool / service use
- Improve UI (e.g. web based, a good TUI) - or integrate it into another application
  - Show Diffs for code changes
  - Track costs/token usage of LLM calls
- Other Use Cases, like text writing, data analysis, ...
- Try Local Models with tool support