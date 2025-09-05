# -*- coding: utf-8 -*-
"""
Created on Mon May  5 13:34:19 2025

@author: ACRANMER
"""

# Clean Energy Climate Goals Tracker page

import streamlit as st
import pandas as pd
import numpy as np
import streamlit_analytics2 as streamlit_analytics

st.set_page_config(layout='wide',
                   page_title='Climate Goals Tracker'
                   )

st.markdown('''
<style>
.custom-bullets ul {
    padding-left:40px;
}
.custom-bullets li {
   font-size: 14px; 
   }
</style>
''', unsafe_allow_html=True)

st.markdown('''
<style>
.custom-bullets1 ul {
    padding-left:0px;
}
.custom-bullets1 li {
   font-size: 18px;
   }
</style>
''', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.image('images/bds_GEC_Logo_Horizontal_cmyk.jpg',
             use_container_width=True
             )
with col2:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.image('images/MassEnergize-logo.png',
             use_container_width=True
             )
with col3:
    st.image('images/MCAN Logo_Highest resolution.png',
             use_container_width=True
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

st.title(f'Climate Goals Tracker')
st.markdown("<span style='font-size: 18px;'>Climate Goals Tracker provides information to \
            set climate goals for municipalities and track progress.</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size: 18px;'>Massachusetts's Global Warming Solutions Act **mandates** 50% greenhouse gas \
            emissions reduction by 2030 (compared to 1990). From that, the Commonwealth derived statewide numerical \
                **goals** for the adoption of three key decarbonization measures in the residential sector: \
                **900,000 electric vehicles (EVs), 500,000 heat pumps, and 8,360 MW of solar photovoltaics (PVs)**. \
                    </span>", unsafe_allow_html=True)
st.markdown("<span style='font-size: 18px;'>Climate Goals Tracker translates these statewide goals to individual \
            municipalities. Click in the box below and enter the name of your municipality.\
                    </span>", unsafe_allow_html=True)
                    
st.text('')
streamlit_analytics.start_tracking()
# Choose municipality
locality = st.selectbox('**Click in the box and type the name or scroll through the drop down list.**',
                                 goals_df['Municipality'].unique().tolist(),
                                 index=0,
                                 key='locality')
streamlit_analytics.stop_tracking()

st.subheader(f'Consumer-Level Decarbonization Adoption in {locality}: progress needed')

# Preparing data for the table

# State values
# Values from CECP page    
ma_2024_evs = 139085 #139969 # EVs and PHEVs
ma_2024_hps = 125678 # HPs
ma_2022_pvs = 4754000 # PVs All
ma_2022_pvs_res = 1048691 # PVs Residential only
ma_2022_pvs_res_count = 133901 # current count of residential solar projects in MA 
ma_pv_avg = ma_2022_pvs_res/ma_2022_pvs_res_count
    
ma_numbers_cecp = [ma_2024_evs,
                  ma_2024_hps,
                  ma_2022_pvs_res,
                  ma_2022_pvs_res_count 
                  ]
    
growth_numbers_ma = [int(round(ma_2024_evs*0.9,-2)),
                      int(round(ma_2024_hps*0.5,-2)),
                      int(round(ma_2022_pvs_res*0.1,0)),
                      int(round(ma_2022_pvs_res*0.1/ma_pv_avg,0)) # growth in count of projects is based on 10% growth in kW capacity
                      ]
growth_numbers_ma = [127000,
                     62000,
                     107200,
                     '13,400'
                     ]

# Local data    
if hp_df[hp_df['Municipality']==locality].empty:
    add_df = pd.DataFrame(data=np.array([[locality,0,0]]),columns=hp_df.columns)
    hp_df = pd.concat([hp_df,add_df])

locality_numbers = [goals_df.loc[(goals_df['Municipality']==locality)&(goals_df['Year']==2025),'Count Res EVs 01'].round(0).astype('int').item(),
                        pd.to_numeric(hp_df.loc[(hp_df['Municipality']==locality),'Installed heat pumps (accounts)'],errors='coerce').astype('int').item(),
                        solar_df.loc[(solar_df['City']==locality)&(solar_df['Year']==2022),'Capacity (kW DC) Residential Cumulative'].round(0).astype('int').item(),
                        solar_df.loc[(solar_df['City']==locality)&(solar_df['Year']==2022),'Project Count Residential Cumulative'].round(0).astype('int').item(),
                        ]

locality_nums = locality_numbers.copy()
if locality_numbers[1] == 0:
    locality_nums[1] = '<100'
    
growth_numbers = [int(round(locality_numbers[0]*0.9,0)),
                  int(round(locality_numbers[1]*0.5,0)),
                  int(round(locality_numbers[2]*0.1,0)) # solar in kW
                  ]

locality_hh = goals_df.loc[(goals_df['Municipality']==locality)&(goals_df['Year']==2023),'Households'].item()
locality_vehicles = goals_df.loc[(goals_df['Municipality']==locality)&(goals_df['Year']==2025),'Count Res Total 01'].item()
locality_respv_avg = round(solar_df.loc[(solar_df['City']==locality)&(solar_df['Year']==2022),'Capacity (kW DC) Residential Cumulative'].item()/solar_df.loc[(solar_df['City']==locality)&(solar_df['Year']==2023),'Project Count Residential Cumulative'].item(),2)

growth = [f'{growth_numbers[0]:,}', # EV count
          f'{growth_numbers[1]:,}', # HP count
          f'{growth_numbers[2]:,}', # PV kw 
          f'{int(round(growth_numbers[2]/locality_respv_avg,0)):,}' # PV count
          ]

if locality == 'Massachusetts':
    locality_numbers = ma_numbers_cecp
    growth_numbers = growth_numbers_ma
    growth = growth_numbers

total_new_evs = growth_numbers[0]*6
total_2030_evs = locality_numbers[0] + total_new_evs
total_2030_ev_pct = int(round((total_2030_evs/locality_vehicles) * 100,0))

total_new_hps = growth_numbers[1]*6
total_2030_hps = locality_numbers[1] + total_new_hps
total_2030_hp_pct = int(round((total_2030_hps/locality_hh) * 100,0))

total_new_pvs = growth_numbers[2]*6
total_2030_pvs = locality_numbers[2] + total_new_pvs

if locality == 'Massachusetts':
    total_2030_evs = int(round(locality_numbers[0] + total_new_evs,-3))
    total_2030_hps = int(round(locality_numbers[1] + total_new_hps,-3))
    total_2030_pvs = int(round(locality_numbers[2] + total_new_pvs,-3))
    
    total_2030_evs = 900000
    total_2030_hps = 500000
    #total_2030_pvs = 2090000

local_goal = [f'{total_2030_evs:,}',
              f'{total_2030_hps:,}',
              f'{total_2030_pvs:,}',
              f'{int(round(total_2030_pvs/locality_respv_avg,0)):,}'
              ]

if locality_numbers[1] == 0:
    local_hp_num = 'somewhere between 1-99'
    hp_masssave_statement = '(Mass Save does not provide exact info if the quantity is below 100), so we are conservatively presuming 20.'
    growth_numbers[1] = 10
    growth[1] = 10
    total_2030_hps = 20+growth_numbers[1]*6
    total_2030_hp_pct = int(round((total_2030_hps/locality_hh) * 100,0))
    
else: 
    local_hp_num = f'{locality_numbers[1]:,}'
    hp_masssave_statement = ''

# Create table of values to be displayed
df = pd.DataFrame(data = {'Measure':['Electric Vehicles','Heat Pumps','Solar'],
                              #'2030 Goal ':['900,000','500,000','2,090,000',f'{int(round(2090000/8)):,}'],
                              'MA*':[ma_numbers_cecp[0],ma_numbers_cecp[1],ma_numbers_cecp[3]],
                              #'Year End':['2024','2024','2022','2022'],
                              'MA yearly growth to meet goal':[growth_numbers_ma[0],growth_numbers_ma[1],growth_numbers_ma[3]],
                              #'%':['90%','50%','10%'],
                              #'2030 Goal':local_goal,
                              locality:[locality_nums[0],locality_nums[1],locality_nums[3]],
                              'Most Recent Count Date':['2024','2023','2022'],
                              locality+' yearly growth to meet goal':[growth[0],growth[1],growth[3]]
                              })
    
df['MA*'] = df['MA*'].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)
df['MA yearly growth to meet goal'] = df['MA yearly growth to meet goal'].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)
df[locality] = df[locality].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)
df[locality+' yearly growth to meet goal'] = df[locality+' yearly growth to meet goal'].apply(lambda x: f'{x:,}' if isinstance(x, int) else x)

# Add text explanation of values in the table for locality
# html_str_evs = f"""
#     <style> p.a {{font-size: 18px; }}</style>
#     <p class="a">In {locality} at the end of 2024, there were {locality_numbers[0]:,} electric vehicles (EVs). \
#         Based on the statewide need for 90% annual growth in EV adoption, that would mean \
#         {growth_numbers[0]:,} new EVs this year and a total of {total_2030_evs:,} \
#         in 2030 (about {total_2030_ev_pct}% of all vehicles). \
#         </p>
#     """

# st.markdown(html_str_evs, unsafe_allow_html=True)

# html_str_hps = f"""
#     <style> p.a {{font-size: 18px; }}</style>
#     <p class="a">In {locality} at the end of 2023, there were {local_hp_num} heat pumps installed. \
#         {hp_masssave_statement}\
#         Based on 50% annual growth in heat pump adoption, that would mean \
#         {growth_numbers[1]:,} new installations this year and a total of {total_2030_hps:,} in 2030 \
#         (about {total_2030_hp_pct}% of all households). \
#         </p>
#     """

# st.markdown(html_str_hps, unsafe_allow_html=True)

# html_str_pvs = f"""
#     <style> p.a {{font-size: 18px; }}</style>
#     <p class="a">In {locality} there was {locality_numbers[2]:,} kW of solar installed at the end of 2022. \
#         Based on 10% annual growth in solar adoption, that would mean \
#         {growth_numbers[2]:,} new kW installed this year, which is about {growth[3]} households \
#          and a total of {total_2030_pvs:,} kW in 2030. \
#         </p>
#     """

# st.markdown(html_str_pvs, unsafe_allow_html=True)

st.markdown("""
            <div class="custom-bullets1">
            <ul>
                <li>""" + f"In {locality} at the end of 2024, there were {locality_numbers[0]:,} passenger electric vehicles (EVs). \
                    Based on the statewide goal of 900,000 in 2030, {growth_numbers[0]:,} new EVs need to be adopted this year and \
                        every year thereafter until 2030. This represents <strong>90%</strong> of the total number of EVs currently registered.\
                        " + """</li>
                <li>""" + f"In {locality} at the end of 2023, there were {local_hp_num} heat pumps installed. \
                    {hp_masssave_statement}\
                    Based on the state goal of 500,000 in 2030, {growth_numbers[1]:,} new installations are needed this year \
                    and every year thereafter until 2030. This represents <strong>50%</strong> of the total number of heat pump installations currently. \
                    " + """</li>
                <li>""" + f"In {locality} at the end of 2022, there was {locality_numbers[2]:,} kW of residential solar installed. \
                    Based on the state goal of 8,360 MW in 2030, {growth_numbers[2]:,} kW needs to be installed this year \
                    and thereafter until 2030. This translates to an additional {growth[3]} households adopting solar; \
                    or about <strong>10%</strong> of the total number of households that currently have solar installations.\
                    " + """</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
 
    
# Display table
def merge_table_headings(df):
    html = "<table style='border-collapse: collapse; width: 100%'>"
    #html += f"<tr style='background-color: #f2f2f2; font-size: 18px;' align='center'><th rowspan='2' '>Decarbonization Measure</th><th colspan='4' '>Statewide, Massachusetts</th><th colspan='4' '>{locality}</th></tr>"
    html += f"<tr style='background-color: #f2f2f2; font-size: 18px;' align='center'><th rowspan='3' '>Decarbonization Measure</th><th colspan='3' '>{locality}</th></tr>"
    #html += "<tr style='background-color: #f2f2f2; font-size: 18px;'><th style='width:10%;'>2030 Goal</th><th style='width:10%;'>Most Recent Count*</th><th style='width:10%;'>Most Recent Count Date</th><th style='width:15%;'>Yearly Growth Needed to Meet 2030 Goal</th><th style='width:10%;'>2030 Goal</th><th style='width:10%;'>Most Recent Count</th><th style='width:10%;'>Most Recent Count Date</th><th style='width:15%;'>Yearly Growth Needed to Meet 2030 Goal</th></tr>"
    html += "<tr style='background-color: #f2f2f2; font-size: 18px;' align='center'><th colspan='2' '>Most Recent Data</th><th rowspan='2' '>Additional Units needed this year to meet 2030 Goal</th></tr>"
    html += "<tr style='background-color: #f2f2f2; font-size: 18px;' align='center'><th rowspan='1'; style='width:25%;'>Units</th><th rowspan='1'; style='width:25%;'>as of (year-end):</th></tr>"
    for idx, row in df.iterrows():
        html += "<tr>"
        for val, col_name in zip(row, df.columns):
            if col_name == 'Measure':
                html += f"<td style='border: 1px solid #dddddd; background-color: #f2f2f2; font-weight: bold; font-size: 18px;' align='center'>{val}</td>"
            elif col_name == locality+' yearly growth to meet goal':
                html += f"<td style='border: 1px solid #dddddd; background-color: #ffff8f; font-weight: bold; font-size: 18px;' align='center'>{val}</td>"
            else:
                html += f"<td style='border: 1px solid #dddddd; font-size: 18px;' align='center'>{val}</td>"
        html += "</tr>"            
    html += "</table>"
    return html
# Display the merged table headings with color using HTML
if locality == 'Massachusetts':
    columns = ['Measure','MA*','Most Recent Count Date','MA yearly growth to meet goal']
    df = df[columns].rename(columns={'MA yearly growth to meet goal':'Massachusetts yearly growth to meet goal'})
else: 
    columns = ['Measure',locality,'Most Recent Count Date',locality+' yearly growth to meet goal']
    df = df[columns]
st.write(merge_table_headings(df), unsafe_allow_html=True)


#html = df.to_html(index=False)
#html = html.replace('<th>', '<th style="font-size:20px;">')
#html = html.replace('<td>', '<td style="font-size:20px;">')

#st.write(html,unsafe_allow_html=True)

st.write(' ')
st.write(' ')
st.write(' ')

# Definitions
st.markdown("<span style='font-size: 16px;'>**Definitions:** \
                </span>", unsafe_allow_html=True)
st.markdown("""
            <div class="custom-bullets">
            <ul>
                <li>Electric Vehicles (EVs): passenger vehicles registered as either battery electric (BEV) or plug-in hybrid-electric (PHEV),\
            which run on either electricity or gasoline; statewide, 99% of these are currently light duty.</li>
                <li>Heat Pumps: residential installations incentivized under Mass Save, total of: full- and \
            partial-HVAC conversions, plus hot water heat pumps plus new construction (excludes non-incentivized \
                installations, and most MLPs).</li>
                <li>Solar: residential photovoltaics installations.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)


# Data sources
st.markdown("<span style='font-size: 16px;'>**Data sources for community-level targets and progress:** \
                </span>", unsafe_allow_html=True)
st.markdown("""
            <div class="custom-bullets">
            <ul>
                <li>Electric Vehicles: Passenger BEVs and PHEVs from the MA Vehicle Census https://geodot-massdot.hub.arcgis.com/pages/vehicle-census.</li>
                <li>Heat Pumps: Mass Save program https://masssavedata.com/public/home. (Exception: values below 100 are not provided by Mass Save \
            due to confidentiality concerns, therefore data may be incomplete particularly for smaller communities. \
            Data is unavailable for most MLP communities.)</li>
                <li>Solar: Residential solar data comes from the MassCEC Production Tracking System (PTS). The tracker uses data from the \
            year 2022 for solar data because the PTS site notes that data from 2022-2024 may be incomplete, \
            visit https://www.masscec.com/production-tracking-system-pts for more information.</li>
            </ul>
            """, unsafe_allow_html=True)

st.markdown("<span style='font-size: 16px;'>**Data sources for state-level targets and progress:** \
                </span>", unsafe_allow_html=True)
st.markdown("""
            <div class="custom-bullets">
            <ul>
                <li>Massachusetts Clean Energy and Climate Metrics: \
                https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-metrics. </li>
            </ul>
                   """, unsafe_allow_html=True)
    
# Methodology
st.markdown("<span style='font-size: 16px;'>**Methodology for deriving annual state-level and municipal-level goals:** \
                </span>", unsafe_allow_html=True)

st.markdown("<span style='font-size: 14px;'>For simplicity, the Climate Goals Tracker tool assumes that the total number of heat pumps, \
            solar installations and electric vehicles increases in a straight line between now and 2030. \
                Currently, achieving the 2030 statewide goals means the following growth is required: \
                </span>", unsafe_allow_html=True)
                
st.markdown("""
            <div class="custom-bullets">
            <ul>
                <li><p><strong>EVs</strong>: In Massachusetts at the end of 2024, there were 139,969 EVs. \
                    In order to meet the state goal, Massachusetts needs 900,000 EVs by 2030 (that represents \
                    about 18% of the 4.9 million passenger vehicles registered in Massachusetts). \
                    Assuming straight-line growth, 127,000 EVs need to be added annually from now to 2030. \
                    127,000 is about <strong>90%</strong> of the 139,969 EVs currently registered in the state. \
                    We therefore assume that every community should also annually add a number of EVs equal to \
                    90% of the EVs it had at the end of 2024. </p>
                    <p>For example, a community with 100 EVs at the end of \
                    2024 would need to add an additional 90 EVs this year and every year thereafter \
                    for a total of 640 in 2030.</p></li>
                <li><p><strong>Heat pumps</strong>: The 2030 goal is 500,000 heat pump installations or about 16% \
                    of all 2.8 million households need to adopt heat pumps by 2030. At the end of 2024, \
                    there were 125,678 heat pumps across the state. Meeting the 2030 goal will require adding \
                    62,000 more heat pump installations this year and each year after that. 62,000 is \
                    <strong>50%</strong> of the 125,678 heat pumps that are currently installed in the state. \
                    We therefore assume that every community should also annually add the number of heat pump \
                    installations equal to 50% of heat pumps it had at the end of 2024. </p>
                    <p>For example, a community with 100 heat pumps installed by the end of 2023 would need to add 50 additional heat pumps \
                    this year and every year thereafter for a total of 400 in 2030.</p></li>
                <li><p><strong>Solar PVs</strong>: The 2030 goal is 8,360 megawatts (MW) of total solar generation \
                    in Massachusetts. Based on recent years of solar data, residential solar has made up about 25% \
                    of total solar installed in Massachusetts. That amounts to 2,090 MW of residential solar in 2030. \
                    At the end of 2022 (the latest year of complete data available), residential solar installed \
                    capacity was 1,049 MW. Meeting the 2030 goals will require adding 107 MW of solar in 2025 and \
                    each year after that. That translates to approximately 13,400 new projects each year, assuming \
                    that the average size of current residential projects of 8 kilowatts (kW). Putting it in perspective, \
                    each year Massachusetts residents need to adopt an additional 10% more solar than there are currently \
                    operating.</p>
                    <p>For example, a community with 100 kW of solar installed across 10 households would \
                    need to add about 10 kW of solar capacity, or the equivalent of one new household installation, \
                    this year and every year thereafter for a total of 160 kW across 16 households in 2030.</p></li>
            </ul>
            """, unsafe_allow_html=True)

st.markdown("<span style='font-size: 14px;'>This page will be updated as new data becomes available. \
                    </span>", unsafe_allow_html=True)

st.divider()

st.markdown("<span style='font-size: 14px;'>**Climate Goals Tracker tool** is a collaborative project of three leading \
            climate organizations in Massachusetts. A group of volunteers developed this work in the first half of \
                2025. Thanks particularly to the following colleagues: </span>", unsafe_allow_html=True)
ty = """
<table style='border-collapse: collapse; font-size: 14px; line-height: 1.2;'>
    <tr align='left' valign='top'>
        <td style='border: none; border-left: 1px solid #E6E6E6; vertical-align: top;'><strong>Zana Cranmer</strong></td>
        <td style='border: none; border-right: 1px solid #E6E6E6; vertical-align: top;'>Bentley University</td>
    </tr>
    <tr align='left' valign='top'>
        <td style='border: none; border-left: 1px solid #E6E6E6; vertical-align: top;'><strong>Larry Chretien<br>Anna Vanderspek</strong><br>Lillian Zhu</td>
        <td style='border: none; border-right: 1px solid #E6E6E6; vertical-align: top;'>Green Energy Consumers Alliance</td>
    </tr>
    <tr align='left' valign='top'>
        <td style='border: none; border-left: 1px solid #E6E6E6; vertical-align: top;'><strong>Ellen Tohn</strong><br>Steve Breit<br>Bradley Hubbard-Nelson<br>Megan Sullivan</td>
        <td style='border: none; border-right: 1px solid #E6E6E6; vertical-align: top;'>MassEnergize</td>
    </tr>
    <tr align='left' valign='top'>
        <td style='border: none; border-left: 1px solid #E6E6E6; vertical-align: top;'><strong>Fred Davis<br>Halina Brown</strong><br>Mamadou Balde<br>Janet Bowser<br>Mary Dewart<br>Khadija Hussaini<br>Phil Thayer</td>
        <td style='border: none; border-right: 1px solid #E6E6E6; vertical-align: top;'>Massachusetts Climate Action Network</td>
    </tr>
    <tr align='left' valign='top'>
        <td style='border: none; border-left: 1px solid #E6E6E6; vertical-align: top;'>Aimee Powelka</td>
        <td style='border: none; border-right: 1px solid #E6E6E6; vertical-align: top;'>Mass, EEA</td>
    </tr>
    <tr align='left' valign='top'>
        <td style='border: none; border-left: 1px solid #E6E6E6; vertical-align: top;'>Hilli Passas</td>
        <td style='border: none; border-right: 1px solid #E6E6E6; vertical-align: top;'>Medfield Environment Action</td>
    </tr>
    <tr align='left' valign='top'>
        <td style='border: none; border-left: 1px solid #E6E6E6; vertical-align: top;'>Zara Dowling<br>Lauren Mattison</td>
        <td style='border: none; border-right: 1px solid #E6E6E6; vertical-align: top;'>UMass Clean Energy Extension</td>
    </tr>
    <tr>
    </tr>
</table>
"""

st.write(ty, unsafe_allow_html=True)
