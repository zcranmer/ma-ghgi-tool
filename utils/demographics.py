# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:18:15 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# functions for demographic figures
@st.cache_data
def m_demog_graph(m,dataset,start_year,end_year):
    subset = dataset[(dataset['Municipality']==m)&(dataset['Year']<=end_year)]
    
    fig = make_subplots(rows=3,cols=1,specs=[[{'type':'scatter'}],
                                             [{'type':'scatter'}],
                                             [{'type':'scatter'}]],
                        subplot_titles=('Population','Households','Median Household Income'),
                        vertical_spacing = 0.1
                        )
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Population']),
        row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Total Heating Fuel Households']),
        row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Median household income']),
        row=3,col=1)
    
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',showlegend=False,
                      yaxis=dict(range=[0,1.4*(subset['Population'].max())],
                                 title=dict(text='People',font=dict(size=18)),
                                 tickfont=dict(size=14)),
                      yaxis2=dict(range=[0,1.4*(subset['Total Heating Fuel Households'].max())],
                                  title=dict(text='Households',font=dict(size=18)),
                                  tickfont=dict(size=14)),
                      yaxis3=dict(range=[0,1.4*(subset['Median household income'].max())],
                                  title=dict(text='$',font=dict(size=18)),
                                  tickfont=dict(size=14)),
                      height=1200,width=500
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
                     tickvals=list(range(start_year,end_year+1)),
                     tickfont=dict(size=14))
    
    st.plotly_chart(fig)
    return subset
