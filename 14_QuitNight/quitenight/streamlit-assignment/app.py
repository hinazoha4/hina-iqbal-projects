import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import plotly.express as px

# === FIREBASE INITIALIZATION ===
@st.cache_resource

def init_firebase():
    cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your path
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://live-tv-a98f9.firebaseio.com'  # Replace with your DB URL
    })

if not firebase_admin._apps:
    init_firebase()

# === SESSION STATE INITIALIZATION ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "node" not in st.session_state:
    st.session_state.node = "esp32"
if "thresholds" not in st.session_state:
    st.session_state.thresholds = {
        "temperature_c": 37,
        "humidity": 75,
        "light_lux": 1000,
        "vibration_digital": 1
    }

# === FIREBASE UTILITY ===
def fetch_data(node):
    ref = db.reference(f"data/{node}")
    data = ref.get()
    if not data:
        return pd.DataFrame()

    records = []
    for timestamp, values in data.items():
        dt = datetime.fromtimestamp(int(timestamp) / 1000.0)
        record = {"datetime": dt}
        record.update(values)
        records.append(record)

    df = pd.DataFrame(records).sort_values("datetime")
    return df

# === PAGE: LOGIN ===
def login_page():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.logged_in = True  # Stub login
        st.success("Logged in successfully!")

# === PAGE: REGISTER ===
def register_page():
    st.title("📝 Register")
    st.text_input("Email")
    st.text_input("Password", type="password")
    if st.button("Register"):
        st.success("Registered successfully! (stub)")

# === PAGE: WELCOME ===
def welcome_page():
    st.title("👋 Welcome to QuietNight")
    st.markdown("Monitor sleep environment in real-time.")
    node_selector()

# === NODE SELECTOR (global UI) ===
def node_selector():
    st.session_state.node = st.selectbox("Select Node", ["esp32", "simulator"], index=["esp32", "simulator"].index(st.session_state.node))

# === PAGE: LIVE READINGS ===
def live_readings_page():
    st.title("📟 Live Sensor Readings")
    node_selector()
    df = fetch_data(st.session_state.node)
    if df.empty:
        st.warning("No data available.")
        return

    latest = df.iloc[-1]

    # === Alert logic ===
    thresholds = st.session_state.thresholds
    alerts = []
    if latest['temperature_c'] > thresholds["temperature_c"]:
        alerts.append("🌡️ Temperature exceeds safe threshold!")
    if latest['humidity'] > thresholds["humidity"]:
        alerts.append("💧 Humidity exceeds safe threshold!")
    if latest['light_lux'] > thresholds["light_lux"]:
        alerts.append("💡 Light level is too high!")
    if latest.get("vibration_digital", 0) >= thresholds["vibration_digital"]:
        alerts.append("⚠️ Vibration detected!")

    if alerts:
        st.error("\n".join(alerts))

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Temperature", f"{latest['temperature_c']} °C")
        st.metric("Humidity", f"{latest['humidity']} %")
    with col2:
        st.metric("Light", f"{latest['light_lux']} lux")
        vib = "High" if latest.get("vibration_digital", 0) else "Low"
        st.metric("Vibration", vib)

# === PAGE: GRAPHS ===
def graphs_page():
    st.title("📊 Sensor Graphs")
    node_selector()
    df = fetch_data(st.session_state.node)
    if df.empty:
        st.warning("No data available.")
        return

    show_all = st.checkbox("Show all graphs")
    if show_all:
        for col in ["temperature_c", "humidity", "light_lux"]:
            fig = px.line(df, x="datetime", y=col, title=f"{col.replace('_', ' ').title()} Over Time")
            st.plotly_chart(fig, use_container_width=True)
    else:
        sensor = st.selectbox("Select graph to view", ["temperature_c", "humidity", "light_lux"])
        fig = px.line(df, x="datetime", y=sensor, title=f"{sensor.replace('_', ' ').title()} Over Time")
        st.plotly_chart(fig, use_container_width=True)

# === PAGE: ALERTS ===
def alerts_page():
    st.title("⚠️ Alert Settings")
    node_selector()
    enable_alerts = st.checkbox("Enable Alerts", value=True)

    st.markdown("### Configure Thresholds")
    col1, col2 = st.columns(2)
    with col1:
        max_temp = st.number_input("Max Temperature (°C)", value=st.session_state.thresholds["temperature_c"])
        max_light = st.number_input("Max Light (lux)", value=st.session_state.thresholds["light_lux"])
    with col2:
        max_humidity = st.number_input("Max Humidity (%)", value=st.session_state.thresholds["humidity"])
        vib_level = st.selectbox("Max Vibration Level", ["LOW", "MEDIUM", "HIGH"], index=2)

    if st.button("Save Settings"):
        st.session_state.thresholds["temperature_c"] = max_temp
        st.session_state.thresholds["humidity"] = max_humidity
        st.session_state.thresholds["light_lux"] = max_light
        st.session_state.thresholds["vibration_digital"] = 1 if vib_level == "HIGH" else 0
        st.success("Alert settings saved and applied.")

# === MAIN NAVIGATION ===
def main():
    st.sidebar.title("QuietNight")
    page = st.sidebar.radio("Navigate", ["Login", "Register", "Welcome", "Live Readings", "Graphs", "Alerts"])

    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()
    elif not st.session_state.logged_in:
        st.warning("🔒 Please login first.")
        login_page()
    elif page == "Welcome":
        welcome_page()
    elif page == "Live Readings":
        live_readings_page()
    elif page == "Graphs":
        graphs_page()
    elif page == "Alerts":
        alerts_page()

if __name__ == '__main__':
    main()
