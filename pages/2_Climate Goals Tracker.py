# -*- coding: utf-8 -*-
"""
Created on Mon May  5 13:34:19 2025

@author: ACRANMER
"""

# Clean Energy Climate Goals Tracker page

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide',
                   page_title='Climate Goals Tracker'
                   )

# Load data either from the main app or from the data files
start_year = 2017

if 'df' not in st.session_state:
    from utils.load_data import load_data
    goals_df, geo, solar_df, stations, hp_df = load_data(start_year)
else:
    goals_df = st.session_state.df
    solar_df = st.session_state.df_solar
    hp_df = st.session_state.df_hp

    
hp_df.loc[hp_df['Municipality']=='Concord','Installed heat pumps (accounts)'] = 839 # from Concord MLP https://storymaps.arcgis.com/stories/a665b137c40b4174841c52bb474962ec

hp_df['Installed heat pumps (accounts)'] = hp_df['Installed heat pumps (accounts)'].astype('str').replace({'*': 0})

st.title('Climate Goals Tracker')

#st.header('Climate Goals Tracker')
    
st.markdown('<span style="font-size: 16px;">The table below provides key data for three measures at the \
            local level and suggested targets based on the state goals and local data.\
                </span>', unsafe_allow_html=True)

# Values from CECP page    
ma_2024_evs = 139969 # EVs and PHEVs
ma_2024_hps = 125678 # HPs
ma_2022_pvs = 4754000 # PVs
    
ma_numbers_cecp = [ma_2024_evs,
                  ma_2024_hps,
                  ma_2022_pvs,
                  ]
    
growth_numbers_ma = [int(round(ma_2024_evs*0.9,-2)),
                      int(round(ma_2024_hps*0.5,-2)),
                      int(round(ma_2022_pvs*0.1,0))
                      ]
    
# Choose municipality
locality = st.selectbox('Click in the box and type the name or scroll through the drop down list.',
                                 goals_df['Municipality'].unique().tolist(),
                                 index=0,
                                 key='locality')
    
if hp_df[hp_df['Municipality']==locality].empty:
    add_df = pd.DataFrame(data=np.array([[locality,0,0]]),columns=hp_df.columns)
    hp_df = pd.concat([hp_df,add_df])

locality_numbers = [goals_df.loc[(goals_df['Municipality']==locality)&(goals_df['Year']==2025),['Count EVs 01','Count PHEVs 01']].sum(axis=1).round(0).astype('int').item(),
                        pd.to_numeric(hp_df.loc[(hp_df['Municipality']==locality),'Installed heat pumps (accounts)'],errors='coerce').astype('int').item(),
                        solar_df.loc[(solar_df['City']==locality)&(solar_df['Year']==2024),'Capacity (kW DC) All Cumulative'].round(0).astype('int').item(),
                        ]

locality_nums = locality_numbers.copy()
if locality_numbers[1] == 0:
    locality_nums[1] = '<100 **'
    
growth_numbers = [int(round(locality_numbers[0]*0.9,0)),
                  int(round(locality_numbers[1]*0.5,0)),
                  int(round(locality_numbers[2]*0.1,0))
                  ]

locality_hh = goals_df.loc[(goals_df['Municipality']==locality)&(goals_df['Year']==2023),'Households'].item()
locality_vehicles = goals_df.loc[(goals_df['Municipality']==locality)&(goals_df['Year']==2025),'Count Total 01'].item()

pct_2030_evs = int(round(locality_vehicles * 0.17,0))
pct_2030_hps = int(round(locality_hh * 0.16,0))
pct_2030_pvs = int(round(locality_hh * 0.1 * 8,0))

growth_nums_pct = [int(round((pct_2030_evs-locality_numbers[0])*(1/6),0)),
                   int(round((pct_2030_hps-locality_numbers[1])*(1/6),0)),
                   int(round((pct_2030_pvs-locality_numbers[2])*(1/6),0))
                   ]

for i in range(0,3):
    if min(growth_numbers[0],growth_nums_pct[0]) <= 0:
        if growth_numbers[0] < growth_nums_pct[0]:
            growth_numbers[0] = 1
        elif growth_nums_pct[0] < growth_numbers[0]:
            growth_nums_pct[0] = 1
    if min(growth_numbers[1],growth_nums_pct[1]) <= 0:
        if growth_numbers[1] < growth_nums_pct[1]:
            growth_numbers[1] = 1
        elif growth_nums_pct[1] < growth_numbers[1]:
            growth_nums_pct[1] = 1
    if min(growth_numbers[2],growth_nums_pct[2]) <= 0:
        if growth_numbers[2] < growth_nums_pct[2]:
            growth_numbers[2] = 1
        elif growth_nums_pct[2] < growth_numbers[2]:
            growth_nums_pct[2] = 8

growth = [str(min(growth_numbers[0],growth_nums_pct[0])) + ' - ' + str(max(growth_numbers[0],growth_nums_pct[0])),
          str(min(growth_numbers[1],growth_nums_pct[1])) + ' - ' + str(max(growth_numbers[1],growth_nums_pct[1])),
          str(min(growth_numbers[2],growth_nums_pct[2])) + ' - ' + str(max(growth_numbers[2],growth_nums_pct[2]))
          ]

pct_2030_pvs_hh = int(round(growth_nums_pct[2]/8,0))

if locality == 'Massachusetts':
    locality_numbers = ma_numbers_cecp
    growth_numbers = growth_numbers_ma

total_new_evs = growth_numbers[0]*6
total_2030_evs = locality_numbers[0] + total_new_evs
total_2030_ev_pct = int(round((total_2030_evs/locality_vehicles) * 100,0))
total_new_hps = growth_numbers[1]*6
total_2030_hps = locality_numbers[1] + total_new_hps
total_new_pvs = growth_numbers[2]*6
total_2030_pvs = locality_numbers[2] + total_new_pvs

local_goal = [str(min(pct_2030_evs,total_2030_evs)) + ' - ' + str(max(pct_2030_evs,total_2030_evs)),
              str(min(pct_2030_hps,total_2030_hps)) + ' - ' + str(max(pct_2030_hps,total_2030_hps)),
              str(min(pct_2030_pvs,total_2030_pvs)) + ' - ' + str(max(pct_2030_pvs,total_2030_pvs))
              ]

# Create table of values to be displayed
df = pd.DataFrame(data = {'Measure':['Electric Vehicles (count)','Heat Pumps (count)','Solar (kW)'],
                              '2030 Goal ':['900,000','500,000','8,360'],
                              'MA*':ma_numbers_cecp,
                              'Year End':['2024','2024','2022'],
                              'MA yearly growth to meet goal':growth_numbers_ma,
                              #'%':['90%','50%','10%'],
                              '2030 Goal':local_goal,
                              locality:locality_nums,
                              'Most Recent Count Date':['2024','2023','2022'],
                              locality+' yearly growth to meet goal':growth
                              })
    
df['MA*'] = df['MA*'].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)
df['MA yearly growth to meet goal'] = df['MA yearly growth to meet goal'].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)
df[locality] = df[locality].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)
df[locality+' yearly growth to meet goal'] = df[locality+' yearly growth to meet goal'].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)
    
# Add text explanation of values in the table for locality
html_str_evs = f"""
    <style> p.a {{font: 16px; }}</style>
    <p class="a">In {locality} there are currently {locality_numbers[0]:,} EVs (including BEVs and PHEVs). \
        Based on the statewide need for 90% annual growth in EV adoption, that would mean \
        {growth_numbers[0]:,} new EVs per year through 2030 for a total of {total_2030_evs:,} \
        in 2030 (about {total_2030_ev_pct}% of all vehicles). \
        Alternatively, 17% of all vehicles in {locality} is {pct_2030_evs:,}, which would require {growth_nums_pct[0]:,}\
         new EVs per year through 2030. \
        </p>
    """
st.markdown(html_str_evs, unsafe_allow_html=True)

if locality_numbers[1] == 0:
    local_hp_num = 'an unknown number of'
else: local_hp_num = f'{locality_numbers[1]:,}'

html_str_hps = f"""
    <style> p.a {{font: 16px; }}</style>
    <p class="a">In {locality} there are currently {local_hp_num} heat pumps installed. \
        Based on 50% annual growth in heat pump adoption, that would mean \
        {growth_numbers[1]:,} new installations per year through 2030 for a total of {total_2030_hps:,} in 2030. \
        Alternatively, 16% of all households in {locality} is {pct_2030_hps:,}, which would require {growth_nums_pct[1]:,} \
         new heat pump installations per year through 2030. \
        </p>
    """
st.markdown(html_str_hps, unsafe_allow_html=True)

# solar exceedance statement
if pct_2030_pvs < locality_numbers[2]:
    solar_str = f'{locality} has already exceeded this value.'
else:
    solar_str = f'Meeting this goal is equivalent to {growth_nums_pct[2]:,} kW of new solar annually or {pct_2030_pvs_hh:,} households installing 8 kW solar systems each year through 2030.'

html_str_pvs = f"""
    <style> p.a {{font: 16px; }}</style>
    <p class="a">In {locality} there are currently {locality_numbers[2]:,} kW of solar installed. \
        Based on 10% annual growth in solar adoption, that would mean \
        {growth_numbers[2]:,} new kW installed per year through 2030 for a total of {total_2030_pvs:,} kW in 2030. \
        Alternatively, 10% of all households in {locality} adopting solar would be equivalent to about \
        {pct_2030_pvs:,} kW. {solar_str}\
        </p>
    """
st.markdown(html_str_pvs, unsafe_allow_html=True)
    
# Display table
def merge_table_headings(df):
    html = "<table style='border-collapse: collapse; width: 100%'>"
    html += f"<tr style='background-color: #f2f2f2; font-size: 18px;' align='center'><th rowspan='2' '>Measure</th><th colspan='4' '>Statewide, Massachusetts</th><th colspan='4' '>{locality}</th></tr>"
    html += "<tr style='background-color: #f2f2f2; font-size: 18px;'><th style='width:10%;'>2030 Goal</th><th style='width:10%;'>Most Recent Count*</th><th style='width:10%;'>Most Recent Count Date</th><th style='width:15%;'>Yearly Growth Needed to Meet 2030 Goal</th><th style='width:10%;'>2030 Goal</th><th style='width:10%;'>Most Recent Count</th><th style='width:10%;'>Most Recent Count Date</th><th style='width:15%;'>Yearly Growth Needed to Meet 2030 Goal</th></tr>"
    for idx, row in df.iterrows():
        html += "<tr>"
        for val, col_name in zip(row, df.columns):
            if col_name == 'Measure':
                html += f"<td style='border: 1px solid #dddddd; background-color: #f2f2f2; font-weight: bold; font-size: 18px;' align='center'>{val}</td>"
            else:
                html += f"<td style='border: 1px solid #dddddd; font-size: 18px;' align='center'>{val}</td>"
        html += "</tr>"            
    html += "</table>"
    return html
# Display the merged table headings with color using HTML
st.write(merge_table_headings(df), unsafe_allow_html=True)

#html = df.to_html(index=False)
#html = html.replace('<th>', '<th style="font-size:20px;">')
#html = html.replace('<td>', '<td style="font-size:20px;">')

#st.write(html,unsafe_allow_html=True)
    
st.markdown('<span style="font-size: 16px;">*Current adoption numbers are from the Massachusetts Clean Energy and Climate Metrics: \
                https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-metrics.\
                    </span>', unsafe_allow_html=True)
st.markdown('<span style="font-size: 16px;">**Heat pump adoption data is from the Mass Save program. Values below 100 are not \
            provided due to confidentiality concerns and therefore data may be incomplete particularly for including \
            smaller communities and MLP communities.\
            </span>', unsafe_allow_html=True)
st.markdown('<span style="font-size: 16px;">Community scale data for EVs includes BEVs and PHEVs from the MA Vehicle Census. \
                    </span>', unsafe_allow_html=True)
st.markdown('<span style="font-size: 16px;">Data for solar adoption comes from the MassCEC Production Tracking System (PTS). \
                </span>', unsafe_allow_html=True)


st.header('About')
    
st.markdown("<span style='font-size: 16px;'>Massachusett's GWSA **mandates** 33% GHG reduction by 2025 (compared to 1990), \
                50% by 2030, then net zero by 2050. From that, the Commonwealth set specific \
                **goals** for three key measures: **electric vehicles (EVs), heat pumps, and solar photovoltaics (PVs)**. \
                Assuming linear growth every year from 2024 to 2030 from current \
                adoption levels to the state targets, we calculate the needed growth for each technology \
                The 2030 statewide goals are: \
                </span>", unsafe_allow_html=True)
st.markdown("- **EVs**: 900,000 vehicles or about 17% of all 5.4 million vehicles in MA. As of the end of 2024, \
            there were 139,969 EVs in MA, meeting the goal will require adding 127,000 more EVs \
            each year or about 90% of the current EVs on the road added annually.")
st.markdown("- **Heat pumps**: 500,000 heat pumps or about 16% of all 2.8 million households in MA. As of the \
            end of 2024, there were 125,678 heat pumps across the state, so we need \
            to install about 62,000 more heat pumps each year or about 50% of the current amount.")
st.markdown("- **Solar PVs**: 8,360 MW or about 1 million average residential installations in MA. As of the end \
            of 2022, there were 4,754 MW of solar installed in MA, so we need to install \
            about 600 MW each year or about 10% of the current installed capacity.")
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
</style>
''', unsafe_allow_html=True)
    
st.markdown("<span style='font-size: 16px;'>In the table below, these growth percentages are applied to each community \
            as well as an alternative calculation of total percent aligned with the statewide percentages above. \
            Depending on the local context, a reasonable goal likely falls somewhere within this range. \
            Data provided on this page will be updated as new data becomes available. \
                </span>", unsafe_allow_html=True)    
    

    
