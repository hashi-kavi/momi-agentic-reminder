from typing import TypedDict,List,Annotated
import operator

# this is AI's 'memory notepad'
class AgentState(TypedDict):
    #'messages' will store the whole chat history
    # Annotated with operator.add means "append new messages to the list"
    messages: Annotated[List[str],operator.add]
    user_name:str
    current_intent:str