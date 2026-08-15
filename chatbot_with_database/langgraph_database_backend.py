from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph ,START,END
from pydantic import BaseModel,Field
from typing import Literal,TypedDict,Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,BaseMessage
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver #just for prototyping and postgre for productionbased 
SQLiteSaver = SqliteSaver

import sqlite3

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


#why false ->To handle mutiple conversation in multithreading
#
conn=sqlite3.connect(database="chatbot.db",check_same_thread=False) 
check_pointer=SQLiteSaver(conn=conn)              
graph=StateGraph(ChatState)

graph.add_node("Chat_node",Chat_node)

graph.add_edge(START,"Chat_node")
graph.add_edge("Chat_node",END)

chatbot=graph.compile(checkpointer=check_pointer)



#step1-install langgraph-checkpoint-sqlite/
#test
response=chatbot.invoke(
                {'messages': [HumanMessage(content="Hii my name is Prathamesh")]},
                config={'configurable': {'thread_id': 'thread-1'}}
              
            )

print(response['messages'][-1].content)

#thread_id -> to save state for diffrent conversation
#checkpointer -> to save state in database
#stream_mode -> to get response in real time
