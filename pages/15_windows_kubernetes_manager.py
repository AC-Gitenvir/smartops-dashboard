# pages/15_windows_kubernetes_manager.py

import streamlit as st
import subprocess

# --- Page Configuration ---
st.set_page_config(page_title="Local Kubernetes Manager", page_icon="☸️")
st.title("☸️ Local Kubernetes Manager (Windows)")
st.markdown("Interact with your local Minikube cluster by running `kubectl` commands.")

# --- Local Command Execution Function ---
def execute_local_command(command):
    """Executes a command locally on the host machine and returns the output."""
    if not command.strip():
        return "", "Command cannot be empty."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout
        errors = result.stderr
        return output, errors
    except subprocess.TimeoutExpired:
        return "", "Command timed out after 60 seconds."
    except Exception as e:
        return "", f"An unexpected error occurred: {str(e)}"

# --- Streamlit UI ---
st.info("Ensure your Minikube cluster is running. You can start it by opening Command Prompt and running `minikube start`.", icon="ℹ️")
st.divider()

st.subheader("Quick Actions")
st.write("Run common `kubectl` commands with a single click.")

col1, col2, col3, col4 = st.columns(4)

quick_commands = {
    "Get Pods": "kubectl get pods -o wide",
    "Get Nodes": "kubectl get nodes",
    "Get Services": "kubectl get services",
    "Get Deployments": "kubectl get deployments"
}

def run_and_display(command):
    with st.spinner(f"Running `{command}`..."):
        output, errors = execute_local_command(command)
    
    if errors:
        st.error(f"Errors from `{command}`:")
        st.code(errors, language="bash")
    if output:
        st.success(f"Output from `{command}`:")
        st.code(output, language="bash")

if col1.button("📦 Get Pods", use_container_width=True):
    run_and_display(quick_commands["Get Pods"])
if col2.button("🖥️ Get Nodes", use_container_width=True):
    run_and_display(quick_commands["Get Nodes"])
if col3.button("🔌 Get Services", use_container_width=True):
    run_and_display(quick_commands["Get Services"])
if col4.button("🚀 Get Deployments", use_container_width=True):
    run_and_display(quick_commands["Get Deployments"])

st.divider()

st.subheader("Custom `kubectl` Command")
custom_command = st.text_input("Enter your full command:", placeholder="e.g., kubectl describe pod my-pod-name")

if st.button("Execute Custom Command"):
    run_and_display(custom_command)