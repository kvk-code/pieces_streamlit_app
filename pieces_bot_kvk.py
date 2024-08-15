import streamlit as st
from pieces_copilot_sdk import PiecesClient
from collections import deque

# Initialize Pieces Client
pieces_client = PiecesClient(config={'baseUrl': 'http://localhost:1000'})

# Set page configuration
st.set_page_config(page_title="Pieces Copilot Chat by KIRAN", page_icon="🧩", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm the Pieces Copilot. How can I assist you today?"}]
if "conversation_id" not in st.session_state:
    conversation = pieces_client.create_conversation(props={"name": "New Streamlit Chat"})
    st.session_state.conversation_id = conversation['conversation'].id
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "recent_messages" not in st.session_state:
    st.session_state.recent_messages = deque(maxlen=5)  # Store last 5 messages

# Sidebar with additional features
with st.sidebar:
    st.header("Chat Options")
    
    if st.button("Start New Conversation", key="new_convo"):
        st.session_state.messages = [{"role": "assistant", "content": "New conversation started. How can I help you?"}]
        conversation = pieces_client.create_conversation(props={"name": "New Streamlit Chat"})
        st.session_state.conversation_id = conversation['conversation'].id
        st.session_state.question_count = 0
        st.session_state.recent_messages.clear()
        st.rerun()
    
    st.markdown("---")
    st.subheader("Past Conversations")
    
    # Get all conversations
    conversations = pieces_client.get_conversations()
    
    if conversations:
        for conv in conversations:
            if st.button(f"{conv.name}", key=conv.id):
                st.session_state.conversation_id = conv.id
                try:
                    conversation_details = pieces_client.get_conversation(
                        conversation_id=conv.id,
                        include_raw_messages=True
                    )
                    if conversation_details and 'raw_messages' in conversation_details:
                        st.session_state.messages = [
                            {"role": "user" if msg['is_user_message'] else "assistant", "content": msg['message']}
                            for msg in conversation_details['raw_messages']
                        ]
                    else:
                        st.warning("No messages found in the selected conversation.")
                except Exception as e:
                    st.error(f"Error retrieving conversation: {str(e)}")
                st.rerun()
    else:
        st.write("No past conversations.")
    
    st.markdown("---")
    
    if st.button("Clear Current Conversation"):
        st.session_state.messages = [{"role": "assistant", "content": "Conversation cleared. How can I help you?"}]
        conversation = pieces_client.create_conversation(props={"name": "New Streamlit Chat"})
        st.session_state.conversation_id = conversation['conversation'].id
        st.session_state.question_count = 0
        st.session_state.recent_messages.clear()
        st.rerun()
    
    if st.button("Get Conversation History"):
        conversation_details = pieces_client.get_conversation(
            conversation_id=st.session_state.conversation_id,
            include_raw_messages=True
        )
        st.json(conversation_details)

# Main chat interface
st.title("🧩 Pieces Copilot Chat by KIRAN")

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
    st.session_state.recent_messages.append({"role": "user", "content": query})
    
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
    st.session_state.recent_messages.append({"role": "assistant", "content": response['text']})
    
    # Increment question count
    st.session_state.question_count += 1
    
    # Update conversation name after every 3 questions
    if st.session_state.question_count % 3 == 0:
        updated_name = pieces_client.update_conversation_name(st.session_state.conversation_id)
        if updated_name:
            st.success(f"Conversation renamed to: {updated_name}")
        else:
            st.warning("Failed to update conversation name")

# Footer
st.markdown("---")
st.markdown("Powered by Pieces Copilot SDK and Streamlit")