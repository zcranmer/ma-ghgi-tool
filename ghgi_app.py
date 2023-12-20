# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gp
import matplotlib.pyplot as plt
import plotly.express as px

st.title('Municipal Greenhouse Gas Inventory Tool')

#@st.cache_data
def load_data():
    # set file location
    os.chdir('C:/Users/acranmer/OneDrive - Bentley University/Municipal Emissions')
    df = pd.read_excel('municipal_emissions.xlsx')
    return df

#data_load_state = st.text('Loading data...')
dataset = load_data()
#data_load_state.text('Loading data...done!')

municipality = st.sidebar.selectbox(
    'Which city or town would you like to explore?',
    dataset['Municipality'].unique())

subset = dataset[dataset['Municipality']==municipality]
fig = px.line(subset,x='Year',y='Total (CO2e)',title='Total GHG emissions in '+municipality)
fig.update_layout(yaxis_title='CO2e')
fig.update_xaxes(tickvals=subset['Year'].unique())
st.plotly_chart(fig)
#st.line_chart(data=subset,x='Year',y='Total (CO2e)')

year = st.sidebar.slider('Choose a year',
    min_value=subset['Year'].min(),max_value=subset['Year'].max(),
    value=2021)
#'You selected: ', year

year_set = subset[subset['Year']==year]

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
             title='Share of emissions by fuel')
fig.update_traces(textposition='outside',textinfo='percent+label')
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
             title='Share of emissions by sector')
fig.update_traces(textposition='outside',textinfo='percent+label')
fig.layout.update(showlegend=False)

st.plotly_chart(fig)
