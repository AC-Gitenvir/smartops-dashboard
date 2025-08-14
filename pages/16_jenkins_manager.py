# pages/16_jenkins_manager.py (Robust Connection Version)

import streamlit as st
import jenkins
import time

# --- Page Configuration ---
st.set_page_config(page_title="Jenkins Manager", page_icon="🚀")
st.title("🚀 Jenkins CI/CD Manager")
st.markdown("Monitor and trigger jobs on your Jenkins server.")

# --- Jenkins Connection ---

# This new connection function is more robust for troubleshooting.
@st.cache_resource
def connect_to_jenkins():
    """Connects to the Jenkins server using credentials from secrets."""
    try:
        creds = st.secrets["jenkins_credentials"]
        
        # We create the server object first
        server = jenkins.Jenkins(creds["url"], username=creds["username"], password=creds["token"])
        
        # Then, we explicitly check the connection. This provides better error messages.
        user = server.get_whoami()
        st.success(f"Successfully connected to Jenkins as '{user['fullName']}'")
        return server

    except jenkins.JenkinsException as e:
        st.error(f"Jenkins API Error: {e}")
        st.warning("Please check that your API token is correct and has the right permissions.")
        return None
    except Exception as e:
        st.error(f"Failed to connect to Jenkins: {e}")
        st.warning("Please check your Jenkins URL in secrets.toml and ensure the server is running and accessible.")
        return None

server = connect_to_jenkins()

# --- Main App UI ---

if server:
    st.divider()

    # --- Job Listing and Triggering ---
    st.subheader("🛠️ Jenkins Jobs")
    try:
        jobs = server.get_jobs()
        if not jobs:
            st.warning("No jobs found on the Jenkins server.")
        else:
            job_dict = {job['name']: job for job in jobs}
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_job_name = st.selectbox("Select a job to see details:", options=job_dict.keys())
            
            with col2:
                st.write("") # Spacer
                st.write("") # Spacer
                if st.button(f"🚀 Build '{selected_job_name}'", use_container_width=True):
                    try:
                        # Get the next build number before triggering
                        next_build_number = server.get_job_info(selected_job_name)['nextBuildNumber']
                        server.build_job(selected_job_name)
                        st.toast(f"Build #{next_build_number} for '{selected_job_name}' started!")
                        time.sleep(2) # Give Jenkins a moment to update
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to start build: {e}")

            st.divider()
            
            # --- Build Status and Console Output ---
            st.subheader(f"🔍 Details for '{selected_job_name}'")
            
            try:
                job_info = server.get_job_info(selected_job_name)
                last_build_number = job_info.get('lastBuild', {}).get('number')

                if last_build_number:
                    build_info = server.get_build_info(selected_job_name, last_build_number)
                    
                    status = build_info.get('result', 'RUNNING').upper()
                    duration = build_info.get('duration', 0) / 1000  # Convert ms to s
                    
                    sc1, sc2, sc3 = st.columns(3)
                    sc1.metric("Last Build #", last_build_number)
                    sc2.metric("Status", status)
                    sc3.metric("Duration (s)", f"{duration:.2f}")

                    if st.button("📄 View Console Output", use_container_width=True):
                        with st.spinner("Fetching console output..."):
                            console_output = server.get_build_console_output(selected_job_name, last_build_number)
                            st.code(console_output, language="log")
                else:
                    st.info(f"The job '{selected_job_name}' has not been built yet.")
            
            except Exception as e:
                st.error(f"Could not retrieve build details: {e}")

    except Exception as e:
        st.error(f"An error occurred while fetching jobs: {e}")