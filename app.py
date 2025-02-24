import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import pytz
from humpback_whale import migration_page

# ✅ Streamlit Page Configuration
st.set_page_config(page_title="Humpback Migration Dashboard", layout="wide")

# API Configuration
API_URL = "https://data.oceannetworks.ca/api/scalardata/device"
DEFAULT_TIME_RANGE = "Past 10 Minutes"
API_TOKEN = "492d6df3-c559-4e2b-8da0-1263e326ae1f"  
DEVICE_CODES = {
    "standard": "SBEDSPHOXV2SN7212038",
    "fluorometer": "TURNERCYCLOPS7F-900143"
}
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
        return now - datetime.timedelta(days=365), now
    elif option == "All Available Data":
        return datetime.datetime(2023, 12, 13), now
    return None, None

def fetch_data(time_range):
    date_from, date_to = get_time_range(time_range)
    if not date_from or not date_to:
        return None

    # Base parameters
    base_params = {
        "rowLimit": ROW_LIMIT,
        "outputFormat": OUTPUT_FORMAT,
        "qualityControl": QUALITY_CONTROL,
        "dateFrom": date_from.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "dateTo": date_to.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "token": API_TOKEN,
    }


    if time_range == "Past 6 Months":
        base_params["resamplePeriod"] = 86400
    elif time_range == "Past 1 Year" or time_range == "All Available Data":
        base_params["resamplePeriod"] = 259200

    data = {}

    standard_params = base_params.copy()
    standard_params["deviceCode"] = DEVICE_CODES["standard"]
    response = requests.get(API_URL, params=standard_params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Fetch chlorophyll data
        try:
            chlorophyll_params = base_params.copy()
            chlorophyll_params.update({
                "deviceCode": DEVICE_CODES["fluorometer"],
                "sensorsToInclude": "original",
            })
            
            chlorophyll_response = requests.get(API_URL, params=chlorophyll_params)
            
            if chlorophyll_response.status_code == 200:
                chlorophyll_data = chlorophyll_response.json()
                if "sensorData" in chlorophyll_data and chlorophyll_data["sensorData"]:
                    data["chlorophyll"] = chlorophyll_data
        except Exception as e:
            st.warning(f"Error fetching chlorophyll data: {str(e)}")
        
        return data
    else:
        st.error(f"API Request Failed. Status: {response.status_code}")
        return None

def process_api_data(data):
    if not data:
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
            "Internal Temperature",
            "Chlorophyll"
        ]

        if "sensorData" in data:
            for sensor in data["sensorData"]:
                if "data" in sensor and "sampleTimes" in sensor["data"]:
                    time_values = sensor["data"]["sampleTimes"]
                    break

        if time_values is None:
            return pd.DataFrame()

        utc_times = pd.to_datetime(time_values)
        if utc_times.tz is None:
            utc_times = utc_times.tz_localize(pytz.utc)
        processed_data["Time (Atlantic)"] = utc_times.tz_convert(pytz.timezone("America/Halifax"))

        # Process sensor data
        if "sensorData" in data:
            for sensor in data["sensorData"]:
                if "data" in sensor and "values" in sensor["data"]:
                    sensor_name = sensor["sensorName"]
                    values = sensor["data"]["values"]
                    if len(values) > len(time_values):
                        values = values[:len(time_values)]
                    elif len(values) < len(time_values):
                        values += [None] * (len(time_values) - len(values))
                    processed_data[sensor_name] = values

        if "chlorophyll" in data and "sensorData" in data["chlorophyll"]:
            for sensor in data["chlorophyll"]["sensorData"]:
                if sensor.get("sensorName") == "Chlorophyll":
                    if "data" in sensor and "values" in sensor["data"]:
                        chlorophyll_values = sensor["data"]["values"]
                        if len(chlorophyll_values) > len(time_values):
                            chlorophyll_values = chlorophyll_values[:len(time_values)]
                        elif len(chlorophyll_values) < len(time_values):
                            chlorophyll_values += [None] * (len(time_values) - len(chlorophyll_values))
                        processed_data["Chlorophyll"] = chlorophyll_values

        df = pd.DataFrame(processed_data)

        for sensor in expected_sensors:
            if sensor not in df.columns:
                df[sensor] = None

        return df
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return pd.DataFrame()

if "df" not in st.session_state:
    with st.spinner("Fetching initial data..."):
        api_data = fetch_data(DEFAULT_TIME_RANGE)
        st.session_state.df = process_api_data(api_data)

st.sidebar.header("Filter Options")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Past 10 Minutes", "Past 2 Hours", "Past 24 Hours", "Past 7 Days", 
     "Past 1 Month", "Past 6 Months", "Past 1 Year", "All Available Data"]
)

if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching real-time data..."):
        api_data = fetch_data(time_range)
        st.session_state.df = process_api_data(api_data)

st.sidebar.markdown("---")
page = st.sidebar.radio("View", ["Humpback Migration", "Ocean Data Dashboard"])

if page == "Humpback Migration":
    st.markdown('<div id="top"></div>', unsafe_allow_html=True)
    migration_page()
else:
    st.title("🌊 Ocean Data Dashboard")
    st.write("This dashboard provides insights into ocean health using real-time sensor data.")

    df = st.session_state.df
    if not df.empty:
        st.subheader("📉 Ocean Acidification Trends")
        fig1 = px.line(df, x="Time (Atlantic)", y="External pH (Dynamic Salinity)", 
                      title="pH Level Over Time (Atlantic Time)")
        st.plotly_chart(fig1)

        st.subheader("🌍 Hypoxia Risk Zones (Low Oxygen Levels)")
        fig2 = px.scatter(df, x="Time (Atlantic)", y="Oxygen Concentration Corrected", 
                         color="Oxygen Concentration Corrected",
                         title="Oxygen Concentration Over Time (Atlantic Time)")
        st.plotly_chart(fig2)
    else:
        st.write("No data available. Please fetch real-time data.")