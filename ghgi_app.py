# -*- coding: utf-8 -*-
"""
Main file in public dashboard tool
MA Greenhouse Gas Inventory Tool
"""

import streamlit as st
import pandas as pd
#import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

start_year = 2019
end_year = 2022

st.set_page_config(layout='wide',
                   page_title='MA GHGI Tool'
                   )

st.title('Community Greenhouse Gas Inventory Tool')
st.write('This tool shows municipality-wide energy and emissions data from \
        buildings, transportation, and waste. Residential and commercial \
        activities are included in addition to municipal. This is app is \
        under development and does not yet include all possible sources of \
        emissions. Please use the feedback page on the left if you have \
        questions about anything in this dashboard.')
        
colors_fuel = {'Electricity':'darkgreen',
               'Wood':'forestgreen',
               'Natural Gas':'mediumseagreen',
               'Propane':'yellowgreen',
               'Fuel Oil':'darkkhaki',
               'Gasoline':'olive',
               'Other':'goldenrod'}

colors_waste = {'Trash':'darkblue',
                'Single Stream Recycling':'blue',
                'Other Recycling':'royalblue',
                'Organics':'lightsteelblue'}

# loading data function
@st.cache_data
def load_data():
    df = pd.read_excel('datasets/municipal_emissions.xlsx')
    df = df.drop(columns=['Unnamed: 0'])
    gdf = json.load(open('datasets/municipalities.json'))
    
    dataset = df[df['Year']>start_year-1]
    dataset['Median household income'] = dataset['Median household income'].str.replace('+','')
    dataset['Median household income'] = pd.to_numeric(dataset['Median household income'],errors='coerce')
    dataset['Per Capita (CO2e)'] = dataset['Total (CO2e)']/dataset['Population']
    #print(dataset['Per Capita (CO2e)'])
    
    return dataset,gdf

# function for annual emissions graph(s)
@st.cache_data
def m_graph1(m):
    st.session_state.key = m
    
    subset = dataset[dataset['Municipality']==m]
    
    # Line graph of total emissions and emission per capita
    # make the figure
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'},{'type':'scatter'}]],
                        subplot_titles=('Total CO2e','Per Capita CO2e')
                        )
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Total (CO2e)'].round(0),name='Total CO2e'),
        row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Per Capita (CO2e)'].round(2),name='Per Capita CO2e'),
        row=1,col=2)
    
    fig.update_layout(title=dict(text='Emissions in '+m,font=dict(size=28)),
                      yaxis=dict(range=[0,1.4*(subset['Total (CO2e)'].max())],
                                 title=dict(text='Total CO2e',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      yaxis2=dict(range=[0,1.5*(subset['Per Capita (CO2e)'].max())],
                                  title=dict(text='Per Capita CO2e',font=dict(size=18),standoff=0),
                                  tickfont=dict(size=14))
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
                     tickvals=list(range(start_year,end_year+1)),
                     tickfont=dict(size=14))
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',showlegend=False)
    st.plotly_chart(fig)
    
    return subset

# function for one year pie charts
@st.cache_data
def my_graph1(m,y):
    year_set = dataset[(dataset['Year']==y)&(dataset['Municipality']==m)]
    
    # data prep for pie charts
    graph_cols1 = ['Total Electricity (CO2e)','Total Gas (CO2e)',
                  'Total Propane (CO2e)','Total Fuel Oil (CO2e)',
                  'Total Gasoline (CO2e)']
    year_sub1 = year_set[graph_cols1].T
    year_sub1 = year_sub1.rename(columns={year_sub1.columns[0]:'Emissions'},
                               index={'Total Electricity (CO2e)':'Electricity',
                                      'Total Gas (CO2e)':'Natural Gas',
                                         'Total Fuel Oil (CO2e)':'Fuel Oil',
                                         'Total Propane (CO2e)':'Propane',
                                         'Total Gasoline (CO2e)':'Gasoline'
                                         }
                               )
    year_sub1 = year_sub1.reset_index()
    
    graph_cols2 = ['Total Residential Buildings (CO2e)',
                   'Total Commercial & Industrial Buildings (CO2e)',
                   'Total Transportation (CO2e)']
    year_sub2 = year_set[graph_cols2].T
    year_sub2 = year_sub2.rename(columns={year_sub2.columns[0]:'Emissions'},
                               index={'Total Residential Buildings (CO2e)':'Residential',
                                      'Total Commercial & Industrial Buildings (CO2e)':'Commercial & Industrial',
                                      'Total Transportation (CO2e)':'Transportation'
                                      }
                                   )
    year_sub2 = year_sub2.reset_index()
    
    graph_cols3 = ['Total Electricity (MMBTU)','Total Gas (MMBTU)',
                  'Total Propane (MMBTU)','Total Fuel Oil (MMBTU)',
                  'Total Gasoline (MMBTU)']
    year_sub3 = year_set[graph_cols3].T
    year_sub3 = year_sub3.rename(columns={year_sub3.columns[0]:'Energy'},
                               index={'Total Electricity (MMBTU)':'Electricity',
                                      'Total Gas (MMBTU)':'Natural Gas',
                                      'Total Fuel Oil (MMBTU)':'Fuel Oil',
                                      'Total Propane (MMBTU)':'Propane',
                                      'Total Gasoline (MMBTU)':'Gasoline'
                                      }
                               )
    year_sub3 = year_sub3.reset_index()
    
    graph_cols4 = ['Total Residential Buildings (MMBTU)',
                   'Total Commercial & Industrial Buildings (MMBTU)',
                   'Total Gasoline (MMBTU)']
    year_sub4 = year_set[graph_cols4].T
    year_sub4 = year_sub4.rename(columns={year_sub4.columns[0]:'Energy'},
                               index={'Total Residential Buildings (MMBTU)':'Residential',
                                      'Total Commercial & Industrial Buildings (MMBTU)':'Commercial & Industrial',
                                      'Total Gasoline (MMBTU)':'Transportation'
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
                        vertical_spacing=0.1
                        )
    fig.add_trace(
        go.Pie(labels=year_sub1['index'], values=year_sub1['Emissions'].round(0),
               sort=False,marker_colors=year_sub1['index'].map(colors_fuel),
               textinfo='label+percent',textfont_size=14),
        row=1,col=1)
    fig.add_trace(
        go.Pie(labels=year_sub2['index'], values=year_sub2['Emissions'].round(0),
               sort=False,
               textinfo='label+percent',textfont_size=14),
        row=1,col=2)
    fig.add_trace(
        go.Pie(labels=year_sub3['index'],values=year_sub3['Energy'].round(0),
               sort=False,
               textinfo='label+percent',textfont_size=14),
        row=2,col=1)
    fig.add_trace(
        go.Pie(labels=year_sub4['index'],values=year_sub4['Energy'].round(0),
               sort=False,
               textinfo='label+percent',textfont_size=14),
        row=2,col=2)
    
    fig.update_layout(title=dict(text='Shares of energy and emissions in '+str(y),font=dict(size=28)),
                      height=750,width=800,
                      showlegend=False
                      )
    
    st.plotly_chart(fig)
    return year_set

# functions for demographic figures
@st.cache_data
def m_demog_graph(m2):
    st.session_state.key = m2
    
    subset = dataset[dataset['Municipality']==m2]
    
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
        go.Scatter(x=subset.Year,y=subset['Total Heating Fuels Households']),
        row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Median household income']),
        row=3,col=1)
    
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',showlegend=False,
                      yaxis=dict(range=[0,1.4*(subset['Population'].max())],
                                 title=dict(text='People',font=dict(size=18)),
                                 tickfont=dict(size=14)),
                      yaxis2=dict(range=[0,1.4*(subset['Total Heating Fuels Households'].max())],
                                  title=dict(text='Households',font=dict(size=18)),
                                  tickfont=dict(size=14)),
                      yaxis3=dict(range=[0,1.4*(subset['Median household income'].max())],
                                  title=dict(text='$',font=dict(size=18)),
                                  tickfont=dict(size=14)),
                      height=1200,width=700
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
                     tickvals=list(range(start_year,end_year+1)),
                     tickfont=dict(size=14))
    
    st.plotly_chart(fig)
    return subset

# function for buildings
@st.cache_data
def bldg_graph1(m3):
    subset = dataset[dataset['Municipality']==m3]
    
    # stacked area charts - energy and emissions
    fig = make_subplots(rows=2,cols=2,
                        subplot_titles=('Residential Energy by fuel in MMBTU',
                                        'Commercial Energy by fuel in MMBTU',
                                        'Residential Emissions by fuel in CO2e',
                                        'Commercial Emissions by fuel in CO2e'),
                        vertical_spacing = 0.2
                        )
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Electricity (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Electricity',line=dict(color=colors_fuel['Electricity']),
                   legendgroup = '1'),
                   row=1,col=1)
    #fig.add_trace(
    #    go.Scatter(x=subset['Year'],y=subset['Residential Wood (MMBTU)'],
    #               hoverinfo='x+y+name',mode='lines',stackgroup='one',
    #               name='Wood',line=dict(color=colors_fuel['Wood']),
    #               legendgroup = '1'),
    #               row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Gas (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
                   legendgroup = '1'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Propane (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Propane',line=dict(color=colors_fuel['Propane']),
                   legendgroup = '1'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Fuel Oil (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
                   legendgroup = '1'),
                   row=1,col=1)
    
    
    
    # Commercial and Industrial Energy
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Commercial & Industrial Electricity (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='two',
                   name='Electricity',line=dict(color=colors_fuel['Electricity']),
                   legendgroup = '1',showlegend=False),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Commercial & Industrial Gas (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='two',
                   name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
                   legendgroup = '1',showlegend=False),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Commercial Fuel Oil (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='two',
                   name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
                   legendgroup = '1',showlegend=False),
                   row=1,col=2)
    
    # Residential Emissions 
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Electricity (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Electricity',line=dict(color=colors_fuel['Electricity']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    #fig.add_trace(
    #    go.Scatter(x=subset['Year'],y=subset['Residential Wood (CO2e)'],
    #               hoverinfo='x+y+name',mode='lines',stackgroup='three',
    #               name='Wood',line=dict(color=colors_fuel['Wood']),
    #               legendgroup = '1',showlegend=False),
    #               row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Gas (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Propane (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Propane',line=dict(color=colors_fuel['Propane']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Fuel Oil (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    
    
    # Commercial and Industrial Emissions
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Commercial & Industrial Electricity (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='four',
                   name='Electricity',line=dict(color=colors_fuel['Electricity']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Commercial & Industrial Gas (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='four',
                   name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Commercial Fuel Oil (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='four',
                   name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Direct Emissions (CO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='four',
                   name='Other',line=dict(color=colors_fuel['Other']),
                   legendgroup = '1'),
                   row=2,col=2)

    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',
                      title=dict(text='Building energy and emissions in '+m3,font=dict(size=28)),
                      yaxis=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      yaxis2=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=0),
                                  tickfont=dict(size=14)),
                      yaxis3=dict(title=dict(text='CO2e',font=dict(size=18),standoff=0),
                                  tickfont=dict(size=14)),
                      yaxis4=dict(title=dict(text='CO2e',font=dict(size=18),standoff=0),
                                  tickfont=dict(size=14)),
                      height=750,width=900
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
                     tickvals=list(range(start_year,end_year+1)),
                     tickfont=dict(size=14))
    
    st.plotly_chart(fig)
    return subset
    
def bldg_graph2(m3,y3):    
    year_set = dataset[(dataset['Year']==y3)&(dataset['Municipality']==m3)]
    # Data prep
    # Residential emissions
    graph_cols1 = ['Residential Electricity (CO2e)','Residential Gas (CO2e)',
                   'Residential Propane (CO2e)','Residential Fuel Oil (CO2e)']
    
    rf_year_sub = year_set[graph_cols1].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Electricity (CO2e)':'Electricity',
                                            'Residential Gas (CO2e)':'Natural Gas',
                                            'Residential Fuel Oil (CO2e)':'Fuel Oil',
                                            'Residential Propane (CO2e)':'Propane'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    #print(rf_year_sub)
    
    # Commercial emissions
    graph_cols2 = ['Commercial & Industrial Electricity (CO2e)','Commercial & Industrial Gas (CO2e)',
                      'Commercial Fuel Oil (CO2e)','Direct Emissions (CO2e)']

    cf_year_sub = year_set[graph_cols2].T
    cf_year_sub = cf_year_sub.rename(columns={cf_year_sub.columns[0]:'Emissions'},
                                     index={'Commercial & Industrial Electricity (CO2e)':'Electricity',
                                      'Commercial & Industrial Gas (CO2e)':'Natural Gas',
                                         'Commercial Fuel Oil (CO2e)':'Fuel Oil',
                                         'Direct Emissions (CO2e)':'Other'}
                                     )
    cf_year_sub = cf_year_sub.reset_index()
    #print(cf_year_sub)
    
    # Residential heating fuels pie chart
    hh_graph_cols = ['Electricity','Utility gas',
                     'Fuel oil, kerosene, etc.','Bottled, tank, or LP gas',
                     'Wood','Solar energy','Coal or coke',
                     'Other fuel','No fuel used']
    
    hh_year_sub = year_set[hh_graph_cols].T*100
    hh_year_sub = hh_year_sub.rename(columns={hh_year_sub.columns[0]:'Fuels'},
                                     index={'Utility gas':'Natural Gas',
                                            'Fuel oil, kerosene, etc.':'Fuel Oil',
                                            'Bottled, tank, or LP gas':'Propane'}
                                     )
    hh_year_sub = hh_year_sub.reset_index()
    
    #print(hh_year_sub)
    threshold = hh_year_sub['Fuels'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    #print('threshold: '+str(threshold))
    hh_row_other = hh_year_sub.loc[hh_year_sub['Fuels']<threshold].sum(numeric_only=True)
    hh_row_other = hh_row_other.rename('Fuels')
    hh_row_other = hh_row_other.rename(index={hh_row_other.index[0]:'Other'}).reset_index()
    #print(hh_row_other)
    hh_year_sub_t = hh_year_sub.loc[hh_year_sub['Fuels']>=threshold]
    hh_year_sub_f = pd.concat([hh_year_sub_t,hh_row_other])
    #print(hh_year_sub_f)
    
    
    # Commercial sectors pie chart
    cc_graph_cols = year_set.loc[:,year_set.columns.str.startswith('Average Monthly Employment')].columns
    cc_year_sub = year_set[cc_graph_cols].T*100
    cc_year_sub = cc_year_sub.rename(columns={cc_year_sub.columns[0]:'Employment'})
    cc_year_sub = cc_year_sub.reset_index()
    cc_year_sub['index'] = cc_year_sub['index'].str.replace('Average Monthly Employment ','')
    
    #print(cc_year_sub)
    threshold_c = cc_year_sub['Employment'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    #print(threshold_c)
    cc_row_other = cc_year_sub.loc[cc_year_sub['Employment']<threshold_c].sum(numeric_only=True)
    cc_row_other = cc_row_other.rename('Employment')
    cc_row_other = cc_row_other.rename(index={cc_row_other.index[0]:'Other'}).reset_index()
    #print(cc_row_other)
    cc_year_sub_t = cc_year_sub.loc[cc_year_sub['Employment']>=threshold_c]
    cc_year_sub_f = pd.concat([cc_year_sub_t,cc_row_other])
    #print(cc_year_sub_f)
    
    # pie charts
    fig = make_subplots(rows=2,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}],
                                             [{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=('Share of residential emissions by fuel',
                                        'Share of commercial emissions by fuel',
                                        'Share of households by heating fuel',
                                        'Share of commercial employment by sector'),
                        horizontal_spacing = 0.03,
                        vertical_spacing = 0.1
                        )
    fig.add_trace(
        go.Pie(labels=rf_year_sub['index'], values=rf_year_sub['Emissions'].round(0),
               sort=False,
               textinfo='label+percent',textfont_size=14),
        row=1,col=1)
    fig.add_trace(
        go.Pie(labels=cf_year_sub['index'], values=cf_year_sub['Emissions'].round(0),
               sort=False,marker_colors=cf_year_sub['index'].map(colors_fuel),
               textinfo='label+percent',textfont_size=14),
        row=1,col=2)
    fig.add_trace(
        go.Pie(labels=hh_year_sub_f['index'], values=hh_year_sub_f['Fuels'].round(0),
               sort=False,marker_colors=hh_year_sub_f['index'].map(colors_fuel),
               textinfo='label+percent',textfont_size=14),
        row=2,col=1)
    fig.add_trace(
        go.Pie(labels=cc_year_sub_f['index'], values=cc_year_sub_f['Employment'].round(0),
               textinfo='label+percent',textfont_size=14),
        row=2,col=2)
    
    fig.update_layout(title=dict(text='Share emissions and sources in '+str(y3),font=dict(size=28)),
                      height=900,width=900,
                      showlegend=False
                      )

    st.plotly_chart(fig)
    return year_set
    
    # add graph showing number of employers and jobs in different sectors


# function for transportation
@st.cache_data
def trans_graph(m5,y5):
    subset = dataset[dataset['Municipality']==m5]
    year_set5 = dataset[(dataset['Year']==y5)&(dataset['Municipality']==m5)]
    # Transportation emissions pie chart
    graph_cols = ['Residential Gasoline (CO2e)','Residential Vehicle Electricity (CO2e)',
                  'Commercial Gasoline (CO2e)','Commercial Vehicle Electricity (CO2e)',
                  'Municipal Gasoline (CO2e)','Municipal Vehicle Electricity (CO2e)']

    rf_year_sub = year_set5[graph_cols].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Gasoline (CO2e)':'Passenger Gasoline',
                                      'Residential Vehicle Electricity (CO2e)':'Passenger Electricity',
                                        'Commercial Gasoline (CO2e)':'Commercial Gasoline',
                                        'Commercial Vehicle Electricity (CO2e)':'Commercial Electricity',
                                        'Municipal Gasoline (CO2e)':'Municipal Gasoline',
                                        'Municipal Vehicle Electricity (CO2e)':'Municipal Electricity'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    
    #print(rf_year_sub)
    threshold_v = rf_year_sub['Emissions'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    #print('threshold: '+str(threshold_v))
    rf_row_other = rf_year_sub.loc[rf_year_sub['Emissions']<threshold_v].sum(numeric_only=True)
    rf_row_other = rf_row_other.rename('Emissions')
    rf_row_other = rf_row_other.rename(index={rf_row_other.index[0]:'Other'}).reset_index()
    #print(rf_row_other)
    rf_year_sub_t = rf_year_sub.loc[rf_year_sub['Emissions']>=threshold_v]
    rf_year_sub_f = pd.concat([rf_year_sub_t,rf_row_other])
    #print(rf_year_sub_f)
    
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'}, {'type':'domain'}]],
                        subplot_titles=('Share of electric vehicles over time',
                                        'Share of emissions by fuel and sector'),
                        horizontal_spacing = 0.05,
                        )
    
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Residential Gasoline (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Passenger Gasoline'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Residential Vehicle Electricity (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Passenger Electricity'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Commercial Gasoline (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Commercial Gasoline'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Commercial Vehicle Electricity (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Commercial Electricity'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Municipal Gasoline (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Municipal Gasoline'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Municipal Vehicle Electricity (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   name='Municipal Electricity'),
                   row=1,col=1)
    
    fig.add_trace(
        go.Pie(labels=rf_year_sub_f['index'], values=rf_year_sub_f['Emissions'].round(0),
               textinfo='label+percent',textfont_size=14,showlegend=False),
        row=1,col=2)
    
    fig.update_layout(title=dict(text='Share emissions and sources in '+str(y5),font=dict(size=28)),
                      yaxis=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      xaxis=dict(title=dict(text='Year',font=dict(size=18)),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14)),
                      height=600,width=500
                      )

    st.plotly_chart(fig)
    
    # plot trends in VMT and # of vehicles

# function for waste
@st.cache_data
def waste_graph(m6,y6):
    subset = dataset[dataset['Municipality']==m6]
    year_set6 = dataset[(dataset['Year']==y6)&(dataset['Municipality']==m6)]
    
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'scatter'}, {'type':'domain'}]],
                        subplot_titles=('Solid waste over time',
                                        'Share of waste in '+str(y6)),
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

    msw_year_sub = year_set6[graph_cols].T
    msw_year_sub = msw_year_sub.rename(columns={msw_year_sub.columns[0]:'Waste'},
                                     index={'trash':'Trash',
                                      'single stream recyc':'Single Stream Recycling',
                                        'other recyc':'Other Recycling',
                                        'organics':'Organics'}
                                     )
    msw_year_sub = msw_year_sub.reset_index()
    
    fig.add_trace(
        go.Pie(labels=msw_year_sub['index'], values=msw_year_sub['Waste'].round(0),
               marker_colors=msw_year_sub['index'].map(colors_waste),
               textinfo='label+percent',textfont_size=14,showlegend=False),
        row=1,col=2)
    
    fig.update_layout(title=dict(text='Solid waste in '+str(m6),font=dict(size=28)),
                      yaxis=dict(title=dict(text='tons',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      xaxis=dict(title=dict(text='Year',font=dict(size=18)),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14)),
                      height=600,width=1200)
    #fig.layout.update(showlegend=False)

    st.plotly_chart(fig)
    return year_set6

# function for statewide maps for a single year
@st.cache_data
def map_figure(y,d):
    st.session_state.key = d
    
    dataset_year = dataset[dataset['Year']==y]
    
    #geo should be a dictionary of geospatial data and df has the non-spatial data
    #then they are linked together via an id
    
    # add a way to select different items to display on the map
    if d == 'Total Emissions':
        # total emissions
        st.write('Total emissions by municipality')
        fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                            featureidkey='properties.Name',color='Total (CO2e)')
    
    elif d == 'Per Capita Emissions':
        # per capita emissions
        st.write('Per person emissions by municipality in '+str(y))
        fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                            featureidkey='properties.Name',color='Per Capita (CO2e)')
        
    elif d == 'Building Emissions':
        dataset_year['Total Buildings (CO2e)'] = dataset_year[['Total Residential Buildings (CO2e)',
                                                               'Total Commercial & Industrial Buildings (CO2e)']].sum()
        st.write('Per person emissions by municipality in '+str(y))
        fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                            featureidkey='properties.Name',color='Total Buildings (CO2e)')
        
    elif d == 'Transportation Emissions':
        st.write('Per person emissions by municipality in '+str(y))
        fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                            featureidkey='properties.Name',color='Total Transportation (CO2e)')
    
    fig.update_geos(fitbounds='locations',visible=False)
    fig.update_layout(height=500,width=800,
                      margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
        
    return dataset_year

#############################################################################
# Running the dashboard

dataset, geo = load_data()

#municipality = st.sidebar.selectbox(
#    'Which city or town would you like to explore?',
#    dataset['Municipality'].unique())
#
#year = st.sidebar.slider('Choose a year',
#                        min_value=start_year,max_value=end_year,
#                       value=end_year)

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Overview','Demographics',
                                        'Buildings','Transportation','Waste'])

with tab1:
    st.header('Overview of Energy and Emissions')
    
    # annual emissions graph
    municipality1 = st.selectbox('Which city or town would you like to explore? \n \
                                 Click in the box and type the name or scroll through the drop down list.',
                                 dataset['Municipality'].unique().tolist(),
                                 index=0,
                                 key='municipality1')
    subset1 = m_graph1(municipality1)
    
    year1 = st.selectbox('Which year would you like to look at?',
                         range(end_year,start_year-1,-1),
                         index=0,
                         key='year1')
    
    data1 = st.selectbox('Which dataset would you like to map?',
                         ['Total Emissions','Per Capita Emissions',
                          'Building Emissions','Transportation Emissions'],
                         index=1,
                         key='data1')
    
    dataset_year = map_figure(year1,data1)
    
    # emissions pie charts
    
    year_set1 = my_graph1(municipality1,year1)
    
    st.write('Note: Commercial & Industrial includes emissions from industrial \
             processes as well as any on site combustion at industrial facilities.')


with tab2:
    st.header('Demographics')
    
    municipality2 = st.selectbox('Which city or town would you like to explore? \n \
                                 Click in the box and type the name or scroll through the drop down list.',
                                 dataset['Municipality'].unique().tolist(),
                                 index=0,
                                 key='municipality2')
    subset2 = m_demog_graph(municipality2)
   
    st.write('Note: The Census does not report median household income above \$250,000. \
             Values of \$250,000 should be interpreted as \$250,000+.')
    st.write('Data sources: U.S. Census Bureau')
    
with tab3:
    st.header('Building Energy and Emissions')
    
    municipality3 = st.selectbox('Which city or town would you like to explore? \n \
                                 Click in the box and type the name or scroll through the drop down list.',
                                 ['Massachusetts'] + dataset['Municipality'].unique().tolist(),
                                 index=0,
                                 key='municipality3')
    
    subset3 = bldg_graph1(municipality3)
    
    year3 = st.selectbox('Which year would you like to look at?',
                            range(end_year,start_year-1,-1),
                            index=0,
                            key='year3')
    year_set3 = bldg_graph2(municipality3,year3)
    
    st.write('Notes: (1) The Census uses a statistical model, not direct measurement, to estimate the number \
             of households using each type of hearing fuel. Sometimes there will be a nonzero number \
            of households using natural gas for heat in communities that do not have any natural gas \
            infrastructure. The emissions calculations for natural gas rely on utility sales data and \
                so are not affected by this.\
                (2) Commercial and Industrial includes emissions from industrial processes as well as on site combustion emissions.')
    
    st.write('Data sources: Mass Save Data, MA DOER, MA DPU, U.S. Census Bureau, U.S. EIA')

with tab4:
    st.header('Transportation Energy and Emissions')
    
    municipality5 = st.selectbox('Which city or town would you like to explore? \n \
                                 Click in the box and type the name or scroll through the drop down list.',
                                 ['Massachusetts'] + dataset['Municipality'].unique().tolist(),
                                 index=0,
                                 key='municipality5')
    year5 = st.selectbox('Which year would you like to look at?',
                            range(end_year,start_year-1,-1),
                            index=0,
                            key='year5')
    year_set5 = trans_graph(municipality5,year5)
    
    st.write('Data Sources: MA DOT')

with tab5:
    st.header('Waste Emissions')
    
    municipality6 = st.selectbox('Which city or town would you like to explore? \n \
                                 Click in the box and type the name or scroll through the drop down list.',
                                 ['Massachusetts'] + dataset['Municipality'].unique().tolist(),
                                 index=0,
                                 key='municipality6')
    year6 = st.selectbox('Which year would you like to look at?',
                            range(end_year,start_year-1,-1),
                            index=0,
                            key='year6')
    year_set6 = waste_graph(municipality6,year6)
    
    st.write('Data Sources: MA DEP')
    
    
    




