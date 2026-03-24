import os
from typing import TypedDict, Annotated,List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph , END
import operator

# 1. load the API Key

load_dotenv()
# 2. define the 'State'(the AI's Notepad)
class AgentState(TypedDict):
    #this stores the conversation history
    messages: Annotated[List[dict], operator.add]
    user_name:str
    current_intent:str

# 3. initialize the Model(Gemini 2.5 Flash)

llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')

# 4. build the first node: The 'chat agent'
def chat_node(state: AgentState):
    print("--AI IS THINKING--")
    messages = state['messages']

    #Ask the LLM for a response
    response = llm.invoke(messages)

    #Return the updated state
    return{"messages":[{"role": "assistant","content":response.content}]}

# 5. build the Graph (The nervous system)
workflow = StateGraph(AgentState)

#Add node to the graph
workflow.add_node("momi_chat",chat_node)

#Set the entry point and the exit
workflow.set_entry_point("momi_chat")
workflow.add_edge("momi_chat",END)

#Comple the graph
momi_app = workflow.compile()

# TEST
if __name__== "__main__":
    inputs = {"messages": [{"role": "user","content":"HI,I'm Kavindya.Who are you?"}]}
    for output in momi_app.stream(inputs):
        for key, value in output.items():
            print(f"Node '{key}': {value['messages'][-1]['content']}")




