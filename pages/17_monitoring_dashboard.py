# pages/17_monitoring_dashboard.py (Corrected Queries)

import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="System Monitoring", page_icon="📈")
st.title("📈 Live Host Monitoring Dashboard")
st.markdown("This dashboard connects to a Prometheus server to display live metrics from your RHEL9 VM.")

# --- Connection and Data Fetching ---
PROMETHEUS_HOST = st.secrets.get("ssh_credentials", {}).get("host", "localhost")
PROMETHEUS_URL = f"http://{PROMETHEUS_HOST}:9090"

@st.cache_data(ttl=15) # Cache data for 15 seconds
def fetch_prometheus_data(query):
    """Fetches data from the Prometheus API."""
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={'query': query}
        )
        response.raise_for_status()
        result = response.json()['data']['result']
        
        data_points = []
        for r in result:
            if 'value' in r: # PromQL aggregations return a single 'value'
                metric_name = query # Use the query as the metric name
                val = r['value']
                data_points.append([datetime.fromtimestamp(val[0]), float(val[1]), metric_name])
        
        df = pd.DataFrame(data_points, columns=['Timestamp', 'Value', 'Metric'])
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Prometheus at {PROMETHEUS_URL}. Is it running and accessible?")
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"Could not fetch or process data for query: {query}")
        return pd.DataFrame()

# --- Streamlit UI ---
st.info(f"Connecting to Prometheus server at `{PROMETHEUS_URL}`. Refresh the page to update data.", icon="ℹ️")

# --- Key Metrics Display ---
st.subheader("RHEL9 Host Metrics")

# --- CORRECTED QUERIES FOR NODE EXPORTER ---
queries = {
    "Host CPU Usage (%)": '(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[2m]))) * 100',
    "Host Memory Usage (%)": '((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100',
    "Root FS Usage (%)": '((node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_free_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"}) * 100'
}

cols = st.columns(len(queries))

for col, (metric_name, query) in zip(cols, queries.items()):
    df = fetch_prometheus_data(query)
    if not df.empty:
        latest_value = df['Value'].iloc[-1]
        col.metric(metric_name, f"{latest_value:.2f}%")
    else:
        col.metric(metric_name, "N/A")

st.divider()

# --- Time-Series Chart ---
st.subheader("CPU Usage Over Time")

cpu_df = fetch_prometheus_data(queries["Host CPU Usage (%)"])

if not cpu_df.empty:
    chart = alt.Chart(cpu_df).mark_area(
        line={'color': '#00d4ff'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='rgba(0, 212, 255, 0.5)', offset=1),
                   alt.GradientStop(color='rgba(0, 212, 255, 0)', offset=0)],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('Timestamp:T', title='Time'),
        y=alt.Y('Value:Q', title='CPU Usage (%)', scale=alt.Scale(domain=[0, 100])),
        tooltip=['Timestamp', 'Value']
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("No CPU data to display.")