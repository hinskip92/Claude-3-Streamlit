import streamlit as st
from streamlit_chat import message
import anthropic
import base64
import os

st.title("Talk to Claude-3")

@st.cache_resource
def get_anthropic_client():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    return anthropic.Anthropic(api_key=api_key)

client = get_anthropic_client()

model_names = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
selected_model = st.sidebar.selectbox("Select a model:", model_names)
temperature = st.sidebar.slider("Select the temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
system_message = st.sidebar.text_input("System Message (optional):")
uploaded_file = st.sidebar.file_uploader("Upload an image:", type=['png', 'jpg', 'jpeg'])
if st.sidebar.button("Start New Chat"):
    st.session_state.messages = []
    st.session_state.uploaded_image = None
    st.session_state.image_processed = False
    st.session_state.image_displayed = False
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "image_processed" not in st.session_state:
    st.session_state.image_processed = False

if "image_displayed" not in st.session_state:
    st.session_state.image_displayed = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], list):
            for content in message["content"]:
                if content["type"] == "text":
                    st.write(content["text"])
                elif content["type"] == "image" and message["image_displayed"]:
                    st.image(base64.b64decode(content["source"]["data"]), caption="Uploaded Image")
        else:
            st.write(message["content"])

if prompt := st.chat_input("What would you like to ask?"):
    user_message_content = []
    if prompt:  # This ensures that prompt is not None or empty
        user_message_content.append({
            "type": "text",
            "text": prompt  # Ensure this is a valid non-empty string
        })
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        base64_encoded_data = base64.b64encode(bytes_data).decode("utf-8")
        image_media_type = uploaded_file.type
        new_uploaded_image = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image_media_type,
                "data": base64_encoded_data
            }
        }
        if new_uploaded_image != st.session_state.uploaded_image:
            print("Processing new uploaded image...")
            st.session_state.uploaded_image = new_uploaded_image
            st.session_state.image_processed = True
            st.session_state.image_displayed = False
            print("New image processed and stored in session state.")
        else:
            print("Using previously uploaded image from session state.")
    if st.session_state.uploaded_image:
        user_message_content.append(st.session_state.uploaded_image)
    image_displayed = not st.session_state.image_displayed
    st.session_state.messages.append({"role": "user", "content": user_message_content, "image_displayed": image_displayed})
    with st.chat_message("user"):
        if prompt:
            st.write(prompt)
        if st.session_state.uploaded_image and not st.session_state.image_displayed:
            st.image(base64.b64decode(st.session_state.uploaded_image["source"]["data"]), caption="Uploaded Image")
            st.session_state.image_displayed = True
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            accumulated_response = ""
            messages_to_send = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
            stream_kwargs = {
                "max_tokens": 4000,
                "messages": messages_to_send,
                "model": selected_model,
                "temperature": temperature,
            }
            if system_message:
                stream_kwargs["system"] = system_message
            with client.messages.stream(**stream_kwargs) as stream:
                for text in stream.text_stream:
                    accumulated_response += text
                    response_placeholder.write(accumulated_response)
            st.session_state.messages.append({"role": "assistant", "content": accumulated_response})