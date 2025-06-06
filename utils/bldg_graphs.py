# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:28:09 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# function for buildings
@st.cache_data
def bldg_graph1(m,dataset,colors_fuel,start_year,end_year):
    subset = dataset[(dataset['Municipality']==m)&(dataset['Year']<2024)]
    
    # stacked area charts - energy and emissions
    fig = make_subplots(rows=2,cols=2,
                        subplot_titles=('Residential Energy by fuel in MMBTU',
                                        'Commercial Energy by fuel in MMBTU',
                                        'Residential Emissions by fuel in MTCO2e',
                                        'Commercial Emissions by fuel in MTCO2e'),
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
        go.Scatter(x=subset['Year'],y=subset['Residential Electricity (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Electricity',line=dict(color=colors_fuel['Electricity']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    #fig.add_trace(
    #    go.Scatter(x=subset['Year'],y=subset['Residential Wood (MTCO2e)'],
    #               hoverinfo='x+y+name',mode='lines',stackgroup='three',
    #               name='Wood',line=dict(color=colors_fuel['Wood']),
    #               legendgroup = '1',showlegend=False),
    #               row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Gas (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Propane (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Propane',line=dict(color=colors_fuel['Propane']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Residential Fuel Oil (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='three',
                   name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=1)
    
    
    # Commercial and Industrial Emissions
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Commercial & Industrial Electricity (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='four',
                   name='Electricity',line=dict(color=colors_fuel['Electricity']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Commercial & Industrial Gas (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='four',
                   name='Natural Gas',line=dict(color=colors_fuel['Natural Gas']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=2)
    fig.add_trace(
        go.Scatter(x=subset['Year'],y=subset['Commercial Fuel Oil (MTCO2e)'],
                   hoverinfo='x+y+name',mode='lines',stackgroup='four',
                   name='Fuel Oil',line=dict(color=colors_fuel['Fuel Oil']),
                   legendgroup = '1',showlegend=False),
                   row=2,col=2)
    #fig.add_trace(
    #    go.Scatter(x=subset['Year'],y=subset['Direct Emissions (MTCO2e)'],
    #               hoverinfo='x+y+name',mode='lines',stackgroup='four',
    #               name='Other',line=dict(color=colors_fuel['Other']),
    #               legendgroup = '1'),
    #               row=2,col=2)

    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',
                      title=dict(text='Building energy and emissions in '+m,font=dict(size=28)),
                      yaxis=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=10),
                                 tickfont=dict(size=14)),
                      yaxis2=dict(title=dict(text='MMBTU',font=dict(size=18),standoff=0),
                                  tickfont=dict(size=14)),
                      yaxis3=dict(title=dict(text='MTCO2e',font=dict(size=18),standoff=10),
                                  tickfont=dict(size=14)),
                      yaxis4=dict(title=dict(text='MTCO2e',font=dict(size=18),standoff=0),
                                  tickfont=dict(size=14)),
                      height=750,width=1000
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=18)),
                     tickvals=list(range(start_year,end_year+1)),
                     tickfont=dict(size=14))
    
    st.plotly_chart(fig)
    return subset
    
def bldg_graph2(m,y3,dataset,colors_fuel):    
    year_set = dataset[(dataset['Year']==y3)&(dataset['Municipality']==m)]
    # Data prep
    # Residential emissions
    graph_cols1 = ['Residential Electricity (MTCO2e)','Residential Gas (MTCO2e)',
                   'Residential Propane (MTCO2e)','Residential Fuel Oil (MTCO2e)']
    
    rf_year_sub = year_set[graph_cols1].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Electricity (MTCO2e)':'Electricity',
                                            'Residential Gas (MTCO2e)':'Natural Gas',
                                            'Residential Fuel Oil (MTCO2e)':'Fuel Oil',
                                            'Residential Propane (MTCO2e)':'Propane'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    
    # Commercial emissions
    graph_cols2 = ['Commercial & Industrial Electricity (MTCO2e)','Commercial & Industrial Gas (MTCO2e)',
                      'Commercial Fuel Oil (MTCO2e)',#'Direct Emissions (MTCO2e)'
                      ]

    cf_year_sub = year_set[graph_cols2].T
    #print(cf_year_sub)
    cf_year_sub = cf_year_sub.rename(columns={cf_year_sub.columns[0]:'Emissions'},
                                     index={'Commercial & Industrial Electricity (MTCO2e)':'Electricity',
                                      'Commercial & Industrial Gas (MTCO2e)':'Natural Gas',
                                         'Commercial Fuel Oil (MTCO2e)':'Fuel Oil',
                                         #'Direct Emissions (MTCO2e)':'Other'
                                         }
                                     )
    cf_year_sub = cf_year_sub.reset_index()
    
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
    
    threshold = hh_year_sub['Fuels'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    #print('threshold: '+str(threshold))
    hh_row_other = hh_year_sub.loc[hh_year_sub['Fuels']<threshold].sum(numeric_only=True)
    hh_row_other = hh_row_other.rename('Fuels')
    hh_row_other = hh_row_other.rename(index={hh_row_other.index[0]:'Other'}).reset_index()
    
    hh_year_sub_t = hh_year_sub.loc[hh_year_sub['Fuels']>=threshold]
    hh_year_sub_f = pd.concat([hh_year_sub_t,hh_row_other])
    
    # Commercial sectors pie chart
    cc_graph_cols = year_set.loc[:,year_set.columns.str.startswith('Average Monthly Employment')].columns
    cc_year_sub = year_set[cc_graph_cols].T*100
    cc_year_sub = cc_year_sub.rename(columns={cc_year_sub.columns[0]:'Employment'})
    cc_year_sub = cc_year_sub.reset_index()
    cc_year_sub['index'] = cc_year_sub['index'].str.replace('Average Monthly Employment ','')
    
    
    threshold_c = cc_year_sub['Employment'].sum()*0.04 # aggregate any categories that are less than 4% of the total
    
    cc_row_other = cc_year_sub.loc[cc_year_sub['Employment']<threshold_c].sum(numeric_only=True)
    cc_row_other = cc_row_other.rename('Employment')
    cc_row_other = cc_row_other.rename(index={cc_row_other.index[0]:'Other'}).reset_index()
    
    cc_year_sub_t = cc_year_sub.loc[cc_year_sub['Employment']>=threshold_c]
    cc_year_sub_f = pd.concat([cc_year_sub_t,cc_row_other])
    
    # pie charts
    fig = make_subplots(rows=2,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}],
                                             [{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=('Share of residential emissions by fuel',
                                        'Share of commercial emissions by fuel',
                                        'Share of households by heating fuel',
                                        #'Share of commercial employment by sector'
                                        ),
                        horizontal_spacing = 0.03,
                        vertical_spacing = 0.2
                        )
    fig.add_trace(
        go.Pie(labels=rf_year_sub['index'], values=rf_year_sub['Emissions'].round(0),
               sort=False,rotation=120,
               textinfo='label+percent',textfont_size=14),
        row=1,col=1)
    fig.add_trace(
        go.Pie(labels=cf_year_sub['index'], values=cf_year_sub['Emissions'].round(0),
               sort=False,marker_colors=cf_year_sub['index'].map(colors_fuel),
               rotation=-90,
               textinfo='label+percent',textfont_size=14),
        row=1,col=2)
    fig.add_trace(
        go.Pie(labels=hh_year_sub_f['index'], values=hh_year_sub_f['Fuels'].round(0),
               sort=False,marker_colors=hh_year_sub_f['index'].map(colors_fuel),
               rotation=45,
               textinfo='label+percent',textfont_size=14),
        row=2,col=1)
    #fig.add_trace(
    #    go.Pie(labels=cc_year_sub_f['index'], values=cc_year_sub_f['Employment'].round(0),
    #           textinfo='label+percent',textfont_size=14),
    #    row=2,col=2)
    
    fig.update_layout(title=dict(text='Share of emissions and sources in '+m+' in '+str(y3),
                                 font=dict(size=28),
                                 y = 1,
                                 yanchor='top',
                                 ),
                      height=750,width=1000,
                      showlegend=False
                      )
    fig.layout.annotations[0].update(y=1.05)
    fig.layout.annotations[1].update(y=1.05)
    fig.layout.annotations[2].update(y=0.46)

    st.plotly_chart(fig)
    return year_set
    
    # add graph showing number of employers and jobs in different sectors