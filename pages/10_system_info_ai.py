# pages/system_info_ai.py

import streamlit as st
import psutil
import platform
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

# --- BACKEND LOGIC (LangChain Agent and Tools) ---

# Helper function to check for API key
def check_api_key():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("🚨 Google API Key not found! Please add it to your Streamlit secrets.")
        st.info("Create a file at `/.streamlit/secrets.toml` and add your key: `GOOGLE_API_KEY = 'YOUR_KEY_HERE'`")
        st.stop()

# Define system information tools
# Note: LangChain tools require a single (often unused) string argument.
def get_cpu_info(input_str: str) -> str:
    """Returns the current CPU usage percentage."""
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_memory_info(input_str: str) -> str:
    """Returns system memory statistics."""
    mem = psutil.virtual_memory()
    return f"RAM Stats — Total: {mem.total / (1024**3):.2f} GB, Available: {mem.available / (1024**3):.2f} GB, Used: {mem.percent}%"

def get_system_info(input_str: str) -> str:
    """Returns general operating system information."""
    sys = platform.uname()
    return f"System: {sys.system}, Node Name: {sys.node}, OS Version: {sys.version}, Processor: {sys.processor}"

def get_disk_info(input_str: str) -> str:
    """Returns disk usage statistics for the root directory."""
    disk = psutil.disk_usage('/')
    return f"Disk Usage (/) — Total: {disk.total / (1024**3):.2f} GB, Used: {disk.used / (1024**3):.2f} GB, Free: {disk.free / (1024**3):.2f} GB"

# Use st.cache_resource to initialize the agent only once
@st.cache_resource
def get_langchain_agent():
    """Initializes and returns the LangChain agent."""
    st.write("Initializing AI Agent... (This happens only once)")
    
    # Load Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )

    # Wrap functions into LangChain Tools
    tools = [
        Tool(name="CPU Info", func=get_cpu_info, description="Useful for getting the current CPU utilization percentage."),
        Tool(name="Memory Info", func=get_memory_info, description="Useful for getting system RAM and memory statistics."),
        Tool(name="System Info", func=get_system_info, description="Useful for getting operating system (OS) and hardware info."),
        Tool(name="Disk Info", func=get_disk_info, description="Useful for getting root disk space and usage statistics.")
    ]

    # Create the LangChain Agent
    # LangChainDeprecationWarning is expected here, but the code works as intended.
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True, # Set to True to see the agent's thought process in the terminal
        handle_parsing_errors=True # Handles cases where the LLM output is not perfect
    )
    return agent

# --- STREAMLIT UI ---

# First, check for the API key
check_api_key()

st.title("💻 System Info via AI")
st.markdown(
    "This is an interactive chat agent powered by **Google Gemini** and **LangChain**. "
    "Ask it questions in natural language about your system's status."
)
st.markdown("---")

# Examples of questions to guide the user
with st.expander("💡 Examples of what you can ask"):
    st.write("- What is my current CPU usage?")
    st.write("- How much RAM is free?")
    st.write("- Give me a summary of the system status.")
    st.write("- Tell me about my OS and disk space.")

# Initialize the agent
agent = get_langchain_agent()

# Initialize chat history in session state
if "sys_agent_messages" not in st.session_state:
    st.session_state.sys_agent_messages = [{"role": "assistant", "content": "Hi! How can I help you check the system status today?"}]

# Display chat messages from history
for message in st.session_state.sys_agent_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask about your system..."):
    # Add user message to chat history
    st.session_state.sys_agent_messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("🤖 The agent is thinking..."):
            try:
                response = agent.run(prompt)
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.sys_agent_messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"❌ An error occurred: {str(e)}"
                st.error(error_message)
                st.session_state.sys_agent_messages.append({"role": "assistant", "content": error_message})