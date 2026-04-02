# Clown

Clown is a Python-based terminal coding assistant built from scratch.

Current status:
- local-first scaffold
- terminal CLI entrypoint
- agent loop skeleton
- provider abstraction
- tool registry foundation
- local transcript storage

## Goals

- Build a safe terminal-native coding assistant
- Keep the core engine modular and provider-agnostic
- Start local-first, then grow into a SaaS platform

## Project Layout

- `apps/cli`: CLI entrypoint and chat command
- `clown_core`: settings, logging, and paths
- `clown_agent`: agent engine and session loop
- `clown_llm`: model provider abstraction
- `clown_tools`: tool framework and built-in tools
- `clown_security`: approval and policy layer
- `clown_storage`: local persistence

## Development

```bash
cd clown
python -m clown.apps.cli.main chat
```

## Next Milestones

1. Add a real LLM provider implementation
2. Expand file and shell tools
3. Add permission prompts and safety policies
4. Improve chat UX and session resume
