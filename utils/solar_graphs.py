# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:49:32 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

palette = px.colors.qualitative.Safe
color_sector = {'All':'#0068c9',
                'Residential':'#83c9ff',
                'Commercial':'#ff2b2b'}

# function for solar graphs
@st.cache_data
def solar_graph(m,solar):
    solar = solar.rename(columns={'City':'Municipality'})
    subset = solar[solar['Municipality']==m]
    # new and cumulative graph
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'},{'type':'scatter'}]],
                        subplot_titles=('New solar capacity','Cumulative solar capacity'),
                        horizontal_spacing=0.1
                        )
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) All'],
                   hoverinfo='x+y+name',mode='lines',
                   line=dict(color=color_sector['All']),
                   name='All Capacity'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) Residential'],
                   hoverinfo='x+y+name',mode='lines',
                   line=dict(color=color_sector['Residential']),
                   name='Residential Capacity'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) Commercial'],
                   hoverinfo='x+y+name',mode='lines',
                   line=dict(color=color_sector['Commercial']),
                   name='Commercial Capacity'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Cumulative Capacity (kW DC) All'],
                   hoverinfo='x+y+name',mode='lines',
                   line=dict(color=color_sector['All']),
                   showlegend=False,
                   name='Cumulative Capacity'),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Cumulative Capacity (kW DC) Residential'],
                   hoverinfo='x+y+name',mode='lines',
                   line=dict(color=color_sector['Residential']),
                   showlegend=False,
                   name='Cumulative Residential Capacity'),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Cumulative Capacity (kW DC) Commercial'],
                   hoverinfo='x+y+name',mode='lines',
                   line=dict(color=color_sector['Commercial']),
                   showlegend=False,
                   name='Cumulative Commercial Capacity'),
                   row=1,col=2)
    
    fig.update_layout(title=dict(text='Solar adoption in '+m,font=dict(size=24)),
                      yaxis=dict(#range=[0,1.4*(subset['Total (CO2e)'].max())],
                                 title=dict(text='Capacity (kW DC)',font=dict(size=18,color='black'),standoff=15),
                                 tickfont=dict(size=14,color='black')),
                      yaxis2=dict(#range=[0,1.4*(subset['Total (CO2e)'].max())],
                                 title=dict(text='Capacity (kW DC)',font=dict(size=18,color='black'),standoff=10),
                                 tickfont=dict(size=14,color='black'))
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18,color='black')),
                     tickvals=list(range(2000,2026,5)),
                     tickfont=dict(size=14,color='black'))
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',showlegend=True,
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=-0.4,
                                  xanchor="right",
                                  x=1,
                                  font=dict(size=14)),
                      height = 500, width = 1000,
                      annotations=[dict(font=dict(color='black'))]
                      )
    st.plotly_chart(fig)
    
    st.text('')
    st.text('')
    
    # sector pie charts
    year_set4 = solar[(solar['Municipality']==m)&(solar['Year']==2023)]
    graph_cols1 = ['Cumulative Capacity (kW DC) Residential',
                  'Cumulative Capacity (kW DC) Multi-family residential',
                  'Cumulative Capacity (kW DC) Mixed Use',
                  'Cumulative Capacity (kW DC) Commercial',
                  'Cumulative Capacity (kW DC) Municipal',
                  'Cumulative Capacity (kW DC) Industrial',
                  'Cumulative Capacity (kW DC) Agricultural',
                  'Cumulative Capacity (kW DC) Community Solar',
                  'Cumulative Capacity (kW DC) Other',
                  'Cumulative Capacity (kW DC) Unknown']
    
    graph_cols2 = ['Cumulative Project Count Residential',
                  'Cumulative Project Count Multi-family residential',
                  'Cumulative Project Count Mixed Use',
                  'Cumulative Project Count Commercial',
                  'Cumulative Project Count Municipal',
                  'Cumulative Project Count Industrial',
                  'Cumulative Project Count Agricultural',
                  'Cumulative Project Count Community Solar',
                  'Cumulative Project Count Other',
                  'Cumulative Project Count Unknown']
    
    sa_year_sub1 = year_set4[graph_cols1].T
    sa_year_sub1 = sa_year_sub1.rename(columns={sa_year_sub1.columns[0]:'Sectors'},
                                     index={'Cumulative Capacity (kW DC) Residential':'Residential',
                                      'Cumulative Capacity (kW DC) Multi-family residential':'Multifamily',
                                        'Cumulative Capacity (kW DC) Mixed Use':'Mixed Use',
                                        'Cumulative Capacity (kW DC) Commercial':'Commercial',
                                        'Cumulative Capacity (kW DC) Municipal':'Municipal',
                                        'Cumulative Capacity (kW DC) Industrial':'Industrial',
                                        'Cumulative Capacity (kW DC) Agricultural':'Agricultural',
                                        'Cumulative Capacity (kW DC) Community Solar':'Community Solar',
                                        'Cumulative Capacity (kW DC) Other':'Other',
                                        'Cumulative Capacity (kW DC) Unknown':'Unknown'
                                        }
                                     )
    sa_year_sub1 = sa_year_sub1.reset_index()
    
    sa_year_sub2 = year_set4[graph_cols2].T
    sa_year_sub2 = sa_year_sub2.rename(columns={sa_year_sub2.columns[0]:'Sectors'},
                                     index={'Cumulative Project Count Residential':'Residential',
                                      'Cumulative Project Count Multi-family residential':'Multifamily',
                                        'Cumulative Project Count Mixed Use':'Mixed Use',
                                        'Cumulative Project Count Commercial':'Commercial',
                                        'Cumulative Project Count Municipal':'Municipal',
                                        'Cumulative Project Count Industrial':'Industrial',
                                        'Cumulative Project Count Agricultural':'Agricultural',
                                        'Cumulative Project Count Community Solar':'Community Solar',
                                        'Cumulative Project Count Other':'Other',
                                        'Cumulative Project Count Unknown':'Unknown'
                                        }
                                     )
    sa_year_sub2 = sa_year_sub2.reset_index()
    
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=('Share of capacity by sector',
                                        'Share of projects by sector'),
                        horizontal_spacing = 0.2,
                        )
    
    fig.add_trace(
        go.Pie(labels=sa_year_sub1['index'], values=sa_year_sub1['Sectors'].round(0),
               sort=False,rotation=120,
               textinfo='label+percent',textfont_size=14,showlegend=False,
               textfont=dict(color='black'),
               insidetextfont=dict(color=['white','black','white','black','white','black','black','black','white','black']),
               outsidetextfont=dict(color='black'),
               ),
        row=1,col=1)
    
    fig.add_trace(
        go.Pie(labels=sa_year_sub2['index'], values=sa_year_sub2['Sectors'].round(0),
               sort=False,rotation=-75,
               textinfo='label+percent',textfont_size=14,showlegend=False,
               textfont=dict(color='black'),
               insidetextfont=dict(color=['white','black','white','black','white','black','black','black','white','black']),
               outsidetextfont=dict(color='black'),
               ),
        row=1,col=2)
    
    fig.update_layout(height = 500, width = 1000,
                      annotations=[dict(font=dict(color='black'))]
                      )
    fig.layout.annotations[0].update(y=1.2)
    fig.layout.annotations[1].update(y=1.2)
    
    st.markdown('Pie charts for solar are capacity and projects as of 2023.')
    st.plotly_chart(fig)
    return year_set4