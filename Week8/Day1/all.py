"""
================================================================================
  LangGraph Comprehensive Guide: Days 3-7
  Topics: Tool Calling, Agent Workflows, State & Memory, Streaming,
          Human-in-the-Loop, Parallelization, Subgraphs, FastAPI Integration
================================================================================

THEORETICAL OVERVIEW
====================

────────────────────────────────────────────────────────────────────────────────
DAY 3: AGENTS AND TOOLS
────────────────────────────────────────────────────────────────────────────────

TOOL CALLING
─────────────
In LangGraph, a "tool" is any Python callable decorated with @tool (from
langchain_core.tools) or defined as a StructuredTool. Tools represent discrete
actions an agent can take: searching the web, querying a database, calling an
API, doing arithmetic, etc.

When a LLM is bound to tools (via llm.bind_tools(tools)), the model can emit a
special "tool_call" message instead of plain text. This message contains:
  - tool name (which function to call)
  - tool arguments (a JSON-compatible dict of inputs)

LangGraph captures this via a ToolNode — a pre-built node that:
  1. Reads the AIMessage.tool_calls list
  2. Looks up the matching tool function
  3. Executes it with the provided arguments
  4. Returns a ToolMessage with the result back to the graph

AGENT WORKFLOWS
────────────────
An agent in LangGraph is a graph with a cyclical structure:
  1. LLM node  →  decides what to do (answer or call a tool)
  2. Tool node →  executes the chosen tool
  3. Back to LLM node with tool result
  4. Repeat until LLM decides to produce a final answer (no more tool calls)

The routing logic (should_continue function) inspects the last message:
  - If it has tool_calls → route to tools node
  - Otherwise → route to END

This creates the classic ReAct (Reason + Act) loop pattern.

STRUCTURED EXECUTION
─────────────────────
LangGraph enforces structured execution via:
  - Typed state (TypedDict / Pydantic) — only valid state shapes flow through
  - Conditional edges — routing logic is explicit and inspectable
  - Node contracts — each node receives State, returns a dict of updates
  - The graph is compiled before running, catching wiring errors early

────────────────────────────────────────────────────────────────────────────────
DAY 4: STATE AND MEMORY
────────────────────────────────────────────────────────────────────────────────

STATE SCHEMAS
──────────────
State is the single source of truth passed between all nodes. Defined as a
TypedDict (or Pydantic BaseModel), every key is a field the graph can read or
write. Nodes return partial dicts — only keys they want to update.

Example schema:
  class AgentState(TypedDict):
      messages: Annotated[list, add_messages]  # special reducer
      user_name: str
      tool_results: list

REDUCERS
─────────
A reducer defines HOW a field is updated when multiple nodes write to it.
Without a reducer, each write overwrites the previous value.

The most important reducer is `add_messages` (from langgraph.graph):
  - It APPENDS new messages rather than replacing the list
  - It deduplicates by message ID (idempotent replays)
  - It handles AIMessage → ToolMessage threading

You can write custom reducers:
  def keep_latest(existing, new): return new        # default behavior
  def append_all(existing, new): return existing + new

Annotated[list[str], append_all] tells LangGraph to use append_all as the
reducer for that field.

MESSAGE HISTORY
────────────────
LangGraph tracks conversation via the `messages` field in state. Each round trip
adds:
  HumanMessage  → user input
  AIMessage     → LLM response (may contain tool_calls)
  ToolMessage   → result from executing a tool
  SystemMessage → injected context/instructions

The full history travels with every node invocation, giving LLMs full context.

MEMORY MANAGEMENT
──────────────────
For long-running conversations, unlimited history grows expensive. Strategies:
  1. Trim messages:  trim_messages(state["messages"], max_tokens=2000)
  2. Summarize:      periodically collapse old messages into a SystemMessage summary
  3. Checkpointing:  LangGraph's MemorySaver / SqliteSaver persists state across
                     invocations — the thread_id acts as a session key
  4. Store:          LangGraph's BaseStore API provides cross-thread, persistent
                     key-value memory (user profiles, long-term facts)

CONTEXT HANDLING
─────────────────
Context is managed by what you put in state and what you inject into system
prompts. Common patterns:
  - Inject retrieved documents into state, then reference in the prompt
  - Store user preferences in a separate memory store, load at graph start
  - Use RunnableConfig to pass runtime config (user_id, thread_id) through nodes

────────────────────────────────────────────────────────────────────────────────
DAY 5: STREAMING AND HUMAN APPROVAL
────────────────────────────────────────────────────────────────────────────────

STREAMING RESPONSES
────────────────────
LangGraph supports multiple streaming modes:
  1. "values"  — emits the full state after each node completes
  2. "updates" — emits only the delta (what each node changed)
  3. "messages" — streams LLM tokens as they generate (for real-time UI)

Usage:
  async for chunk in graph.astream(input, config, stream_mode="messages"):
      if chunk[1]["langgraph_node"] == "agent":
          print(chunk[0].content, end="", flush=True)

INTERRUPTS
───────────
An interrupt pauses graph execution BEFORE a node runs, returning control to the
caller. Defined via:
  graph = builder.compile(interrupt_before=["dangerous_tool_node"])

When interrupted, the graph's state is saved to the checkpointer. You can:
  - Inspect the pending state
  - Modify state (inject human feedback)
  - Resume with graph.invoke(None, config)  ← None means "continue"
  - Or abort the run entirely

HUMAN-IN-THE-LOOP WORKFLOWS
─────────────────────────────
The standard HitL pattern:
  1. Agent decides to call a sensitive tool
  2. Graph pauses (interrupt_before=["tools"])
  3. System shows the pending tool call to a human
  4. Human approves → resume | Human rejects → inject rejection message + resume
  5. Graph continues from saved checkpoint

This requires a checkpointer (MemorySaver minimum) to persist paused state.

WORKFLOW CHECKPOINTS
─────────────────────
Checkpoints are snapshots of the full graph state stored at every superstep.
They enable:
  - Resumability  — continue interrupted/failed runs
  - Time-travel   — roll back to any previous state with graph.update_state()
  - Auditability  — full execution history via graph.get_state_history()
  - Forking       — branch from a past checkpoint to explore alternatives

Checkpoint backends: MemorySaver (in-process), SqliteSaver, PostgresSaver

────────────────────────────────────────────────────────────────────────────────
DAY 6: PARALLELIZATION AND SUBGRAPHS
────────────────────────────────────────────────────────────────────────────────

PARALLEL EXECUTION
───────────────────
LangGraph executes nodes in the same "superstep" in PARALLEL if they share no
data dependency. You create parallel branches by adding edges from one node to
multiple nodes simultaneously:
  builder.add_edge("router", "branch_a")
  builder.add_edge("router", "branch_b")

Both branch_a and branch_b run concurrently. Results merge at the next node
that both connect to.

SUBGRAPHS
──────────
A subgraph is a compiled LangGraph graph used as a NODE in a parent graph.
This enables:
  - Encapsulation — hide implementation details
  - Reuse — same subgraph used in multiple parent graphs
  - Modularity — teams own separate subgraphs
  - Recursion-like nesting (agents spawning sub-agents)

The parent and subgraph can share state keys (overlapping TypedDict fields),
or communicate through explicit input/output mapping.

FAN-OUT / FAN-IN PATTERNS
──────────────────────────
Fan-out: one node dispatches work to N parallel nodes
Fan-in:  a downstream node collects and merges results from all N nodes

The fan-in node only runs after ALL fan-out branches complete (LangGraph
waits for all parallel branches to finish before advancing).

MAP-REDUCE CONCEPTS
────────────────────
Map: apply the same operation to each item in a collection in parallel
Reduce: aggregate all results into a single output

In LangGraph, Send() API implements map-reduce:
  from langgraph.types import Send

  def map_node(state):
      return [Send("process_item", {"item": i}) for i in state["items"]]
      # ↑ spawns one parallel execution per item, each routed to process_item

Results accumulate back via a reducer on the collecting field.

────────────────────────────────────────────────────────────────────────────────
DAY 7: FASTAPI INTEGRATION
────────────────────────────────────────────────────────────────────────────────

FASTAPI BASICS
───────────────
FastAPI is an ASGI web framework for Python. Key concepts:
  - Routes defined with @app.get / @app.post decorators
  - Pydantic models for request/response validation
  - async def handlers for non-blocking I/O
  - Depends() for dependency injection (DB sessions, auth, etc.)
  - StreamingResponse for server-sent events (SSE)

LANGGRAPH INTEGRATION
──────────────────────
LangGraph graphs are compiled once at startup (expensive operation) and reused
across requests. Each request gets its own:
  - thread_id  → isolates that user's state in the checkpointer
  - RunnableConfig → passes thread_id + runtime config into graph nodes

STREAMING WITH FASTAPI + LANGGRAPH
────────────────────────────────────
For real-time token streaming:
  1. Define an async generator that streams from graph.astream_events()
  2. Wrap in FastAPI's StreamingResponse with media_type="text/event-stream"
  3. Client reads SSE stream and appends tokens to UI

REQUEST/RESPONSE HANDLING
──────────────────────────
  Request  → Pydantic model validates incoming JSON → extract message + thread_id
  Response → Either await graph.ainvoke() for full response, or
             StreamingResponse for token-by-token streaming

API DEPLOYMENT BASICS
──────────────────────
  - Use uvicorn to serve the ASGI app
  - Store compiled graph as a module-level singleton
  - MemorySaver is fine for development; use SqliteSaver/PostgresSaver in prod
  - Add CORS middleware for browser clients
  - Rate-limit endpoints in production
  - Use lifespan context manager for startup/shutdown resource management

================================================================================
"""

# ============================================================
#  IMPORTS
# ============================================================
import asyncio
import operator
from typing import Annotated, Any, TypedDict
from contextlib import asynccontextmanager

# LangChain / LangGraph core
from langchain_core.messages import (
    HumanMessage, AIMessage, SystemMessage, ToolMessage
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send

# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json


# ============================================================
#  SHARED LLM INSTANCE  (swap model as needed)
# ============================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ╔══════════════════════════════════════════════════════════╗
# ║  DAY 3 — TOOL CALLING & AGENT WORKFLOWS                  ║
# ╚══════════════════════════════════════════════════════════╝

# ── Tool definitions ─────────────────────────────────────────

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@tool
def web_search(query: str) -> str:
    """Simulate a web search (returns a canned result for demo)."""
    # In production: call SerpAPI, Tavily, etc.
    return f"[Search results for '{query}']: LangGraph is a graph-based framework for building stateful LLM agents."


# ── Agent State (Day 3 uses simple messages-only state) ──────

class BasicAgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ── Agent graph builder ───────────────────────────────────────

def build_basic_agent() -> StateGraph:
    tools = [add, multiply, web_search]
    llm_with_tools = llm.bind_tools(tools)

    # Node 1 — LLM decides what to do
    def agent_node(state: BasicAgentState) -> dict:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    # Node 2 — Execute whatever tool the LLM chose
    tool_node = ToolNode(tools)

    builder = StateGraph(BasicAgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")

    # Conditional edge: if the last AIMessage has tool_calls → tools, else END
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")   # loop back after tool execution

    return builder.compile()


basic_agent = build_basic_agent()


def demo_day3():
    """Run the basic tool-calling agent."""
    print("\n" + "═"*60)
    print("  DAY 3 DEMO — Tool Calling Agent")
    print("═"*60)

    result = basic_agent.invoke({
        "messages": [HumanMessage(content="What is (3 + 7) * 12?")]
    })

    for msg in result["messages"]:
        role = msg.__class__.__name__
        content = msg.content or str(getattr(msg, "tool_calls", ""))
        print(f"[{role}] {content}")


# ╔══════════════════════════════════════════════════════════╗
# ║  DAY 4 — STATE SCHEMAS, REDUCERS, MEMORY                 ║
# ╚══════════════════════════════════════════════════════════╝

# ── Rich State Schema with custom fields and reducers ────────

def append_reducer(existing: list, new: list) -> list:
    """Custom reducer: always appends new items."""
    return existing + new


class RichAgentState(TypedDict):
    # messages uses the built-in add_messages reducer (append + deduplicate)
    messages:     Annotated[list, add_messages]
    # collected tool outputs — appended, never overwritten
    tool_outputs: Annotated[list[str], append_reducer]
    # simple scalar — last write wins (no reducer)
    user_name:    str
    # turn counter — use operator.add as reducer to increment
    turn_count:   Annotated[int, operator.add]


tools = [add, multiply, web_search]
llm_with_tools = llm.bind_tools(tools)


def rich_agent_node(state: RichAgentState) -> dict:
    system = SystemMessage(
        content=f"You are a helpful assistant. The user's name is {state.get('user_name', 'unknown')}."
    )
    # Trim to last 10 messages to avoid unbounded growth (memory management)
    recent_messages = state["messages"][-10:]
    response = llm_with_tools.invoke([system] + recent_messages)
    return {
        "messages": [response],
        "turn_count": 1,          # reducer adds 1 each turn
    }


def rich_tool_node(state: RichAgentState) -> dict:
    # Execute tools and also record results in tool_outputs
    last_msg = state["messages"][-1]
    results = []
    tool_map = {t.name: t for t in tools}

    for tc in getattr(last_msg, "tool_calls", []):
        fn = tool_map.get(tc["name"])
        if fn:
            output = fn.invoke(tc["args"])
            results.append(ToolMessage(content=str(output), tool_call_id=tc["id"]))

    return {
        "messages": results,
        "tool_outputs": [r.content for r in results],  # also record in custom field
    }


def build_memory_agent() -> StateGraph:
    builder = StateGraph(RichAgentState)
    builder.add_node("agent", rich_agent_node)
    builder.add_node("tools", rich_tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    # MemorySaver checkpointer — persists state keyed by thread_id
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


memory_agent = build_memory_agent()


def demo_day4():
    """Show multi-turn memory with state schema and reducers."""
    print("\n" + "═"*60)
    print("  DAY 4 DEMO — State, Reducers, Memory")
    print("═"*60)

    config = {"configurable": {"thread_id": "user-alice-session-1"}}
    init_state = {"user_name": "Alice", "tool_outputs": [], "turn_count": 0}

    # Turn 1
    r1 = memory_agent.invoke(
        {**init_state, "messages": [HumanMessage(content="Hi! Add 5 and 3.")]},
        config=config
    )
    print(f"Turn 1 — turns so far: {r1['turn_count']}")
    print(f"Last message: {r1['messages'][-1].content}")

    # Turn 2 — same thread_id, state is resumed from checkpoint
    r2 = memory_agent.invoke(
        {"messages": [HumanMessage(content="Now multiply that result by 4.")]},
        config=config
    )
    print(f"Turn 2 — turns so far: {r2['turn_count']}")
    print(f"Last message: {r2['messages'][-1].content}")
    print(f"All tool outputs this session: {r2['tool_outputs']}")


# ╔══════════════════════════════════════════════════════════╗
# ║  DAY 5 — STREAMING AND HUMAN-IN-THE-LOOP                 ║
# ╚══════════════════════════════════════════════════════════╝

# ── Sensitive tool that requires human approval ───────────────

@tool
def delete_file(filename: str) -> str:
    """Delete a file from the filesystem. DANGEROUS — requires approval."""
    # In reality: os.remove(filename)
    return f"File '{filename}' deleted successfully."


def build_hitl_agent() -> StateGraph:
    """Agent that pauses before executing any tool — human approves/rejects."""
    all_tools = [add, multiply, delete_file]
    llm_bound = llm.bind_tools(all_tools)

    class HitLState(TypedDict):
        messages: Annotated[list, add_messages]

    def agent_node(state: HitLState):
        response = llm_bound.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(HitLState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(all_tools))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    memory = MemorySaver()
    # ↓ Graph pauses BEFORE "tools" node — gives human a chance to review
    return builder.compile(checkpointer=memory, interrupt_before=["tools"])


hitl_agent = build_hitl_agent()


def demo_day5_hitl():
    """Demonstrate interrupt → human review → resume workflow."""
    print("\n" + "═"*60)
    print("  DAY 5 DEMO — Human-in-the-Loop + Streaming")
    print("═"*60)

    config = {"configurable": {"thread_id": "hitl-session-1"}}

    # Step 1: Agent runs, hits interrupt before tools node
    hitl_agent.invoke(
        {"messages": [HumanMessage(content="Please delete the file 'old_backup.txt'")]},
        config=config
    )

    # Step 2: Inspect what the agent wants to do
    snapshot = hitl_agent.get_state(config)
    last_msg = snapshot.values["messages"][-1]
    print(f"\nAgent wants to call: {last_msg.tool_calls}")
    print("Graph is paused. Awaiting human approval...")

    # Step 3a: Human APPROVES → resume with None (continue as-is)
    human_decision = input("\nApprove? (y/n): ").strip().lower()

    if human_decision == "y":
        print("Resuming graph...")
        final = hitl_agent.invoke(None, config=config)  # None = "continue"
        print(f"Result: {final['messages'][-1].content}")
    else:
        # Step 3b: Human REJECTS → inject a rejection message + resume
        print("Injecting rejection...")
        hitl_agent.update_state(
            config,
            {"messages": [HumanMessage(content="No, don't delete that file.")]},
            as_node="agent"
        )
        final = hitl_agent.invoke(None, config=config)
        print(f"Result: {final['messages'][-1].content}")


async def demo_day5_streaming():
    """Demonstrate token-level streaming from a LangGraph agent."""
    print("\n" + "═"*60)
    print("  DAY 5 DEMO — Token Streaming")
    print("═"*60)

    graph = build_basic_agent()
    print("Streaming response: ", end="", flush=True)

    async for event in graph.astream_events(
        {"messages": [HumanMessage(content="What is LangGraph? Answer briefly.")]},
        version="v2"
    ):
        kind = event["event"]
        # Stream token chunks from the LLM as they arrive
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                print(chunk.content, end="", flush=True)

    print("\n[Stream complete]")


# ╔══════════════════════════════════════════════════════════╗
# ║  DAY 6 — PARALLELIZATION, SUBGRAPHS, MAP-REDUCE          ║
# ╚══════════════════════════════════════════════════════════╝

# ── Parallel Fan-Out / Fan-In ─────────────────────────────────

class ParallelState(TypedDict):
    query:          str
    search_result:  str
    calc_result:    str
    final_answer:   str


def parallel_search_node(state: ParallelState) -> dict:
    """Simulate a search branch."""
    return {"search_result": f"[Search result for: {state['query']}]"}


def parallel_calc_node(state: ParallelState) -> dict:
    """Simulate a calculation branch."""
    return {"calc_result": f"[Calculation result for: {state['query']}]"}


def fan_in_node(state: ParallelState) -> dict:
    """Merge results from both parallel branches."""
    combined = f"Search: {state['search_result']} | Calc: {state['calc_result']}"
    response = llm.invoke([HumanMessage(content=f"Synthesize: {combined}")])
    return {"final_answer": response.content}


def build_parallel_graph() -> StateGraph:
    builder = StateGraph(ParallelState)
    builder.add_node("search",   parallel_search_node)
    builder.add_node("calc",     parallel_calc_node)
    builder.add_node("merge",    fan_in_node)

    # Fan-out: START → search AND calc simultaneously
    builder.add_edge(START, "search")
    builder.add_edge(START, "calc")

    # Fan-in: both branches must complete before merge runs
    builder.add_edge("search", "merge")
    builder.add_edge("calc",   "merge")
    builder.add_edge("merge",  END)

    return builder.compile()


# ── Subgraph ──────────────────────────────────────────────────

class SubgraphState(TypedDict):
    messages: Annotated[list, add_messages]
    summary:  str


def summarizer_node(state: SubgraphState) -> dict:
    """Internal node: summarises message history."""
    history_text = "\n".join(
        f"{m.__class__.__name__}: {m.content}" for m in state["messages"]
    )
    response = llm.invoke([
        HumanMessage(content=f"Summarise this conversation in one sentence:\n{history_text}")
    ])
    return {"summary": response.content}


def build_summarizer_subgraph() -> StateGraph:
    """A reusable subgraph that summarises any conversation."""
    builder = StateGraph(SubgraphState)
    builder.add_node("summarize", summarizer_node)
    builder.add_edge(START, "summarize")
    builder.add_edge("summarize", END)
    return builder.compile()


summarizer_subgraph = build_summarizer_subgraph()


# Parent graph that USES the subgraph as a node
class ParentState(TypedDict):
    messages: Annotated[list, add_messages]
    summary:  str
    response: str


def main_agent_node(state: ParentState) -> dict:
    """Main agent: answers using the pre-computed summary."""
    system = SystemMessage(content=f"Context summary: {state.get('summary', 'none')}")
    response = llm.invoke([system] + state["messages"])
    return {"response": response.content}


def build_parent_graph() -> StateGraph:
    builder = StateGraph(ParentState)
    # The subgraph is used as a regular node — it sees the same state fields it knows
    builder.add_node("summarize", summarizer_subgraph)
    builder.add_node("agent",     main_agent_node)
    builder.add_edge(START,       "summarize")
    builder.add_edge("summarize", "agent")
    builder.add_edge("agent",     END)
    return builder.compile()


# ── Map-Reduce with Send() ────────────────────────────────────

class MapReduceState(TypedDict):
    items:   list[str]
    results: Annotated[list[str], operator.add]  # reducer accumulates results


class ItemState(TypedDict):
    item: str


def map_dispatcher(state: MapReduceState):
    """Fan-out: dispatch one process_item execution per item in parallel."""
    return [Send("process_item", {"item": item}) for item in state["items"]]


def process_item_node(state: ItemState) -> dict:
    """Worker: process a single item."""
    result = f"Processed: {state['item'].upper()}"
    return {"results": [result]}    # list so reducer appends it


def reduce_node(state: MapReduceState) -> dict:
    """Fan-in: all results are already aggregated by the reducer."""
    print(f"All results collected: {state['results']}")
    return {}


def build_map_reduce_graph() -> StateGraph:
    builder = StateGraph(MapReduceState)
    builder.add_node("process_item", process_item_node)
    builder.add_node("reduce",       reduce_node)

    # Send() in a conditional edge creates the dynamic fan-out
    builder.add_conditional_edges(START, map_dispatcher, ["process_item"])
    builder.add_edge("process_item", "reduce")
    builder.add_edge("reduce",       END)
    return builder.compile()


def demo_day6():
    print("\n" + "═"*60)
    print("  DAY 6 DEMO — Parallel Execution + Map-Reduce")
    print("═"*60)

    # Parallel fan-out/fan-in
    parallel_graph = build_parallel_graph()
    result = parallel_graph.invoke({"query": "LangGraph architecture"})
    print(f"Parallel merge result: {result['final_answer'][:100]}...")

    # Map-Reduce
    mr_graph = build_map_reduce_graph()
    mr_result = mr_graph.invoke({"items": ["alpha", "beta", "gamma", "delta"], "results": []})
    print(f"Map-Reduce results: {mr_result['results']}")


# ╔══════════════════════════════════════════════════════════╗
# ║  DAY 7 — FASTAPI INTEGRATION                             ║
# ╚══════════════════════════════════════════════════════════╝

# ── Pydantic request/response models ─────────────────────────

class ChatRequest(BaseModel):
    message:   str
    thread_id: str = "default"
    user_name: str = "User"


class ChatResponse(BaseModel):
    reply:       str
    thread_id:   str
    turn_count:  int


# ── Lifespan: compile graphs once at startup ──────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown resource management."""
    # Compile once — expensive; reused for all requests
    app.state.agent        = memory_agent
    app.state.hitl_agent   = hitl_agent
    print("[startup] LangGraph agents compiled and ready.")
    yield
    print("[shutdown] Cleaning up resources.")


# ── FastAPI app ───────────────────────────────────────────────

app = FastAPI(
    title="LangGraph Agent API",
    description="Days 3-7: full agent stack exposed over HTTP",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoint 1: standard (non-streaming) chat ────────────────

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Send a message and get the full response once generation completes.
    thread_id scopes memory to this session.
    """
    config = {"configurable": {"thread_id": req.thread_id}}
    agent  = app.state.agent

    try:
        result = await agent.ainvoke(
            {
                "messages":     [HumanMessage(content=req.message)],
                "user_name":    req.user_name,
                "tool_outputs": [],
                "turn_count":   0,
            },
            config=config,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    last_msg = result["messages"][-1]
    return ChatResponse(
        reply=last_msg.content,
        thread_id=req.thread_id,
        turn_count=result.get("turn_count", 0),
    )


# ── Endpoint 2: streaming chat (SSE) ─────────────────────────

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Stream tokens in real-time using Server-Sent Events.
    Frontend can display tokens as they arrive.
    """
    config = {"configurable": {"thread_id": req.thread_id + "-stream"}}
    agent  = app.state.agent

    async def token_generator():
        try:
            async for event in agent.astream_events(
                {
                    "messages":     [HumanMessage(content=req.message)],
                    "user_name":    req.user_name,
                    "tool_outputs": [],
                    "turn_count":   0,
                },
                config=config,
                version="v2",
            ):
                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]
                    if chunk.content:
                        # SSE format: data: <payload>\n\n
                        payload = json.dumps({"token": chunk.content})
                        yield f"data: {payload}\n\n"

            # Signal completion
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Endpoint 3: Human-in-the-Loop — initiate run ─────────────

@app.post("/hitl/run")
async def hitl_run(req: ChatRequest):
    """
    Start a HITL run. Returns immediately after the first interrupt,
    with the pending tool call for the human to inspect.
    """
    config  = {"configurable": {"thread_id": req.thread_id}}
    agent   = app.state.hitl_agent

    await agent.ainvoke(
        {"messages": [HumanMessage(content=req.message)]},
        config=config,
    )

    snapshot = agent.get_state(config)
    last_msg = snapshot.values["messages"][-1]
    pending  = getattr(last_msg, "tool_calls", [])

    return {
        "status":       "interrupted",
        "thread_id":    req.thread_id,
        "pending_tools": pending,
        "message":      "Human review required. POST /hitl/approve or /hitl/reject.",
    }


# ── Endpoint 4: Human-in-the-Loop — approve / reject ─────────

class HitLDecision(BaseModel):
    thread_id: str
    approve:   bool


@app.post("/hitl/decide")
async def hitl_decide(decision: HitLDecision):
    """
    Resume a paused HITL graph.
    approve=true  → continue as-is
    approve=false → inject rejection and continue
    """
    config = {"configurable": {"thread_id": decision.thread_id}}
    agent  = app.state.hitl_agent

    if not decision.approve:
        agent.update_state(
            config,
            {"messages": [HumanMessage(content="Cancelled by user — do not proceed with that action.")]},
            as_node="agent",
        )

    result = await agent.ainvoke(None, config=config)
    return {
        "status":   "completed",
        "response": result["messages"][-1].content,
    }


# ── Endpoint 5: Map-Reduce batch job ─────────────────────────

class BatchRequest(BaseModel):
    items: list[str]


@app.post("/batch/process")
async def batch_process(req: BatchRequest):
    """
    Run a parallel Map-Reduce job over a list of items.
    Items are processed concurrently via LangGraph's Send() API.
    """
    mr_graph = build_map_reduce_graph()
    result   = await mr_graph.ainvoke({"items": req.items, "results": []})
    return {"results": result["results"]}


# ── Endpoint 6: health check ──────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "agents_loaded": True}


# ============================================================
#  ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "demo"

    if mode == "api":
        # Run FastAPI server
        print("Starting FastAPI server on http://0.0.0.0:8000")
        print("Docs at http://0.0.0.0:8000/docs")
        uvicorn.run("langgraph_days3to7:app", host="0.0.0.0", port=8000, reload=True)

    else:
        # Run demo functions for Days 3, 4, 6
        demo_day3()
        demo_day4()
        demo_day6()

        # Day 5 streaming demo (async)
        asyncio.run(demo_day5_streaming())

        print("\n" + "═"*60)
        print("  Run `python langgraph_days3to7.py api` to start FastAPI server")
        print("═"*60)