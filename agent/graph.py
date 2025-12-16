from dotenv import load_dotenv
from langchain_core.globals import set_verbose, set_debug
from langchain_groq import ChatGroq
from agent.prompts import *
from agent.states import *
from langgraph.constants import END
from langgraph.graph import StateGraph

load_dotenv()

set_debug(True)
set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b")

def planner_agent(state: dict) -> dict:
    user = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return { "plan": resp }

def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if resp is None:
        raise ValueError("Architect did not return a valid response.")
    resp.plan = plan
    return { "task_plan": resp }

graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_edge("planner", "architect")

graph.set_entry_point("planner")

agent = graph.compile()

if __name__ == "__main__":
    user_prompt = "create a simple calculator web application"

    result = agent.invoke({"user_prompt": user_prompt})
    print(result)