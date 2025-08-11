
from langgraph.graph import StateGraph, START, END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage, HumanMessage
# from langchain_openai import ChatOpenAI   # for open ai
from langchain_google_genai import ChatGoogleGenerativeAI   # for google gemin
from langgraph.checkpoint.memory import InMemorySaver  # it store in RAMloa
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("MY_API_KEY")


# llm = ChatOpenAI()   for open ai
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",google_api_key=API_KEY)


class ChatState(TypedDict):
  messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state: ChatState):
  # take user query from state
  messages = state['messages']

  # send to llm
  response = llm.invoke(messages)

  # response store state
  return {'messages':[response]}

# checkpoint for memory storage
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

#add nodes
graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)

