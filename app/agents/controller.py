import os
import operator
from typing import TypedDict, Annotated,List
from dotenv import load_dotenv

# langchain & langraph imports 
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph , END
from app.agents.memory_agent import store_user_fact
from app.agents.memory_agent import MemoryManager

# 1. load the API Key

load_dotenv()
# 2. define the 'State'(the AI's Notepad)
class AgentState(TypedDict):
    #this stores the conversation history
    messages: Annotated[List[dict], operator.add]
    

# 3. initialize the Model(Gemini 2.5 Flash)

llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')
tools = [store_user_fact]
llm_with_tools = llm.bind_tools(tools)

# 4. build the first node: The 'chat agent'
def call_model(state: AgentState):
    print("--AI IS THINKING--")
    messages = state['messages']
    # 1. fetch memories from the database
    memory_manager = MemoryManager()
    past_memories = memory_manager.get_memories_string()

    # 2. create a "System Message" to give the AI context
    system_message = {
        "role": "system",
        "content": f"You are MOMI, a helpful AI assistant."
        f"Here is what you remember about the user:\n{past_memories}"
    }

    # 3 . put the system message at the VERY START of the conversation
    # we don't save this to the state,we just 'inject' it into this specific call
    full_message = [system_message] + messages

    #Ask the LLM for a response
    response = llm_with_tools.invoke(full_message)

    #Return the updated state
    return{"messages":[response]}

def handle_tools(state:AgentState):
    last_message = state['messages'][-1]

    #check if the AI wants to use a tool
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        print(f"--MOMI IS SAVING A FACT--")
        tool_call = last_message.tool_calls[0]

        #execute the tool
        result = store_user_fact.invoke(tool_call['args'])

        #return a 'system' message so the AI knows the save was successful
        return {"messages":[{"role":"system","content":f"Memory stored:{result}"}]}
    return {"messages":[]}#No tool called

# 5. Conditional Logic: Should we continue or stop?
def should_continue(state:AgentState):
    last_message = state['messages'][-1]
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

# 6. Build the Nervous System(The Graph)
workflow = StateGraph(AgentState)

workflow.add_node("agent",call_model)
workflow.add_node("tool_executor",handle_tools)

#Set the entry point and the exit
workflow.set_entry_point("agent")

#Logic:Agent->(Tool?)->If Tool,go to executor then back to Agent.Else,End.
workflow.add_conditional_edges("agent",should_continue,{"continue":"tool_executor","end":END})

workflow.add_edge("tool_executor","agent")


#Comple the graph
momi_app = workflow.compile()

# TEST
if __name__== "__main__":
    print("MOMI Agent is running..")
    user_input = "Do you remember my name and what I do?"
    inputs = {"messages": [{"role": "user","content":user_input}]}
    for output in momi_app.stream(inputs):
        for key, value in output.items():
            if "messages" in value and value["messages"]:
                last_msg = value["messages"][-1]
                #only print if it's a text response(assistant role)
                if hasattr(last_msg,'content'):
                    if isinstance(last_msg.content,list):
                        #extract text from structured response
                        text_parts = [item["text"] for item in last_msg.content if item["type"]=="text"]
                        print(f"\n[{key}]:{' '.join(text_parts)}")
                    else:
                        printf(f"\n[{key}]:{last_msg.content}")
                    
                    print(f"\n[{key}]:{last_msg.content}")
           




