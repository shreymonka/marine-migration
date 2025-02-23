# humberback_whale.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Define prey data
PREY_DATA = {
    "Capelin": {
        "temp_range": {"min": 2, "max": 12},
        "peak_season": "June-July"
    },
    "Krill": {
        "temp_range": {"min": -1.5, "max": 10},
        "peak_season": "April-September"
    },
    "Herring": {
        "temp_range": {"min": 4, "max": 15},
        "peak_season": "May-June & Aug-Sep"
    }
}

def safe_float_convert(value, default=0.0):
    """Safely convert a value to float"""
    try:
        if value and isinstance(value, str):
            return float(value.replace("°C", "").strip())
        elif isinstance(value, (int, float)):
            return float(value)
        return default
    except (ValueError, TypeError):
        return default

def create_dual_axis_figure(df):
    """Create a dual-axis figure for temperature and pH"""
    fig = go.Figure()
    
    # Add temperature trace
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["Temperature"],
        name="Temperature (°C)",
        line=dict(color="#82ca9d", width=2)
    ))
    
    # Add pH trace
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["External pH (Dynamic Salinity)"],
        name="pH",
        line=dict(color="#8884d8", width=2),
        yaxis="y2"
    ))

    # Update layout
    fig.update_layout(
        xaxis=dict(
            title="Time",
            gridcolor="LightGray",
            gridwidth=1
        ),
        yaxis=dict(
            title=dict(
                text="Temperature (°C)",
                font=dict(color="#82ca9d")
            ),
            gridcolor="LightGray",
            gridwidth=1
        ),
        yaxis2=dict(
            title=dict(
                text="pH",
                font=dict(color="#8884d8")
            ),
            anchor="x",
            overlaying="y",
            side="right",
            gridcolor="LightGray",
            gridwidth=1
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=60, t=50, b=50),
        plot_bgcolor="white",
        height=400
    )
    
    return fig

def create_simplified_species_chart():
    """Create a simplified bar chart showing species presence by month"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month = datetime.now().month - 1
    
    colors = {
        'Humpback': '#1f77b4',  # Blue
        'Capelin': '#2ca02c',   # Green
        'Krill': '#ff7f0e',     # Orange
        'Herring': '#9467bd'    # Purple
    }

    fig = go.Figure()

    # Add traces for each species
    species_data = [
        ('🐋 Humpback Whales', [0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0], 'Humpback'),
        ('🐟 Capelin', [0, 0, 0, 0, 1, 3, 3, 2, 1, 0, 0, 0], 'Capelin'),
        ('🦐 Krill', [1, 1, 1, 2, 3, 3, 3, 3, 2, 1, 1, 1], 'Krill'),
        ('🐠 Herring', [0, 0, 0, 0, 2, 1, 0, 2, 2, 1, 0, 0], 'Herring')
    ]

    for name, values, color_key in species_data:
        fig.add_trace(go.Bar(
            name=name,
            x=months,
            y=values,
            marker_color=colors[color_key]
        ))

    # Update layout
    fig.update_layout(
        title=dict(
            text='Species Presence Throughout the Year',
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        xaxis=dict(
            title='Month',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title='Presence Level',
            ticktext=['Absent', 'Low', 'Medium', 'High'],
            tickvals=[0, 1, 2, 3],
            tickfont=dict(size=12)
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        plot_bgcolor='white',
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        )
    )

    # Add current month indicator
    fig.add_vline(
        x=current_month,
        line_dash="dash",
        line_color="red",
        annotation_text="Current Month",
        annotation_position="top"
    )

    return fig

def show_condition_alerts(df):
    """Display alerts based on current conditions"""
    if df.empty:
        return
        
    latest = df.iloc[-1]
    st.subheader("🚨 Current Conditions Alert")
    
    temp = safe_float_convert(latest.get("Temperature"))
    ph = safe_float_convert(latest.get("External pH (Dynamic Salinity)"))
    
    if temp != 0.0:
        alerts_shown = False
        current_month = datetime.now().month
        
        for species, data in PREY_DATA.items():
            min_temp = data["temp_range"]["min"]
            max_temp = data["temp_range"]["max"]
            
            if temp < min_temp or temp > max_temp:
                st.warning(f"⚠️ Temperature ({temp:.1f}°C) is outside optimal range for {species} ({min_temp}°C - {max_temp}°C)")
                alerts_shown = True
            elif current_month in [6, 7, 8]:  # Summer months
                st.success(f"✅ Current conditions are optimal for {species}")
                alerts_shown = True
        
        if not alerts_shown:
            st.info("ℹ️ Current conditions are within acceptable ranges.")
    else:
        st.warning("⚠️ No current temperature data available")

def show_metrics(df):
    """Display environmental metrics"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="pH Levels",
            value=f"{df['External pH (Dynamic Salinity)'].mean():.2f}",
            delta=f"Range: {df['External pH (Dynamic Salinity)'].min():.2f} - {df['External pH (Dynamic Salinity)'].max():.2f}"
        )

    with col2:
        st.metric(
            label="Temperature (°C)",
            value=f"{df['Temperature'].mean():.2f}",
            delta=f"Range: {df['Temperature'].min():.2f} - {df['Temperature'].max():.2f}"
        )

    with col3:
        st.metric(
            label="Oxygen (ml/l)",
            value=f"{df['Oxygen Concentration Corrected'].mean():.2f}",
            delta=f"Range: {df['Oxygen Concentration Corrected'].min():.2f} - {df['Oxygen Concentration Corrected'].max():.2f}"
        )

def show_species_info():
    """Display species information cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        ### Capelin 🐟
        - Temperature: 2-12°C
        - Peak spawning: June-July
        
        *Data source: DFO Stock Assessment*
        """)

    with col2:
        st.success("""
        ### Krill 🦐
        - pH Sensitivity: High
        - Temperature: -1.5-10°C
        
        *Data source: Memorial University*
        """)

    with col3:
        st.success("""
        ### Herring 🐠
        - Temperature: 4-15°C
        - Spawning: Spring/Fall
        
        *Data source: DFO Atlantic Herring*
        """)

def migration_page():
    """Main migration page"""
    st.title("🐋 Humpback Whale Migration Dashboard")
    
    st.info("""
    This dashboard provides insights into humpback whale migration patterns and environmental conditions 
    in Holyrood waters. The data combines real-time measurements with historical migration patterns.
    """)

    df = st.session_state.df if "df" in st.session_state else pd.DataFrame()

    if not df.empty:
        tab1, tab2, tab3 = st.tabs(["📊 Environmental Conditions", "🗓️ Migration Patterns", "🐟 Prey Species"])

        with tab1:
            st.plotly_chart(create_dual_axis_figure(df), use_container_width=True)
            show_metrics(df)

        with tab2:
            st.plotly_chart(create_simplified_species_chart(), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### Presence Level Guide
                - **0**: Absent
                - **1**: Low Presence
                - **2**: Medium Presence
                - **3**: High Presence
                """)
            with col2:
                st.markdown("""
                ### Peak Activity Periods
                - 🐋 **Whales**: June - August
                - 🐟 **Capelin**: June - July
                - 🦐 **Krill**: April - September
                - 🐠 **Herring**: May & August - September
                """)
            
            st.info("""
            ### Environmental Influences on Migration
            - 🌊 Water temperature triggers movement patterns
            - 🐟 Prey availability affects whale presence
            - 🌡️ Seasonal changes impact all species
            """)

        with tab3:
            st.subheader("Key Prey Species in Holyrood Waters")
            show_species_info()
            
            st.info("""
            ### Environmental Factors Affecting Migration
            - 🌊 Water temperature influences capelin spawning timing
            - 🌡️ Krill distribution varies with water column stratification
            - 🐋 Humpback arrival typically correlates with capelin presence
            """)
            
            show_condition_alerts(df)
    else:
        st.warning("No data available. Please fetch real-time data using the sidebar controls.")

    st.markdown("""
    ---
    ### Data Sources
    - 📊 Real-time sensor data from Ocean Networks Canada
    - 🔬 Migration patterns from DFO Canada
    - 🎓 Species data from Memorial University Research
    
    *Note: Migration patterns are general guidelines and may vary based on local conditions.*
    """)

if __name__ == "__main__":
    migration_page()