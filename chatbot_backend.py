from langchain_aws import ChatBedrockConverse
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# Connecting to AWS Bedrock and setting up the chatbot
def demo_chatbot():
    demo_llm = ChatBedrockConverse(
        credentials_profile_name="default",
        model="deepseek.v3-v1:0",
        temperature=0.1,
        max_tokens=1000,
    )

    return demo_llm


# Setting up memory for the conversation
def demo_memory():
    memory = InMemoryChatMessageHistory()
    return memory


# Running a demo conversation with the chatbot
def demo_conversation(input_text, memory):

    llm_chain_data = demo_chatbot()

    def get_session_history(session_id):
        return memory

    llm_conversation = RunnableWithMessageHistory(llm_chain_data,get_session_history)

    # chat response using invoke
    chat_reply = llm_conversation.invoke(
        input_text,
        config={"configurable": {"session_id": "demo"}}
    )

    return chat_reply.content