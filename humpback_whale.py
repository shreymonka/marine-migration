import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from pathlib import Path
import os

CURRENT_DIR = Path(__file__).parent.absolute()
IMAGE_PATH = os.path.join(CURRENT_DIR, "assets", "humpback_whale.jpeg")

FEEDING_FACTORS = ["Chlorophyll", "External pH (Dynamic Salinity)", "Temperature"]
BREEDING_FACTORS = ["Temperature", "External pH (Dynamic Salinity)", "Oxygen Concentration Corrected"]

def preprocess_data(df, factors):
    """Preprocess the data before visualization."""
    df = df.dropna(subset=factors)
    return df

def create_conditions_chart(df, factors, title, colors):
    """Create a simple and clean time-series graph showing environmental factors over time.
       Graph generated using Plotly (https://plotly.com)."""
    fig = go.Figure()
    
    for factor in factors:
        fig.add_trace(go.Scatter(
            x=df["Time (Atlantic)"],
            y=df[factor],
            name=factor,
            line=dict(color=colors[factor], width=2)
        ))
    
    fig.update_layout(
        title=title,
        xaxis=dict(title="Time (Atlantic)", showgrid=False),
        yaxis=dict(title="Environmental Factor Levels", showgrid=False),
        legend=dict(
            x=0.01, y=0.99, bgcolor="rgba(255, 255, 255, 0.6)", bordercolor="black", borderwidth=1
        ),
        plot_bgcolor="white",
        height=500
    )
    return fig

def feeding_conditions_page():
    """Feeding conditions dashboard section"""
    st.title("🐋 Feeding Conditions")
    st.info("""
    This section visualizes key environmental factors affecting humpback whale feeding behavior.
    """)
    
    if "df" in st.session_state and not st.session_state.df.empty:
        st.session_state.df = preprocess_data(st.session_state.df, FEEDING_FACTORS)
        
        st.plotly_chart(create_conditions_chart(
            st.session_state.df, 
            FEEDING_FACTORS, 
            "🌊 Feeding Conditions Over Time", 
            {"Chlorophyll": "#2ca02c", "External pH (Dynamic Salinity)": "#1f77b4", "Temperature": "#ff7f0e"}
        ), use_container_width=True)
        st.caption("Graph generated using Plotly (https://plotly.com)")  # Citation for the graph
        
        st.subheader("🐳 How These Factors Affect Whale Feeding")
        st.markdown("""
        ### 🌿 Chlorophyll-a Concentration: Nature’s Buffet Table!
        - More chlorophyll = **More plankton = More food for krill and small fish!**  
        - Humpback whales **follow the buffet** to feast on nutrient-rich areas. 🐟🐋


        ### ⚖️ pH Levels: The Ocean’s Recipe for a Healthy Food Chain
        - If the ocean gets too acidic, **krill populations drop**, affecting the entire food chain. 😱
        - A stable pH (7.5 - 8.5) keeps marine life **happy and thriving**! 🌊


        ### 🌡️ Temperature: The Secret to a Perfect Feeding Spot
        - Cooler waters bring **nutrients to the surface**, **attracting plankton and prey**.  
        - **5°C - 15°C**? That’s the **Goldilocks zone** for humpback whales! 🏊‍♂️🐳


        ### 🌊 Ocean Currents and Upwelling Zones: The Whale’s GPS
        - Cold, nutrient-rich waters rise up, fueling the entire ecosystem.  
        - Humpbacks **prefer regions with high biological productivity**—it’s like finding the best seafood restaurant! 🍣🐋


        ### 🦐 Prey Density and Distribution: The Whale’s Shopping List
        - **Krill, capelin, and herring** are the top picks for a hungry humpback.  
        - Whales follow **prey migration patterns** to find their next meal. 🎯🐟


        ### 🫧 Oxygen Concentration: The Ocean’s Breathing Room
        - Higher oxygen = **better conditions for prey species**.  
        - Whales thrive in **moderate oxygen zones**—too low and the prey disappears! 🏊‍♂️🐳
        """)
    else:
        st.warning("No data available. Ensure the API has fetched data in app.py.")

def breeding_conditions_page():
    """Breeding conditions dashboard section"""
    st.title("🐋 Breeding Conditions")
    st.info("""
    This section visualizes key environmental factors affecting humpback whale breeding behavior.
    """)
    
    if "df" in st.session_state and not st.session_state.df.empty:
        st.session_state.df = preprocess_data(st.session_state.df, BREEDING_FACTORS)
        
        st.plotly_chart(create_conditions_chart(
            st.session_state.df, 
            BREEDING_FACTORS, 
            "🌊 Breeding Conditions Over Time", 
            {"Temperature": "#ff7f0e", "External pH (Dynamic Salinity)": "#1f77b4", "Oxygen Concentration Corrected": "#2ca02c"}
        ), use_container_width=True)
        st.caption("Graph generated using Plotly (https://plotly.com)")  # Citation for the graph
        
        st.subheader("🐳 How These Factors Affect Whale Breeding")
        st.markdown("""
        ### 🌡️ Temperature: Love in the Warm Waters!
        - Whales migrate to warmer tropical waters to breed. **25°C - 28°C** is the ideal range for calf development! 🐋💙
        
        ### ⚖️ Salinity: Stable Waters for Newborns
        - Higher salinity provides a **stable environment** for newborn calves.
        - It influences **calf buoyancy** and early development. 🌊🍼
        
        ### 🫧 Oxygen Levels: A Breath of Fresh Air
        - Higher oxygen = **better conditions for young whales and mothers**.
        - Oxygen-rich waters **support energy levels** for nursing mothers. 🏊‍♀️🐳
        
        ### 🦐 Can Prey Availability Affect Breeding?
        - If food is scarce, females may **delay pregnancy** or give birth to undernourished calves.
        - Humpbacks prefer areas where **prey is abundant before migration** to store enough energy.
        
        ### 🌊 Why Warmer Waters for Breeding?
        - Warm waters **reduce energy loss** for newborn calves.
        - It minimizes **predator presence**, making it safer for young whales.

        ### 🧐 How Does Ocean Salinity Play a Role?
        - Stable salinity helps newborns **float easily**, reducing energy spent on movement. 🍼🌊  
        - It prevents **dehydration** and ensures smooth **nursing** for calves. 🐳💙  

        ### 🚨 What if Oxygen Levels Drop?
        - **Low oxygen** can cause **stress** for both mother and calf. 😟🫧  
        - Oxygen-rich waters **support high energy needs** for nursing mothers, keeping them **healthy and strong**! 💪🐋  
        """)
    else:
        st.warning("No data available. Ensure the API has fetched data in app.py.")

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
    """Create a combined figure for all environmental parameters.
       Graph generated using Plotly (https://plotly.com)."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["Temperature"],
        name="Temperature (°C)",
        line=dict(color="#FF4B4B", width=2) 
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["External pH (Dynamic Salinity)"],
        name="pH",
        line=dict(color="#36A2EB", width=2),  
        yaxis="y2"
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["Oxygen Concentration Corrected"],
        name="Oxygen (ml/l)",
        line=dict(color="#4BC0C0", width=2),  
        yaxis="y3"
    ))
    
    if "Chlorophyll" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Time (Atlantic)"],
            y=df["Chlorophyll"],
            name="Chlorophyll",
            line=dict(color="#9966FF", width=2), 
            yaxis="y4"
        ))

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

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    
    return fig

def create_simplified_species_chart():
    """Create a simplified bar chart showing species presence by month.
       Graph generated using Plotly (https://plotly.com)."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month = datetime.now().month - 1
    
    colors = {
        'Humpback': '#1f77b4',  
        'Capelin': '#2ca02c',   
        'Krill': '#ff7f0e',     
        'Herring': '#9467bd'    
    }

    fig = go.Figure()

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
            elif current_month in [6, 7, 8]: 
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
    st.markdown("Explore the interactive lifecycle phases of humpback whales. Click on each tab to view details, then use the buttons to learn even more about each phase. (Citations: NOAA Fisheries; Meynecke et al., 2021)")
    
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
        **Reference:** Research reviews (e.g., Meynecke et al., 2021) detail these environmental drivers.
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
        **Reference:** Reviews (e.g., Meynecke et al., 2021) emphasize the importance of these areas for whale recovery.
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
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "ℹ️ About",
            "🌊 Phases",
            "📊 Feeding Conditions",
            "🗓️ Migration Patterns",
            "🐟 Breeding Conditions",
            "📚 Data Sources"
        ])
    
        with tab1:
            st.header("About Humpback Whales")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(
                    IMAGE_PATH,
                    caption="Humpback Whale (Image source: NOAA Fisheries - https://www.fisheries.noaa.gov/species/humpback-whale)",
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
                - 🏷 **Size:** Adults range Up to about 60 feet 
                - ⚖ **Weight:** Can up to about 40 tons  
                - ⌛ **Lifespan:** About 80 to 90 years  
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
            feeding_conditions_page()
    
        with tab4:
            st.plotly_chart(create_simplified_species_chart(), use_container_width=True)
            st.caption("Graph generated using Plotly (https://plotly.com)")  # Citation for the graph
            
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
            breeding_conditions_page()
    
        with tab6:
            st.header("📚 Data Sources")
            st.markdown("""
            ### Useful References
            - **Ocean Networks Canada – API Source:**  
              Main API source for real-time sensor data.  
              [Ocean Networks Canada Data](https://data.oceannetworks.ca/DataPreview?TREETYPE=1&LOCATION=11&TIMECONFIG=0)
              
            - **ONC - Sea-Bird Deep SeapHOx V2 SN 721-2038:**
              
              API source for Integrated CTD pH O2 Instrument.
              
              Citation: Marine Institute of Memorial University. 2022. Conception Bay Integrated CTD pH O2 Instrument Deployed 2022-08-21. Ocean Networks Canada Society. https://doi.org/10.34943/ac118b10-0718-401d-ac27-ca7e7791f458.
              DOI: [10.34943/ac118b10-0718-401d-ac27-ca7e7791f458]
              
            - **ONC - Turner Cyclops-7F Fluorometer (S/N 900143) :**
              
              API source for Fluorometer.
              
              Citation: Marine Institute of Memorial University. 2021. Conception Bay Fluorometer Deployed 2021-02-14. Ocean Networks Canada Society. https://doi.org/10.34943/4cd438cb-64b3-4f3d-ae91-af54a259c145.
              DOI: [10.34943/4cd438cb-64b3-4f3d-ae91-af54a259c145]
              
            - **NOAA Fisheries – Humpback Whale:**  
              Detailed species information including habitat, behavior, and conservation efforts.  
              [NOAA Fisheries - Humpback Whale](https://www.fisheries.noaa.gov/species/humpback-whale)
              
            - **Newfoundland Labrador Whale Watching:**  
              A comprehensive guide to whale watching opportunities and information on local migration patterns.  
              [Whale Watching Newfoundland Labrador](https://www.newfoundlandlabrador.com/things-to-do/whale-watching)
              
            - **Scientific Review:**  
              Meynecke, J-O., et al. (2021). *The Role of Environmental Drivers in Humpback Whale Distribution, Movement and Behavior: A Review*. Frontiers in Marine Science.  
              DOI: [10.3389/fmars.2021.720774](https://doi.org/10.3389/fmars.2021.720774)
            """)
    else:
        st.warning("No data available. Please fetch real-time data using the sidebar controls.")

if __name__ == "__main__":
    migration_page()
