# Source: Below code is provided by Streamlit and AWS 

#1 Import streamlit and chatbot file
import streamlit as st 
import chatbot_backend as demo

#2 Configure page layout and theme
st.set_page_config(
    page_title="AI Chatbot Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for Claude-like UI
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        padding: 1rem 0;
    }
    
    .stChatMessage {
        padding: 0 !important;
    }
    
    .chat-container {
        max-width: 850px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    
    .message-wrapper {
        display: flex;
        margin-bottom: 1rem;
        padding: 0 1rem;
    }
    
    .message-wrapper.user {
        justify-content: flex-end;
    }
    
    .message-wrapper.assistant {
        justify-content: flex-start;
    }
    
    .message-bubble {
        max-width: 65%;
        padding: 0.875rem 1.25rem;
        border-radius: 1.125rem;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff;
        border-radius: 1.125rem 0.25rem 1.125rem 1.125rem;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }
    
    .assistant-message {
        background-color: #2a2f3a;
        color: #e5e7eb;
        border-radius: 0.25rem 1.125rem 1.125rem 1.125rem;
        border: 1px solid #404854;
    }
    
    .header-section {
        text-align: center;
        padding: 2rem 1rem 1.5rem;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
        border-bottom: 1px solid #404854;
        margin-bottom: 1.5rem;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        color: #9ca3af;
        font-size: 0.95rem;
    }
    
    .input-container {
        max-width: 850px;
        margin: 1.5rem auto 0;
        padding: 1rem;
        display: flex;
        gap: 0.75rem;
    }
    
    .chat-input-wrapper {
        flex: 1;
    }
    
    .stChatInputContainer {
        background-color: transparent !important;
    }
    
    .stChatInput {
        background-color: #2a2f3a !important;
        border: 1px solid #404854 !important;
        border-radius: 0.75rem !important;
        color: #e5e7eb !important;
    }
    
    .stChatInput input {
        background-color: #2a2f3a !important;
        color: #e5e7eb !important;
    }
    
    .spinner-text {
        color: #60a5fa;
        text-align: center;
        padding: 1rem;
    }
    
    .divider {
        border-top: 1px solid #404854;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

#3 Header section
st.markdown("""
<div class="header-section">
    <h1 class="header-title">🤖 AI Assistant</h1>
    <p class="header-subtitle">Powered by AWS Bedrock • Always here to help</p>
</div>
""", unsafe_allow_html=True)

#4 Initialize session state - LangChain memory
if 'memory' not in st.session_state: 
    st.session_state.memory = demo.demo_memory()

#5 Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

#6 Create chat container
chat_container = st.container()

#7 Display chat history with Claude-like styling
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="message-wrapper user">
                    <div class="message-bubble user-message">
                        {message['text']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="message-wrapper assistant">
                    <div class="message-bubble assistant-message">
                        {message['text']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

#8 Chat input
input_text = st.chat_input("Message AI Assistant...")

if input_text: 
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "text": input_text})
    
    # Display user message immediately
    st.markdown(
        f"""
        <div class="message-wrapper user">
            <div class="message-bubble user-message">
                {input_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Get response from chatbot
    with st.spinner("✨ Thinking..."):
        chat_response = demo.demo_conversation(input_text=input_text, memory=st.session_state.memory)
    
    # Add assistant response to history
    st.session_state.chat_history.append({"role": "assistant", "text": chat_response})
    
    # Display assistant message
    st.markdown(
        f"""
        <div class="message-wrapper assistant">
            <div class="message-bubble assistant-message">
                {chat_response}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Rerun to update display and position input at bottom
    st.rerun() 