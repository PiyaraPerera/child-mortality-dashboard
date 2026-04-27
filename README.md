# Child Mortality Analysis Dashboard

This repository contains my coursework project for the **5DATA004C Data Science Project Lifecycle** module. The project explores child mortality trends across countries over time using an interactive **Streamlit dashboard**.

## Project Overview

The dashboard analyses child mortality data by:
- country
- sex
- year
- mortality rate
- lower and upper uncertainty bounds

It allows users to explore long-term trends, compare countries, examine sex-based differences, and view global mortality patterns through interactive charts and filters.

## Dashboard Features

The Streamlit dashboard includes:
- country filter
- sex filter
- year range filter
- ranking year filter
- top/bottom country selector

It also includes:
- KPI cards
- child mortality trend chart
- country ranking bar chart
- sex comparison chart
- uncertainty chart
- global choropleth map

## Files Included

- `app/streamlit_app.py` – main Streamlit dashboard application
- `data/raw/` – original raw dataset
- `data/cleaned/cme_cleaned.csv` – cleaned dataset used in the dashboard
- `notebooks/data_cleaning.ipynb` – notebook used for data cleaning and preparation
- `requirements.txt` – Python libraries required to run the project

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## How to Run the App

1. Clone or download this repository  
2. Install the required libraries:

```bash
pip install -r requirements.txt
