# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:48:50 2026

@author: ACRANMER
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import copy


# function for statewide maps for a single year
@st.cache_data
def compare_table(dataset,main_muni,peer_munis):
    data_cols = ['Municipality','Year',
                 'Total (MTCO2e)','HH with HPs','HH with PVs','Percent EVs',
                 'Population','Median household income',
                 ]
    data_year = {'Total (MTCO2e)':2024,
                 'HH with HPs':2024,
                 'HH with PVs':2024,
                 'Percent EVs':2025,
                 'Population':2024,
                 'Median household income':2024,
                 }
    display_labels = {"Total (MTCO2e)":"Total GHGs",
                      'Median household income':'Income',
                      'HH with HPs':'% HPs',
                      'HH with PVs':'% Solar',
                      'Percent EVs':'% EVs',
                      }
    
    # Selected list with main first, de-duplicated while preserving order
    selected = [main_muni] + [m for m in peer_munis if m != main_muni]
    seen = set()
    selected = [m for m in selected if not (m in seen or seen.add(m))]

    metrics = list(data_year.keys())
    df = dataset.loc[dataset["Municipality"].isin(selected),["Municipality", "Year"] + metrics].copy()
    
    table = pd.DataFrame({"Municipality": selected})

    for metric in metrics:
        yr = int(data_year[metric])

        col_label = f"{display_labels.get(metric, metric)}\n({yr})"

        s = (
            df.loc[df["Year"] == yr, ["Municipality", metric]]
              .set_index("Municipality")[metric]
        )

        table[col_label] = table["Municipality"].map(s)

    # Ensure a simple index so hide_index behaves
    table = table.reset_index(drop=True)

    # Missing data handling: keep NaN (Streamlit shows blanks) or fill with "—"
    table = table.fillna("—")
    
    return table.reset_index()


def map_figure(dataset,solar_data,geodata,y,d):
    st.session_state.key = d
    
    dataset_year = dataset[dataset['Year']==y].copy()
    dataset_year['TOWN'] = dataset_year["Municipality"].astype(str).str.strip().str.title()
    
    solar_year = solar_data.loc[solar_data['Year']==y,:].copy()
    solar_year['City'] = solar_year['City'].astype(str).str.strip().str.title()
    
    map_specs = {
        "Total Emissions": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "Total (MTCO2e)",
            "label": "Total emissions (MTCO2e)",
            "raw_fmt": ":,.0f",
        },
        "Per Capita Emissions": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "Per Capita (MTCO2e)",
            "label": "Per-capita emissions (MTCO2e)",
            "raw_fmt": ":.2f",
        },
        "Building Emissions": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "Total Buildings (MTCO2e)",
            "label": "Building emissions (MTCO2e)",
            "raw_fmt": ":,.0f",
        },
        "Transportation Emissions": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "Total Transportation (MTCO2e)",
            "label": "Transportation emissions (MTCO2e)",
            "raw_fmt": ":,.0f",
        },
        "Solar PV Capacity": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "Capacity (kW DC) All Cumulative",
            "label": "Solar PV capacity (kW DC, cumulative)",
            "raw_fmt": ":,.0f",
        },
        "Residential Solar PV Capacity": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "Capacity (kW DC) Residential Cumulative",
            "label": "Solar PV capacity (kW DC, cumulative)",
            "raw_fmt": ":,.0f",
        },
        "Percent EVs": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "Percent EVs",
            "label": "Percent EVs",
            "raw_fmt": ":.1f",
        },
        "Percent Households with Heat Pumps": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "HH with HPs",
            "label": 'Percent HPs',
            "raw_fmt": ":.1f",
            },
        "Percent Households with Solar": {
            "df": dataset_year,
            "loc_col": "Municipality",
            "val_col": "HH with PVs",
            "label": 'Percent Solar',
            "raw_fmt": ":.1f",
            },
        }
    
    spec = map_specs[d]
    df = spec['df'].copy()
    df[spec["val_col"]] = pd.to_numeric(df[spec["val_col"]], errors="coerce")
    df["Percentile"] = df[spec["val_col"]].rank(pct=True, method="average") * 100
    st.write(f"{spec['label']} — Percentile map ({y})")
    
    fig = px.choropleth(
        df,
        geojson=geodata,
        locations="Municipality",
        featureidkey="properties.TOWN",
        color="Percentile",
        range_color=(0, 100),
        color_continuous_scale="Viridis",
        hover_name=spec["loc_col"],
        hover_data={
            spec["val_col"]: spec["raw_fmt"],
            "Percentile": ":.1f",
            "Municipality": False,
        },
        labels={
            "Percentile": "Percentile (0–100)",
            spec["val_col"]: spec["label"],
        },
    )
    
    fig.update_geos(fitbounds='geojson',visible=False)
    fig.update_layout(height=520,width=1000,
                      margin={"r":0,"t":0,"l":0,"b":0},
                      coloraxis_colorbar=dict(title='Percentile'),
                      )
    
    st.plotly_chart(fig)
        
    return dataset_year

def scatter_explore(dataset,x_val,y,d,m,p):
    x_val_dict = {'Population':'Population', 
                  'Households':'Households', 
                  'Median household income':'Median household income',
                  'Households with <$50,000 income':'pct households <$50k',
                  'Median age':'Median age (years)',
                  'Owner occupied housing':'pct owner occupied', 
                  'Renter occupied housing':'pct renter occupied',
                  'Single family homes':'pct single family',
                  'Education':'pct BS+',
                  'Limited English':'pct Limited English',
                  'Use of public transit':'pct public transit', 
                  'Working from home':'pct work from home',
                  'Heating fuels: Natural gas':'pct ng', 
                  'Heating fuels: Fuel oil':'pct fuel oil',
                  'Heating fuels: Propane':'pct propane', 
                  'Heating fuels: Wood':'pct wood',
                  'EJ block groups':'Percent of EJ block groups', 
                  'Race: White':'pct white', 
                  'Race: Black or African American':'pct black',
                  'Race: Asian':'pct asian',
                  'Race: Hispanic or Latinx':'pct latinx',
                  }
    y_val_dict = {'Total Emissions':'Total (MTCO2e)',
                  'Per Capita Emissions':'Per Capita (MTCO2e)',
                  'Building Emissions':'Total Buildings (MTCO2e)',
                  'Transportation Emissions':'Total Transportation (MTCO2e)',
                  'Solar PV Capacity':'Capacity (kW DC) All Cumulative',
                  'Residential Solar PV Capacity':'Capacity (kW DC) Residential Cumulative',
                  'Percent EVs':'Percent EVs',
                  'Percent Households with Heat Pumps':'HH with HPs',
                  'Percent Households with Solar':'HH with PVs',
                  }
    
    dataset_scatter = dataset.loc[dataset['Year']==y,['Municipality',x_val_dict[x_val],y_val_dict[d]]].copy()
    
    highlight = [m] + p
    mask = dataset_scatter['Municipality'].isin(highlight)
    
    base_df = dataset_scatter.loc[~mask]
    hi_df = dataset_scatter.loc[mask]
    
    PERCENT_COLS = {"pct households <$50k",
                    "pct owner occupied",
                    "pct renter occupied",
                    "pct single family",
                    "pct BS+",
                    "pct Limited English",
                    "pct public transit",
                    "pct work from home",
                    "pct ng",
                    "pct fuel oil",
                    "pct propane",
                    "pct wood",
                    "Percent of EJ block groups",
                    "pct white",
                    "pct black",
                    "pct asian",
                    "pct latinx",
                    }
    
    def make_hovertemplate(x_label, y_label, x_col, y_col, percent_cols, percent_scale="0-100"):
        x_is_pct = x_col in percent_cols
        y_is_pct = y_col in percent_cols
        
        if percent_scale == "0-1":
            x_token = f"%{{x:.1%}}" if x_is_pct else f"%{{x:,.0f}}"
            y_token = f"%{{y:.1%}}" if y_is_pct else f"%{{y:,.0f}}"
        else:
            # 0-100 stored percent: show number then a % sign
            x_token = f"%{{x:,.1f}}%" if x_is_pct else f"%{{x:,.0f}}"
            y_token = f"%{{y:,.1f}}%" if y_is_pct else f"%{{y:,.0f}}"
            
        return (
            "<b>%{text}</b><br>"
            f"{x_label}: {x_token}<br>"
            f"{y_label}: {y_token}"
            "<extra></extra>"
            )
    
    hover_tmpl = make_hovertemplate(x_label=x_val,
                                    y_label=d,
                                    x_col=x_val_dict[x_val],
                                    y_col=y_val_dict[d],
                                    percent_cols=PERCENT_COLS,
                                    percent_scale="0-100"  # change to "0-1" if your percent columns are 0–1
                                    )

    
    fig = make_subplots(rows=1,cols=1,specs=[[{'type':'scatter'}]])
    
    # Line graph of vehicle counts over time
    fig.add_trace(
        go.Scatter(x=base_df[x_val_dict[x_val]],y=base_df[y_val_dict[d]],
                   #hoverinfo='x+y+name',
                   mode='markers',
                   showlegend=False,
                   #name=d,
                   text=base_df['Municipality'],
                   hovertemplate=hover_tmpl,
                   ),
    row=1,col=1)
    fig.add_trace(
        go.Scatter(x=hi_df[x_val_dict[x_val]],y=hi_df[y_val_dict[d]],
                   #hoverinfo='x+y+name',
                   mode='markers',
                   showlegend=False,
                   #name=d,
                   #marker=dict(size=12, color='red', opacity=0.95)
                   text=hi_df['Municipality'],
                   hovertemplate=hover_tmpl,
                   ),
    row=1,col=1)
    
    fig.update_layout(hovermode='closest',
                      title=dict(text=f'Comparing {d} and {x_val}',font=dict(size=24)),
                      yaxis=dict(title=dict(text=d,font=dict(size=18,color='black'),standoff=10),
                                 tickfont=dict(size=14,color='black')),
                      xaxis=dict(title=dict(text=x_val,font=dict(size=18,color='black')),
                                 tickfont=dict(size=14,color='black')),
                      height=400,width=500,
                      #annotations=[dict(font=dict(color='black'),showarrow=False)]
                      )
    
    st.plotly_chart(fig)
    
    return dataset_scatter