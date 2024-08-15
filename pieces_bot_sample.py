import streamlit as st
from pieces_copilot_sdk import PiecesClient

pieces_client = PiecesClient(config={'baseUrl': 'http://localhost:1000'})


st.title("Pieces Copilot Streamlit Bot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ask me anything - Pieces Copilot"}]

if "conversation_id" not in st.session_state:
    # Create a new conversation
    conversation = pieces_client.create_conversation(props={"name": "Streamlit Chat"})
    st.session_state.conversation_id = conversation['conversation'].id

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask a question to the Pieces Copilot")

if query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Get response from Pieces Copilot
    response = pieces_client.prompt_conversation(
        message=query,
        conversation_id=st.session_state.conversation_id
    )
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response['text'])
    st.session_state.messages.append({"role": "assistant", "content": response['text']})