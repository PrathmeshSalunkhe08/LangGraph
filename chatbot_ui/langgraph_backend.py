from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph ,START,END
from pydantic import BaseModel,Field
from typing import Literal,TypedDict,Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
# import operator


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7
)


#operator.add Badle add_messages built in langgraph
from  langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]



def Chat_node(state:ChatState):
    #take user query 
    messages=state['messages']

    #send to llm
    response=llm.invoke(messages)

    #response store in state
    return {"messages":[response]}



check_pointer=InMemorySaver()
graph=StateGraph(ChatState)

graph.add_node("Chat_node",Chat_node)

graph.add_edge(START,"Chat_node")
graph.add_edge("Chat_node",END)

workflow=graph.compile(checkpointer=check_pointer)
chatbot = workflow