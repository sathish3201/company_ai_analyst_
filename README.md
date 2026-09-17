# Company AI Analyst

Enterprise **Personal Assistant + Dynamic Company Data Analyst + Deep Agent** platform.

The system accepts text or voice input, understands the request, builds relevant context, and eventually executes dynamic enterprise data-analysis workflows through Deep Agent and LangGraph.

---

## Architecture

```text
                         USER
                    ┌──────┴──────┐
                    │             │
                  TEXT          VOICE
                                  │
                                  ▼
                                 STT
                                  │
                    └──────┬──────┘
                           ▼
                  PERSONAL ASSISTANT
                           │
                           ▼
                 CONTEXT ENGINEERING
                           │
                           ▼
                    LiteLLM Gateway
                           │
             ┌─────────────┼─────────────┐
             │             │             │
        Guardrails       Router       Fallback
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                      DEEP AGENT
                           │
                           ▼
                       LANGGRAPH
                           │
             Dynamic Workflow Execution
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
       SQL                RAG               Python
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                        Reducer
                           │
                       Validator
                           │
                          HITL
                           │
                           ▼
                    Final Response
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                  TEXT           TTS
```

---

# Development Architecture

The project is developed incrementally.

```text
Day 1
Enterprise Core + LLM Gateway
        │
        ▼
Day 2
Personal Assistant + Context Engineering
        │
        ▼
Day 3
Deep Agent Runtime
        │
        ▼
Day 4
LangGraph Dynamic Workflows
        │
        ▼
Day 5
Dynamic Capabilities + Metaprogramming
        │
        ▼
Day 6
Enterprise Data Analyst
        │
        ▼
Day 7
Enterprise RAG
        │
        ▼
Day 8
Security + Guardrails + HITL
        │
        ▼
Day 9
Visualization + Memory + Observability
        │
        ▼
Day 10
Full Integration + Deployment
```

---

# Day 1

## Enterprise Core + LLM Foundation

```text
Request
   │
   ▼
RequestContext
   │
   ├── Request Identity
   ├── User Identity
   └── Permissions
   │
   ▼
Model Registry
   │
   ▼
Model Router
   │
   ▼
LiteLLM Gateway
   │
   ▼
Ollama / Cloud Models
```

Main focus:

* SOLID architecture
* Interfaces / ABCs
* Dependency injection
* Request and trace IDs
* User/company context
* Authorization foundation
* Model registry
* Model routing
* Retry/fallback
* LiteLLM gateway
* Guardrail abstraction
* Ollama integration

Current local model:

```text
ollama/qwen2.5-coder:1.5b
```

### Day 1 Tests

```text
tests/unit/
    test_model_registry.py
    test_model_router.py
    test_llm_gateway.py
    test_fallback.py
    test_authorization.py
    ...

tests/integration/
    test_litellm_ollama.py
    test_ollama_gateway.py
```

Run:

```bash
pytest tests/unit -v
```

Integration:

```bash
pytest tests/integration -v -m integration
```

Detailed documentation:

`docs/day_1.md`

---

# Day 2

## Personal Assistant + Context Engineering

```text
USER
 │
 ├── TEXT
 │
 └── VOICE
       │
       ▼
      STT
       │
       ▼
Personal Assistant
       │
       ├────────► Intent Analyzer
       │
       └────────► Context Engine
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
           Request    User   Enterprise
              │        │        │
              └────────┼────────┘
                       ▼
                    Ranker
                       ▼
                    Filter
                       ▼
                  Compressor
                       ▼
                   Assembler
                       ▼
                 ContextBundle
```

Main focus:

* Personal Assistant
* Intent classification
* Request context
* User context
* Enterprise context
* Memory context foundation
* Context ranking
* Context filtering
* Context compression abstraction
* Context assembly
* Context Engine
* STT interface
* TTS interface

### Day 2 Tests

```text
tests/unit/
    test_context_models.py
    test_context_providers.py
    test_context_processing.py
    test_context_engine.py
    test_intent_analyzer.py
    test_personal_assistant.py
    test_voice.py

tests/integration/
    test_personal_assistant_flow.py
```

Run:

```bash
pytest tests/unit -v
```

Integration:

```bash
pytest tests/integration/test_personal_assistant_flow.py -v -m integration
```

Detailed documentation:

`docs/day_2.md`

---

# Testing Strategy

The project follows block-by-block testing.

```text
Implement Component
        │
        ▼
Write Unit Tests
        │
        ▼
Run Unit Tests
        │
        ▼
Fix Component
        │
        ▼
Next Component
        │
        ▼
Integration Testing
```

## Unit Tests

Unit tests verify individual components independently and mock external infrastructure.

```bash
pytest tests/unit -v
```

## Integration Tests

Integration tests verify communication between real components and external infrastructure.

Examples:

```text
LiteLLM → Ollama
Personal Assistant → Context Engine
```

```bash
pytest tests/integration -v -m integration
```

---

# Detailed Documentation

Detailed implementation, architecture, class responsibilities, code changes, and test cases are maintained separately:

* [Day 1 Documentation](docs/day_1.md)
* [Day 2 Documentation](docs/day_2.md)

Future days will follow the same documentation structure.

---

# Project Status

| Day | Area                         | Status                |
| --- | ---------------------------- | --------------------- |
| 1   | Enterprise Core + LLM        | In Progress / Testing |
| 2   | Personal Assistant + Context | Completed             |
| 3   | Deep Agent                   | Planned               |
| 4   | LangGraph Workflows          | Planned               |
| 5   | Dynamic Capabilities         | Planned               |
| 6   | Enterprise Data Analyst      | Planned               |
| 7   | Enterprise RAG               | Planned               |
| 8   | Security + HITL              | Planned               |
| 9   | Visualization + Memory       | Planned               |
| 10  | Integration + Deployment     | Planned               |
