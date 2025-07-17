# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 09:44:05 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# function for transportation
@st.cache_data
def trans_graph0(m,dataset,start_year,end_year,colors_vehicles,colors_fuel):
    subset = dataset.loc[(dataset['Municipality']==m)&(dataset['Year']>2019),:]
    
    fig = make_subplots(rows=2,cols=2,specs=[[{'type':'scatter'}, {'type':'scatter'}],
                                             [{'type':'scatter'}, {'type':'scatter'}]],
                        subplot_titles=('Vehicle counts over time',
                                        'Vehicle miles traveled over time',
                                        'Energy use over time',
                                        'Emissions over time'),
                        horizontal_spacing = 0.15,
                        vertical_spacing = 0.2
                        )
    
    # Line graph of vehicle counts over time
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Count FFs 01'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '1',
                   name='Fossil Fuel',line=dict(color=colors_vehicles['Fossil Fuel'])
                   ),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Count GHYs 01'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '1',
                   name='Gas Hybrid',line=dict(color=colors_vehicles['Hybrid Electric'])
                   ),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Count PHEVs 01'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '1',
                   name='Plug-in Hybrid',line=dict(color=colors_vehicles['Plug-in Hybrid'])
                   ),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Count EVs 01'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '1',
                   name='Electric',line=dict(color=colors_vehicles['Electric Vehicle'])
                   ),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset[[' Count    Fuel Cell Electric Vehicle  Commercial 01',
                                          ' Count    Fuel Cell Electric Vehicle  Municipal 01',
                                          ' Count    Fuel Cell Electric Vehicle  Passenger 01',
                                          ' Count    Fuel Cell Electric Vehicle  State 01']].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '1',
                   name='Fuel Cell',line=dict(color=colors_vehicles['Fuel Cell'])
                   ),
                   row=1,col=1)
    
    # Line graph of Daily Vehicle Miles Traveled over time
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Fossil Fuel  Commercial 01',
                                          ' DailyVMT    Fossil Fuel  Municipal 01',
                                          ' DailyVMT    Fossil Fuel  Passenger 01',
                                          ' DailyVMT    Fossil Fuel  State 01']].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '1',
                   name='Fossil Fuel',line=dict(color=colors_vehicles['Fossil Fuel'])
                   ),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Hybrid Electric Vehicle  Commercial 01',
                                          ' DailyVMT    Hybrid Electric Vehicle  Municipal 01',
                                          ' DailyVMT    Hybrid Electric Vehicle  Passenger 01',
                                          ' DailyVMT    Hybrid Electric Vehicle  State 01']].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '1',
                   name='Gas Hybrid',line=dict(color=colors_vehicles['Hybrid Electric'])
                   ),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Plug in Hybrid Electric  Commercial 01',
                                          ' DailyVMT    Plug in Hybrid Electric  Municipal 01',
                                          ' DailyVMT    Plug in Hybrid Electric  Passenger 01',
                                          ' DailyVMT    Plug in Hybrid Electric  State 01']].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '1',
                   name='Plug-in Hybrid',line=dict(color=colors_vehicles['Plug-in Hybrid'])
                   ),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Electric Vehicle  Commercial 01',
                                          ' DailyVMT    Electric Vehicle  Municipal 01',
                                          ' DailyVMT    Electric Vehicle  Passenger 01',
                                          ' DailyVMT    Electric Vehicle  State 01']].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '1',
                   name='Electric',line=dict(color=colors_vehicles['Electric Vehicle'])
                   ),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset[[' DailyVMT    Fuel Cell Electric Vehicle  Commercial 01',
                                          ' DailyVMT    Fuel Cell Electric Vehicle  Municipal 01',
                                          ' DailyVMT    Fuel Cell Electric Vehicle  Passenger 01',
                                          ' DailyVMT    Fuel Cell Electric Vehicle  State 01']].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '1',
                   name='Fuel Cell',line=dict(color=colors_vehicles['Fuel Cell'])),
                   row=1,col=2)
    
    # Transportation energy
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset['Total Gasoline (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '2',
                   name='Gasoline',line=dict(color=colors_fuel['Gasoline'])
                   ),
                   row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset['Total Diesel (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '2',
                   name='Diesel',line=dict(color=colors_fuel['Diesel'])
                   ),
                   row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset['Total Vehicle Electricity (MMBTU)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '2',
                   name='Electricity',line=dict(color=colors_fuel['Electricity'])
                   ),
                   row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset[['Total Public Transportation (MMBTU)']].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   showlegend=False,legendgroup = '2',
                   name='Electricity',line=dict(color='lightsteelblue')
                   ),
                   row=2,col=1)
    
    # Transportation emissions
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset['Total Gasoline (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '2',
                   name='Gasoline',line=dict(color=colors_fuel['Gasoline'])
                   ),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset['Total Diesel (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '2',
                   name='Diesel',line=dict(color=colors_fuel['Diesel'])
                   ),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset['Total Vehicle Electricity (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '2',
                   name='Electricity',line=dict(color=colors_fuel['Electricity'])
                   ),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year[:-1],y=subset[['Total Public Transportation (MTCO2e)',
                                                'MBTA Diesel (MTCO2e)','MBTA Electricity (MTCO2e)','MBTA CNG (MTCO2e)'
                                                ]].sum(axis=1),
                   hoverinfo='x+y+name',mode='lines',stackgroup='one',
                   legendgroup = '2',
                   name='Public Transit',line=dict(color='lightsteelblue')
                   ),
                   row=2,col=2)
    
    fig.update_layout(hovermode='x',
                      title=dict(text='Share of vehicles and miles driven in '+m,font=dict(size=24)),
                      yaxis=dict(title=dict(text='Vehicles',font=dict(size=18,color='black'),standoff=10),
                                 tickfont=dict(size=14,color='black')),
                      yaxis2=dict(title=dict(text='Daily VMT',font=dict(size=18,color='black'),standoff=0),
                                 tickfont=dict(size=14,color='black')),
                      yaxis3=dict(title=dict(text='MMBTU',font=dict(size=18,color='black'),standoff=10),
                                 tickfont=dict(size=14,color='black')),
                      yaxis4=dict(title=dict(text='MTCO2e',font=dict(size=18,color='black'),standoff=0),
                                 tickfont=dict(size=14,color='black')),
                      xaxis=dict(title=dict(text='Year',font=dict(size=18,color='black')),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14,color='black')),
                      xaxis2=dict(title=dict(text='Year',font=dict(size=18,color='black')),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14,color='black')),
                      xaxis3=dict(title=dict(text='Year',font=dict(size=18,color='black')),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14,color='black')),
                      xaxis4=dict(title=dict(text='Year',font=dict(size=18,color='black')),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14,color='black')),
                      legend_tracegroupgap = 280,
                      height=800,width=1000,
                      annotations=[dict(font=dict(color='black'))]
                      )

    st.plotly_chart(fig)
    

@st.cache_data
def trans_graph(m,y5,dataset):
    subset = dataset[(dataset['Municipality']==m)&(dataset['Year']>2019)]
    year_set5 = dataset[(dataset['Year']==y5)&(dataset['Municipality']==m)]
    
    # Transportation energy pie chart
    graph_cols = ['Residential Gasoline (MMBTU)','Residential Diesel (MMBTU)','Residential Vehicle Electricity (MMBTU)',
                  'Commercial Gasoline (MMBTU)','Commercial Diesel (MMBTU)','Commercial Vehicle Electricity (MMBTU)',
                  'Municipal Gasoline (MMBTU)','Municipal Diesel (MMBTU)','Municipal Vehicle Electricity (MMBTU)',
                  'Total Public Transportation (MMBTU)'
                  ]

    rf_year_sub = year_set5[graph_cols].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Energy'},
                                     index={'Residential Gasoline (MMBTU)':'Passenger Gasoline',
                                            'Residential Diesel (MMBTU)':'Passenger Diesel',
                                      'Residential Vehicle Electricity (MMBTU)':'Passenger Electricity',
                                        'Commercial Gasoline (MMBTU)':'Commercial Gasoline',
                                        'Commercial Diesel (MMBTU)':'Commercial Diesel',
                                        'Commercial Vehicle Electricity (MMBTU)':'Commercial Electricity',
                                        'Municipal Gasoline (MMBTU)':'Municipal Gasoline',
                                        'Municipal Diesel (MMBTU)':'Municipal Diesel',
                                        'Municipal Vehicle Electricity (MMBTU)':'Municipal Electricity',
                                        'Total Public Transportation (MMBTU)':'Public Transit'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    
    threshold_v = rf_year_sub['Energy'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    rf_row_other = rf_year_sub.loc[rf_year_sub['Energy']<threshold_v].sum(numeric_only=True)
    rf_row_other = rf_row_other.rename('Energy')
    rf_row_other = rf_row_other.rename(index={rf_row_other.index[0]:'Other'}).reset_index()
    rf_year_sub_t = rf_year_sub.loc[rf_year_sub['Energy']>=threshold_v]
    rf_year_sub_s = pd.concat([rf_year_sub_t,rf_row_other])
    
    # Transportation emissions pie chart
    graph_cols = ['Residential Gasoline (MTCO2e)','Residential Diesel (MTCO2e)','Residential Vehicle Electricity (MTCO2e)',
                  'Commercial Gasoline (MTCO2e)','Commercial Diesel (MTCO2e)','Commercial Vehicle Electricity (MTCO2e)',
                  'Municipal Gasoline (MTCO2e)','Municipal Diesel (MTCO2e)','Municipal Vehicle Electricity (MTCO2e)',
                  'Total Public Transportation (MTCO2e)'
                  ]

    rf_year_sub = year_set5[graph_cols].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Gasoline (MTCO2e)':'Passenger Gasoline',
                                            'Residential Diesel (MTCO2e)':'Passenger Diesel',
                                      'Residential Vehicle Electricity (MTCO2e)':'Passenger Electricity',
                                        'Commercial Gasoline (MTCO2e)':'Commercial Gasoline',
                                        'Commercial Diesel (MTCO2e)':'Commercial Diesel',
                                        'Commercial Vehicle Electricity (MTCO2e)':'Commercial Electricity',
                                        'Municipal Gasoline (MTCO2e)':'Municipal Gasoline',
                                        'Municipal Diesel (MTCO2e)':'Municipal Diesel',
                                        'Municipal Vehicle Electricity (MTCO2e)':'Municipal Electricity',
                                        'Total Public Transportation (MTCO2e)':'Public Transit'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    
    threshold_v = rf_year_sub['Emissions'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    rf_row_other = rf_year_sub.loc[rf_year_sub['Emissions']<threshold_v].sum(numeric_only=True)
    rf_row_other = rf_row_other.rename('Emissions')
    rf_row_other = rf_row_other.rename(index={rf_row_other.index[0]:'Other'}).reset_index()
    rf_year_sub_t = rf_year_sub.loc[rf_year_sub['Emissions']>=threshold_v]
    rf_year_sub_f = pd.concat([rf_year_sub_t,rf_row_other])
    
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=('Share of fuel by sector',
                                        'Share of emissions by fuel and sector'),
                        horizontal_spacing = 0.1,
                        )
    # Energy pie chart
    fig.add_trace(
        go.Pie(labels=rf_year_sub_s['index'], values=rf_year_sub_s['Energy'].round(0),
               sort=False,rotation=180,
               textinfo='label+percent',textfont_size=14,showlegend=False,
               textfont=dict(color='black'),
               insidetextfont=dict(color=['white','white','black','black','black']),
               outsidetextfont=dict(color='black'),
               ),
        row=1,col=1)
    
    # Emissions pie chart
    fig.add_trace(
        go.Pie(labels=rf_year_sub_f['index'], values=rf_year_sub_f['Emissions'].round(0),
               sort=False,rotation=180,
               textinfo='label+percent',textfont_size=14,showlegend=False,
               textfont=dict(color='black'),
               insidetextfont=dict(color=['white','white','black','black','black']),
               outsidetextfont=dict(color='black'),
               ),
        row=1,col=2)
    
    fig.update_layout(title=dict(text='Share of emissions and sources in '+m+' in '+str(y5),font=dict(size=24)),
                      yaxis=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      xaxis=dict(title=dict(text='Year',font=dict(size=18)),
                                 tickvals=subset.Year,
                                 tickfont=dict(size=14)),
                      height=400,width=1000,
                      margin_t=125,
                      annotations=[dict(font=dict(color='black'))]
                      )
    fig.layout.annotations[0].update(y=1.1)
    fig.layout.annotations[1].update(y=1.1)

    st.plotly_chart(fig)