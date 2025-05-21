import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.figure_factory import create_table
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Global Health Trends Data Visualization", layout="wide")

# Page title
st.title("Global Health and Development Dashboard")

# Load datasets
gapminder = px.data.gapminder()
child_mortality = pd.read_csv("child_mortality_0_5_year_olds_dying_per_1000_born.csv")

# Merge child mortality with gapminder
child_mortality_long = child_mortality.melt(id_vars=["country"], var_name="year", value_name="childMortality")
child_mortality_long["year"] = child_mortality_long["year"].astype(int)
gapminder_cm = pd.merge(gapminder, child_mortality_long, on=["country", "year"], how="left")

# Intro context
st.markdown("""
Welcome to the Global Health and Development Dashboard!  
This interactive app explores trends in life expectancy, child mortality, GDP per capita, and population  
using the Gapminder and child mortality datasets. Use the visualizations below to identify global patterns  
and gain insights into health and development across regions and time.
""")

# Visualization 1: Table of Gapminder Data
st.subheader("📋 Merged Dataset Table")
st.markdown("""
This table combines key indicators from the Gapminder dataset with child mortality data,  
providing a comprehensive view of each country's health and economic conditions over time.
""")
table = create_table(gapminder_cm.head(10))
st.plotly_chart(table, use_container_width=True)


# Visualization 2: Dropdown Line Plot for Life Expectancy
st.subheader("📈 Life Expectancy Trends Over Time")
st.markdown("""
This line chart shows the evolution of life expectancy across selected countries.  
It highlights improvements in global health and helps compare how different nations have progressed.
""")
countries = gapminder["country"].unique()
traces = []
buttons = []

for i, country in enumerate(countries):
    country_df = gapminder[gapminder["country"] == country]
    trace = go.Scatter(
        x=country_df["year"],
        y=country_df["lifeExp"],
        mode="lines+markers",
        name=country,
        visible=(country == "Afghanistan"),
    )
    traces.append(trace)
    button = dict(
        label=country,
        method="update",
        args=[{"visible": [j == i for j in range(len(countries))]},
              {"title": f"Life Expectancy Over Time: {country}"}]
    )
    buttons.append(button)

layout = go.Layout(
    title="Life Expectancy Over Time: Afghanistan",
    updatemenus=[
        dict(
            active=0,
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            x=0.0,
            xanchor="left",
            y=1.2,
            yanchor="top",
            showactive=True
        )
    ],
    xaxis=dict(title="Year"),
    yaxis=dict(title="Life Expectancy")
)

fig_line = go.Figure(data=traces, layout=layout)
st.plotly_chart(fig_line, use_container_width=True)

# Visualization 3: Scatter Plot (GDP vs Child Mortality)
st.subheader("💸 GDP vs Child Mortality")
st.markdown("""
This scatter plot compares GDP per capita with child mortality rates over time.  
It helps visualize the correlation between a country's wealth and child health outcomes.
""")
fig_scatter = px.scatter(
    gapminder_cm,
    x="gdpPercap",
    y="childMortality",
    color="continent",
    size="pop",
    size_max=60,
    hover_name="country",
    animation_frame="year",
    animation_group="country",
    log_x=True,
    range_x=[100, 100000],
    range_y=[0, 400],
    labels={"pop": "Population", "gdpPercap": "GDP per Capita", "childMortality": "Child Mortality(per 1,000 births 0-5 years)"},
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Visualization 4: Choropleth Map (Child Mortality)
st.subheader("🗺️ Global Child Mortality Map")
st.markdown("""
This choropleth map displays child mortality rates across the globe for a given year.  
Darker colors indicate higher child mortality, allowing users to identify regions needing attention.
""")
fig_choropleth = px.choropleth(
    gapminder_cm,
    locations="iso_alpha",
    color="childMortality",
    hover_name="country",
    animation_frame="year",
    color_continuous_scale=px.colors.sequential.Plasma,
    projection="natural earth"
)
st.plotly_chart(fig_choropleth, use_container_width=True)