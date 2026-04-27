import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Child Mortality Dashboard",
    layout="wide"
)

df = pd.read_csv("cme_cleaned.csv")

st.title("Child Mortality Analysis Dashboard")
st.markdown(
    "Explore child mortality trends across countries over time, "
    "compare by sex, and identify key patterns in mortality outcomes."
)

st.sidebar.header("Filters")

countries = sorted(df["country"].unique())
selectedCountry = st.sidebar.selectbox("Select Country", countries)

sexOptions = sorted(df["sex"].unique())
selectedSex = st.sidebar.selectbox("Select Sex", sexOptions)

minYear = int(df["year"].min())
maxYear = int(df["year"].max())

selectedYearRange = st.sidebar.slider(
    "Select Year Range",
    min_value=minYear,
    max_value=maxYear,
    value=(minYear, maxYear)
)

rankingYear = st.sidebar.selectbox(
    "Select Ranking Year",
    sorted(df["year"].unique(), reverse=True)
)

rankingType = st.sidebar.selectbox(
    "Top or Bottom Countries",
    ["Top 10", "Bottom 10"]
)

filteredData = df[
    (df["country"] == selectedCountry) &
    (df["sex"] == selectedSex) &
    (df["year"] >= selectedYearRange[0]) &
    (df["year"] <= selectedYearRange[1])
]

st.markdown(
    f"Showing child mortality data for **{selectedCountry}**, **{selectedSex}**, "
    f"from **{selectedYearRange[0]}** to **{selectedYearRange[1]}**. "
    f"Country rankings and the global map use **{rankingYear}**."
)

rankingData = df[
    (df["sex"] == selectedSex) &
    (df["year"] == rankingYear)
]

if rankingType == "Top 10":
    rankingData = rankingData.sort_values("obs value", ascending=False).head(10)
else:
    rankingData = rankingData.sort_values("obs value", ascending=True).head(10)

if selectedSex == "Female":
    mainColor = "#E75480"
elif selectedSex == "Male":
    mainColor = "#4F81BD"
else:
    mainColor = "#2FA13D"

mapData = df[
    (df["sex"] == selectedSex) &
    (df["year"] == rankingYear)
]

if not filteredData.empty:
    firstYear = filteredData["year"].min()
    latestYear = filteredData["year"].max()

    firstValue = filteredData.loc[
        filteredData["year"] == firstYear, "obs value"
    ].values[0]
    latestValue = filteredData.loc[
        filteredData["year"] == latestYear, "obs value"
    ].values[0]

    absoluteChange = latestValue - firstValue

    if firstValue != 0:
        percentageChange = ((latestValue - firstValue) / firstValue) * 100
    else:
        percentageChange = 0

    countryCount = rankingData["country"].nunique()

    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latest Child Mortality Rate", round(latestValue, 2))
    col2.metric("Absolute Change Over Period", round(absoluteChange, 2))
    col3.metric("Percentage Change Over Period", f"{round(percentageChange, 2)}%")
    col4.metric("Countries in Ranking Year", countryCount)

    trendChart = px.line(
        filteredData,
        x="year",
        y="obs value",
        title=f"Child Mortality Trend in {selectedCountry} ({selectedSex})"
    )
    trendChart.update_traces(line_color=mainColor)
    trendChart.update_layout(
        xaxis_title="Year",
        yaxis_title="Child Mortality Rate"
    )

    rankingChart = px.bar(
        rankingData,
        x="country",
        y="obs value",
        title=f"{rankingType} Child Mortality Rates in {rankingYear} ({selectedSex})"
    )
    rankingChart.update_traces(marker_color=mainColor)
    rankingChart.update_layout(
        xaxis_title="Country",
        yaxis_title="Child Mortality Rate"
    )

    sexComparisonData = df[
        (df["country"] == selectedCountry) &
        (df["year"] >= selectedYearRange[0]) &
        (df["year"] <= selectedYearRange[1])
    ]

    sexComparisonChart = px.line(
        sexComparisonData,
        x="year",
        y="obs value",
        color="sex",
        title=f"Child Mortality by Sex in {selectedCountry}",
        color_discrete_map={
            "Female": "#E75480",
            "Male": "#4F81BD",
            "Total": "#2FA13D"
        }
    )
    sexComparisonChart.update_layout(
        xaxis_title="Year",
        yaxis_title="Child Mortality Rate"
    )

    uncertaintyData = filteredData.copy()

    uncertaintyChart = go.Figure()

    uncertaintyChart.add_trace(go.Scatter(
        x=uncertaintyData["year"],
        y=uncertaintyData["upper bound"],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))

    uncertaintyChart.add_trace(go.Scatter(
        x=uncertaintyData["year"],
        y=uncertaintyData["lower bound"],
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        name="Uncertainty Range",
        hoverinfo="skip"
    ))

    uncertaintyChart.add_trace(go.Scatter(
        x=uncertaintyData["year"],
        y=uncertaintyData["obs value"],
        mode="lines",
        name="Observed Value",
        line=dict(color=mainColor)
    ))

    uncertaintyChart.update_layout(
        title=f"Mortality Rate and Uncertainty in {selectedCountry} ({selectedSex})",
        xaxis_title="Year",
        yaxis_title="Child Mortality Rate"
    )

    row1Col1, row1Col2 = st.columns(2)
    with row1Col1:
        st.plotly_chart(trendChart, width="stretch")
    with row1Col2:
        st.plotly_chart(rankingChart, width="stretch")

    row2Col1, row2Col2 = st.columns(2)
    with row2Col1:
        st.plotly_chart(sexComparisonChart, width="stretch")
    with row2Col2:
        st.plotly_chart(uncertaintyChart, width="stretch")

    st.subheader("Global Child Mortality Map")

    mapChart = px.choropleth(
        mapData,
        locations="country",
        locationmode="country names",
        color="obs value",
        hover_name="country",
        title=f"Global Child Mortality Rates in {rankingYear} ({selectedSex})",
        labels={"obs value": "Child Mortality Rate"}
    )

    st.plotly_chart(mapChart, width="stretch")

else:
    st.warning("No data available for the selected filters.")