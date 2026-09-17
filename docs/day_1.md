# Day 1 — Enterprise Core + LLM Foundation

## 1. Day 1 Objective

The objective of Day 1 is to build the **enterprise-grade foundation** of the Company AI Analyst before introducing agents, workflows, databases, RAG, or analytics.

Day 1 establishes the contracts and infrastructure required by all future layers.

### Day 1 focuses on

* Python project architecture
* `uv` environment
* Configuration foundation
* Project path management
* Request identity
* Request/trace IDs
* User identity
* Company/tenant context
* Permission context
* Authorization abstraction
* LLM contracts
* Model registry
* Model router
* Retry policy
* Model fallback
* LiteLLM gateway
* Guardrail abstraction
* Ollama integration
* Unit testing
* Integration testing

---

# 2. Day 1 Scope

```text
┌──────────────────────────────────────────────┐
│                 DAY 1 SCOPE                  │
├──────────────────────────────────────────────┤
│                                              │
│  Project Foundation                          │
│       │                                      │
│       ▼                                      │
│  Request / User / Permission Context         │
│       │                                      │
│       ▼                                      │
│  Authorization                               │
│       │                                      │
│       ▼                                      │
│  Model Registry                              │
│       │                                      │
│       ▼                                      │
│  Model Router                                │
│       │                                      │
│       ▼                                      │
│  LiteLLM Gateway                             │
│       │                                      │
│       ├── Retry                              │
│       ├── Fallback                           │
│       └── Guardrail abstraction              │
│       │                                      │
│       ▼                                      │
│  Ollama                                      │
│       │                                      │
│       ▼                                      │
│  qwen2.5-coder:1.5b                         │
│                                              │
└──────────────────────────────────────────────┘
```

---

# 3. Explicitly Out of Scope

The following are **not implemented in Day 1**:

* Personal Assistant
* Intent classification
* Deep Agent
* LangGraph workflows
* Dynamic workflow generation
* Dynamic subgraphs
* SQL execution
* Database connectivity
* Pandas analysis
* Enterprise RAG
* Vector database
* Document ingestion
* Embeddings
* Tool execution
* Subagents
* HITL workflows
* Production guardrails
* Long-term memory
* Visualization
* FastAPI API
* Web UI
* Authentication
* Deployment

These are introduced in later development days.

---

# 4. High-Level Architecture

```text
                         APPLICATION
                              │
                              ▼
                       RequestContext
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        RequestIdentity   UserIdentity   PermissionContext
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                     Authorization Layer
                              │
                              ▼
                       Model Registry
                              │
                              ▼
                        Model Router
                              │
                              ▼
                       LLM Gateway
                              │
                              ▼
                     LiteLLM Gateway
                              │
                  ┌───────────┴───────────┐
                  │                       │
              Guardrails              Fallback
                  │                       │
                  └───────────┬───────────┘
                              ▼
                           LiteLLM
                              │
                              ▼
                            Ollama
                              │
                              ▼
                    qwen2.5-coder:1.5b
```

---

# 5. Engineering Principles

Day 1 establishes the engineering principles that will continue through the entire project.

## SOLID

### Single Responsibility

Each component has one primary responsibility.

Examples:

```text
ModelRegistry  → stores model routes
ModelRouter    → resolves model routes
FallbackPolicy → decides retry behavior
LiteLLMGateway → executes LLM requests
Authorization  → evaluates permissions
```

### Open/Closed Principle

New providers and implementations should be added through interfaces instead of modifying existing application logic.

### Liskov Substitution

Concrete implementations follow their abstract contracts.

### Interface Segregation

Separate contracts are used for different responsibilities.

### Dependency Inversion

Application code depends on abstractions rather than concrete providers.

---

# 6. Project Structure

Current Day 1 structure:

```text
company-ai-analyst/
│
├── src/
│   └── company_ai/
│       │
│       ├── app/
│       │
│       ├── config/
│       │   ├── settings.py
│       │   ├── paths.py
│       │   ├── security.py
│       │   └── logging.py
│       │
│       ├── core/
│       │   ├── exceptions.py
│       │   ├── request.py
│       │   └── context.py
│       │
│       ├── contracts/
│       │   ├── llm.py
│       │   ├── security.py
│       │   └── models.py
│       │
│       ├── models/
│       │   ├── llm.py
│       │   └── security.py
│       │
│       ├── llm/
│       │   ├── gateway.py
│       │   ├── litellm_gateway.py
│       │   ├── router.py
│       │   ├── model_registry.py
│       │   ├── fallback.py
│       │   └── guardrails.py
│       │
│       └── security/
│           └── authorization.py
│
├── configs/
│
├── data/
│
├── knowledge/
│
├── artifacts/
│
├── logs/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

# 7. Environment

The project uses:

```text
Python 3.12
uv
.global_env
```

Python requirement:

```text
>=3.12,<3.13
```

The project does not use a project-local `.venv`.

Activate the shared environment:

```bash
source ~/.global_env/bin/activate
```

Install the project:

```bash
uv pip install -e .
```

Verify:

```bash
python -c "import company_ai; print(company_ai.__file__)"
```

---

# 8. Request Identity

File:

```text
src/company_ai/core/request.py
```

The `RequestIdentity` object provides unique identifiers for each request.

```text
RequestIdentity
    │
    ├── request_id
    │
    └── trace_id
```

The object is immutable.

Example:

```python
identity = RequestIdentity.create()
```

This provides the foundation for future:

* Logging
* Debugging
* Observability
* Distributed tracing
* Workflow execution tracking

---

# 9. User Identity

File:

```text
src/company_ai/models/security.py
```

The current user identity contains:

```text
user_id
company_id
role
```

Conceptually:

```text
UserIdentity
    │
    ├── user_id
    ├── company_id
    └── role
```

`company_id` provides the foundation for future multi-tenant enterprise isolation.

---

# 10. Permission Context

The current permission model contains:

```text
allowed_tools
allowed_tables
allowed_columns
can_read
can_write
can_access_pii
```

Conceptually:

```text
PermissionContext
       │
       ├── Tool permissions
       ├── Table permissions
       ├── Column permissions
       ├── Read permission
       ├── Write permission
       └── PII permission
```

This will later become important when agents dynamically select tools and databases.

---

# 11. Request Context

File:

```text
src/company_ai/core/context.py
```

`RequestContext` combines:

```text
RequestIdentity
UserIdentity
PermissionContext
```

Architecture:

```text
                 RequestContext
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 RequestIdentity  UserIdentity  PermissionContext
```

It also exposes convenient properties:

```text
user_id
company_id
role
```

---

# 12. Authorization Architecture

File:

```text
src/company_ai/security/authorization.py
```

The project defines:

```text
AuthorizationPort
```

as the abstraction.

The default implementation is:

```text
DefaultAuthorizationService
```

Current authorization operations:

```text
can_use_tool()
can_access_table()
can_access_column()
can_write()
can_access_pii()
```

Architecture:

```text
Application
    │
    ▼
AuthorizationPort
    │
    ▼
DefaultAuthorizationService
    │
    ▼
PermissionContext
```

The application therefore does not need to know how authorization is implemented.

---

# 13. LLM Architecture

The LLM layer is provider-independent.

```text
Application
     │
     ▼
LLMGatewayPort
     │
     ▼
LiteLLMGateway
     │
     ▼
LiteLLM
     │
     ├── Ollama
     ├── OpenAI
     └── Future providers
```

The rest of the application communicates through:

```text
LLMGatewayPort
```

rather than directly calling LiteLLM or Ollama.

---

# 14. LLM Request Contract

File:

```text
src/company_ai/contracts/llm.py
```

The `LLMRequest` contains:

```text
purpose
messages
temperature
max_tokens
metadata
```

Messages contain:

```text
role
content
```

Example:

```python
LLMRequest(
    purpose="personal_assistant",
    messages=[
        Message(
            role="user",
            content="Analyze the sales data"
        )
    ],
    temperature=0.0,
)
```

The `purpose` field is important because future model routing will be based on logical task purpose rather than hardcoded model names.

---

# 15. LLM Response Contract

The provider response is normalized into:

```text
LLMResponse
```

Current fields:

```text
content
model
input_tokens
output_tokens
metadata
```

Architecture:

```text
Provider Response
       │
       ▼
LiteLLMGateway
       │
       ▼
LLMResponse
```

This keeps provider-specific response formats out of the application.

---

# 16. Model Route

File:

```text
src/company_ai/llm/model_registry.py
```

A `ModelRoute` describes how a logical model purpose should be handled.

Current fields:

```text
purpose
primary
fallbacks
max_retries
timeout_seconds
```

Example:

```python
ModelRoute(
    purpose="fast",
    primary="ollama/qwen2.5-coder:1.5b",
)
```

A logical purpose can therefore map to one or multiple models.

---

# 17. Model Registry

The `ModelRegistry` stores configured routes.

Architecture:

```text
ModelRegistry
      │
      ├── personal_assistant
      ├── planner
      ├── reasoning
      ├── fast
      └── analysis
```

The registry provides:

```text
get()
has()
all()
```

This prevents model configuration from being scattered throughout the application.

---

# 18. Model Router

File:

```text
src/company_ai/llm/router.py
```

The `ModelRouter` is responsible for resolving a logical purpose.

Example:

```python
router = ModelRouter(registry)

route = router.route("fast")
```

Architecture:

```text
"fast"
   │
   ▼
ModelRouter
   │
   ▼
ModelRegistry
   │
   ▼
ModelRoute
```

The router does **not** execute the model.

This separation is intentional:

```text
Router   → selects route
Gateway  → executes route
```

---

# 19. Retry Policy

File:

```text
src/company_ai/llm/fallback.py
```

The `FallbackPolicy` determines whether an error should be retried.

Current configuration supports:

```text
retryable_errors
max_attempts
```

Conceptual flow:

```text
LLM Request
     │
     ▼
Attempt
     │
 ┌───┴────┐
 │        │
Success  Error
 │        │
 ▼        ▼
Return   Retry?
           │
       ┌───┴────┐
       │        │
      Yes       No
       │        │
       ▼        ▼
    Retry     Raise
```

---

# 20. Model Fallback

The gateway supports multiple configured models.

Example:

```text
Primary
   │
   ├── success ──► response
   │
   └── failure
          │
          ▼
       fallback
          │
          ▼
       response
```

Example configuration:

```text
personal_assistant
    │
    ├── primary
    │     └── ollama/qwen2.5-coder:1.5b
    │
    └── fallback
          └── configured secondary model
```

Fallback behavior is intended for infrastructure/provider failures.

Security failures should not be bypassed by blindly switching models.

---

# 21. LiteLLM Gateway

File:

```text
src/company_ai/llm/litellm_gateway.py
```

`LiteLLMGateway` implements:

```text
LLMGatewayPort
```

Its responsibility is to:

1. Resolve the requested model route.
2. Determine the primary/fallback model sequence.
3. Execute the LLM request through LiteLLM.
4. Apply retry policy.
5. Move to fallback models when appropriate.
6. Normalize the provider response.
7. Return `LLMResponse`.

Architecture:

```text
LLMRequest
     │
     ▼
ModelRegistry
     │
     ▼
ModelRoute
     │
     ▼
Primary Model
     │
     ├── success ────────► LLMResponse
     │
     └── failure
            │
            ▼
        Retry Policy
            │
            ▼
        Fallback Model
            │
            ▼
        LLMResponse
```

---

# 22. Guardrail Abstraction

File:

```text
src/company_ai/llm/guardrails.py
```

Day 1 establishes the guardrail interface.

Current abstraction:

```text
GuardrailPort
```

Operations:

```text
validate_input()
validate_output()
```

Current development implementation:

```text
NoOpGuardrail
```

This is deliberately an abstraction at this stage.

Future production guardrails will be introduced later.

Target architecture:

```text
Input
  │
  ▼
Input Guardrail
  │
  ▼
LLM Gateway
  │
  ▼
Output Guardrail
  │
  ▼
Application
```

---

# 23. Ollama Integration

The local development model is:

```text
qwen2.5-coder:1.5b
```

Model identifier used by LiteLLM:

```text
ollama/qwen2.5-coder:1.5b
```

Verify Ollama:

```bash
ollama --version
```

List models:

```bash
ollama list
```

Run the model:

```bash
ollama run qwen2.5-coder:1.5b "Reply with exactly OLLAMA_OK"
```

The intended integration path is:

```text
Python
  │
  ▼
LiteLLMGateway
  │
  ▼
LiteLLM
  │
  ▼
Ollama
  │
  ▼
qwen2.5-coder:1.5b
```

---

# 24. Day 1 Testing Strategy

Testing is divided into:

```text
Unit Tests
     │
     ▼
Integration Tests
```

The development process is:

```text
Implement Block
      │
      ▼
Unit Test Block
      │
      ▼
Fix Block
      │
      ▼
Move to Next Block
      │
      ▼
Integration Test
```

This prevents infrastructure problems from being confused with application logic problems.

---

# 25. Unit Testing

Location:

```text
tests/unit/
```

Unit tests should be:

* Fast
* Deterministic
* Independent
* Free from external infrastructure

Unit tests mock external LLM behavior where appropriate.

They should not require Ollama.

---

# 26. Model Registry Test Cases

Expected test coverage:

### Test 1 — Return configured route

```text
Given a registered route
When get() is called
Then the correct ModelRoute is returned
```

### Test 2 — Unknown route

```text
Given an unregistered purpose
When get() is called
Then an appropriate error is raised
```

### Test 3 — Route existence

```text
has("fast") == True
has("unknown") == False
```

### Test 4 — Return all routes

Verify that `all()` returns the configured routes.

---

# 27. Model Router Test Cases

File:

```text
tests/unit/test_model_router.py
```

Current test:

```python
registry = ModelRegistry(
    [
        ModelRoute(
            purpose="fast",
            primary="ollama/qwen2.5-coder:1.5b",
        )
    ]
)

router = ModelRouter(registry)

route = router.route("fast")

assert route.primary == "ollama/qwen2.5-coder:1.5b"
```

Expected behavior:

```text
Purpose
   │
   ▼
ModelRouter
   │
   ▼
Correct ModelRoute
```

Additional behavior can verify:

```text
has_route()
unknown purpose
```

---

# 28. Fallback Test Cases

File:

```text
tests/unit/test_fallback.py
```

Important cases:

### Retryable error

Verify retry is allowed.

### Maximum attempts

Verify retry stops at the configured limit.

### Non-retryable error

Verify the error is not retried.

Conceptual test:

```text
Retryable error
      │
      ▼
should_retry()
      │
      ▼
True
```

versus:

```text
Non-retryable error
      │
      ▼
should_retry()
      │
      ▼
False
```

---

# 29. Authorization Test Cases

File:

```text
tests/unit/test_authorization.py
```

Important cases:

### Tool permission

```text
Allowed tool     → True
Unknown tool     → False
```

### Table permission

```text
Allowed table    → True
Unknown table    → False
```

### Column permission

```text
Allowed column   → True
Unknown column   → False
```

### Write permission

```text
can_write=True   → True
can_write=False  → False
```

### PII permission

```text
can_access_pii=True  → True
can_access_pii=False → False
```

---

# 30. LLM Gateway Test Cases

File:

```text
tests/unit/test_llm_gateway.py
```

The gateway test suite covers:

1. Successful completion
2. Request passed correctly to LiteLLM
3. Token usage mapping
4. Primary model failure followed by fallback
5. Retry of retryable errors
6. No retry for non-retryable errors
7. All models failing
8. Unknown model purpose
9. Empty LLM choices
10. `None` content handling
11. Multiple messages
12. Fallback order
13. Primary-only configuration

The tests mock LiteLLM.

Therefore:

```text
Unit Test
   │
   ▼
LiteLLMGateway
   │
   ▼
Mock LiteLLM
```

No real Ollama connection is required.

---

# 31. Ollama Integration Test

The Ollama integration test verifies the actual infrastructure.

Expected path:

```text
Test
 │
 ▼
LLMRequest
 │
 ▼
LiteLLMGateway
 │
 ▼
LiteLLM
 │
 ▼
Ollama
 │
 ▼
qwen2.5-coder:1.5b
 │
 ▼
LLMResponse
```

The test should verify:

```text
response.content is not empty
response.model is correct
```

A simple prompt can be:

```text
Reply with exactly OLLAMA_OK
```

---

# 32. Running Day 1 Tests

## Run all unit tests

```bash
pytest tests/unit -v
```

## Run model router test

```bash
pytest tests/unit/test_model_router.py -v
```

## Run gateway tests

```bash
pytest tests/unit/test_llm_gateway.py -v
```

## Run all integration tests

```bash
pytest tests/integration -v -m integration
```

## Run Ollama integration

```bash
pytest tests/integration/test_ollama_gateway.py -v -m integration
```

---

# 33. Test Layers

The complete Day 1 test structure is:

```text
tests/
│
├── unit/
│   │
│   ├── Model Registry
│   ├── Model Router
│   ├── Fallback
│   ├── Authorization
│   └── LLM Gateway
│
└── integration/
    │
    ├── LiteLLM → Ollama
    │
    └── Gateway → LiteLLM → Ollama
```

---

# 34. Day 1 Dependency Flow

```text
Python 3.12
     │
     ▼
uv / .global_env
     │
     ▼
company_ai package
     │
     ▼
Contracts
     │
     ▼
Services
     │
     ▼
LiteLLM
     │
     ▼
Ollama
     │
     ▼
qwen2.5-coder:1.5b
```

---

# 35. Day 1 Completion Checklist

## Project Foundation

* [x] Python 3.12
* [x] `uv` configuration
* [x] Shared `.global_env`
* [x] `src` package structure
* [x] Project paths
* [x] `pyproject.toml`
* [x] pytest configuration

## Enterprise Context

* [x] Request identity
* [x] Request ID
* [x] Trace ID
* [x] User identity
* [x] Company ID
* [x] Role
* [x] Permission context

## Authorization

* [x] Authorization interface
* [x] Default authorization service
* [x] Tool authorization
* [x] Table authorization
* [x] Column authorization
* [x] Write authorization
* [x] PII authorization

## LLM Layer

* [x] Message contract
* [x] LLM request contract
* [x] LLM response contract
* [x] LLM gateway interface
* [x] Model route
* [x] Model registry
* [x] Model router
* [x] Retry policy
* [x] Fallback architecture
* [x] LiteLLM gateway
* [x] Guardrail interface
* [x] Ollama integration foundation

## Testing

* [x] Unit test structure
* [x] Model registry tests
* [x] Model router tests
* [x] Fallback tests
* [x] Authorization tests
* [x] LLM gateway tests
* [x] Integration test structure
* [x] Ollama integration test

---

# 36. Day 1 Final Architecture

```text
                         DAY 1
                           │
                           ▼
                       Application
                           │
                           ▼
                    RequestContext
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
         Request          User       Permissions
         Identity       Identity       Context
            │              │              │
            └──────────────┼──────────────┘
                           │
                           ▼
                     Authorization
                           │
                           ▼
                    Model Registry
                           │
                           ▼
                     Model Router
                           │
                           ▼
                   LLMGatewayPort
                           │
                           ▼
                  LiteLLMGateway
                           │
                 ┌─────────┴─────────┐
                 │                   │
             Retry Policy        Fallback
                 │                   │
                 └─────────┬─────────┘
                           │
                           ▼
                        LiteLLM
                           │
                           ▼
                         Ollama
                           │
                           ▼
                 qwen2.5-coder:1.5b
```

---

# 37. Day 1 Outcome

At the end of Day 1, the project has a **provider-independent enterprise LLM foundation**.

The application can conceptually perform:

```text
Request
   ↓
Identify request/user/context
   ↓
Resolve permissions
   ↓
Resolve logical model purpose
   ↓
Select configured model
   ↓
Execute through LiteLLM
   ↓
Retry/fallback when applicable
   ↓
Return normalized LLMResponse
```

The most important architectural result is that future layers do not need to directly depend on Ollama.

Instead:

```text
Future Agent
     │
     ▼
LLMGatewayPort
     │
     ▼
LiteLLMGateway
     │
     ▼
ModelRouter
     │
     ▼
ModelRegistry
     │
     ▼
Configured Provider
```

This foundation is the dependency-inverted base for **Day 2 Personal Assistant**, followed by the Deep Agent and dynamic LangGraph workflow layers.
