# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import openpyxl
#from matplotlib import pyplot as plt
import numpy as np
import dash
import datetime
from datetime import date,timedelta
import os
import seaborn as sns
from plotly.subplots import make_subplots


stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.FONT_AWESOME],
)
server = app.server
df = pd.read_excel('wfp.xlsx', engine='openpyxl')
#df["date"] = pd.to_datetime(df["date"])
data = pd.read_excel('wfp.xlsx', engine='openpyxl')
data = pd.DataFrame(data)
data = data.drop([0])


series = df['admin1'].value_counts()
series2 = df['admin2'].value_counts()
series3 = df['market'].value_counts()
series4 = df['commodity'].value_counts()

df_result = pd.DataFrame(series)
df_result2 = pd.DataFrame(series2)
df_result3 = pd.DataFrame(series3)
df_result4 = pd.DataFrame(series4)

df_result = df_result.reset_index()
df_result2 = df_result2.reset_index()
df_result3 = df_result3.reset_index()
df_result4 = df_result4.reset_index()

df_result.columns = ['admin1', 'Total']
df_result2.columns = ['admin2', 'Total']
df_result3.columns = ['market', 'Total']
df_result4.columns = ['commodity', 'Total']

#Pie Chart

fig1 = px.pie(df_result,
             values='Total',
             names='admin1',
             labels='admin1',
             title='Pie Chart for Market Data Proportions Based on Adminstrative Region1 ')

fig12 = go.Figure(data=[go.Bar(x=df_result4['commodity'], y=df_result4['Total'], text=df_result4['commodity'], orientation='v')])

#Donut Chart
# Create a figure with a donut chart
fig2 = go.Figure(data=[go.Pie(values=df_result2['Total'], labels=df_result2['admin2'], hole=0.5)])

# Add a title and labels
fig2.update_layout(title='Administrative Region 2 Data Proportions ', xaxis_title='x', yaxis_title='y', height=600)


# Create a figure with a bar chart
fig3 = go.Figure(data=[go.Bar(x=df_result3['market'], y=df_result3['Total'], text=df_result3['market'], orientation='v')])

# Add a title and labels
fig3.update_layout(title='Bar Chart on Major Market Proportions Data', xaxis_title='', yaxis_title='Total', height=800)




data['date'] = pd.to_datetime(data['date'])

data = data.query("unit == 'KG'")
#maize
data = data.query("commodity == 'Maize'")

#-forecast
data = data.query("priceflag == 'actual'")



#Linechart

fig = px.line(data, x="date", y="price", color="market", hover_name="market", title= "Maize Price Series", height=800)

data = data.query("market == 'Nairobi'")

fig14 = px.area(data, x="date", y="price", color="market", hover_name="market", title= "Nairobi Maize Price Series")
fig15 = px.scatter(data, x="date", y="price", color="market", hover_name="market", title= "Nairobi Maize Price Series", trendline="ols", trendline_scope="overall")


"""
==========================================================================
Markdown Text
"""

datasource_text = dcc.Markdown(
    """
    [Data source:](https://data.humdata.org/dataset/wfp-food-prices-for-kenya?force_layout=desktop)
    Kenya - Food PricesThis dataset contains Food Prices data for Kenya, sourced from the World Food Programme Price Database.
    The World Food Programme Price Database covers foods such as maize, rice, beans, fish, and sugar for 98 countries and some 3000 markets.
    It is updated weekly but contains to a large extent monthly data.
     The data goes back as far as 1992 for a few countries, although many countries started reporting from 2003 or thereafter.
    """
)

Introduction_text = dcc.Markdown(
    """
    The dashboard provides an overview of price trends across multiple regions in Kenya, enabling us to analyze price movements over time and identify contrasts in price changes across various markets.
    By examining the data, we can gain valuable insights into the performance of different commodities and make informed decisions based on the latest market trends.
    
    Objectives
    
    ⦁	 Get a visual analysis of regional market sizes.
    
    ⦁	Study the trends in prices for commodities across time.
    
    ⦁	Attempt a forecast on the changes in market prices.
    
    ⦁	Understand the dynamics of price movements relative to time.  

    """
)

Visual_Report_text = dcc.Markdown(
    """
    For our dataset, the first administrative region has the highest collective representation and supersedes all other regions in terms of geographic distribution of food. 
    The rift valley accounts for the largest share of the market data, with approximately 38% of the total. 
    This suggests that the region is a significant producer of food and has a substantial impact on the subsequent administrative tiers and local markets within the region.
    """
)
Visual_Report_text_b = dcc.Markdown(
    """
    The second administrative tier displays a higher level of refinement in its geographic representation, with smaller regions within the tier. 
    Nairobi takes the lead with a significant representation of approximately 28%, according to our data. 
    A unique perspective could suggest that the Rift Valley region from the first administrative tier has a higher aggregate representation in the second administrative region. 
    Nairobi is followed closely by Turkana, Garissa, and Mombasa with notable data output.
    """
)



Timeseries_text = dcc.Markdown(
    """
> In this section, our main goal is to study the price trends of commodities, focusing on Maize in Kenya.
  Maize is essential in agriculture and widely consumed in households. The study aims to uncover patterns in prices over the past few years and understand if there are predictable changes.
  Given Maize's importance as a staple food, understanding what influences its prices is crucial.

> We're not only looking at one market but exploring different regions, comparing pricing behaviors.
 Through careful time series analysis, our goal is to provide detailed insights into the Maize market, enhancing our understanding of its trends and regional differences.
"""
)
Timeseries2_text = dcc.Markdown(
    """
>  Based on our case study, it appears that Nairobi dominates the market share of commodities for our dataset, followed by Eldoret. 
 The significant proportion of commodities traded in Nairobi suggests that it is an ideal destination for marketing solutions, which can be attributed to its large population and well-developed network infrastructure that connects buyers and sellers.

"""
)

analysis_text = dcc.Markdown(
    """
    Using the visual analysis,it appears that Nairobi is the dominant region for market activity and administration, and maize is the dominant crop with a significant proportion of the market share. 
    Additionally, there is a positive relationship between price changes and time for maize in Nairobi, with some outliers detected in 2017 that may indicate an abnormal increase in price followed by a slump. 
    Further confirmation is needed to fully understand these price fluctuations.

    """
)
analysis2_text = dcc.Markdown(
    """
    From the time series graph, it appears that the prices of maize in the 5 major markets in Kenya have been relatively similar in terms of changes  over the period from 2006 to 2023. 
    However, there are some noticeable differences between the lowest and highest performing markets. 
    Specifically, Nakuru consistently had the lowest prices for a kilo of maize, while prices in Kisumu were significantly higher.

    """
)

forecast_text = dcc.Markdown(
    """
    forecast stuff
    """
)

Summary_text = dcc.Markdown(
    """
    To summarize the project, we have successfully extracted valuable insights from our data, providing a visual representation of the distribution of commodities across two administrative regions and markets. 
    Our timeseries data has enabled us to analyze changes in prices over time and identify events, cycles, or seasons that influence these changes. 
    Additionally, we have explored the market volumes of commodities, laying the groundwork for more dynamic and interactive data exploration. 
    Our next step is to enhance user interactivity with the data, allowing for more in-depth analysis and exploration of our datasets. This will enable us to fully leverage the rich content of our data and improve our analyses.
    """
)

footer = html.Div(
    dcc.Markdown(
        """
         This information is intended solely as general information for educational
        and entertainment purposes only and is not a substitute for professional advice and
        services from qualified financial services providers familiar with your financial
        situation.
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)
Introduction_card = dbc.Card(
    [
        dbc.CardHeader("Report Analysis on Kenyan Food Market"),
        dbc.CardBody(Introduction_text),
    ],
    className="mt-4",
)

Visual_Report_card = dbc.Card(
    [
        dbc.CardHeader("Visual Analysis of the Report"),
        dbc.CardBody(Visual_Report_text),
        dcc.Graph(id="fig1", figure=fig1, className="mb-2"),
        dbc.CardBody(Visual_Report_text_b),
        dcc.Graph(id="fig2", figure=fig2, className="mb-2"),
        dbc.CardBody(Visual_Report_text_b),
        dcc.Graph(id="fig12", figure=fig12, className="mb-2"),
    ],
    className="mt-4",
)

Summary_card = dbc.Card(
    [
        dbc.CardHeader("Report Summary"),
        dbc.CardBody(Summary_text),
    ],
    className="mt-4",
)

timeseries_card = dbc.Card(
    [
        dbc.CardHeader("Analysis"),
        dbc.CardBody(Timeseries_text),
        dcc.Graph(id="fig14", figure=fig14, className="mb-2"),
        dbc.CardBody(analysis_text),
        dcc.Graph(id="fig15", figure=fig15, className="mb-2"),
    ],
    className="mt-4",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(Introduction_card, tab_id="tab-1", label="Introduction"),
        dbc.Tab(Visual_Report_card, tab_id="tab-1", label="Visual Analysis"),
        dbc.Tab(
            [timeseries_card, forecast_text],
            tab_id="tab-3",
            label="Timeseries Analysis",
            className="pb-4",
        ),
        dbc.Tab(Summary_card, tab_id="tab-3", label="Summary"),
    ],
    id="tabs",
    active_tab="tab-2",
    className="mt-2",
)

navbar = dbc.NavbarSimple(
brand='Attain Solutions Ltd',
brand_style={'fontSize': 40, 'color': 'white'},
children=html.A('Data Source',
href='https://data.humdata.org/dataset/wfp-food-prices-for-kenya?force_layout=desktop',
target='_blank',
style={'textAlign':'center','color': 'black'}),
color='primary',
fluid=True,
sticky='top'
)

dropdown = dcc.Dropdown(
    id="dropdown",
    multi=True,
    options=[
        {"label": x, "value": x}
        for x in sorted(df["market"].unique())
    ],
    value="market",
)
"""
===========================================================================
Main Layout
"""

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Kenya Food Market Report",
                    className="text-center bg-primary text-white p-2",
                ),
            )
        ),
        dbc.Row(dbc.Col(dropdown)),
        dbc.Row(
            [
                dbc.Col(tabs, width=12, lg=5, className="mt-4 border"),
                dbc.Col(
                    [
                     dcc.Graph(id="fig3", figure=fig3, className="mb-2"),
                     dbc.CardBody(Timeseries2_text),
                     dcc.Graph(id="fig", figure=fig, className="mb-2"),
                     dbc.CardBody(analysis2_text),
                    ],
                    width=12,
                    lg=7,
                ),
            ],
            className="ms-1",
        ),
        dbc.Row(dbc.Col(footer)),
    ],
    fluid=True,
)

# Callbacks ***************************************************************
@app.callback(
    Output(component_id="fig1", component_property="figure"),
    [Input(component_id="dropdown", component_property="value")],
)
def update_graph(chosen_value):
    print(f"Values chosen by user: {chosen_value}")

    if len(chosen_value) == 0:
        return {}
    else:
        df_filtered = df[df["market"].isin(chosen_value)]
        fig = px.line(
            data_frame=df_filtered,
            x="date",
            y="price",
            color="market",
            log_y=True,
            labels={
                "price": "price",
                "dates": "dates",
                "market": "market",
            },
        )
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)