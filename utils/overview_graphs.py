# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:07:19 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# function for annual emissions graph(s)
@st.cache_data
def m_graph1(m,dataset,start_year,end_year):
    subset = dataset[(dataset['Municipality']==m)&(dataset['Year']>2019)&(dataset['Year']<=end_year)]
    
    # Line graph of total emissions and emission per capita
    # make the figure
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'},{'type':'scatter'}]],
                        subplot_titles=('Total MTCO2e','Per Capita MTCO2e')
                        )
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Total (MTCO2e)'].round(0),name='Total MTCO2e'),
        row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Per Capita (MTCO2e)'].round(2),name='Per Capita MTCO2e'),
        row=1,col=2)
    
    fig.update_layout(title=dict(text='Emissions in '+m,font=dict(size=28)),
                      yaxis=dict(range=[0,1.4*(subset['Total (MTCO2e)'].max())],
                                 title=dict(text='Total MTCO2e',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      yaxis2=dict(range=[0,1.5*(subset['Per Capita (MTCO2e)'].max())],
                                  title=dict(text='Per Capita MTCO2e',font=dict(size=18),standoff=0),
                                  tickfont=dict(size=14))
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
                     tickvals=list(range(start_year,end_year+1)),
                     tickfont=dict(size=14))
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',showlegend=False,
                      height=400,width=1000)
    st.plotly_chart(fig)
    
    return subset

# function for one year pie charts
@st.cache_data
def my_graph1(m,y,dataset,colors_fuel):
    year_set = dataset[(dataset['Year']==y)&(dataset['Municipality']==m)]
    
    # data prep for pie charts
    graph_cols1 = ['Total Electricity (MTCO2e)','Total Gas (MTCO2e)',
                  'Total Propane (MTCO2e)','Total Fuel Oil (MTCO2e)',
                  'Total Gasoline (MTCO2e)',
                  'Total Diesel (MTCO2e)',
                  #'Solid Waste Emissions (MTCO2e)',
                  #'Wastewater Emissions (MTCO2e)'
                  ]
    year_sub1 = year_set[graph_cols1].T
    year_sub1 = year_sub1.rename(columns={year_sub1.columns[0]:'Emissions'},
                               index={'Total Electricity (MTCO2e)':'Electricity',
                                      'Total Gas (MTCO2e)':'Natural Gas',
                                         'Total Fuel Oil (MTCO2e)':'Fuel Oil',
                                         'Total Propane (MTCO2e)':'Propane',
                                         'Total Gasoline (MTCO2e)':'Gasoline',
                                         'Total Diesel (MTCO2e)':'Diesel',
                                         #'Solid Waste Emissions (MTCO2e)':'Solid Waste',
                                         #'Wastewater Emissions (MTCO2e)':'Wastewater'
                                         }
                               )
    year_sub1 = year_sub1.reset_index()
    
    graph_cols2 = ['Total Residential Buildings (MTCO2e)',
                   'Total Commercial & Industrial Buildings (MTCO2e)',
                   'Total Transportation (MTCO2e)',
                   #'Public Transit Total (MTCO2e)',
                   #'Waste Emissions (MTCO2e)'
                   ]
    year_sub2 = year_set[graph_cols2].T
    year_sub2 = year_sub2.rename(columns={year_sub2.columns[0]:'Emissions'},
                               index={'Total Residential Buildings (MTCO2e)':'Residential',
                                      'Total Commercial & Industrial Buildings (MTCO2e)':'Commercial & Industrial',
                                      'Total Transportation (MTCO2e)':'Transportation',
                                      #'Public Transit Total (MTCO2e)':'Public Transit',
                                      #'Waste Emissions (CO2e)':'Waste'
                                      }
                                   )
    year_sub2 = year_sub2.reset_index()
    
    graph_cols3 = ['Total Electricity (MMBTU)','Total Gas (MMBTU)',
                  'Total Propane (MMBTU)','Total Fuel Oil (MMBTU)',
                  'Total Gasoline (MMBTU)','Total Diesel (MMBTU)']
    year_sub3 = year_set[graph_cols3].T
    year_sub3 = year_sub3.rename(columns={year_sub3.columns[0]:'Energy'},
                               index={'Total Electricity (MMBTU)':'Electricity',
                                      'Total Gas (MMBTU)':'Natural Gas',
                                      'Total Fuel Oil (MMBTU)':'Fuel Oil',
                                      'Total Propane (MMBTU)':'Propane',
                                      'Total Gasoline (MMBTU)':'Gasoline',
                                      'Total Diesel (MMBTU)':'Diesel'
                                      }
                               )
    year_sub3 = year_sub3.reset_index()
    
    graph_cols4 = ['Total Residential Buildings (MMBTU)',
                   'Total Commercial & Industrial Buildings (MMBTU)',
                   'Total Transportation (MMBTU)']
    year_sub4 = year_set[graph_cols4].T
    year_sub4 = year_sub4.rename(columns={year_sub4.columns[0]:'Energy'},
                               index={'Total Residential Buildings (MMBTU)':'Residential',
                                      'Total Commercial & Industrial Buildings (MMBTU)':'Commercial & Industrial',
                                      'Total Transportation (MMBTU)':'Transportation'
                                      }
                               )
    year_sub4 = year_sub4.reset_index()
    #print(year_sub4)

    # making the pie charts
    fig = make_subplots(rows=2,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}], 
                                              [{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=('Share of emissions by fuel in MTCO2e',
                                        'Share of emissions by sector in MTCO2e',
                                        'Share of energy by fuel in MMBTU',
                                        'Share of energy by sector in MMBTU'),
                        vertical_spacing=0.2
                        )
    fig.add_trace(
        go.Pie(labels=year_sub1['index'], values=year_sub1['Emissions'].round(0),
               sort=False,marker_colors=year_sub1['index'].map(colors_fuel),
               rotation=90,
               textinfo='label+percent',textfont_size=14),
        row=1,col=1)
    fig.add_trace(
        go.Pie(labels=year_sub2['index'], values=year_sub2['Emissions'].round(0),
               sort=False,rotation=-90,
               textinfo='label+percent',textfont_size=14),
        row=1,col=2)
    fig.add_trace(
        go.Pie(labels=year_sub3['index'],values=year_sub3['Energy'].round(0),
               sort=False,rotation=120,
               textinfo='label+percent',textfont_size=14),
        row=2,col=1)
    fig.add_trace(
        go.Pie(labels=year_sub4['index'],values=year_sub4['Energy'].round(0),
               sort=False,rotation=-70,
               textinfo='label+percent',textfont_size=14),
        row=2,col=2)
    
    fig.update_layout(title=dict(text='Shares of energy and emissions in '+m+' in '+str(y),
                                 font=dict(size=28),
                                 y = 1,
                                 yanchor='top',
                                 ),
                      #title_pad_b = 20,
                      height=750,width=1000,
                      showlegend=False
                      )
    fig.layout.annotations[0].update(y=1.05)
    fig.layout.annotations[1].update(y=1.05)
    fig.layout.annotations[2].update(y=0.46)
    fig.layout.annotations[3].update(y=0.46)
    
    st.plotly_chart(fig)
    return year_set
