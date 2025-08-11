import streamlit as st
import time
import markdown
from langGraph import chatbot
from langchain_core.messages import HumanMessage
import uuid




def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread_id(st.session_state['thread_id'])
    st.session_state['memory_history'] = []

def add_thread_id(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    state_val = state.values
    messages = state_val.get('messages', [])
    return messages


# Page configuration
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="wide")


# Session state for memory
if "memory_history" not in st.session_state:
    st.session_state.memory_history = []

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread_id(st.session_state['thread_id'])


CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

st.sidebar.title("LangGraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")
for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            else:   
                role = "assistant"
            temp_messages.append({"role": role, "content": message.content})
        st.session_state.memory_history = temp_messages

# Chat bubble styles
st.markdown("""
    <style>
    .user-bubble {
        background-color: #DCF8C6;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 4px 0;
        max-width: 70%;
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    .assistant-bubble {
        background-color: #F1F0F0;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 4px 0;
        max-width: 70%;
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 5px 10px;
        margin-top: 0;
    }
    #end-of-chat { height: 1px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("### 🤖 Chatbot Using LangGraph")

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.memory_history:
    rendered_content = markdown.markdown(message["content"])
    bubble_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
    st.markdown(f'<div class="{bubble_class}">{rendered_content}</div>', unsafe_allow_html=True)

st.markdown('<div id="end-of-chat"></div>', unsafe_allow_html=True)
st.markdown(
    "<script>document.getElementById('end-of-chat').scrollIntoView({behavior: 'smooth'});</script>",
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Input box
user_input = st.chat_input("Type your message here...")

if user_input:
    # 1️⃣ Show user message immediately
    st.session_state.memory_history.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-bubble">{markdown.markdown(user_input)}</div>', unsafe_allow_html=True)

    # 2️⃣ Get AI response with typing effect
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_response = response['messages'][-1].content

    typing_placeholder = st.empty()
    typing_text = ""
    for char in ai_response:
        typing_text += char
        rendered_typing = markdown.markdown(typing_text)
        typing_placeholder.markdown(f'<div class="assistant-bubble">{rendered_typing}</div>', unsafe_allow_html=True)
        time.sleep(0.02)



   # this code for straming response

    # ai_response = st.write_stream(
    #         message_chunk.content for message_chunk, metadata in chatbot.stream(
    #             {'messages': [HumanMessage(content=user_input)]},
    #             config= {'configurable': {'thread_id': 'thread-1'}},
    #             stream_mode= 'messages'
    #         )
    #     )
    # typing_placeholder = st.empty()
    # rendered_typing = markdown.markdown(ai_response)
    # typing_placeholder.markdown(f'<div class="assistant-bubble">{rendered_typing}</div>', unsafe_allow_html=True)
    # 3️⃣ Save AI response to memory
    st.session_state.memory_history.append({"role": "assistant", "content": ai_response})

    st.rerun()
