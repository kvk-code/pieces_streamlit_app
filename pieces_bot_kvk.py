import streamlit as st
from pieces_copilot_sdk import PiecesClient

# Initialize Pieces Client
pieces_client = PiecesClient(config={'baseUrl': 'http://localhost:1000'})

# Set page configuration
st.set_page_config(page_title="Pieces Copilot Chat", page_icon="🧩", layout="wide")

# Sidebar with additional features
with st.sidebar:
    st.header("Chat Options")
    
    if st.button("Start New Conversation", key="new_convo"):
        st.session_state.messages = [{"role": "assistant", "content": "New conversation started. How can I help you?"}]
        conversation = pieces_client.create_conversation(props={"name": "New Streamlit Chat"})
        st.session_state.conversation_id = conversation['conversation'].id
        st.rerun()
    
    st.markdown("---")
    st.subheader("Past Conversations")
    
    # Get all conversations
    conversations = pieces_client.get_conversations()
    
    if conversations:
        for conv in conversations:
            if st.button(f"{conv.name}", key=conv.id):
                st.session_state.conversation_id = conv.id
                conversation_details = pieces_client.get_conversation(
                    conversation_id=conv.id,
                    include_raw_messages=True
                )
                st.session_state.messages = [{"role": msg.role, "content": msg.text} for msg in conversation_details.messages]
                st.rerun()
    else:
        st.write("No past conversations.")
    
    st.markdown("---")
    
    if st.button("Clear Current Conversation"):
        st.session_state.messages = [{"role": "assistant", "content": "Conversation cleared. How can I help you?"}]
        conversation = pieces_client.create_conversation(props={"name": "New Streamlit Chat"})
        st.session_state.conversation_id = conversation['conversation'].id
        st.rerun()
    
    if st.button("Get Conversation History"):
        conversation_details = pieces_client.get_conversation(
            conversation_id=st.session_state.conversation_id,
            include_raw_messages=True
        )
        st.json(conversation_details)

# Main chat interface
st.title("🧩 Pieces Copilot Chat")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm the Pieces Copilot. How can I assist you today?"}]

if "conversation_id" not in st.session_state:
    # Create a new conversation
    conversation = pieces_client.create_conversation(props={"name": "Streamlit Chat"})
    st.session_state.conversation_id = conversation['conversation'].id

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Ask a question")

if query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Get response from Pieces Copilot
    with st.spinner("Thinking..."):
        response = pieces_client.prompt_conversation(
            message=query,
            conversation_id=st.session_state.conversation_id
        )
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response['text'])
    st.session_state.messages.append({"role": "assistant", "content": response['text']})

# Footer
st.markdown("---")
st.markdown("Powered by Pieces Copilot SDK and Streamlit")