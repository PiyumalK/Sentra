from dotenv import load_dotenv
from langchain_groq import ChatGroq
from agent.prompts import *
from agent.states import *
from langgraph.constants import END
from langgraph.graph import StateGraph

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b")

def planner_agent(state: dict) -> dict:
    user = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    return { "plan": resp }

graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.set_entry_point("planner")

agent = graph.compile()

user_prompt = "create a simple calculator web application"

result = agent.invoke({"user_prompt": user_prompt})
print(result)