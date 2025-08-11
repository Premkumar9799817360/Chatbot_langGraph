import streamlit as st
import time
import markdown
from langGraph import chatbot
from langchain_core.messages import HumanMessage

# Page configuration
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="wide")

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# Session state for memory
if "memory_history" not in st.session_state:
    st.session_state.memory_history = []

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

    # 3️⃣ Save AI response to memory
    st.session_state.memory_history.append({"role": "assistant", "content": ai_response})

    st.rerun()
