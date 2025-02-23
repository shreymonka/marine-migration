import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Updated PREY_DATA to include chlorophyll preferences
PREY_DATA = {
    "Capelin": {
        "temp_range": {"min": 2, "max": 12},
        "chlorophyll_range": {"min": 0.5, "max": 3.0},
        "peak_season": "June-July"
    },
    "Krill": {
        "temp_range": {"min": -1.5, "max": 10},
        "chlorophyll_range": {"min": 1.0, "max": 5.0},
        "peak_season": "April-September"
    },
    "Herring": {
        "temp_range": {"min": 4, "max": 15},
        "chlorophyll_range": {"min": 0.3, "max": 2.5},
        "peak_season": "May-June & Aug-Sep"
    }
}

def create_environmental_figure(df):
    """Create a multi-parameter environmental conditions figure"""
    fig = go.Figure()
    
    # Temperature trace
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["Temperature"],
        name="Temperature (°C)",
        line=dict(color="#82ca9d", width=2)
    ))
    
    # pH trace
    fig.add_trace(go.Scatter(
        x=df["Time (Atlantic)"],
        y=df["External pH (Dynamic Salinity)"],
        name="pH",
        line=dict(color="#8884d8", width=2),
        yaxis="y2"
    ))
    
    # Chlorophyll trace
    if "Chlorophyll" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Time (Atlantic)"],
            y=df["Chlorophyll"],
            name="Chlorophyll (mg/m³)",
            line=dict(color="#ff7f0e", width=2),
            yaxis="y3"
        ))

    # Update layout
    fig.update_layout(
        title="Environmental Parameters Affecting Whale Migration",
        xaxis=dict(title="Time"),
        yaxis=dict(
            title="Temperature (°C)",
            tickfont=dict(color="#82ca9d")
        ),
        yaxis2=dict(
            title="pH",
            tickfont=dict(color="#8884d8"),
            anchor="free",
            overlaying="y",
            side="right",
            position=0.85
        ),
        yaxis3=dict(
            title="Chlorophyll (mg/m³)",
            tickfont=dict(color="#ff7f0e"),
            anchor="free",
            overlaying="y",
            side="right",
            position=1.0
        ),
        showlegend=True,
        height=600
    )
    
    return fig

def analyze_chlorophyll_impact(chlorophyll_level):
    """Analyze impact of chlorophyll levels on whale presence"""
    if chlorophyll_level > 2.0:
        return {
            "status": "High",
            "description": "Strong correlation with whale presence - Prime feeding conditions",
            "color": "success"
        }
    elif chlorophyll_level > 0.5:
        return {
            "status": "Moderate",
            "description": "Moderate feeding probability - Some whale activity expected",
            "color": "warning"
        }
    else:
        return {
            "status": "Low",
            "description": "Limited feeding opportunities - Reduced whale presence likely",
            "color": "error"
        }

def show_environmental_metrics(df):
    """Display environmental metrics including chlorophyll"""
    cols = st.columns(4)
    
    metrics = {
        "pH Levels": "External pH (Dynamic Salinity)",
        "Temperature (°C)": "Temperature",
        "Oxygen (ml/l)": "Oxygen Concentration Corrected",
        "Chlorophyll (mg/m³)": "Chlorophyll"
    }
    
    for i, (label, column) in enumerate(metrics.items()):
        if column in df.columns:
            with cols[i]:
                mean_val = df[column].mean()
                min_val = df[column].min()
                max_val = df[column].max()
                if pd.notna(mean_val):
                    st.metric(
                        label=label,
                        value=f"{mean_val:.2f}",
                        delta=f"Range: {min_val:.2f} - {max_val:.2f}"
                    )

def show_chlorophyll_analysis(df):
    """Display detailed chlorophyll analysis"""
    st.subheader("🌿 Chlorophyll Impact Analysis")
    
    if "Chlorophyll" in df.columns:
        try:
            current_level = df['Chlorophyll'].iloc[-1]
            if pd.notna(current_level):
                impact = analyze_chlorophyll_impact(current_level)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"""
                    **Current Chlorophyll Level:** {current_level:.2f} mg/m³
                    
                    **Impact Status:** {impact['status']}
                    
                    **Analysis:** {impact['description']}
                    """)
                    
                with col2:
                    st.info("""
                    **Research Findings:**
                    - High chlorophyll areas strongly correlate with increased whale presence
                    - 2-3 week lag observed between chlorophyll peaks and whale arrival
                    - Chlorophyll concentration above 2.0 mg/m³ indicates potential feeding grounds
                    - Temporal and spatial variations affect whale distribution patterns
                    """)
            else:
                st.warning("Current chlorophyll data is not available.")
        except Exception as e:
            st.warning(f"Unable to perform chlorophyll analysis: {str(e)}")
    else:
        st.warning("Chlorophyll data is not available in the current dataset.")

def show_migration_pattern_analysis(df):
    """Show migration patterns with environmental correlations"""
    st.subheader("🐋 Migration Pattern Analysis")
    
    try:
        # Select environmental parameters for correlation
        params = ['Temperature', 'External pH (Dynamic Salinity)', 
                 'Oxygen Concentration Corrected']
        if 'Chlorophyll' in df.columns:
            params.append('Chlorophyll')
            
        # Create correlation matrix
        corr_data = df[params].corr()
        
        fig = px.imshow(corr_data,
                       labels=dict(color="Correlation"),
                       color_continuous_scale="RdBu",
                       title="Environmental Parameter Correlations")
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        ### Key Migration Indicators:
        - 🌿 **Chlorophyll Levels**: Primary indicator of potential feeding grounds
        - 🌡️ **Temperature**: Influences prey distribution and whale comfort
        - 🌊 **Ocean Chemistry**: pH and oxygen affect prey availability
        """)
    except Exception as e:
        st.warning("Unable to perform correlation analysis due to insufficient data.")

def create_simplified_species_chart():
    """Create a simplified bar chart showing species presence by month"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month = datetime.now().month - 1
    
    colors = {
        'Humpback': '#1f77b4',
        'Chlorophyll': '#2ecc71',
        'Krill': '#ff7f0e',
        'Herring': '#9467bd'
    }

    fig = go.Figure()

    species_data = [
        ('🐋 Humpback Whales', [0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0], 'Humpback'),
        ('🌿 Chlorophyll Levels', [1, 1, 1, 3, 3, 2, 1, 1, 1, 1, 1, 1], 'Chlorophyll'),
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
        title="Species Presence and Chlorophyll Levels Throughout the Year",
        xaxis_title="Month",
        yaxis=dict(
            title="Presence Level",
            ticktext=['Absent', 'Low', 'Medium', 'High'],
            tickvals=[0, 1, 2, 3]
        ),
        barmode='group',
        height=500,
        showlegend=True
    )

    fig.add_vline(
        x=current_month,
        line_dash="dash",
        line_color="red",
        annotation_text="Current Month",
        annotation_position="top"
    )

    return fig

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

def migration_page():
    """Main migration page with enhanced chlorophyll analysis"""
    st.title("🐋 Humpback Whale Migration Dashboard")
    
    st.info("""
    This dashboard provides insights into humpback whale migration patterns and environmental conditions 
    in Holyrood waters. The data combines real-time measurements with historical migration patterns, 
    including chlorophyll analysis based on recent research findings.
    """)

    df = st.session_state.df if "df" in st.session_state else pd.DataFrame()

    if not df.empty:
        tab1, tab2, tab3 = st.tabs(["📊 Environmental Conditions", "🗓️ Migration Patterns", "🔍 Detailed Analysis"])

        with tab1:
            st.plotly_chart(create_environmental_figure(df), use_container_width=True)
            show_environmental_metrics(df)
            show_chlorophyll_analysis(df)

        with tab2:
            st.plotly_chart(create_simplified_species_chart(), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### Environmental Influence Guide
                - **High Impact**: Strong correlation with whale presence
                - **Moderate Impact**: Some influence on behavior
                - **Low Impact**: Limited effect on distribution
                """)
            with col2:
                st.markdown("""
                ### Peak Activity Periods
                - 🐋 **Whales**: June - August
                - 🌿 **Chlorophyll Peaks**: April - June
                - 🦐 **Prey Abundance**: Follows chlorophyll by 2-3 weeks
                """)

        with tab3:
            show_migration_pattern_analysis(df)
            
            st.markdown("""
            ### Research-Based Insights
            
            Based on the analyzed research paper, there are several key findings regarding 
            chlorophyll's influence on humpback whale migration:
            
            1. **Feeding Areas:**
               - Strong preference for upwelling regions
               - High chlorophyll-a concentration correlates with prey abundance
               - Optimal feeding conditions in areas with chlorophyll > 2.0 mg/m³
            
            2. **Migration Timing:**
               - Temporal lag between chlorophyll peaks and whale arrival
               - Seasonal patterns influenced by primary productivity
               - Regional variations in feeding ground selection
            
            3. **Environmental Factors:**
               - Combined effect of temperature and chlorophyll
               - Influence of ocean currents on productivity zones
               - Impact of seasonal environmental changes
            """)
    else:
        st.warning("No data available. Please fetch real-time data using the sidebar controls.")

    st.markdown("""
    ---
    ### Data Sources
    - 📊 Real-time sensor data from Ocean Networks Canada
    - 🔬 Migration patterns from DFO Canada
    - 🎓 Species data from Memorial University Research
    - 📚 Chlorophyll analysis based on peer-reviewed research
    
    *Note: Migration patterns are general guidelines and may vary based on local conditions.*
    """)

if __name__ == "__main__":
    migration_page()