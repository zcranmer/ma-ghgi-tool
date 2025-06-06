# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 09:50:18 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# function for waste
@st.cache_data
def waste_graph(m,y,dataset,colors_waste):
    subset = dataset[dataset['Municipality']==m]
    year_set = dataset[(dataset['Year']==y)&(dataset['Municipality']==m)]
    
    if m == 'Massachusetts':
        landfill = 1
        incinerator = 1
        mwra = 1
        wwtp = 1
        septic = 1
    else:
        incinerator = 1-landfill
        wwtp = 1-septic
    
    fig = make_subplots(rows=1,cols=1)
    # solid waste emissions
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Landfill (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Landfill',line=dict(color=colors_waste['Trash L'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Incineration (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Incinerator',line=dict(color=colors_waste['Trash I'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Compost (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Compost',line=dict(color=colors_waste['Organics'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['MWRA AD (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Wastewater w/AD',line=dict(color=colors_waste['Wastewater AD'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['WWTP (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Wastewater',line=dict(color=colors_waste['Wastewater'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Septic (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Septic',line=dict(color=colors_waste['Septic'])),
                   row=1,col=1)
    
    fig.update_layout(title=dict(text='Waste Emissions in '+str(m),font=dict(size=28)),
                      yaxis=dict(title=dict(text='CO2e',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      xaxis=dict(title=dict(text='Year',font=dict(size=18)),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14)),
                      height=600,width=1000)
    st.plotly_chart(fig)
    
    
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'}, {'type':'domain'}],
                                             ],
                        subplot_titles=('Solid waste over time',
                                        'Share of waste in '+str(y)),
                        horizontal_spacing = 0.1,
                        )
    
    # line chart
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['trash'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Trash',line=dict(color=colors_waste['Trash'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['single stream recyc'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Single Stream Recycling',line=dict(color=colors_waste['Single Stream Recycling'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['other recyc'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Other Recycling',line=dict(color=colors_waste['Other Recycling'])),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['organics'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Organics',line=dict(color=colors_waste['Organics'])),
                   row=1,col=1)
    
    
    # pie chart
    graph_cols = ['trash','single stream recyc',
                  'other recyc','organics']

    msw_year_sub = year_set[graph_cols].T
    msw_year_sub = msw_year_sub.rename(columns={msw_year_sub.columns[0]:'Waste'},
                                     index={'trash':'Trash',
                                      'single stream recyc':'Single Stream\nRecycling',
                                        'other recyc':'Other Recycling',
                                        'organics':'Organics'}
                                     )
    msw_year_sub = msw_year_sub.reset_index()
    
    fig.add_trace(
        go.Pie(labels=msw_year_sub['index'], values=msw_year_sub['Waste'].round(0),
               marker_colors=msw_year_sub['index'].map(colors_waste),
               textinfo='label+percent',textfont_size=14,showlegend=False),
        row=1,col=2)
    
    fig.update_layout(title=dict(text='Solid waste in '+str(m),font=dict(size=28)),
                      yaxis=dict(title=dict(text='tons',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      xaxis=dict(title=dict(text='Year',font=dict(size=18)),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14)),
                      height=600,width=1200)
    #fig.layout.update(showlegend=False)

    st.plotly_chart(fig)