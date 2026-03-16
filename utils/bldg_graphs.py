# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:28:09 2025

@author: ACRANMER
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def has_any_values(df_wide, years, months):
    """True if any non-null numeric values exist for the selected years/months."""
    if df_wide is None or df_wide.empty:
        return False
    block = df_wide.loc[df_wide["Year"].isin(years), months]
    vals = pd.to_numeric(block.to_numpy().ravel(), errors="coerce")
    return np.isfinite(vals).any()


def add_missing_panel_message(fig, row, col, message):
    """Hide axes for a subplot panel and place a centered annotation message."""
    fig.update_xaxes(visible=False, row=row, col=col)
    fig.update_yaxes(visible=False, row=row, col=col)

    fig.add_annotation(
        text=message,
        xref='paper', yref='paper',
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="black"),
        align="left",
        row=row, col=col
    )

# function for buildings
@st.cache_data
def ms_hp_graph(m,dataset,start_year,end_year):
    cols = ['Year',
            'Average annual location participation rate [%]',
            'Cumulative location participation rate [%] (4)',
            'Heat pumps all (accounts)', 
            'Heat pumps hvac (accounts)', 
            'Cumulative heat pumps all (accounts)',
            'Cumulative heat pumps hvac (accounts)']
    
    subset = dataset.loc[(dataset['Municipality']==m)&(dataset['Year']<=end_year),cols].copy()
    
    
    fig = make_subplots(rows=1,cols=2,
                        subplot_titles=('Mass Save Program Participation',
                                        'Heat Pump Adoption'),
                        )
    
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Average annual location participation rate [%]'],
                   hoverinfo='x+y+name',mode='lines',
                   showlegend=True,legendgroup = '1',
                   name='Annual participation'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Cumulative location participation rate [%] (4)'],
                   hoverinfo='x+y+name',mode='lines',
                   showlegend=True,legendgroup = '1',
                   name='Cumulative participation'),
                   row=1,col=1)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Heat pumps all (accounts)'],
                   hoverinfo='x+y+name',mode='lines',
                   showlegend=True,legendgroup = '1',
                   name='Annual all'),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Heat pumps hvac (accounts)'],
                   hoverinfo='x+y+name',mode='lines',
                   showlegend=True,legendgroup = '1',
                   name='Annual HVAC'),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Cumulative heat pumps all (accounts)'],
                   hoverinfo='x+y+name',mode='lines',
                   showlegend=True,legendgroup = '1',
                   name='Cumulative all'),
                   row=1,col=2)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Cumulative heat pumps hvac (accounts)'],
                   hoverinfo='x+y+name',mode='lines',
                   showlegend=True,legendgroup = '1',
                   name='Cumulative HVAC'),
                   row=1,col=2)
    
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',
                      title=dict(text=f'Mass Save participation and heat pump adoption in {m}',
                                font=dict(size=24)),
                      yaxis=dict(title=dict(text='Locations',font=dict(size=14,color='black'),standoff=10),
                                 tickfont=dict(size=14,color='black')),
                      yaxis2=dict(title=dict(text='Accounts',font=dict(size=14,color='black'),standoff=0),
                                  tickfont=dict(size=14,color='black')),
                      height=400,width=1000,
                      annotations=[dict(font=dict(color='black'))]
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=14,color='black')),
                     tickfont=dict(size=14,color='black'))
        
    st.plotly_chart(fig)


def bldg_graph0(m,dataset,start_year,end_year):
    years = list(range(end_year-4,end_year+1))  # however you're defining years
    palette = px.colors.qualitative.Safe

    year_color = {
        y: palette[i % len(palette)]
        for i, y in enumerate(years)
        }

    elec_cols = ['Year','Jan Residential IOU Electricity (MWh)',
                 'Feb Residential IOU Electricity (MWh)',
                 'Mar Residential IOU Electricity (MWh)',
                 'Apr Residential IOU Electricity (MWh)',
                 'May Residential IOU Electricity (MWh)',
                 'Jun Residential IOU Electricity (MWh)',
                 'Jul Residential IOU Electricity (MWh)',
                 'Aug Residential IOU Electricity (MWh)',
                 'Sept Residential IOU Electricity (MWh)',
                 'Oct Residential IOU Electricity (MWh)',
                 'Nov Residential IOU Electricity (MWh)',
                 'Dec Residential IOU Electricity (MWh)',
                 ]
    rename_elec = {'Jan Residential IOU Electricity (MWh)':'Jan',
                 'Feb Residential IOU Electricity (MWh)':'Feb',
                 'Mar Residential IOU Electricity (MWh)':'Mar',
                 'Apr Residential IOU Electricity (MWh)':'Apr',
                 'May Residential IOU Electricity (MWh)':'May',
                 'Jun Residential IOU Electricity (MWh)':'Jun',
                 'Jul Residential IOU Electricity (MWh)':'Jul',
                 'Aug Residential IOU Electricity (MWh)':'Aug',
                 'Sept Residential IOU Electricity (MWh)':'Sept',
                 'Oct Residential IOU Electricity (MWh)':'Oct',
                 'Nov Residential IOU Electricity (MWh)':'Nov',
                 'Dec Residential IOU Electricity (MWh)':'Dec',}
    subset_elec = dataset.loc[(dataset['Municipality']==m),elec_cols].rename(columns=rename_elec).copy()
    
    #st.dataframe(subset_elec.loc[subset_elec['Year']==end_year,:])
    
    gas_cols = ['Year','Jan Residential IOU Gas (therms)',
                 'Feb Residential IOU Gas (therms)',
                 'Mar Residential IOU Gas (therms)',
                 'Apr Residential IOU Gas (therms)',
                 'May Residential IOU Gas (therms)',
                 'Jun Residential IOU Gas (therms)',
                 'Jul Residential IOU Gas (therms)',
                 'Aug Residential IOU Gas (therms)',
                 'Sept Residential IOU Gas (therms)',
                 'Oct Residential IOU Gas (therms)',
                 'Nov Residential IOU Gas (therms)',
                 'Dec Residential IOU Gas (therms)',
                 ]
    rename_gas = {'Jan Residential IOU Gas (therms)':'Jan',
                 'Feb Residential IOU Gas (therms)':'Feb',
                 'Mar Residential IOU Gas (therms)':'Mar',
                 'Apr Residential IOU Gas (therms)':'Apr',
                 'May Residential IOU Gas (therms)':'May',
                 'Jun Residential IOU Gas (therms)':'Jun',
                 'Jul Residential IOU Gas (therms)':'Jul',
                 'Aug Residential IOU Gas (therms)':'Aug',
                 'Sept Residential IOU Gas (therms)':'Sept',
                 'Oct Residential IOU Gas (therms)':'Oct',
                 'Nov Residential IOU Gas (therms)':'Nov',
                 'Dec Residential IOU Gas (therms)':'Dec',}
    subset_gas = dataset.loc[(dataset['Municipality']==m),gas_cols].rename(columns=rename_gas).copy()
    
    #st.dataframe(subset_gas.loc[subset_gas['Year']==end_year,:])
    
    months = subset_elec.columns[1:]
    
    elec_ok = has_any_values(subset_elec, years, months)
    gas_ok  = has_any_values(subset_gas, years, months)
    
    if not elec_ok and not gas_ok:
        st.warning(
            f"No monthly residential electricity or natural gas data available for {m}."
        )
        return
    fig = make_subplots(rows=1,cols=2,
                        subplot_titles=('Monthly Electricity Consumption',
                                        'Monthly Natural Gas Consumption'),
                        )

    if elec_ok:
        for y in years:
            row = subset_elec.loc[subset_elec["Year"] == y, months]
            if row.empty:
                continue

            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=pd.to_numeric(row.iloc[0], errors="coerce"),
                    mode="lines+markers",
                    name=str(y),
                    legendgroup=str(y),
                    line=dict(color=year_color[y])
                    ),
                row=1, col=1
                )
        elec_block = subset_elec.loc[subset_elec["Year"].isin(years),months]
        elec_vals = pd.to_numeric(
            elec_block.to_numpy().ravel(),
            errors="coerce"
            )
        elec_max = np.nanmax(elec_vals) if elec_vals.size else 0
        elec_ymax = elec_max * 1.3 if elec_max > 0 else 1
        fig.update_yaxes(range=[0, elec_ymax], row=1, col=1)
    
    else:
        add_missing_panel_message(
            fig, 1, 1,
            f"ℹ️ No monthly residential electricity data for {m}."
        )


    if gas_ok:
        for y in years:
            row = subset_gas.loc[subset_gas["Year"] == y, months]
            if row.empty:
                continue
            
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=pd.to_numeric(row.iloc[0], errors="coerce"),
                    mode="lines+markers",
                    name=str(y),
                    legendgroup=str(y),
                    showlegend=not elec_ok,
                    line=dict(color=year_color[y])
                    ),
                row=1, col=2
                )
        fig.update_yaxes(rangemode='tozero', row=1, col=2)
    else:
        add_missing_panel_message(
            fig, 1, 2,
            f"ℹ️ No monthly residential natural gas data for {m}."
        )

    fig.update_layout(hovermode='x',
                      title=dict(text=f'Monthly utility energy consumption in {m}',font=dict(size=24)),
                      yaxis=dict(title=dict(text='MWh',font=dict(size=14,color='black'),standoff=10),
                                 tickfont=dict(size=14,color='black')),
                      yaxis2=dict(title=dict(text='therms',font=dict(size=14,color='black'),standoff=0),
                                  tickfont=dict(size=14,color='black')),
                      height=400,width=1000,
                      annotations=[dict(font=dict(color='black'))]
                      )
    fig.update_xaxes(title=dict(text='Month',font=dict(size=14,color='black')),
                     tickfont=dict(size=14,color='black'))
    
    st.plotly_chart(fig)


def bldg_graph1(m,dataset,colors_fuel,start_year,end_year):
    subset = dataset[(dataset['Municipality']==m)&(dataset['Year']<end_year+1)].copy()
    
    # stacked area charts - energy and emissions
    fig = make_subplots(rows=2,cols=2,
                        subplot_titles=('Residential Energy by fuel in MMBTU',
                                        'Commercial Energy by fuel in MMBTU',
                                        'Residential Emissions by fuel in MTCO2e',
                                        'Commercial Emissions by fuel in MTCO2e'),
                        vertical_spacing = 0.2
                        )
    panels = {
        # (row, col): dict(stackgroup=..., fuels={display_name: column_name, ...}, showlegend=?)
        (1, 1): dict(
            stackgroup="one",
            showlegend=True,  # legend only here
            fuels={
                "Electricity": "Residential Electricity (MMBTU)",
                "Natural Gas": "Residential Gas (MMBTU)",
                "Propane": "Residential Propane (MMBTU)",
                "Fuel Oil": "Residential Fuel Oil (MMBTU)",
                # "Wood": "Residential Wood (MMBTU)",  # easy to re-enable
            },
        ),
        (1, 2): dict(
            stackgroup="two",
            showlegend=False,
            fuels={
                "Electricity": "Commercial & Industrial Electricity (MMBTU)",
                "Natural Gas": "Commercial & Industrial Gas (MMBTU)",
                "Fuel Oil": "Commercial Fuel Oil (MMBTU)",
            },
        ),
        (2, 1): dict(
            stackgroup="three",
            showlegend=False,
            fuels={
                "Electricity": "Residential Electricity (MTCO2e)",
                "Natural Gas": "Residential Gas (MTCO2e)",
                "Propane": "Residential Propane (MTCO2e)",
                "Fuel Oil": "Residential Fuel Oil (MTCO2e)",
                # "Wood": "Residential Wood (MTCO2e)",  # easy to re-enable
            },
        ),
        (2, 2): dict(
            stackgroup="four",
            showlegend=False,
            fuels={
                "Electricity": "Commercial & Industrial Electricity (MTCO2e)",
                "Natural Gas": "Commercial & Industrial Gas (MTCO2e)",
                "Fuel Oil": "Commercial Fuel Oil (MTCO2e)",
                # "Other": "Direct Emissions (MTCO2e)",  # easy to re-enable
            },
        ),
    }
    
    def add_stacked_panel(row, col, stackgroup, fuels, showlegend):
        for fuel_name, col_name in fuels.items():
            if col_name not in subset.columns:
                # If a column is missing, skip it (robust against schema changes)
                continue

            fig.add_trace(
                go.Scatter(
                    x=subset["Year"],
                    y=pd.to_numeric(subset[col_name], errors="coerce"),
                    hoverinfo="x+y+name",
                    mode="lines",
                    stackgroup=stackgroup,
                    name=fuel_name,
                    line=dict(color=colors_fuel.get(fuel_name, "#666")),  # fallback color
                    legendgroup="1",
                    showlegend=showlegend,
                ),
                row=row, col=col
            )

    # --- Add all panels via loop ---
    for (r, c), spec in panels.items():
        add_stacked_panel(
            row=r, col=c,
            stackgroup=spec["stackgroup"],
            fuels=spec["fuels"],
            showlegend=spec["showlegend"],
        )

    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x',
                      title=dict(text=f'Building energy and emissions in {m}',font=dict(size=24)),
                      yaxis=dict(title=dict(text='MMBTU',font=dict(size=14,color='black'),standoff=10),
                                 tickfont=dict(size=14,color='black')),
                      yaxis2=dict(title=dict(text='MMBTU',font=dict(size=14,color='black'),standoff=0),
                                  tickfont=dict(size=14,color='black')),
                      yaxis3=dict(title=dict(text='MTCO2e',font=dict(size=14,color='black'),standoff=10),
                                  tickfont=dict(size=14,color='black')),
                      yaxis4=dict(title=dict(text='MTCO2e',font=dict(size=14,color='black'),standoff=0),
                                  tickfont=dict(size=14,color='black')),
                      height=750,width=1000,
                      annotations=[dict(font=dict(color='black'))],
                      )
    fig.update_xaxes(title=dict(text='Year',font=dict(size=14,color='black')),
                     tickvals=list(range(start_year,end_year+1)),
                     tickfont=dict(size=14,color='black'))
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
                     'Fuel oil, kerosene, etc.','Bottled or tank gas',
                     'Wood','Solar energy','Coal or coke',
                     'Other fuel','No fuel used']
    
    hh_year_sub = year_set[hh_graph_cols].T*100
    hh_year_sub = hh_year_sub.rename(columns={hh_year_sub.columns[0]:'Fuels'},
                                     index={'Utility gas':'Natural Gas',
                                            'Fuel oil, kerosene, etc.':'Fuel Oil',
                                            'Bottled or tank gas':'Propane'}
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
               textinfo='label+percent',textfont_size=14,
               textfont=dict(color='black'),
               insidetextfont=dict(color=['white','white','black','black']),
               outsidetextfont=dict(color='black'),
               ),
        row=1,col=1)
    fig.add_trace(
        go.Pie(labels=cf_year_sub['index'], values=cf_year_sub['Emissions'].round(0),
               sort=False,marker_colors=cf_year_sub['index'].map(colors_fuel),
               rotation=-90,
               textinfo='label+percent',textfont_size=14,
               textfont=dict(color='black'),
               insidetextfont=dict(color=['white','white','black']),
               outsidetextfont=dict(color='black'),
               ),
        row=1,col=2)
    fig.add_trace(
        go.Pie(labels=hh_year_sub_f['index'], values=hh_year_sub_f['Fuels'].round(0),
               sort=False,marker_colors=hh_year_sub_f['index'].map(colors_fuel),
               rotation=45,
               textinfo='label+percent',textfont_size=14,
               textfont=dict(color='black'),
               insidetextfont=dict(color=['white','white','black','black','black']),
               outsidetextfont=dict(color='black'),
               ),
        row=2,col=1)
    #fig.add_trace(
    #    go.Pie(labels=cc_year_sub_f['index'], values=cc_year_sub_f['Employment'].round(0),
    #           textinfo='label+percent',textfont_size=14),
    #    row=2,col=2)
    
    fig.update_layout(title=dict(text='Share of emissions and sources in '+m+' in '+str(y3),
                                 font=dict(size=24),
                                 y = 1,
                                 yanchor='top',
                                 ),
                      height=750,width=1000,
                      showlegend=False,
                      annotations=[dict(font=dict(color='black'))]
                      )
    fig.layout.annotations[0].update(y=1.05)
    fig.layout.annotations[1].update(y=1.05)
    fig.layout.annotations[2].update(y=0.46)

    st.plotly_chart(fig)
    return year_set
    
    # add graph showing number of employers and jobs in different sectors