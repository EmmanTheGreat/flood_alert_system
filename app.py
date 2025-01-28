import streamlit as st
import requests

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
    except Exception as e:
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
