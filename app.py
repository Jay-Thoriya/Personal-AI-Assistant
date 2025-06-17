import streamlit as st
import openai
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file (for local development without secrets.toml)
load_dotenv()

# Get API key from Streamlit secrets or fallback to environment variable
api_key = st.secrets.get("api_key", os.getenv("OPENAI_API_KEY"))
# This approach allows the app to work both locally with .env and in Streamlit Cloud with secrets.toml

# Initialize client with API key
client = AsyncOpenAI(api_key=api_key)

st.set_page_config(page_title="Personal AI Assistant", layout="wide")

# Sidebar for logs and settings
with st.sidebar:
    st.header("Settings & Logs")
    
    # Display conversation logs
    st.subheader("Conversation Logs")
    
    if "messages" in st.session_state:
        log_messages = [msg for msg in st.session_state["messages"] if msg["role"] != "system"]
        if log_messages:
            for i, msg in enumerate(log_messages):
                role = "👤 You" if msg["role"] == "user" else "🤖 Assistant"
                with st.container():
                    st.text(f"{role}:")
                    st.info(msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'])
                    st.success(f"Message {i+1} of {len(log_messages)}")
        else:
            st.info("No conversation history yet.")

# Main content area
st.title("Personal AI Assistant")
st.subheader("Ask me anything about myself and I'll respond as if I were you")

# Voice features removed as they are not supported by Streamlit deploy

# System prompt with personal information
personal_prompt = """
You are an AI assistant that responds as if you were the user. Answer questions about yourself with the following information:

your information : i am a Personal Voice Assistant developed by "Jay Thoriya".
Life story: I grew up in a small town, developed a passion for technology early on, and pursued computer science in college. After graduation, I worked at several tech startups before finding my current role where I'm developing AI applications.

Superpower: My #1 superpower is the ability to quickly learn and adapt to new technologies and situations. I can pick up new programming languages and frameworks faster than most people.

Areas to grow: 
1. Public speaking and presentation skills
2. Work-life balance and time management
3. Leadership and team management

Misconception: My coworkers often think I'm always serious and focused on work, but I actually have a playful sense of humor and enjoy creative activities outside of coding.

Pushing boundaries: I push my boundaries by deliberately taking on projects that are outside my comfort zone. I also practice the "learn in public" approach where I share my learning journey, which keeps me accountable.

Respond in a conversational, friendly tone. If asked about topics not covered in this information, politely explain that you don't have that information about the user.
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": personal_prompt}
    ]

# Speech input feature removed

for message in st.session_state["messages"]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

question = st.chat_input("Type your question here")

# Main function to handle chat
async def process_chat(question):
    if question:
        # Check if API key is provided
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar to continue.")
            return
            
        st.session_state["messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        try:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state["messages"],
                    stream=True
                )

                # Stream the response
                async for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.write(full_response + "▌")
                
                message_placeholder.write(full_response)

                # Add the assistant's response to the message history
                st.session_state["messages"].append({"role": "assistant", "content": full_response})
                
                # Update sidebar with success message
                with st.sidebar:
                    st.success("New message added to conversation!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            # If there was an error with the API call, remove the user's message from history
            if len(st.session_state["messages"]) > 0 and st.session_state["messages"][-1]["role"] == "user":
                st.session_state["messages"].pop()

if question:
    asyncio.run(process_chat(question))