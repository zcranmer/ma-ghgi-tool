# -*- coding: utf-8 -*-
"""
Main file in public dashboard tool
MA Greenhouse Gas Inventory Tool
"""

import os
import streamlit as st
import pandas as pd
#import numpy as np
import pydeck
import json
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

start_year = 2019
end_year = 2021

st.set_page_config(
    page_title='MA GHGI Tool')

st.title('Municipal Greenhouse Gas Inventory Tool')

#@st.cache_data
def load_data():
    df = pd.read_excel('datasets/municipal_emissions.xlsx')
    df = df.drop(columns=['Unnamed: 0'])
    gdf = json.load(open('datasets/municipalities.json'))
    return df,gdf

dataset, geo = load_data()
dataset = dataset[dataset['Year']>start_year-1]
dataset['Per Capita (CO2e)'] = dataset['Total (CO2e)']/dataset['Population']

municipality = st.sidebar.selectbox(
    'Which city or town would you like to explore?',
    dataset['Municipality'].unique())

st.session_state.key = municipality
subset = dataset[dataset['Municipality']==municipality]

year = st.sidebar.slider('Choose a year',
                         min_value=start_year,max_value=end_year,
                         value=2021)

year_set = subset[subset['Year']==year]
dataset_year = dataset[dataset['Year']==year]

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Overview','Demographics',
                                        'Residential Buildings','Commercial Buildings',
                                        'Transportation','Waste','Massachusetts'])

with tab1:
    st.header('Overview of Emissions')
    
    # Line graph of total emissions and emission per capita
    # make the figure
    fig = make_subplots(specs=[[{'secondary_y':True}]])
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Total (CO2e)'].round(0),name='Total CO2e'),
        secondary_y=False)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Per Capita (CO2e)'].round(2),name='Per Capita CO2e'),
        secondary_y=True)
    fig.update_layout(title_text='Emissions in '+municipality)
    fig.update_yaxes(title_text='Total CO2e',secondary_y=False)
    fig.update_yaxes(title_text='Per Capita CO2e',secondary_y=True)
    fig.update_xaxes(title_text='Year',tickvals=list(range(start_year,end_year+1)))
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x')
    st.plotly_chart(fig)

    # emissions by fuel pie chart
    graph_cols = ['Total Electricity (CO2e)','Total Gas (CO2e)',
                  'Total Fuel Oil (CO2e)','Total Propane (CO2e)',
                  'Total Gasoline (CO2e)']

    year_sub = year_set[graph_cols].T
    year_sub = year_sub.rename(columns={year_sub.columns[0]:'Emissions'},
                               index={'Total Electricity (CO2e)':'Electricity',
                                      'Total Gas (CO2e)':'Natural Gas',
                                         'Total Fuel Oil (CO2e)':'Fuel Oil',
                                         'Total Propane (CO2e)':'Propane',
                                         'Total Gasoline (CO2e)':'Gasoline'}
                               )
    year_sub = year_sub.reset_index()
    fig = px.pie(year_sub.round(0),values='Emissions',names='index',
                 title='Share of emissions by fuel in MTCO2e')
    fig.update_traces(textposition='outside',textinfo='percent+label+value')
    fig.layout.update(showlegend=False)
    st.plotly_chart(fig)

    graph_cols = ['Total Residential Buildings (CO2e)',
                  'Total Commercial & Industrial Buildings (CO2e)',
                  'Total Transportation (CO2e)']

    year_sub = year_set[graph_cols].T
    year_sub = year_sub.rename(columns={year_sub.columns[0]:'Emissions'},
                               index={'Total Residential Buildings (CO2e)':'Residential',
                                  'Total Commercial & Industrial Buildings (CO2e)':'Commercial & Industrial',
                                  'Total Transportation (CO2e)':'Transportation'}
                               )
    year_sub = year_sub.reset_index()
    fig = px.pie(year_sub.round(0),values='Emissions',names='index',
                 title='Share of emissions by sector in MTCO2e')
    fig.update_traces(textposition='outside',textinfo='percent+label+value')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig)

with tab2:
    st.header('Demographics')
    
   # Population    
    fig = px.line(subset,x='Year',y='Population',title='Population in '+municipality)
    fig.update_layout(yaxis_title='people')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    # Number of households
    fig = px.line(subset,x='Year',y='Total Heating Fuels Households',title='Households in '+municipality)
    fig.update_layout(yaxis_title='Occupied Households')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    # Median household income
    fig = px.line(subset,x='Year',y='Median household income',title='Median Household Income in '+municipality)
    fig.update_layout(yaxis_title='$')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    st.write('Data sources: U.S. Census Bureau')
    
with tab3:
    st.header('Residential Building Emissions')
    
    # Residential fuel emissions pie chart
    graph_cols = ['Residential Electricity (CO2e)','Residential Gas (CO2e)',
                  'Residential Fuel Oil (CO2e)','Residential Propane (CO2e)']

    rf_year_sub = year_set[graph_cols].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Electricity (CO2e)':'Electricity',
                                      'Residential Gas (CO2e)':'Natural Gas',
                                        'Residential Fuel Oil (CO2e)':'Fuel Oil',
                                        'Residential Propane (CO2e)':'Propane'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    fig = px.pie(rf_year_sub.round(0),values='Emissions',names='index',
                 title='Share of residential household emissions by fuel')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    
    # Residential heating fuels pie chart
    hh_graph_cols = ['pct electric','pct gas',
                     'pct fuel oil','pct propane',
                    'pct wood','pct other']

    hh_year_sub = year_set[hh_graph_cols].T*100
    hh_year_sub = hh_year_sub.rename(columns={hh_year_sub.columns[0]:'Fuels'},
                                     index={'pct electric':'Electricity',
                                      'pct gas':'Natural Gas',
                                         'pct fuel oil':'Fuel Oil',
                                         'pct propane':'Propane',
                                         'pct wood':'Wood',
                                         'pct other':'Other'}
                                     )
    hh_year_sub = hh_year_sub.reset_index()
    fig = px.pie(hh_year_sub.round(0),values='Fuels',names='index',
                 title='Share of household heating fuels')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    st.write('Note: Census figures shown here are not corrected in communities known \
             to have not natural gas infrastructure. The emissions calculations for natural gas \
            rely on utility sales data and so are not affected by this.')
            
    st.write('Data sources: Mass Save Data, MA DOER, MA DPU, U.S. Census Bureau, U.S. EIA')

with tab4:            
    st.header('Commercial and Industrial Buildings')
    # Commercial fuel emissions pie chart
    graph_cols = ['Commercial & Industrial Electricity (CO2e)','Commercial & Industrial Gas (CO2e)',
                      'Commercial Fuel Oil (CO2e)']

    cf_year_sub = year_set[graph_cols].T
    cf_year_sub = cf_year_sub.rename(columns={cf_year_sub.columns[0]:'Emissions'},
                                     index={'Commercial & Industrial Electricity (CO2e)':'Electricity',
                                      'Commercial & Industrial Gas (CO2e)':'Natural Gas',
                                         'Commercial Fuel Oil (CO2e)':'Fuel Oil'}
                                     )
    cf_year_sub = cf_year_sub.reset_index()
    fig = px.pie(cf_year_sub.round(0),values='Emissions',names='index',
                 title='Share of commercial building emissions by fuel')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    
    # add graph showing number of employers and jobs in different sectors
    
    st.write('Data sources: Mass Save Data, MA DOER, MA DPU, U.S. Census Bureau, U.S. EIA')

with tab5:
    st.header('Transportation Emissions')
    
    # Transportation emissions pie chart
    graph_cols = ['Residential Gasoline (CO2e)','Residential Vehicle Electricity (CO2e)',
                  'Commercial Gasoline (CO2e)','Commercial Vehicle Electricity (CO2e)',
                  'Municipal Gasoline (CO2e)','Municipal Vehicle Electricity (CO2e)']

    rf_year_sub = year_set[graph_cols].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Gasoline (CO2e)':'Passenger Gasoline',
                                      'Residential Vehicle Electricity (CO2e)':'Passenger Electricity',
                                        'Commercial Gasoline (CO2e)':'Commercial Gasoline',
                                        'Commercial Vehicle Electricity (CO2e)':'Commercial Electricity',
                                        'Municipal Gasoline (CO2e)':'Municipal Gasoline',
                                        'Municipal Vehicle Electricity (CO2e)':'Municipal Electricity'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    fig = px.pie(rf_year_sub.round(0),values='Emissions',names='index',
                 title='Share of emissions by fuel and vehicle type')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    
    # plot trends in VMT and # of vehicles
    
    st.write('Data Sources: MA DOT')

with tab6:
    st.header('Waste Emissions')
    # line chart
    fig = px.line(subset,x='Year',y='Trash Disposal Tonnage',
                  title='Waste in '+municipality)
    fig.update_layout(yaxis_title='tons')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    # pie chart
    graph_cols = ['trash','single stream recyc',
                  'other recyc','organics']

    msw_year_sub = year_set[graph_cols].T
    msw_year_sub = msw_year_sub.rename(columns={msw_year_sub.columns[0]:'Waste'},
                                     index={'trash':'Trash',
                                      'single stream recyc':'Single Stream Recycling',
                                        'other recyc':'Other Recycling',
                                        'organics':'Organics'}
                                     )
    msw_year_sub = msw_year_sub.reset_index()
    fig = px.pie(msw_year_sub.round(0),values='Waste',names='index',
                 title='Share of waste by type')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    
    st.write('Data Sources: MA DEP')
    
with tab7:
    st.header('Massachusetts')
    
    #geo should be a dictionary of geospatial data and df has the non-spatial data
    #then they are linked together via an id
    
    # total emissions
    st.write('Total emissions by municipality')
    fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                        featureidkey='properties.Name',color='Total (CO2e)')
    fig.update_geos(fitbounds='locations',visible=False)
    fig.update_layout(height=300,margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    
    # per capita emissions
    st.write('Per person emissions by municipality')
    fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                        featureidkey='properties.Name',color='Per Capita (CO2e)')
    fig.update_geos(fitbounds='locations',visible=False)
    fig.update_layout(height=300,margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)




