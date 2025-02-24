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

def show_whale_lifecycle():
    """Display the four phases of the humpback whale lifecycle with interactive details."""
    st.header("🐋 Humpback Whale Lifecycle")
    st.markdown("Explore the interactive lifecycle phases of humpback whales. Click on each tab to view details, then use the buttons to learn even more about each phase.")

    # Create tabs for each lifecycle phase
    tabs = st.tabs(["Breeding Phase", "Feeding Phase", "Migration Phase", "Resting Phase"])
    
    with tabs[0]:
        st.subheader("1️⃣ Breeding Phase")
        st.markdown("""
        **Habitat:** Warm, shallow (<50 m) coastal or island waters offering calm conditions.  
        **Temperature:** Typically between 19°C and 28°C – ideal for calving and nurturing young.  
        **Behavior:** Involves mating, calving, and early calf-rearing in sheltered environments.  
        **Key Drivers:** Shallow bathymetry, proximity to coastlines or reefs, and low sea state protect vulnerable calves.  
        **Reference:** NOAA Fisheries provides detailed descriptions of these breeding habitats ([NOAA Fisheries](https://www.fisheries.noaa.gov/species/humpback-whale)).
        """)
        if st.button("Learn more about Breeding", key="breeding"):
            st.info("""
            Additional Details:  
            - Breeding areas are chosen for their ability to provide natural protection from predators and rough weather.  
            - Proximity to islands or reefs reduces energy expenditure for mother-calf pairs.  
            - Even slight changes in water temperature or sea state can impact calf survival.
            """)

    with tabs[1]:
        st.subheader("2️⃣ Feeding Phase")
        st.markdown("""
        **Habitat:** Colder, high-latitude waters where nutrient-rich upwelling zones create abundant prey concentrations.  
        **Temperature:** Cooler waters, often in the 10–15°C range, support high densities of krill and small fish.  
        **Behavior:** Whales utilize specialized feeding techniques like lunge feeding and bubble-net feeding.  
        **Key Drivers:** Strong thermal gradients, ocean current patterns, and high chlorophyll levels (a proxy for prey availability) are crucial.
        **Reference:** Research reviews (e.g., Meynecke et al.) detail these environmental drivers.
        """)
        if st.button("Learn more about Feeding", key="feeding"):
            st.info("""
            Additional Details:  
            - Upwelling zones and ocean fronts concentrate prey, forming 'hotspots' for feeding.  
            - Shifts in water temperature due to climate change may affect prey distribution and feeding efficiency.  
            - Whales often adjust their feeding behavior to take advantage of these dynamic conditions.
            """)

    with tabs[2]:
        st.subheader("3️⃣ Migration Phase")
        st.markdown("""
        **Habitat:** Long-distance travel routes connecting cold feeding grounds with warm breeding areas.  
        **Distance & Speed:** Migrations can span thousands of kilometers; typical speeds range from 2–5 km/h, with mother-calf pairs moving more slowly.  
        **Behavior:** Whales follow predictable migratory corridors influenced by ocean currents and seasonal temperature changes.  
        **Key Drivers:** Variations in water temperature, current direction, and the need to optimize energy use shape migratory paths.
        **Reference:** NOAA Fisheries and scientific studies ([NOAA Fisheries](https://www.fisheries.noaa.gov/species/humpback-whale)) provide detailed migratory maps.
        """)
        if st.button("Learn more about Migration", key="migration"):
            st.info("""
            Additional Details:  
            - Migratory routes are often influenced by natural landmarks such as seamounts and continental shelves.  
            - Whales may adjust their timing and pathways in response to subtle environmental shifts.  
            - Efficient migration is critical for ensuring that whales reach productive feeding or safe breeding grounds.
            """)

    with tabs[3]:
        st.subheader("4️⃣ Resting Phase")
        st.markdown("""
        **Habitat:** Calm, shallow, and sheltered waters—often in bays or semi-enclosed coastal areas—that facilitate energy conservation.  
        **Behavior:** During migration, whales, particularly mother-calf pairs, pause for extended surface intervals to reduce energy expenditure.  
        **Key Drivers:** Low wave action, gentle bathymetry, and close proximity to the coast help establish ideal resting areas.
        **Reference:** Reviews (e.g., Meynecke et al.) emphasize the importance of these areas for whale recovery.
        """)
        if st.button("Learn more about Resting", key="resting"):
            st.info("""
            Additional Details:  
            - Resting areas are vital for conserving energy after long migrations.  
            - These zones are highly sensitive to disturbances such as boat traffic and ocean noise.  
            - Protecting these habitats is an emerging focus of conservation efforts.
            """)

def migration_page():
    """Main migration page"""
    st.title("🐋 Whale Watch")
    
    st.info("""
    This dashboard provides insights into humpback whale migration patterns and environmental conditions 
    in Holyrood waters. The data combines real-time measurements with historical migration patterns.
    """)

    df = st.session_state.df if "df" in st.session_state else pd.DataFrame()

    if not df.empty:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "ℹ️ About",
            "🌊 Phases",
            "📊 Environmental Conditions",
            "🗓️ Migration Patterns",
            "🐟 Prey Species"
        ])

        with tab1:
            st.header("About Humpback Whales")
            
            # Use two columns: left for the image, right for species overview
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(
                    IMAGE_PATH,
                    caption="Humpback Whale",
                    use_container_width=True
                )
            
            with col2:
                st.markdown("""
                ### Species Overview
                Humpback whales (*Megaptera novaeangliae*) are among the most majestic marine mammals. 
                Renowned for their haunting songs and acrobatic breaches, these giants of the ocean captivate audiences worldwide.
                """)
                
                st.markdown("""
                ### Key Characteristics
                - 🏷 **Size:** Adults range from 12-16 meters in length  
                - ⚖ **Weight:** Can weigh up to 30,000 kg  
                - ⌛ **Lifespan:** Typically 45-50 years  
                - 🍽 **Diet:** Primarily krill and small fish, with specialized feeding techniques such as bubble-net feeding  
                """)
                
                with st.expander("🤔 Did you know?"):
                    st.markdown("""
                    - 🎶 **Remarkable Songs:** Male humpbacks sing complex, evolving songs that can last 20 minutes or more.
                    - 🌏 **Epic Migrations:** They travel up to 8,000 kilometers annually between feeding and breeding grounds.
                    - 🦸 **Unique Physiology:** Their long pectoral fins, up to 5 meters, are the longest of any whale species relative to body size.
                    - 🤝 **Social Behavior:** Humpbacks often cooperate in hunting, showcasing advanced group coordination.
                    """)
            
            st.markdown("""
            ### Behavior & Migration
            Humpback whales undertake one of the longest migrations of any mammal, traveling between cold, nutrient-rich feeding grounds near the poles and warmer tropical breeding areas. This journey, spanning thousands of kilometers, is essential for their reproduction and population health.
            
            ### Conservation Status
            Although humpback whale populations have rebounded significantly following a moratorium on commercial whaling, they continue to face various threats:
            - 🚢 Ship strikes  
            - 🏷 Entanglement in fishing gear  
            - ♨️ Climate change impacts  
            - 🔊 Ocean noise pollution
            
            ### Unique Features
            1. **Pectoral Fins:** Exceptionally long, aiding in maneuverability  
            2. **Breaching:** Dramatic leaps out of the water  
            3. **Whale Songs:** Complex vocalizations that can evolve over time  
            4. **Bubble-net Feeding:** A group feeding strategy to corral fish
            """, unsafe_allow_html=True)
        
        with tab2:
            show_whale_lifecycle()

        with tab3:
            show_metrics(df)
            st.plotly_chart(create_environmental_figure(df), use_container_width=True)
            show_condition_alerts(df)

        with tab4:
            st.plotly_chart(create_simplified_species_chart(), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### Presence Level Guide
                - **0:** Absent
                - **1:** Low Presence
                - **2:** Medium Presence
                - **3:** High Presence
                """)
            with col2:
                st.markdown("""
                ### Peak Activity Periods
                - 🐋 **Whales:** June - August
                - 🐟 **Capelin:** June - July
                - 🦐 **Krill:** April - September
                - 🐠 **Herring:** May & August - September
                """)
            
            st.info("""
            ### Environmental Influences on Migration
            - 🌊 Water temperature triggers movement patterns  
            - 🐟 Prey availability affects whale presence  
            - 🌡️ Seasonal changes impact all species
            """)

        with tab5:
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
