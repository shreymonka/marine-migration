# Whale Watch Dashboard

**Whale Watch** is an interactive Streamlit dashboard designed to monitor humpback whale migration patterns, feeding conditions, and breeding behaviors in Holyrood waters. The dashboard integrates real-time sensor data, historical migration information, and species data sourced from organizations such as Ocean Networks Canada, DFO Canada, and Memorial University Research.

## Live Site

[Whale Watch Dashboard](https://whale-watch-sd.streamlit.app/)

## Features

- **Interactive Tabs:**
  - **About Humpback Whales:** Provides an overview, key characteristics, and interesting facts about humpback whales.
  - **Lifecycle Phases:** Detailed insights into the breeding, feeding, migration, and resting phases.
  - **Feeding Conditions:** Visualizations of key environmental factors (e.g., chlorophyll, pH, temperature) that influence feeding behavior.
  - **Migration Patterns:** Dynamic charts showing species presence and seasonal migration trends.
  - **Breeding Conditions:** Graphs and analysis of environmental parameters affecting breeding.
  - **Data Sources:** A dedicated section listing useful references and citations.

- **Dynamic Visualizations:**
  - Uses Plotly to generate interactive time-series and bar charts.
  - Responsive design ensures the dashboard works well on both desktop and mobile devices.

- **Real-Time Data Integration:**
  - Leverages real-time sensor data from Ocean Networks Canada and historical datasets for comprehensive analysis.

## Installation

To run the dashboard locally, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/shreymonka/whale-watch.git
    cd whale-watch-dashboard
    ```

2. **Create a Virtual Environment and Install Dependencies:**

    ```bash
    python -m venv venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Run the Dashboard:**

    ```bash
    streamlit run app.py
    ```

## Technologies Used

- **Streamlit:** Framework for building the interactive dashboard.
- **Plotly:** Library for creating dynamic charts and visualizations.  
  *(Graphs are generated using Plotly: [Plotly Official Site](https://plotly.com))*
- **Pandas & NumPy:** Tools for data manipulation and processing.
- **Python:** Core programming language used in the project.

## Data Sources and References

- **Ocean Networks Canada:**  
  Real-time sensor data and oceanographic measurements used in this project are provided by [Ocean Networks Canada](https://data.oceannetworks.ca/DataPreview?TREETYPE=1&LOCATION=11&TIMECONFIG=0).

- **NOAA Fisheries – Humpback Whale:**  
  Provides detailed species information including habitat, behavior, and conservation efforts.  
  [NOAA Fisheries - Humpback Whale](https://www.fisheries.noaa.gov/species/humpback-whale)  

- **Newfoundland Labrador Whale Watching:**  
  A comprehensive guide to whale watching opportunities and information on local migration patterns.  
  [Whale Watching Newfoundland Labrador](https://www.newfoundlandlabrador.com/things-to-do/whale-watching)

- **Scientific Review:**  
  Meynecke, J-O., et al. (2021). *The Role of Environmental Drivers in Humpback Whale Distribution, Movement and Behavior: A Review*. Frontiers in Marine Science.  
  DOI: [10.3389/fmars.2021.720774](https://doi.org/10.3389/fmars.2021.720774)

- **Plotly:**  
  Used for generating interactive charts.  
  [Plotly Official Site](https://plotly.com)


