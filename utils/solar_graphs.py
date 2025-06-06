# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:49:32 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# function for solar graphs
@st.cache_data
def solar_graph(m,solar):
    subset = solar[solar['City']==m]
    # new and cumulative graph
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'},{'type':'scatter'}]],
                        subplot_titles=('New solar capacity','Cumulative solar capacity')
                        )
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) All'],
                   hoverinfo='x+y+name',mode='lines',
                   name='New Capacity'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) Residential (3 or fewer dwelling units per building)'],
                   hoverinfo='x+y+name',mode='lines',
                   name='New Residential Capacity'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) All Cumulative'],
                   hoverinfo='x+y+name',mode='lines',
                   name='Cumulative Capacity'),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) Residential Cumulative'],
                   hoverinfo='x+y+name',mode='lines',
                   name='Cumulative Residential Capacity'),
                   row=1,col=2)
    
    fig.update_layout(title=dict(text='Solar adoption in '+m,font=dict(size=28)),
                      yaxis=dict(#range=[0,1.4*(subset['Total (CO2e)'].max())],
                                 title=dict(text='Capacity (kW DC)',font=dict(size=18),standoff=15),
                                 tickfont=dict(size=14)),
                      yaxis2=dict(#range=[0,1.4*(subset['Total (CO2e)'].max())],
                                 title=dict(text='Capacity (kW DC)',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14))
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
                     tickvals=list(range(2000,2024,5)),
                     tickfont=dict(size=14))
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',showlegend=True,
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=-0.4,
                                  xanchor="right",
                                  x=1,
                                  font=dict(size=14)),
                      height = 500, width = 1000
                      )
    st.plotly_chart(fig)
    
    st.text('')
    st.text('')
    
    # sector pie charts
    year_set4 = solar[(solar['City']==m)&(solar['Year']==2023)]
    graph_cols1 = ['Capacity (kW DC) Residential Cumulative',
                  'Capacity (kW DC) Multifamily Cumulative',
                  'Capacity (kW DC) Mixed use Cumulative',
                  'Capacity (kW DC) Commercial Cumulative',
                  'Capacity (kW DC) Municipal Cumulative',
                  'Capacity (kW DC) State/Fed Cumulative',
                  'Capacity (kW DC) Industrial Cumulative',
                  'Capacity (kW DC) Agricultural Cumulative',
                  'Capacity (kW DC) Community Solar Cumulative',
                  'Capacity (kW DC) Other Cumulative']
    
    graph_cols2 = ['Project Count Residential Cumulative',
                  'Project Count Multifamily Cumulative',
                  'Project Count Mixed use Cumulative',
                  'Project Count Commercial Cumulative',
                  'Project Count Municipal Cumulative',
                  'Project Count State/Fed Cumulative',
                  'Project Count Industrial Cumulative',
                  'Project Count Agricultural Cumulative',
                  'Project Count Community Solar Cumulative',
                  'Project Count Other Cumulative']
    
    sa_year_sub1 = year_set4[graph_cols1].T
    sa_year_sub1 = sa_year_sub1.rename(columns={sa_year_sub1.columns[0]:'Sectors'},
                                     index={'Capacity (kW DC) Residential Cumulative':'Residential',
                                      'Capacity (kW DC) Multifamily Cumulative':'Multifamily',
                                        'Capacity (kW DC) Mixed use Cumulative':'Mixed Use',
                                        'Capacity (kW DC) Commercial Cumulative':'Commercial',
                                        'Capacity (kW DC) Municipal Cumulative':'Municipal',
                                        'Capacity (kW DC) State/Fed Cumulative':'Other Govt',
                                        'Capacity (kW DC) Industrial Cumulative':'Industrial',
                                        'Capacity (kW DC) Agricultural Cumulative':'Agricultural',
                                        'Capacity (kW DC) Community Solar Cumulative':'Community Solar',
                                        'Capacity (kW DC) Other Cumulative':'Other'
                                        }
                                     )
    sa_year_sub1 = sa_year_sub1.reset_index()
    
    sa_year_sub2 = year_set4[graph_cols2].T
    sa_year_sub2 = sa_year_sub2.rename(columns={sa_year_sub2.columns[0]:'Sectors'},
                                     index={'Project Count Residential Cumulative':'Residential',
                                      'Project Count Multifamily Cumulative':'Multifamily',
                                        'Project Count Mixed use Cumulative':'Mixed Use',
                                        'Project Count Commercial Cumulative':'Commercial',
                                        'Project Count Municipal Cumulative':'Municipal',
                                        'Project Count State/Fed Cumulative':'Other Govt',
                                        'Project Count Industrial Cumulative':'Industrial',
                                        'Project Count Agricultural Cumulative':'Agricultural',
                                        'Project Count Community Solar Cumulative':'Community Solar',
                                        'Project Count Other Cumulative':'Other'
                                        }
                                     )
    sa_year_sub2 = sa_year_sub2.reset_index()
    
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=('Share of capacity by sector',
                                        'Share of projects by sector'),
                        horizontal_spacing = 0.05,
                        )
    
    fig.add_trace(
        go.Pie(labels=sa_year_sub1['index'], values=sa_year_sub1['Sectors'].round(0),
               sort=False,rotation=180,
               textinfo='label+percent',textfont_size=14,showlegend=False),
        row=1,col=1)
    
    fig.add_trace(
        go.Pie(labels=sa_year_sub2['index'], values=sa_year_sub2['Sectors'].round(0),
               sort=False,rotation=-75,
               textinfo='label+percent',textfont_size=14,showlegend=False),
        row=1,col=2)
    
    fig.update_layout(height = 500, width = 1000)
    fig.layout.annotations[0].update(y=1.1)
    fig.layout.annotations[1].update(y=1.1)
    
    st.plotly_chart(fig)
    return year_set4