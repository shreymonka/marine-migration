import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from pathlib import Path
import os

# Get the directory of the current script
CURRENT_DIR = Path(__file__).parent.absolute()
IMAGE_PATH = os.path.join(CURRENT_DIR, "assets", "humpback_whale.jpeg")

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

def create_environmental_figure(df):
    """Create a combined figure for all environmental parameters"""
    fig = go.Figure()
    
    # Add traces for each parameter
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["Temperature"],
        name="Temperature (°C)",
        line=dict(color="#FF4B4B", width=2)  # Red
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["External pH (Dynamic Salinity)"],
        name="pH",
        line=dict(color="#36A2EB", width=2),  # Blue
        yaxis="y2"
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["Oxygen Concentration Corrected"],
        name="Oxygen (ml/l)",
        line=dict(color="#4BC0C0", width=2),  # Teal
        yaxis="y3"
    ))
    
    if "Chlorophyll" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Time (Atlantic)"],
            y=df["Chlorophyll"],
            name="Chlorophyll",
            line=dict(color="#9966FF", width=2),  # Purple
            yaxis="y4"
        ))

    # Update layout with multiple y-axes
    fig.update_layout(
        title="Environmental Parameters Over Time",
        xaxis=dict(
            title="Time",
            domain=[0.1, 0.9]
        ),
        yaxis=dict(
            title=dict(
                text="Temperature (°C)",
                font=dict(color="#FF4B4B")
            ),
            tickfont=dict(color="#FF4B4B")
        ),
        yaxis2=dict(
            title=dict(
                text="pH",
                font=dict(color="#36A2EB")
            ),
            tickfont=dict(color="#36A2EB"),
            anchor="free",
            overlaying="y",
            side="left",
            position=0
        ),
        yaxis3=dict(
            title=dict(
                text="Oxygen (ml/l)",
                font=dict(color="#4BC0C0")
            ),
            tickfont=dict(color="#4BC0C0"),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        yaxis4=dict(
            title=dict(
                text="Chlorophyll",
                font=dict(color="#9966FF")
            ),
            tickfont=dict(color="#9966FF"),
            anchor="free",
            overlaying="y",
            side="right",
            position=1
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=100, r=100, t=50, b=50),
        plot_bgcolor="white",
        height=600
    )

    # Add grid for better readability
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    
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
        ('🦐 Krill', [1, 1, 1, 2, 3, 3, 3, 3, 2, 1,1, 1], 'Krill'),
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
    col1, col2, col3, col4 = st.columns(4)
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
        
    with col4:
        if "Chlorophyll" in df.columns:
            st.metric(
                label="Chlorophyll",
                value=f"{df['Chlorophyll'].mean():.2f}",
                delta=f"Range: {df['Chlorophyll'].min():.2f} - {df['Chlorophyll'].max():.2f}"
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
        tab1, tab2, tab3, tab4 = st.tabs([
            "ℹ️ About",
            "📊 Environmental Conditions",
            "🗓️ Migration Patterns",
            "🐟 Prey Species"
        ])

        with tab1:
            st.header("About Humpback Whales")
            
            col1, col2 = st.columns([4, 6])
            
            with col1:
                st.image(IMAGE_PATH,
                        caption="Humpback Whale Breaching",
                        use_container_width=True)

            with col2:
                st.markdown("""
                ### Species Overview
                Humpback whales (*Megaptera novaeangliae*) are one of the largest marine mammals in our oceans. 
                These magnificent creatures are known for their distinctive behaviors, complex songs, and annual migrations.

                ### Key Characteristics
                - **Size**: Adults range from 12-16 meters long
                - **Weight**: Can weigh up to 30,000 kg
                - **Lifespan**: Average 45-50 years
                - **Diet**: Primarily krill and small fish
                """)

            st.markdown("""
            <div style='margin-top: -10px;'>
            
            ### Behavior & Migration
            Humpback whales undertake one of the longest migrations of any mammal. They travel from cold feeding 
            grounds near the poles to warm breeding waters near the equator. During migration, they can travel 
            up to 8,000 kilometers each way.

            ### Conservation Status
            After being heavily impacted by commercial whaling, humpback whale populations have shown remarkable 
            recovery since the international whaling moratorium. However, they still face various threats including:
            - Ship strikes
            - Entanglement in fishing gear
            - Climate change impacts
            - Ocean noise pollution
            
            ### Unique Features
            Humpback whales are known for several distinctive characteristics:
            1. **Pectoral Fins**: Their long pectoral fins (up to 5 meters) are proportionally the longest of any whale
            2. **Breaching**: They regularly leap out of the water, creating spectacular displays
            3. **Whale Songs**: Males produce complex songs that can last for hours and change over time
            4. **Bubble-net Feeding**: A sophisticated hunting technique where groups create bubble nets to trap fish
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            # Show environmental metrics at the top
            show_metrics(df)
            
            # Combined environmental parameters plot
            st.plotly_chart(create_environmental_figure(df), use_container_width=True)
            
            # Show condition alerts
            show_condition_alerts(df)

        with tab3:
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

        with tab4:
            st.subheader("Key Prey Species in Holyrood Waters")
            show_species_info()
            
            st.info("""
            ### Environmental Factors Affecting Migration
            - 🌊 Water temperature influences capelin spawning timing
            - 🌡️ Krill distribution varies with water column stratification
            - 🐋 Humpback arrival typically correlates with capelin presence
            """)

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