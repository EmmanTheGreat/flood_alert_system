import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import psutil
import time

# Dashboard Title
st.title("Floor Alert System Dashboard")

# Subheader
st.subheader("Real-Time Monitoring")

# API Endpoint from Raspberry Pi
API_URL = "http://<raspberry_pi_ip>:5000/sensor_data"

# Fetch data from Raspberry Pi
def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"flow_rate": "N/A", "humidity": "N/A", "water_level": "N/A"}
    except Exception:
        return {"flow_rate": "Error", "humidity": "Error", "water_level": "Error"}

# Fetch real-time data
data = fetch_data()

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Flow Rate (L/s)", value=data.get("flow_rate", "N/A"))

with col2:
    st.metric(label="Humidity (%)", value=data.get("humidity", "N/A"))

with col3:
    st.metric(label="Water Level (m)", value=data.get("water_level", "N/A"))

# Real-time water level visualization
historical_data = pd.DataFrame({
    "Time": pd.date_range(start="2023-01-01", periods=10, freq="h"),
    "Water Level": [2.5, 3.0, 2.8, 2.7, 2.9, 3.1, 2.6, 2.7, 2.8, 3.0]
})
fig = px.line(historical_data, x="Time", y="Water Level", title="Water Level Over Time")
st.plotly_chart(fig)

# System Health Monitoring
cpu_usage = psutil.cpu_percent()
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent

st.subheader("System Health Monitoring")
st.metric("CPU Usage", f"{cpu_usage}%")
st.metric("Memory Usage", f"{memory_usage}%")
st.metric("Disk Usage", f"{disk_usage}%")

# Historical Data Table
historical_data_table = pd.DataFrame({
    "Timestamp": ["2023-01-01 10:00", "2023-01-01 11:00", "2023-01-01 12:00"],
    "Flow Rate (L/s)": [1.2, 1.5, 1.3],
    "Humidity (%)": [45, 50, 48],
    "Water Level (m)": [2.1, 2.5, 2.0]
})

st.subheader("Historical Data")
st.dataframe(historical_data_table)

# Threshold Input
user_threshold = st.slider("Set Water Level Threshold (m)", min_value=0.0, max_value=5.0, value=2.5)

try:
    water_level = float(data["water_level"])
    if water_level > user_threshold:
        st.warning(f"⚠️ Water Level is Above Your Threshold of {user_threshold}m!")
except (ValueError, TypeError):
    st.error("❌ Invalid water level data received.")

# Display last update time
st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
