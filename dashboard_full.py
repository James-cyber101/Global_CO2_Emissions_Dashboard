import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load dataset
df = pd.read_csv("cleaned_co2.csv")

# Initialize Dash app
app = Dash(__name__)
app.title = "Global CO2 Emissions Dashboard"

# Chart 1: CO2 Emissions Over Time
fig_total_co2 = px.line(
    df, x="year", y="co2", color="country",
    title="CO2 Emissions Over Time (Selected Countries)"
)

# Chart 2: Top 10 CO2 Emitters in 2022
fig_top_emitters = px.bar(
    df[df['year'] == 2022].sort_values("co2", ascending=False).head(10),
    x="country", y="co2", title="Top 10 CO2 Emitters in 2022"
)

# Chart 3: CO2 vs GDP per Capita (Bubble)
fig_bubble = px.scatter(
    df[df['year'] == 2022],
    x="gdp_per_capita",
    y="co2",
    size="co2",
    color="continent" if 'continent' in df.columns else None,
    hover_name="country",
    title="CO2 Emissions vs GDP per Capita (2022)",
    size_max=60,
    log_x=True
)

# Chart 4: Top 5 CO2 Emitting Sectors in 2022
if 'sector' in df.columns:
    top5_sector = (
        df[df['year'] == 2022]
        .groupby('sector')['co2']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    fig_sector_top5 = px.bar(
        top5_sector,
        x='sector',
        y='co2',
        title='Top 5 CO2 Emitting Sectors in 2022',
        color='sector'
    )
else:
    fig_sector_top5 = px.scatter(title="No sector data available")

# Chart 5: Global CO2 Emissions by Decade
df['decade'] = (df['year'] // 10) * 10
decadal_co2 = df.groupby('decade')['co2'].sum().reset_index()
fig_decadal = px.line(
    decadal_co2,
    x='decade',
    y='co2',
    title='Global CO2 Emissions by Decade'
)

# Dashboard Layout
app.layout = html.Div([
    html.H1("Global CO2 Emissions Dashboard", style={"textAlign": "center"}),

    html.H2("CO2 Emissions Over Time"),
    dcc.Graph(figure=fig_total_co2),

    html.H2("Top 10 CO2 Emitters in 2022"),
    dcc.Graph(figure=fig_top_emitters),

    html.H2("CO2 Emissions vs GDP per Capita"),
    dcc.Graph(figure=fig_bubble),

    html.H2("Top 5 CO2 Emitting Sectors in 2022"),
    dcc.Graph(figure=fig_sector_top5),

    html.H2("Global CO2 Emissions by Decade"),
    dcc.Graph(figure=fig_decadal)
])

# Run server
if __name__ == "__main__":
    app.run(debug=True)

 

