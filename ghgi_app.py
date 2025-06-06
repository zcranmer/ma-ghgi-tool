# -*- coding: utf-8 -*-
"""
Main file in public dashboard tool
MA Greenhouse Gas Inventory Tool
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit_analytics2 as streamlit_analytics

start_year = 2017
end_year = 2023

st.set_page_config(layout='wide',
                   page_title='MA GHGI Tool'
                   )

st.title('Massachusetts Community Greenhouse Gas Inventory Tool')
st.write('This tool shows community-wide energy and emissions data from \
        buildings, transportation, and waste. Residential and commercial \
        activities are included in addition to municipal. This app is \
        under development and does not yet include all possible sources of \
        emissions. Please use the feedback page on the left if you have \
        questions or comments about anything in this dashboard.')
        
colors_fuel = {'Electricity':'darkgreen',
               'Wood':'forestgreen',
               'Natural Gas':'mediumseagreen',
               'Propane':'yellowgreen',
               'Fuel Oil':'darkkhaki',
               'Diesel':'darkkhaki',
               'Gasoline':'olive',
               'Waste':'tab:brown',
               'Other':'goldenrod'}

colors_vehicles = {'Fossil Fuel':'brown',
                   'Hybrid Electric':'yellowgreen',
                   'Plug-in Hybrid':'mediumseagreen',
                   'Electric Vehicle':'forestgreen',
                   'Fuel Cell':'darkgreen'}

colors_waste = {'Trash':'darkblue',
                'Single Stream Recycling':'blue',
                'Other Recycling':'royalblue',
                'Organics':'lightsteelblue',
                'Trash L':'darkblue',
                'Trash I':'steelblue',
                'Wastewater AD':'saddlebrown',
                'Wastewater':'chocolate',
                'Septic':'gold'}

# loading data function - moved to utils code
# @st.cache_data
# def load_data(start_year):
#     df = pd.read_csv('datasets/municipal_emissions.csv')
#     gdf = json.load(open('datasets/municipalities.json'))
    
#     dataset_ma = pd.concat([df.loc[df['Municipality']=='Massachusetts',:],df.loc[df['Municipality']!='Massachusetts',:]],axis=0)
#     dataset = dataset_ma[dataset_ma['Year']>=start_year]
    
#     df_solar = pd.read_csv('datasets/solar_data.csv')
#     df_stations = pd.read_csv('datasets/ev_stations.csv')
#     df_hp = pd.read_excel('datasets/masssave hp 2019-2023.xlsx')
    
#     return dataset,gdf,df_solar,df_stations,df_hp

# function for annual emissions graph(s)
# @st.cache_data
# def m_graph1(m):
#     subset = dataset[(dataset['Municipality']==m)&(dataset['Year']>2019)&(dataset['Year']<=end_year)]
    
#     # Line graph of total emissions and emission per capita
#     # make the figure
#     fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'},{'type':'scatter'}]],
#                         subplot_titles=('Total MTCO2e','Per Capita MTCO2e')
#                         )
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Total (MTCO2e)'].round(0),name='Total MTCO2e'),
#         row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Per Capita (MTCO2e)'].round(2),name='Per Capita MTCO2e'),
#         row=1,col=2)
    
#     fig.update_layout(title=dict(text='Emissions in '+m,font=dict(size=28)),
#                       yaxis=dict(range=[0,1.4*(subset['Total (MTCO2e)'].max())],
#                                  title=dict(text='Total MTCO2e',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14)),
#                       yaxis2=dict(range=[0,1.5*(subset['Per Capita (MTCO2e)'].max())],
#                                   title=dict(text='Per Capita MTCO2e',font=dict(size=18),standoff=0),
#                                   tickfont=dict(size=14))
#                       )
#     fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
#                      tickvals=list(range(start_year,end_year+1)),
#                      tickfont=dict(size=14))
#     fig.update_traces(mode='markers+lines',hovertemplate=None)
#     fig.update_layout(hovermode='x',showlegend=False,
#                       height=400,width=1000)
#     st.plotly_chart(fig)
    
#     return subset

# # function for one year pie charts
# @st.cache_data
# def my_graph1(m,y):
#     year_set = dataset[(dataset['Year']==y)&(dataset['Municipality']==m)]
    
#     # data prep for pie charts
#     graph_cols1 = ['Total Electricity (MTCO2e)','Total Gas (MTCO2e)',
#                   'Total Propane (MTCO2e)','Total Fuel Oil (MTCO2e)',
#                   'Total Gasoline (MTCO2e)',
#                   'Total Diesel (MTCO2e)',
#                   #'Solid Waste Emissions (MTCO2e)',
#                   #'Wastewater Emissions (MTCO2e)'
#                   ]
#     year_sub1 = year_set[graph_cols1].T
#     year_sub1 = year_sub1.rename(columns={year_sub1.columns[0]:'Emissions'},
#                                index={'Total Electricity (MTCO2e)':'Electricity',
#                                       'Total Gas (MTCO2e)':'Natural Gas',
#                                          'Total Fuel Oil (MTCO2e)':'Fuel Oil',
#                                          'Total Propane (MTCO2e)':'Propane',
#                                          'Total Gasoline (MTCO2e)':'Gasoline',
#                                          'Total Diesel (MTCO2e)':'Diesel',
#                                          #'Solid Waste Emissions (MTCO2e)':'Solid Waste',
#                                          #'Wastewater Emissions (MTCO2e)':'Wastewater'
#                                          }
#                                )
#     year_sub1 = year_sub1.reset_index()
    
#     graph_cols2 = ['Total Residential Buildings (MTCO2e)',
#                    'Total Commercial & Industrial Buildings (MTCO2e)',
#                    'Total Transportation (MTCO2e)',
#                    #'Public Transit Total (MTCO2e)',
#                    #'Waste Emissions (MTCO2e)'
#                    ]
#     year_sub2 = year_set[graph_cols2].T
#     year_sub2 = year_sub2.rename(columns={year_sub2.columns[0]:'Emissions'},
#                                index={'Total Residential Buildings (MTCO2e)':'Residential',
#                                       'Total Commercial & Industrial Buildings (MTCO2e)':'Commercial & Industrial',
#                                       'Total Transportation (MTCO2e)':'Transportation',
#                                       #'Public Transit Total (MTCO2e)':'Public Transit',
#                                       #'Waste Emissions (CO2e)':'Waste'
#                                       }
#                                    )
#     year_sub2 = year_sub2.reset_index()
    
#     graph_cols3 = ['Total Electricity (MMBTU)','Total Gas (MMBTU)',
#                   'Total Propane (MMBTU)','Total Fuel Oil (MMBTU)',
#                   'Total Gasoline (MMBTU)','Total Diesel (MMBTU)']
#     year_sub3 = year_set[graph_cols3].T
#     year_sub3 = year_sub3.rename(columns={year_sub3.columns[0]:'Energy'},
#                                index={'Total Electricity (MMBTU)':'Electricity',
#                                       'Total Gas (MMBTU)':'Natural Gas',
#                                       'Total Fuel Oil (MMBTU)':'Fuel Oil',
#                                       'Total Propane (MMBTU)':'Propane',
#                                       'Total Gasoline (MMBTU)':'Gasoline',
#                                       'Total Diesel (MMBTU)':'Diesel'
#                                       }
#                                )
#     year_sub3 = year_sub3.reset_index()
    
#     graph_cols4 = ['Total Residential Buildings (MMBTU)',
#                    'Total Commercial & Industrial Buildings (MMBTU)',
#                    'Total Transportation (MMBTU)']
#     year_sub4 = year_set[graph_cols4].T
#     year_sub4 = year_sub4.rename(columns={year_sub4.columns[0]:'Energy'},
#                                index={'Total Residential Buildings (MMBTU)':'Residential',
#                                       'Total Commercial & Industrial Buildings (MMBTU)':'Commercial & Industrial',
#                                       'Total Transportation (MMBTU)':'Transportation'
#                                       }
#                                )
#     year_sub4 = year_sub4.reset_index()
#     #print(year_sub4)

#     # making the pie charts
#     fig = make_subplots(rows=2,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}], 
#                                               [{'type':'domain'}, {'type':'domain'}]],
#                         subplot_titles=('Share of emissions by fuel in MTCO2e',
#                                         'Share of emissions by sector in MTCO2e',
#                                         'Share of energy by fuel in MMBTU',
#                                         'Share of energy by sector in MMBTU'),
#                         vertical_spacing=0.2
#                         )
#     fig.add_trace(
#         go.Pie(labels=year_sub1['index'], values=year_sub1['Emissions'].round(0),
#                sort=False,marker_colors=year_sub1['index'].map(colors_fuel),
#                rotation=90,
#                textinfo='label+percent',textfont_size=14),
#         row=1,col=1)
#     fig.add_trace(
#         go.Pie(labels=year_sub2['index'], values=year_sub2['Emissions'].round(0),
#                sort=False,rotation=-90,
#                textinfo='label+percent',textfont_size=14),
#         row=1,col=2)
#     fig.add_trace(
#         go.Pie(labels=year_sub3['index'],values=year_sub3['Energy'].round(0),
#                sort=False,rotation=120,
#                textinfo='label+percent',textfont_size=14),
#         row=2,col=1)
#     fig.add_trace(
#         go.Pie(labels=year_sub4['index'],values=year_sub4['Energy'].round(0),
#                sort=False,rotation=-70,
#                textinfo='label+percent',textfont_size=14),
#         row=2,col=2)
    
#     fig.update_layout(title=dict(text='Shares of energy and emissions in '+m+' in '+str(y),
#                                  font=dict(size=28),
#                                  y = 1,
#                                  yanchor='top',
#                                  ),
#                       #title_pad_b = 20,
#                       height=750,width=1000,
#                       showlegend=False
#                       )
#     fig.layout.annotations[0].update(y=1.05)
#     fig.layout.annotations[1].update(y=1.05)
#     fig.layout.annotations[2].update(y=0.46)
#     fig.layout.annotations[3].update(y=0.46)
    
#     st.plotly_chart(fig)
#     return year_set

# functions for demographic figures
# @st.cache_data
# def m_demog_graph(m):
#     subset = dataset[dataset['Municipality']==m]
    
#     fig = make_subplots(rows=3,cols=1,specs=[[{'type':'scatter'}],
#                                              [{'type':'scatter'}],
#                                              [{'type':'scatter'}]],
#                         subplot_titles=('Population','Households','Median Household Income'),
#                         vertical_spacing = 0.1
#                         )
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Population']),
#         row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Total Heating Fuel Households']),
#         row=2,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Median household income']),
#         row=3,col=1)
    
#     fig.update_traces(mode='markers+lines',hovertemplate=None)
#     fig.update_layout(hovermode='x',showlegend=False,
#                       yaxis=dict(range=[0,1.4*(subset['Population'].max())],
#                                  title=dict(text='People',font=dict(size=18)),
#                                  tickfont=dict(size=14)),
#                       yaxis2=dict(range=[0,1.4*(subset['Total Heating Fuel Households'].max())],
#                                   title=dict(text='Households',font=dict(size=18)),
#                                   tickfont=dict(size=14)),
#                       yaxis3=dict(range=[0,1.4*(subset['Median household income'].max())],
#                                   title=dict(text='$',font=dict(size=18)),
#                                   tickfont=dict(size=14)),
#                       height=1200,width=500
#                       )
#     fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
#                      tickvals=list(range(start_year,end_year+1)),
#                      tickfont=dict(size=14))
    
#     st.plotly_chart(fig)
#     return subset

# function for buildings
# @st.cache_data
# def bldg_graph1(m):
#     subset = dataset[(dataset['Municipality']==m)&(dataset['Year']<2024)]
    
#     # stacked area charts - energy and emissions
#     fig = make_subplots(rows=2,cols=2,
#                         subplot_titles=('Residential Energy by fuel in MMBTU',
#                                         'Commercial Energy by fuel in MMBTU',
#                                         'Residential Emissions by fuel in MTCO2e',
#                                         'Commercial Emissions by fuel in MTCO2e'),
#                         vertical_spacing = 0.2
#                         )
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Electricity (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Electricity',line=dict(color=colors_fuel['Electricity']),
#                    legendgroup = '1'),
#                    row=1,col=1)
#     #fig.add_trace(
#     #    go.Scatter(x=subset['Year'],y=subset['Residential Wood (MMBTU)'],
#     #               hoverinfo='x+y+name',mode='lines',stackgroup='one',
#     #               name='Wood',line=dict(color=colors_fuel['Wood']),
#     #               legendgroup = '1'),
#     #               row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Gas (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
#                    legendgroup = '1'),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Propane (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Propane',line=dict(color=colors_fuel['Propane']),
#                    legendgroup = '1'),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Fuel Oil (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
#                    legendgroup = '1'),
#                    row=1,col=1)
    
    
    
#     # Commercial and Industrial Energy
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Commercial & Industrial Electricity (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='two',
#                    name='Electricity',line=dict(color=colors_fuel['Electricity']),
#                    legendgroup = '1',showlegend=False),
#                    row=1,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Commercial & Industrial Gas (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='two',
#                    name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
#                    legendgroup = '1',showlegend=False),
#                    row=1,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Commercial Fuel Oil (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='two',
#                    name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
#                    legendgroup = '1',showlegend=False),
#                    row=1,col=2)
    
#     # Residential Emissions 
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Electricity (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='three',
#                    name='Electricity',line=dict(color=colors_fuel['Electricity']),
#                    legendgroup = '1',showlegend=False),
#                    row=2,col=1)
#     #fig.add_trace(
#     #    go.Scatter(x=subset['Year'],y=subset['Residential Wood (MTCO2e)'],
#     #               hoverinfo='x+y+name',mode='lines',stackgroup='three',
#     #               name='Wood',line=dict(color=colors_fuel['Wood']),
#     #               legendgroup = '1',showlegend=False),
#     #               row=2,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Gas (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='three',
#                    name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
#                    legendgroup = '1',showlegend=False),
#                    row=2,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Propane (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='three',
#                    name='Propane',line=dict(color=colors_fuel['Propane']),
#                    legendgroup = '1',showlegend=False),
#                    row=2,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Residential Fuel Oil (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='three',
#                    name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
#                    legendgroup = '1',showlegend=False),
#                    row=2,col=1)
    
    
#     # Commercial and Industrial Emissions
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Commercial & Industrial Electricity (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='four',
#                    name='Electricity',line=dict(color=colors_fuel['Electricity']),
#                    legendgroup = '1',showlegend=False),
#                    row=2,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Commercial & Industrial Gas (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='four',
#                    name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
#                    legendgroup = '1',showlegend=False),
#                    row=2,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset['Year'],y=subset['Commercial Fuel Oil (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='four',
#                    name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
#                    legendgroup = '1',showlegend=False),
#                    row=2,col=2)
#     #fig.add_trace(
#     #    go.Scatter(x=subset['Year'],y=subset['Direct Emissions (MTCO2e)'],
#     #               hoverinfo='x+y+name',mode='lines',stackgroup='four',
#     #               name='Other',line=dict(color=colors_fuel['Other']),
#     #               legendgroup = '1'),
#     #               row=2,col=2)

#     fig.update_traces(mode='markers+lines',hovertemplate=None)
#     fig.update_layout(hovermode='x',
#                       title=dict(text='Building energy and emissions in '+m,font=dict(size=28)),
#                       yaxis=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14)),
#                       yaxis2=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=0),
#                                   tickfont=dict(size=14)),
#                       yaxis3=dict(title=dict(text='MTCO2e',font=dict(size=18),standoff=0),
#                                   tickfont=dict(size=14)),
#                       yaxis4=dict(title=dict(text='MTCO2e',font=dict(size=18),standoff=0),
#                                   tickfont=dict(size=14)),
#                       height=750,width=1000
#                       )
#     fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
#                      tickvals=list(range(start_year,end_year+1)),
#                      tickfont=dict(size=14))
    
#     st.plotly_chart(fig)
#     return subset
    
# def bldg_graph2(m,y3):    
#     year_set = dataset[(dataset['Year']==y3)&(dataset['Municipality']==m)]
#     # Data prep
#     # Residential emissions
#     graph_cols1 = ['Residential Electricity (MTCO2e)','Residential Gas (MTCO2e)',
#                    'Residential Propane (MTCO2e)','Residential Fuel Oil (MTCO2e)']
    
#     rf_year_sub = year_set[graph_cols1].T
#     rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
#                                      index={'Residential Electricity (MTCO2e)':'Electricity',
#                                             'Residential Gas (MTCO2e)':'Natural Gas',
#                                             'Residential Fuel Oil (MTCO2e)':'Fuel Oil',
#                                             'Residential Propane (MTCO2e)':'Propane'}
#                                      )
#     rf_year_sub = rf_year_sub.reset_index()
    
#     # Commercial emissions
#     graph_cols2 = ['Commercial & Industrial Electricity (MTCO2e)','Commercial & Industrial Gas (MTCO2e)',
#                       'Commercial Fuel Oil (MTCO2e)',#'Direct Emissions (MTCO2e)'
#                       ]

#     cf_year_sub = year_set[graph_cols2].T
#     #print(cf_year_sub)
#     cf_year_sub = cf_year_sub.rename(columns={cf_year_sub.columns[0]:'Emissions'},
#                                      index={'Commercial & Industrial Electricity (MTCO2e)':'Electricity',
#                                       'Commercial & Industrial Gas (MTCO2e)':'Natural Gas',
#                                          'Commercial Fuel Oil (MTCO2e)':'Fuel Oil',
#                                          #'Direct Emissions (MTCO2e)':'Other'
#                                          }
#                                      )
#     cf_year_sub = cf_year_sub.reset_index()
    
#     # Residential heating fuels pie chart
#     hh_graph_cols = ['Electricity','Utility gas',
#                      'Fuel oil, kerosene, etc.','Bottled, tank, or LP gas',
#                      'Wood','Solar energy','Coal or coke',
#                      'Other fuel','No fuel used']
    
#     hh_year_sub = year_set[hh_graph_cols].T*100
#     hh_year_sub = hh_year_sub.rename(columns={hh_year_sub.columns[0]:'Fuels'},
#                                      index={'Utility gas':'Natural Gas',
#                                             'Fuel oil, kerosene, etc.':'Fuel Oil',
#                                             'Bottled, tank, or LP gas':'Propane'}
#                                      )
#     hh_year_sub = hh_year_sub.reset_index()
    
#     threshold = hh_year_sub['Fuels'].sum()*0.04 # aggregate any categories that are less than 4% of the total
#     #print('threshold: '+str(threshold))
#     hh_row_other = hh_year_sub.loc[hh_year_sub['Fuels']<threshold].sum(numeric_only=True)
#     hh_row_other = hh_row_other.rename('Fuels')
#     hh_row_other = hh_row_other.rename(index={hh_row_other.index[0]:'Other'}).reset_index()
    
#     hh_year_sub_t = hh_year_sub.loc[hh_year_sub['Fuels']>=threshold]
#     hh_year_sub_f = pd.concat([hh_year_sub_t,hh_row_other])
    
#     # Commercial sectors pie chart
#     cc_graph_cols = year_set.loc[:,year_set.columns.str.startswith('Average Monthly Employment')].columns
#     cc_year_sub = year_set[cc_graph_cols].T*100
#     cc_year_sub = cc_year_sub.rename(columns={cc_year_sub.columns[0]:'Employment'})
#     cc_year_sub = cc_year_sub.reset_index()
#     cc_year_sub['index'] = cc_year_sub['index'].str.replace('Average Monthly Employment ','')
    
    
#     threshold_c = cc_year_sub['Employment'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    
#     cc_row_other = cc_year_sub.loc[cc_year_sub['Employment']<threshold_c].sum(numeric_only=True)
#     cc_row_other = cc_row_other.rename('Employment')
#     cc_row_other = cc_row_other.rename(index={cc_row_other.index[0]:'Other'}).reset_index()
    
#     cc_year_sub_t = cc_year_sub.loc[cc_year_sub['Employment']>=threshold_c]
#     cc_year_sub_f = pd.concat([cc_year_sub_t,cc_row_other])
    
#     # pie charts
#     fig = make_subplots(rows=2,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}],
#                                              [{'type':'domain'}, {'type':'domain'}]],
#                         subplot_titles=('Share of residential emissions by fuel',
#                                         'Share of commercial emissions by fuel',
#                                         'Share of households by heating fuel',
#                                         #'Share of commercial employment by sector'
#                                         ),
#                         horizontal_spacing = 0.03,
#                         vertical_spacing = 0.2
#                         )
#     fig.add_trace(
#         go.Pie(labels=rf_year_sub['index'], values=rf_year_sub['Emissions'].round(0),
#                sort=False,rotation=120,
#                textinfo='label+percent',textfont_size=14),
#         row=1,col=1)
#     fig.add_trace(
#         go.Pie(labels=cf_year_sub['index'], values=cf_year_sub['Emissions'].round(0),
#                sort=False,marker_colors=cf_year_sub['index'].map(colors_fuel),
#                rotation=-90,
#                textinfo='label+percent',textfont_size=14),
#         row=1,col=2)
#     fig.add_trace(
#         go.Pie(labels=hh_year_sub_f['index'], values=hh_year_sub_f['Fuels'].round(0),
#                sort=False,marker_colors=hh_year_sub_f['index'].map(colors_fuel),
#                rotation=45,
#                textinfo='label+percent',textfont_size=14),
#         row=2,col=1)
#     #fig.add_trace(
#     #    go.Pie(labels=cc_year_sub_f['index'], values=cc_year_sub_f['Employment'].round(0),
#     #           textinfo='label+percent',textfont_size=14),
#     #    row=2,col=2)
    
#     fig.update_layout(title=dict(text='Share of emissions and sources in '+m+' in '+str(y3),
#                                  font=dict(size=28),
#                                  y = 1,
#                                  yanchor='top',
#                                  ),
#                       height=750,width=1000,
#                       showlegend=False
#                       )
#     fig.layout.annotations[0].update(y=1.05)
#     fig.layout.annotations[1].update(y=1.05)
#     fig.layout.annotations[2].update(y=0.46)

#     st.plotly_chart(fig)
#     return year_set
    
    # add graph showing number of employers and jobs in different sectors

# function for solar graphs
# @st.cache_data
# def solar_graph(m4):
#     subset = solar[solar['City']==m4]
#     # new and cumulative graph
#     fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'},{'type':'scatter'}]],
#                         subplot_titles=('New solar capacity','Cumulative solar capacity')
#                         )
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) All'],
#                    hoverinfo='x+y+name',mode='lines',
#                    name='New Capacity'),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) Residential (3 or fewer dwelling units per building)'],
#                    hoverinfo='x+y+name',mode='lines',
#                    name='New Residential Capacity'),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) All Cumulative'],
#                    hoverinfo='x+y+name',mode='lines',
#                    name='Cumulative Capacity'),
#                    row=1,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Capacity (kW DC) Residential Cumulative'],
#                    hoverinfo='x+y+name',mode='lines',
#                    name='Cumulative Residential Capacity'),
#                    row=1,col=2)
    
#     fig.update_layout(title=dict(text='Solar adoption in '+m4,font=dict(size=28)),
#                       yaxis=dict(#range=[0,1.4*(subset['Total (CO2e)'].max())],
#                                  title=dict(text='Capacity (kW DC)',font=dict(size=18),standoff=15),
#                                  tickfont=dict(size=14)),
#                       yaxis2=dict(#range=[0,1.4*(subset['Total (CO2e)'].max())],
#                                  title=dict(text='Capacity (kW DC)',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14))
#                       )
#     fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
#                      tickvals=list(range(2000,2024,5)),
#                      tickfont=dict(size=14))
#     fig.update_traces(mode='markers+lines',hovertemplate=None)
#     fig.update_layout(hovermode='x',showlegend=True,
#                       legend=dict(orientation="h",
#                                   yanchor="bottom",
#                                   y=-0.4,
#                                   xanchor="right",
#                                   x=1,
#                                   font=dict(size=14)),
#                       height = 500, width = 1000
#                       )
#     st.plotly_chart(fig)
    
#     st.text('')
#     st.text('')
    
#     # sector pie charts
#     year_set4 = solar[(solar['City']==m4)&(solar['Year']==2023)]
#     graph_cols1 = ['Capacity (kW DC) Residential Cumulative',
#                   'Capacity (kW DC) Multifamily Cumulative',
#                   'Capacity (kW DC) Mixed use Cumulative',
#                   'Capacity (kW DC) Commercial Cumulative',
#                   'Capacity (kW DC) Municipal Cumulative',
#                   'Capacity (kW DC) State/Fed Cumulative',
#                   'Capacity (kW DC) Industrial Cumulative',
#                   'Capacity (kW DC) Agricultural Cumulative',
#                   'Capacity (kW DC) Community Solar Cumulative',
#                   'Capacity (kW DC) Other Cumulative']
    
#     graph_cols2 = ['Project Count Residential Cumulative',
#                   'Project Count Multifamily Cumulative',
#                   'Project Count Mixed use Cumulative',
#                   'Project Count Commercial Cumulative',
#                   'Project Count Municipal Cumulative',
#                   'Project Count State/Fed Cumulative',
#                   'Project Count Industrial Cumulative',
#                   'Project Count Agricultural Cumulative',
#                   'Project Count Community Solar Cumulative',
#                   'Project Count Other Cumulative']
    
#     sa_year_sub1 = year_set4[graph_cols1].T
#     sa_year_sub1 = sa_year_sub1.rename(columns={sa_year_sub1.columns[0]:'Sectors'},
#                                      index={'Capacity (kW DC) Residential Cumulative':'Residential',
#                                       'Capacity (kW DC) Multifamily Cumulative':'Multifamily',
#                                         'Capacity (kW DC) Mixed use Cumulative':'Mixed Use',
#                                         'Capacity (kW DC) Commercial Cumulative':'Commercial',
#                                         'Capacity (kW DC) Municipal Cumulative':'Municipal',
#                                         'Capacity (kW DC) State/Fed Cumulative':'Other Govt',
#                                         'Capacity (kW DC) Industrial Cumulative':'Industrial',
#                                         'Capacity (kW DC) Agricultural Cumulative':'Agricultural',
#                                         'Capacity (kW DC) Community Solar Cumulative':'Community Solar',
#                                         'Capacity (kW DC) Other Cumulative':'Other'
#                                         }
#                                      )
#     sa_year_sub1 = sa_year_sub1.reset_index()
    
#     sa_year_sub2 = year_set4[graph_cols2].T
#     sa_year_sub2 = sa_year_sub2.rename(columns={sa_year_sub2.columns[0]:'Sectors'},
#                                      index={'Project Count Residential Cumulative':'Residential',
#                                       'Project Count Multifamily Cumulative':'Multifamily',
#                                         'Project Count Mixed use Cumulative':'Mixed Use',
#                                         'Project Count Commercial Cumulative':'Commercial',
#                                         'Project Count Municipal Cumulative':'Municipal',
#                                         'Project Count State/Fed Cumulative':'Other Govt',
#                                         'Project Count Industrial Cumulative':'Industrial',
#                                         'Project Count Agricultural Cumulative':'Agricultural',
#                                         'Project Count Community Solar Cumulative':'Community Solar',
#                                         'Project Count Other Cumulative':'Other'
#                                         }
#                                      )
#     sa_year_sub2 = sa_year_sub2.reset_index()
    
#     fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]],
#                         subplot_titles=('Share of capacity by sector',
#                                         'Share of projects by sector'),
#                         horizontal_spacing = 0.05,
#                         )
    
#     fig.add_trace(
#         go.Pie(labels=sa_year_sub1['index'], values=sa_year_sub1['Sectors'].round(0),
#                sort=False,rotation=180,
#                textinfo='label+percent',textfont_size=14,showlegend=False),
#         row=1,col=1)
    
#     fig.add_trace(
#         go.Pie(labels=sa_year_sub2['index'], values=sa_year_sub2['Sectors'].round(0),
#                sort=False,rotation=-75,
#                textinfo='label+percent',textfont_size=14,showlegend=False),
#         row=1,col=2)
    
#     fig.update_layout(height = 500, width = 1000)
#     fig.layout.annotations[0].update(y=1.1)
#     fig.layout.annotations[1].update(y=1.1)
    
#     st.plotly_chart(fig)
#     return year_set4

# function for transportation
# @st.cache_data
# def trans_graph0(m5):
#     subset = dataset.loc[(dataset['Municipality']==m5)&(dataset['Year']>2019),:]
    
#     fig = make_subplots(rows=2,cols=2,specs=[[{'type':'scatter'}, {'type':'scatter'}],
#                                              [{'type':'scatter'}, {'type':'scatter'}]],
#                         subplot_titles=('Vehicle counts over time',
#                                         'Vehicle miles traveled over time',
#                                         'Energy use over time',
#                                         'Emissions over time'),
#                         horizontal_spacing = 0.1,
#                         vertical_spacing = 0.2
#                         )
    
#     # Line graph of vehicle counts over time
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Count FFs 01'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '1',
#                    name='Fossil Fuel',line=dict(color=colors_vehicles['Fossil Fuel'])
#                    ),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Count GHYs 01'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '1',
#                    name='Gas Hybrid',line=dict(color=colors_vehicles['Hybrid Electric'])
#                    ),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Count PHEVs 01'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '1',
#                    name='Plug-in Hybrid',line=dict(color=colors_vehicles['Plug-in Hybrid'])
#                    ),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Count EVs 01'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '1',
#                    name='Electric',line=dict(color=colors_vehicles['Electric Vehicle'])
#                    ),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset[[' Count    Fuel Cell Electric Vehicle  Commercial 01',
#                                           ' Count    Fuel Cell Electric Vehicle  Municipal 01',
#                                           ' Count    Fuel Cell Electric Vehicle  Passenger 01',
#                                           ' Count    Fuel Cell Electric Vehicle  State 01']].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '1',
#                    name='Fuel Cell',line=dict(color=colors_vehicles['Fuel Cell'])
#                    ),
#                    row=1,col=1)
    
#     # Line graph of Daily Vehicle Miles Traveled over time
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Fossil Fuel  Commercial 01',
#                                           ' DailyVMT    Fossil Fuel  Municipal 01',
#                                           ' DailyVMT    Fossil Fuel  Passenger 01',
#                                           ' DailyVMT    Fossil Fuel  State 01']].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '1',
#                    name='Fossil Fuel',line=dict(color=colors_vehicles['Fossil Fuel'])
#                    ),
#                    row=1,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Hybrid Electric Vehicle  Commercial 01',
#                                           ' DailyVMT    Hybrid Electric Vehicle  Municipal 01',
#                                           ' DailyVMT    Hybrid Electric Vehicle  Passenger 01',
#                                           ' DailyVMT    Hybrid Electric Vehicle  State 01']].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '1',
#                    name='Gas Hybrid',line=dict(color=colors_vehicles['Hybrid Electric'])
#                    ),
#                    row=1,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Plug in Hybrid Electric  Commercial 01',
#                                           ' DailyVMT    Plug in Hybrid Electric  Municipal 01',
#                                           ' DailyVMT    Plug in Hybrid Electric  Passenger 01',
#                                           ' DailyVMT    Plug in Hybrid Electric  State 01']].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '1',
#                    name='Plug-in Hybrid',line=dict(color=colors_vehicles['Plug-in Hybrid'])
#                    ),
#                    row=1,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Electric Vehicle  Commercial 01',
#                                           ' DailyVMT    Electric Vehicle  Municipal 01',
#                                           ' DailyVMT    Electric Vehicle  Passenger 01',
#                                           ' DailyVMT    Electric Vehicle  State 01']].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '1',
#                    name='Electric',line=dict(color=colors_vehicles['Electric Vehicle'])
#                    ),
#                    row=1,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Fuel Cell Electric Vehicle  Commercial 01',
#                                           ' DailyVMT    Fuel Cell Electric Vehicle  Municipal 01',
#                                           ' DailyVMT    Fuel Cell Electric Vehicle  Passenger 01',
#                                           ' DailyVMT    Fuel Cell Electric Vehicle  State 01']].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '1',
#                    name='Fuel Cell',line=dict(color=colors_vehicles['Fuel Cell'])),
#                    row=1,col=2)
    
#     # Transportation energy
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset['Total Gasoline (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '2',
#                    name='Gasoline',line=dict(color=colors_fuel['Gasoline'])
#                    ),
#                    row=2,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset['Total Diesel (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '2',
#                    name='Diesel',line=dict(color=colors_fuel['Diesel'])
#                    ),
#                    row=2,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset['Total Vehicle Electricity (MMBTU)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '2',
#                    name='Electricity',line=dict(color=colors_fuel['Electricity'])
#                    ),
#                    row=2,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset[['Total Public Transportation (MMBTU)']].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    showlegend=False,legendgroup = '2',
#                    name='Electricity',line=dict(color='lightsteelblue')
#                    ),
#                    row=2,col=1)
    
#     # Transportation emissions
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset['Total Gasoline (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '2',
#                    name='Gasoline',line=dict(color=colors_fuel['Gasoline'])
#                    ),
#                    row=2,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset['Total Diesel (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '2',
#                    name='Diesel',line=dict(color=colors_fuel['Diesel'])
#                    ),
#                    row=2,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset['Total Vehicle Electricity (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '2',
#                    name='Electricity',line=dict(color=colors_fuel['Electricity'])
#                    ),
#                    row=2,col=2)
#     fig.add_trace(
#         go.Scatter(x=subset.Year[:-1],y=subset[['Total Public Transportation (MTCO2e)',
#                                                 'MBTA Diesel (MTCO2e)','MBTA Electricity (MTCO2e)','MBTA CNG (MTCO2e)'
#                                                 ]].sum(axis=1),
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    legendgroup = '2',
#                    name='Public Transit',line=dict(color='lightsteelblue')
#                    ),
#                    row=2,col=2)
    
#     fig.update_layout(hovermode='x',
#                       title=dict(text='Share of vehicles and miles driven in '+m5,font=dict(size=28)),
#                       yaxis=dict(title=dict(text='Vehicles',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14)),
#                       yaxis2=dict(title=dict(text='Daily VMT',font=dict(size=18),standoff=0),
#                                  tickfont=dict(size=14)),
#                       yaxis3=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14)),
#                       yaxis4=dict(title=dict(text='MTCO2e',font=dict(size=18),standoff=0),
#                                  tickfont=dict(size=14)),
#                       xaxis=dict(title=dict(text='Year',font=dict(size=18)),
#                                  tickvals=subset.Year,
#                                  tickfont=dict(size=14)),
#                       xaxis2=dict(title=dict(text='Year',font=dict(size=18)),
#                                  tickvals=subset.Year,
#                                  tickfont=dict(size=14)),
#                       xaxis3=dict(title=dict(text='Year',font=dict(size=18)),
#                                  tickvals=subset.Year,
#                                  tickfont=dict(size=14)),
#                       xaxis4=dict(title=dict(text='Year',font=dict(size=18)),
#                                  tickvals=subset.Year,
#                                  tickfont=dict(size=14)),
#                       legend_tracegroupgap = 280,
#                       height=800,width=1000,
#                       )

#     st.plotly_chart(fig)
    

# @st.cache_data
# def trans_graph(m5,y5):
#     subset = dataset[(dataset['Municipality']==m5)&(dataset['Year']>2019)]
#     year_set5 = dataset[(dataset['Year']==y5)&(dataset['Municipality']==m5)]
    
#     # Transportation energy pie chart
#     graph_cols = ['Residential Gasoline (MMBTU)','Residential Diesel (MMBTU)','Residential Vehicle Electricity (MMBTU)',
#                   'Commercial Gasoline (MMBTU)','Commercial Diesel (MMBTU)','Commercial Vehicle Electricity (MMBTU)',
#                   'Municipal Gasoline (MMBTU)','Municipal Diesel (MMBTU)','Municipal Vehicle Electricity (MMBTU)',
#                   'Total Public Transportation (MMBTU)'
#                   ]

#     rf_year_sub = year_set5[graph_cols].T
#     rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Energy'},
#                                      index={'Residential Gasoline (MMBTU)':'Passenger Gasoline',
#                                             'Residential Diesel (MMBTU)':'Passenger Diesel',
#                                       'Residential Vehicle Electricity (MMBTU)':'Passenger Electricity',
#                                         'Commercial Gasoline (MMBTU)':'Commercial Gasoline',
#                                         'Commercial Diesel (MMBTU)':'Commercial Diesel',
#                                         'Commercial Vehicle Electricity (MMBTU)':'Commercial Electricity',
#                                         'Municipal Gasoline (MMBTU)':'Municipal Gasoline',
#                                         'Municipal Diesel (MMBTU)':'Municipal Diesel',
#                                         'Municipal Vehicle Electricity (MMBTU)':'Municipal Electricity',
#                                         'Total Public Transportation (MMBTU)':'Public Transit'}
#                                      )
#     rf_year_sub = rf_year_sub.reset_index()
    
#     threshold_v = rf_year_sub['Energy'].sum()*0.04 # aggregate any categories that are less than 4% of the total
#     rf_row_other = rf_year_sub.loc[rf_year_sub['Energy']<threshold_v].sum(numeric_only=True)
#     rf_row_other = rf_row_other.rename('Energy')
#     rf_row_other = rf_row_other.rename(index={rf_row_other.index[0]:'Other'}).reset_index()
#     rf_year_sub_t = rf_year_sub.loc[rf_year_sub['Energy']>=threshold_v]
#     rf_year_sub_s = pd.concat([rf_year_sub_t,rf_row_other])
    
#     # Transportation emissions pie chart
#     graph_cols = ['Residential Gasoline (MTCO2e)','Residential Diesel (MTCO2e)','Residential Vehicle Electricity (MTCO2e)',
#                   'Commercial Gasoline (MTCO2e)','Commercial Diesel (MTCO2e)','Commercial Vehicle Electricity (MTCO2e)',
#                   'Municipal Gasoline (MTCO2e)','Municipal Diesel (MTCO2e)','Municipal Vehicle Electricity (MTCO2e)',
#                   'Total Public Transportation (MTCO2e)'
#                   ]

#     rf_year_sub = year_set5[graph_cols].T
#     rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
#                                      index={'Residential Gasoline (MTCO2e)':'Passenger Gasoline',
#                                             'Residential Diesel (MTCO2e)':'Passenger Diesel',
#                                       'Residential Vehicle Electricity (MTCO2e)':'Passenger Electricity',
#                                         'Commercial Gasoline (MTCO2e)':'Commercial Gasoline',
#                                         'Commercial Diesel (MTCO2e)':'Commercial Diesel',
#                                         'Commercial Vehicle Electricity (MTCO2e)':'Commercial Electricity',
#                                         'Municipal Gasoline (MTCO2e)':'Municipal Gasoline',
#                                         'Municipal Diesel (MTCO2e)':'Municipal Diesel',
#                                         'Municipal Vehicle Electricity (MTCO2e)':'Municipal Electricity',
#                                         'Total Public Transportation (MTCO2e)':'Public Transit'}
#                                      )
#     rf_year_sub = rf_year_sub.reset_index()
    
#     threshold_v = rf_year_sub['Emissions'].sum()*0.04 # aggregate any categories that are less than 4% of the total
#     rf_row_other = rf_year_sub.loc[rf_year_sub['Emissions']<threshold_v].sum(numeric_only=True)
#     rf_row_other = rf_row_other.rename('Emissions')
#     rf_row_other = rf_row_other.rename(index={rf_row_other.index[0]:'Other'}).reset_index()
#     rf_year_sub_t = rf_year_sub.loc[rf_year_sub['Emissions']>=threshold_v]
#     rf_year_sub_f = pd.concat([rf_year_sub_t,rf_row_other])
    
#     fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]],
#                         subplot_titles=('Share of fuel by sector',
#                                         'Share of emissions by fuel and sector'),
#                         horizontal_spacing = 0.1,
#                         )
#     # Energy pie chart
#     fig.add_trace(
#         go.Pie(labels=rf_year_sub_s['index'], values=rf_year_sub_s['Energy'].round(0),
#                sort=False,rotation=180,
#                textinfo='label+percent',textfont_size=14,showlegend=False),
#         row=1,col=1)
    
#     # Emissions pie chart
#     fig.add_trace(
#         go.Pie(labels=rf_year_sub_f['index'], values=rf_year_sub_f['Emissions'].round(0),
#                sort=False,rotation=180,
#                textinfo='label+percent',textfont_size=14,showlegend=False),
#         row=1,col=2)
    
#     fig.update_layout(title=dict(text='Share of emissions and sources in '+m5+' in '+str(y5),font=dict(size=28)),
#                       yaxis=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14)),
#                       xaxis=dict(title=dict(text='Year',font=dict(size=18)),
#                                  tickvals=subset.Year,
#                                  tickfont=dict(size=14)),
#                       height=400,width=1000
#                       )

#     st.plotly_chart(fig)

# function for waste
# @st.cache_data
# def waste_graph(m6,y6):
#     subset = dataset[dataset['Municipality']==m6]
#     year_set6 = dataset[(dataset['Year']==y6)&(dataset['Municipality']==m6)]
    
#     if m6 == 'Massachusetts':
#         landfill = 1
#         incinerator = 1
#         mwra = 1
#         wwtp = 1
#         septic = 1
#     else:
#         incinerator = 1-landfill
#         wwtp = 1-septic
    
#     fig = make_subplots(rows=1,cols=1)
#     # solid waste emissions
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Landfill (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Landfill',line=dict(color=colors_waste['Trash L'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Incineration (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Incinerator',line=dict(color=colors_waste['Trash I'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Compost (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Compost',line=dict(color=colors_waste['Organics'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['MWRA AD (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Wastewater w/AD',line=dict(color=colors_waste['Wastewater AD'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['WWTP (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Wastewater',line=dict(color=colors_waste['Wastewater'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['Septic (MTCO2e)'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Septic',line=dict(color=colors_waste['Septic'])),
#                    row=1,col=1)
    
#     fig.update_layout(title=dict(text='Waste Emissions in '+str(m6),font=dict(size=28)),
#                       yaxis=dict(title=dict(text='CO2e',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14)),
#                       xaxis=dict(title=dict(text='Year',font=dict(size=18)),
#                                  tickvals=subset.Year,
#                                  tickfont=dict(size=14)),
#                       height=600,width=1000)
#     st.plotly_chart(fig)
    
    
#     fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'}, {'type':'domain'}],
#                                              ],
#                         subplot_titles=('Solid waste over time',
#                                         'Share of waste in '+str(y6)),
#                         horizontal_spacing = 0.1,
#                         )
    
#     # line chart
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['trash'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Trash',line=dict(color=colors_waste['Trash'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['single stream recyc'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Single Stream Recycling',line=dict(color=colors_waste['Single Stream Recycling'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['other recyc'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Other Recycling',line=dict(color=colors_waste['Other Recycling'])),
#                    row=1,col=1)
#     fig.add_trace(
#         go.Scatter(x=subset.Year,y=subset['organics'],
#                    hoverinfo='x+y+name',mode='lines',stackgroup='one',
#                    name='Organics',line=dict(color=colors_waste['Organics'])),
#                    row=1,col=1)
    
    
#     # pie chart
#     graph_cols = ['trash','single stream recyc',
#                   'other recyc','organics']

#     msw_year_sub = year_set6[graph_cols].T
#     msw_year_sub = msw_year_sub.rename(columns={msw_year_sub.columns[0]:'Waste'},
#                                      index={'trash':'Trash',
#                                       'single stream recyc':'Single Stream\nRecycling',
#                                         'other recyc':'Other Recycling',
#                                         'organics':'Organics'}
#                                      )
#     msw_year_sub = msw_year_sub.reset_index()
    
#     fig.add_trace(
#         go.Pie(labels=msw_year_sub['index'], values=msw_year_sub['Waste'].round(0),
#                marker_colors=msw_year_sub['index'].map(colors_waste),
#                textinfo='label+percent',textfont_size=14,showlegend=False),
#         row=1,col=2)
    
#     fig.update_layout(title=dict(text='Solid waste in '+str(m6),font=dict(size=28)),
#                       yaxis=dict(title=dict(text='tons',font=dict(size=18),standoff=10),
#                                  tickfont=dict(size=14)),
#                       xaxis=dict(title=dict(text='Year',font=dict(size=18)),
#                                  tickvals=subset.Year,
#                                  tickfont=dict(size=14)),
#                       height=600,width=1200)
#     #fig.layout.update(showlegend=False)

#     st.plotly_chart(fig)
#     return year_set6

# function for statewide maps for a single year
@st.cache_data
def map_figure(y,d):
    st.session_state.key = d
    
    dataset_year = dataset[dataset['Year']==y]
    dataset_year['Municipality'] = dataset_year['Municipality'].str.capitalize().str.replace('Attleborough','Attleboro')
    
    solar_year = solar.loc[solar['Year']==y,:]
    solar_year['City'] = solar_year['City'].str.capitalize()
    
    #geo should be a dictionary of geospatial data and df has the non-spatial data
    #then they are linked together via an id
    
    # add a way to select different items to display on the map
    if d == 'Total Emissions':
        # total emissions
        st.write('Total emissions by municipality')
        fig = px.choropleth(dataset_year,geojson=geo,locations='Municipality',
                            featureidkey='properties.Name',color='Total (MTCO2e)',
                            range_color=[1000,200000],
                            labels={'Total (MTCO2e)':'MTCO2e'})
    
    elif d == 'Per Capita Emissions':
        # per capita emissions
        st.write('Per person emissions by municipality in '+str(y))
        fig = px.choropleth(dataset_year,geojson=geo,locations='Municipality',
                            featureidkey='properties.Name',color='Per Capita (MTCO2e)',
                            range_color=[0,15],
                            labels={'Per Capita (MTCO2e)':'MTCO2e'})
        
    elif d == 'Building Emissions':
        st.write('Total emissions from buildings by municipality in '+str(y))
        fig = px.choropleth(dataset_year,geojson=geo,locations='Municipality',
                            featureidkey='properties.Name',color='Total Buildings (MTCO2e)',
                            range_color=[0,100000],
                            labels={'Total Buildings (MTCO2e)':'MTCO2e'})
        
    elif d == 'Transportation Emissions':
        st.write('Total emissions from transportation by municipality in '+str(y))
        fig = px.choropleth(dataset_year,geojson=geo,locations='Municipality',
                            featureidkey='properties.Name',color='Total Transportation (MTCO2e)',
                            range_color=[0,100000],
                            labels={'Total Transportation (MTCO2e)':'MTCO2e'})
        
    elif d == 'Solar PV Capacity':
        st.write('Solar photovoltaic capacity in kW DC by municipality in '+str(y))
        fig = px.choropleth(solar_year,geojson=geo,locations='City',
                            featureidkey='properties.Name',color='Capacity (kW DC) All Cumulative',
                            range_color=[0,50000],
                            labels={'':'kW DC'})
    
    elif d == 'Percent EVs':
        st.write('Share of vehicles that are EVs and PHEVs by municipality in '+str(y))
        fig = px.choropleth(dataset_year,geojson=geo,locations='Municipality',
                            featureidkey='properties.Name',color='Percent EVs',
                            labels={'Percent EVs':'%'})
    
    fig.update_geos(fitbounds='locations',visible=False)
    fig.update_layout(height=500,width=1000,
                      margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
        
    return dataset_year

#############################################################################
# Running the dashboard

if 'df' not in st.session_state:
    from utils.load_data import load_data
    dataset, geo, solar, stations, hps = load_data(start_year)
else:
    dataset = st.session_state.df
    geo = st.session_state.gdf
    solar = st.session_state.df_solar
    stations = st.session_state.df_stations
    hps = st.session_state.df_hp

with streamlit_analytics.track():
    st.markdown('**Which city or town would you like to explore?**')
    municipality = st.selectbox('Click in the box and type the name or scroll through the drop down list.',
                             dataset['Municipality'].unique().tolist(),
                             index=0,
                             key='local')

st.markdown('Choose from the different tabs below to look at different \n \
             elements of the data.')
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['Overview','Demographics',
                                        'Buildings','Solar','Transportation','Waste',
                                        'Compare','Targets'])

with tab1:
    st.header('Overview of Energy and Emissions')
    from utils.overview_graphs import m_graph1, my_graph1
    
    # metrics
    default_year = 2023
    base_year = 2020
    co2_year = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==default_year),'Total (MTCO2e)'].round(decimals=0).astype('int').item()
    co2_base = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==base_year),'Total (MTCO2e)'].round(decimals=0).astype('int').item()
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown(str(default_year)+' Total MTCO2e.')
        st.metric(label=' ',
                    #label='Total 2022 GHGs in MTCO2e',
                  value=f'{co2_year:,.0f}',
                  #delta=round(100*(co2_year-co2_base)/co2_base,2),
                  #delta_color='normal'
                  )
    with col2:
        st.markdown('% change from '+str(base_year)+'.')
        st.metric(label = ' ',
                    #label='% change from 2020.',
                  value=round(100*(co2_year-co2_base)/co2_base,2))
    
    # annual emissions graph    
    subset1 = m_graph1(municipality,dataset,start_year,end_year)
    
    st.text(' ')
    st.text(' ')
    st.markdown('**Which year would you like to look at?**')
    year1 = st.selectbox('Choose a year from the drop down menu',
                         range(end_year,2019,-1),
                         index=0,
                         key='year1')
    
    # emissions pie charts
    year_set1 = my_graph1(municipality,year1,dataset,colors_fuel)


with tab2:
    st.header('Demographics')
    from utils.demographics import m_demog_graph
    
    subset2 = m_demog_graph(municipality,dataset,start_year,end_year)
   
    st.write('Note: The Census does not report median household income above \$250,000. \
             Values of \$250,000 should be interpreted as \$250,000+.')
    st.write('Data sources: U.S. Census Bureau')
    
with tab3:
    st.header('Building Energy and Emissions')
    from utils.bldg_graphs import bldg_graph1, bldg_graph2
    
    if municipality in ['Alford','Berkley','Blackstone','Bolton',
                           'Clarksburg','Dover','Leyden','Mendon',
                           'Millville','Montgomery','Monroe','Oxford',
                           'Rockport','Sterling','Sunderland','Whately']:
        st.markdown('Note: Some data may be missing from Mass Save Data due to a small number of customers.')
        
    # calc # of heat pumps or other metrics to show
    hps = pd.to_numeric(dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2023),'Cumulative heat pumps all (accounts)'],errors='coerce')
    if hps.isna().item():
        hps = 'unknown'
    else: hps = hps.astype('int').item()
    households = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2023),'Households'].astype('int').item()
    ms_participation = (100*pd.to_numeric(dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2023),'Cumulative location participation rate [%] (4)'],errors='coerce'))
    if ms_participation.isna().item():
        ms_participation = 'unknown'
    else: ms_participation = ms_participation.item()
    if dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2023),'CEA Y/N'].item() == 'Yes':
        cea = 'Yes'
    else: cea = 'No'
    
    st.markdown('Building metrics as of 2023.')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        try:
            st.metric(label= 'Mass Save Participation %',
                      value = f'{ms_participation:,.0f}')
        except:
            st.metric(label = 'Mass Save Participation',
                      value = ms_participation)
    with col2:
        try:
            st.metric(label = 'Heat pumps',
                      value = f'{hps:,.0f}')
        except:
            st.metric(label = 'Heat pumps',
                      value = hps)
    with col3:
        st.metric(label = 'Households',
                  value = f'{households:,.0f}')
    with col4:
        st.metric(label = 'Community aggregation?',
                  value = cea)
    # add utility emissions factor in 4th column?
    
    subset3 = bldg_graph1(municipality,dataset,colors_fuel,start_year,end_year)
    
    st.text(' ')
    st.text(' ')
    st.markdown('**Which year would you like to look at?**')
    year3 = st.selectbox('Choose a year from the drop down menu',
                            range(end_year,start_year-1,-1),
                            index=0,
                            key='year3')
    year_set3 = bldg_graph2(municipality,year3,dataset,colors_fuel)
    
    st.write('Notes: The Census uses a statistical model, not direct measurement, to estimate the number \
             of households using each type of heating fuel. Sometimes there will be a nonzero number \
            of households using natural gas for heat in communities that do not have any natural gas \
            infrastructure. The emissions calculations for natural gas rely on utility sales data and \
                so are not affected by this.\
                ')
    
    st.write('Data sources: Mass Save Data, MA DOER, MA DPU, U.S. Census Bureau, U.S. EIA')

with tab4:
    st.header('Solar Energy Adoption')
    from utils.solar_graphs import solar_graph
    st.text(' ')
    st.markdown('Note: Solar data is from the MassCEC PTS as of Feb 2024 and data for 2023 and 2024 are incomplete.')
    st.text(' ')
        
    # add widget w/ total capacity, n projects, avg project size?
    total_cap = solar.loc[(solar['City']==municipality)&(solar['Year']==2023),'Capacity (kW DC) All Cumulative'].round(decimals=0).astype('int').item()
    total_num = solar.loc[(solar['City']==municipality)&(solar['Year']==2023),'Project Count All Cumulative'].round(decimals=0).astype('int').item()
    avg_size = total_cap/total_num
    est_energy = total_cap*8760*0.13*0.001
    col1,col2,col3,col4  = st.columns(4)
    with col1:
        st.metric(label='Capacity (kW DC):',
                  value=f'{total_cap:,.0f}'
                  )
    with col2:
        st.metric(label='Number of projects:',
                  value=f'{total_num:,.0f}'
                  )
    with col3:
        st.metric(label='Average size (kW DC):',
                  value=f'{avg_size:,.0f}'
                  )
    with col4:
        st.metric(label='Est energy (MWh/year):',
                  value=f'{est_energy:,.0f}'
                  )
    
    st.text(' ')
    st.text(' ')
    # add graphs: new and cumulative capacity, pie by sector cap and n
    year_set4 = solar_graph(municipality,solar)
    
    st.write('Data Sources: MassCEC Production Tracking System')

with tab5:
    st.header('Transportation Energy and Emissions')
    from utils.transportation_graphs import trans_graph0, trans_graph
    st.text(' ')
    st.text(' ')
    
    evs_subset = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2025),:]
    bevs = evs_subset.loc[:,'Count EVs 01'].item()
    phevs = evs_subset.loc[:,'Count PHEVs 01'].item()
    ghyb = evs_subset.loc[:,'Count GHYs 01'].item()
    
    stations_subset = stations.loc[(stations['City']==municipality),:]
    charge_stations = stations_subset.loc[:,'Total Level All Station Count'].max()
    
    st.markdown('Electric vehicle metrics for January 2025.')
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric(label='EVs:',
                  value=f'{bevs:,.0f}')
        #st.metric(label='%',
        #          value=f'{}')
    with col2:
        st.metric(label='PHEVs:',
                  value=f'{phevs:,.0f}')
    with col3:
        st.metric(label='Gas Hybrids:',
                  value=f'{ghyb:,.0f}')
    with col4:
        st.metric(label='Charging Stations:',
                  value=f'{charge_stations:,.0f}')
    
    st.text('')
    st.text('')
    set5 = trans_graph0(municipality,dataset,start_year,end_year,colors_vehicles,colors_fuel)
    
    st.text('')
    st.text('')
    st.markdown('**Which year would you like to look at?**')
    year5 = st.selectbox('Choose a year from the drop down menu',
                            range(end_year,2019,-1),
                            index=0,
                            key='year5')
    
    year_set5 = trans_graph(municipality,year5,dataset)
    
    st.write('Data Sources: MA DOT Vehicle Census, MAPC MBTA data, FTA National Transit Database')

with tab6:
    st.header('Waste Emissions: Under construction')
    
    #year6 = st.selectbox('Which year would you like to look at?',
    #                        range(end_year,start_year-1,-1),
    #                        index=0,
    #                        key='year6')
    
    incinerator_towns = ['Bedford','Burlington','Chelmsford','Dracut','Essex', # Covanta Haverhill contract communities
                         'Groton','Harvard','Haverhill','Littleton','Lynnfield',
                         'Middleton','North Reading','Peabody','Reading','Stoneham',
                         'Tewksbury','Tyngsboro','Wakefield','Westford','West Newbury',
                         'Winchester',
                         # SEMASS collects trash from nearly 40 communities in Southeast MA, Cape Cod, and Boston metro area, but not listed in report
                         'Quincy','Braintree','Weymouth','Hingham','Cohasset',
                         'Scituate','Norwell','Hanover','Avon','Stoughton',
                         'Sharon','Dighton','Berkley','Bridgewater','Kingston',
                         'Plymouth','Carver','Wareham','Marion','Rochester',
                         'Acushnet','Fairhaven','Sandwich','Yarmouth','Chatham',
                         'Eastham','Truro',
                         #Wheelabrator Millbury
                         'Auburn','Blackstone','Dedham','Dover','East Brookfield',
                         'Franklin','Grafton','Holden','Holliston','Hopedale',
                         'Hopkinton','Maynard','Medfield','Medway','Mendon',
                         'Milford','Millbury','Millis','Millville','Natick',
                         'Needham','Newton','Northborough','Norfolk','Mansfield',
                         'Paxton','Princeton','Rutland','Sherborn','Shrewsbury',
                         'Southborough','Spencer','Sutton','Upton','Walpole',
                         'Westborough','Weston','Westwood','Worcester',
                         # Wheelabrator North Andover
                         'Acton','Amesbury','Arlington','Belmont','Billerica',
                         'Boxborough','Carlisle','Hamilton','Ipswich','Lexington',
                         'Lincoln','Lowell','Manchester','Merrimac','Newburyport',
                         'North Andover','Pepperell','Salisbury','Waltham','Watertown',
                         'Wenham','Wilmington','Winchester',
                         # Wheelabrator Saugus
                         'Boston','Chelsea','Everett','Lynn','Manchester',
                         'Newton','Revere','Saugus','Somerville'
                         ]
    
    mwra_towns = ['Arlington','Ashland','Bedford','Belmont','Boston','Braintree',
                  'Brookline','Burlington','Cambridge','Canton','Chelsea','Clinton',
                  'Dedham','Everett','Framingham','Hingham','Holbrook','Lancaster',
                  'Lexington','Malden','Medford','Melrose','Milton','Nahant','Natick',
                  'Needham','Newton','Norwood','Quincy','Randolph','Reading','Revere',
                  'Somerville','Stoneham','Stoughton','Wakefield','Walpole','Waltham',
                  'Watertown','Wellesley','Westwood','Weymouth',
                  'Wilmington','Winchester','Winthrop','Woburn'
                  ]
    
    st.markdown('What share (%) of trash in '+municipality+' is disposed in a landfill?')
    if dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2022),'Incinerator'].item()=='Y':
        landfill = 0
    else:
        landfill = 100
        pct_msw = st.slider('Move the slider to adjust. 0 is all going to an incinerator, 100 is all going to a landfill.',
                             value=landfill,
                             min_value=0,max_value=100,key='landfill')
    #mwra = st.toggle('Is your municipality part of the MWRA?',
    #                 value=True,key='mwra')

    #year_set6 = waste_graph(municipality,year6,dataset,colors_waste)
    
    st.write('Data Sources: MA DEP')
    
with tab7:
    st.header('Comparison Tool')
    st.text(' ')
    st.text(' ')
    
    st.markdown('**Which dataset would you like to map?**')
    data1 = st.selectbox('Choose from the drop down menu',
                         ['Total Emissions','Per Capita Emissions',
                          'Building Emissions','Transportation Emissions',
                          'Solar PV Capacity','Percent EVs'],
                         index=1,
                         key='data1')
    st.markdown('**Which year would you like to look at?**')
    
    if data1 in ['Total Emissions','Per Capita Emissions','Transportation Emissions']:
        start_year = 2020
    else: start_year = 2017
    year7 = st.selectbox('Choose from the drop down menu',
                         range(end_year,start_year-1,-1),
                         index=0,
                         key='year7')
    
    dataset_year = map_figure(year7,data1)

with tab8:
    st.header('State Targets')
    st.subheader('MA has established statewide emissions targets by sector.')
    st.markdown('Percent reduction in CO2e relative to 1990.')
    
    target_table = pd.DataFrame({'2025':['29%','24%','18%','53%'],
                                 '2030':['49%','44%','34%','70%'],
                                 '2050':['95%','92%','86%','93%']},
                                index=['Residential Heating and Cooling',
                                       'Commercial Heating and Cooling',
                                       'Transportation',
                                       'Electric Power'])
    st.table(data=target_table)
    




