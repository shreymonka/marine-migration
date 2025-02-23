import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import pytz
from humberback_whale import migration_page

# ✅ Streamlit Page Configuration
st.set_page_config(page_title="Ocean Data Dashboard", layout="wide")

# API Configuration
API_URL = "https://data.oceannetworks.ca/api/scalardata/device"
DEFAULT_TIME_RANGE = "Past 10 Minutes"
API_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxx"  
DEVICE_CODE = "SBEDSPHOXV2SN7212038"
ROW_LIMIT = 10000
OUTPUT_FORMAT = "array"
QUALITY_CONTROL = "clean"


def get_time_range(option):
    now = datetime.datetime.utcnow()
    if option == "Past 10 Minutes":
        return now - datetime.timedelta(minutes=10), now
    elif option == "Past 2 Hours":
        return now - datetime.timedelta(hours=2), now
    elif option == "Past 24 Hours":
        return now - datetime.timedelta(days=1), now
    elif option == "Past 7 Days":
        return now - datetime.timedelta(weeks=1), now
    elif option == "Past 1 Month":
        return now - datetime.timedelta(days=30), now
    elif option == "Past 6 Months":
        return now - datetime.timedelta(days=180), now
    elif option == "Past 1 Year":
        return now - datetime.timedelta(days=365), now  # Fetch last 1 year
    elif option == "All Available Data":
        return datetime.datetime(2023, 12, 13), now  # Fetch all available data
    return None, None


def fetch_data(time_range):
    date_from, date_to = get_time_range(time_range)
    if not date_from or not date_to:
        return None

    # Adjust sampling period for larger date ranges
    resample_period = None  # Default: No resampling
    if time_range == "Past 6 Months":
        resample_period = 86400  # Every 1 day in seconds
    elif time_range == "Past 1 Year" or time_range == "All Available Data":
        resample_period = 259200  # Every 3 days in seconds

    params = {
        "deviceCode": DEVICE_CODE,
        "rowLimit": ROW_LIMIT,  # Max rows per request
        "outputFormat": OUTPUT_FORMAT,
        "qualityControl": QUALITY_CONTROL,
        "dateFrom": date_from.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "dateTo": date_to.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "token": API_TOKEN,
    }

    # Apply resampling if needed
    if resample_period:
        params["resamplePeriod"] = resample_period
        params["resampleType"] = "avg"  # Get averaged data per period

    response = requests.get(API_URL, params=params)

    print("Request URL:", response.url)
    print("Response Status Code:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API Request Failed. Status: {response.status_code}, Response: {response.text}")
        return None

def process_api_data(data):
    if not data or "sensorData" not in data:
        return pd.DataFrame()

    try:
        processed_data = {}
        time_values = None  
        expected_sensors = [
            "External pH (Dynamic Salinity)",
            "Oxygen Concentration Corrected",
            "Practical Salinity",
            "Temperature",
            "Density",
            "Internal Temperature"
        ]

        # Extract timestamps from the first available sensor
        for sensor in data["sensorData"]:
            if "data" in sensor and "sampleTimes" in sensor["data"]:
                time_values = sensor["data"]["sampleTimes"]
                break  # Stop after finding the first valid timestamp list

        if time_values is None:
            return pd.DataFrame()  # No valid timestamps found

        # Convert timestamps to Atlantic Time
        utc_times = pd.to_datetime(time_values)
        if utc_times.tz is None:
            utc_times = utc_times.tz_localize(pytz.utc)
        processed_data["Time (Atlantic)"] = utc_times.tz_convert(pytz.timezone("America/Halifax"))

        # Extract sensor values and align their lengths with timestamps
        for sensor in data["sensorData"]:
            if "data" in sensor and "values" in sensor["data"]:
                sensor_name = sensor["sensorName"]
                values = sensor["data"]["values"]

                # Ensure values match the timestamp length
                if len(values) > len(time_values):
                    values = values[:len(time_values)]  # Trim extra values
                elif len(values) < len(time_values):
                    values += [None] * (len(time_values) - len(values))  # Pad missing values with None

                processed_data[sensor_name] = values

        df = pd.DataFrame(processed_data)

        # Ensure all expected sensors exist
        for sensor in expected_sensors:
            if sensor not in df.columns:
                df[sensor] = None

        return df

    except Exception as e:
        st.error(f"Error processing data: {e}")
        return pd.DataFrame()

# Main Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Ocean Data Dashboard", "Humpback Migration"])

# Sidebar for user input
st.sidebar.header("Filter Options")
time_range = st.sidebar.selectbox("Select Time Range", ["Past 10 Minutes", "Past 2 Hours", "Past 24 Hours", "Past 7 Days", "Past 1 Month", "Past 6 Months", "Past 1 Year", "All Available Data"])

if "df" not in st.session_state:
    with st.spinner("Fetching initial data..."):
        api_data = fetch_data(DEFAULT_TIME_RANGE)
        st.session_state.df = process_api_data(api_data)

if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching real-time data..."):
        api_data = fetch_data(time_range)
        st.session_state.df = process_api_data(api_data)

df = st.session_state.df

if page == "Ocean Data Dashboard":
    # Title
    st.title("🌊 Ocean Data Dashboard")
    st.write("This dashboard provides insights into ocean health using real-time sensor data.")

    if not df.empty:
        st.subheader("📉 Ocean Acidification Trends")
        fig1 = px.line(df, x="Time (Atlantic)", y="External pH (Dynamic Salinity)", title="pH Level Over Time (Atlantic Time)")
        st.plotly_chart(fig1)

        st.subheader("🌍 Hypoxia Risk Zones (Low Oxygen Levels)")
        fig2 = px.scatter(df, x="Time (Atlantic)", y="Oxygen Concentration Corrected", 
                          color="Oxygen Concentration Corrected",
                          title="Oxygen Concentration Over Time (Atlantic Time)")
        st.plotly_chart(fig2)

        st.subheader("🌡️ Internal Temperature Over Time")
        fig3 = px.line(df, x="Time (Atlantic)", y="Internal Temperature", title="Internal Temperature Over Time (Atlantic Time)")
        st.plotly_chart(fig3)
    else:
        st.write("No data available. Please fetch real-time data.")

elif page == "Humpback Migration":
    migration_page()

