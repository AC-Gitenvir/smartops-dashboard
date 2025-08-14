# pages/11_SSH_Remote_Execution.py

import streamlit as st
import paramiko
import time

# --- Page Configuration ---
st.set_page_config(page_title="SSH Command Execution", page_icon="📡")
st.title("📡 Remote SSH Command Execution")
st.markdown("Execute commands on a remote Linux server securely from your dashboard.")

# --- Helper Function for SSH Execution ---
def execute_ssh_command(host, port, username, password, command):
    """
    Connects to a remote server via SSH and executes a given command.
    Returns the command's output and any errors.
    """
    # Defensive check for empty command
    if not command.strip():
        return "", "Command cannot be empty."

    client = paramiko.SSHClient()
    # This policy allows connecting to servers without having their key in the known_hosts file.
    # SECURITY NOTE: In a production environment, it's more secure to manage known_hosts properly.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server
        client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        
        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)

        # Read the output and errors
        # A small sleep can sometimes help ensure all output is captured for long-running commands
        time.sleep(1) 
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')

        return output, errors

    except paramiko.AuthenticationException:
        return "", "Authentication failed. Please check your username and password."
    except paramiko.SSHException as ssh_err:
        return "", f"SSH connection error: {ssh_err}"
    except Exception as e:
        return "", f"An unexpected error occurred: {e}"
    finally:
        # Always ensure the connection is closed
        if client:
            client.close()


# --- Streamlit UI ---

# Use columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Connection Details")
    # Load credentials from st.secrets if they exist, otherwise use empty strings
    host = st.text_input("Host IP / Hostname", value=st.secrets.get("ssh_credentials", {}).get("host", ""))
    port = st.number_input("Port", value=st.secrets.get("ssh_credentials", {}).get("port", 22))

with col2:
    st.subheader("Authentication")
    username = st.text_input("Username", value=st.secrets.get("ssh_credentials", {}).get("username", ""))
    password = st.text_input("Password", type="password", value=st.secrets.get("ssh_credentials", {}).get("password", ""))

st.subheader("Command to Execute")
# Provide some example commands
command_examples = ["ls -la", "df -h", "uname -a", "whoami"]
command = st.text_area("Enter your Linux command here:", placeholder=f"e.g., {command_examples[0]}")

# Execute button
if st.button("🚀 Execute Command", use_container_width=True):
    if not host or not username or not password:
        st.warning("Please fill in all connection and authentication details.")
    else:
        with st.spinner("Connecting and executing... Please wait."):
            output, errors = execute_ssh_command(host, port, username, password, command)

        st.markdown("---")
        st.subheader("Execution Results")

        if errors:
            st.error("Errors occurred:")
            st.code(errors, language="bash")
        
        if output:
            st.success("Output:")
            st.code(output, language="bash")
            
        if not output and not errors:
            st.info("Command executed successfully with no output.")