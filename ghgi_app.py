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
#import streamlit_analytics2 as streamlit_analytics

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

#with streamlit_analytics.track():
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
    




