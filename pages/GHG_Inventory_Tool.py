# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 09:26:11 2025

@author: ACRANMER
"""

import streamlit as st
import pandas as pd
#import numpy as np
#import json
#import plotly.express as px
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#import streamlit_analytics2 as streamlit_analytics

from utils.analytics import get_ga_id, init_analytics, track_page, track_event

init_analytics()
track_page('Home')

def track_selectbox(widget_key: str, widget_name: str, page: str):
    value = st.session_state.get(widget_key)
    if value is None:
        return

    # Avoid duplicate sends (e.g., reruns that don't reflect a user change)
    last_key = f"__last_{widget_key}"
    if st.session_state.get(last_key) == value:
        return
    st.session_state[last_key] = value

    track_event(
        "select_change",
        page=page,
        widget_name=widget_name,
        value=str(value),
    )
    

def track_slider(widget_key: str, widget_name: str, page: str):
    value = st.session_state.get(widget_key)

    # dedupe: only send if changed since last time
    last_key = f"__last_{widget_key}"
    if st.session_state.get(last_key) == value:
        return
    st.session_state[last_key] = value

    track_event(
        "slider_change",
        page=page,
        widget_name=widget_name,
        value=float(value) if value is not None else None,
    )


start_year = 2017
end_year = 2024

st.set_page_config(layout='wide',
                   page_title='MA Community Energy and Emissions Dashboard'
                   )

st.title('Massachusetts Community Greenhouse Gas Inventory Tool')
st.write('This tool shows community-wide energy and emissions data from \
        buildings, transportation, and waste. Residential and commercial \
        activities are included in addition to municipal. This app is \
        under development and does not include all possible sources of \
        emissions. Please use the feedback page on the left if you have \
        questions or comments about anything in this dashboard. ')
        
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

#############################################################################
# Running the dashboard

if 'df' not in st.session_state:
    from utils.load_data import load_data
    dataset, geo, solar= load_data(start_year)
else:
    dataset = st.session_state.df
    geo = st.session_state.gdf
    solar = st.session_state.df_solar


municipalitiesList = dataset['Municipality'].unique().tolist()
municipalityIndex = 0
selectedMunicipality = st.query_params.get('municipality','')
if selectedMunicipality in municipalitiesList :
    municipalityIndex = municipalitiesList.index(selectedMunicipality)


#streamlit_analytics.start_tracking()
st.markdown('**Which city or town would you like to explore?**')
municipality = st.selectbox('**To make a selection, click in the box and type the name or scroll through the drop down list.**',
                             municipalitiesList,
                             index=municipalityIndex,
                             key='local',
                             on_change=track_selectbox,
                             kwargs={"widget_key": "local", "widget_name": "municipality", "page": "Home"}
                             )

st.markdown('Choose from the different tabs below to look at different \n \
             elements of the data.')
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['Overview','Demographics',
                                        'Buildings','Solar','Transportation','Waste',
                                        'Compare','Targets'])

st.markdown("""
<style>
    /* Select the paragraph tag inside the label div to increase font size */
    [data-testid="stMetricLabel"] p {
        overflow-wrap: break-word;
        white-space: break-spaces;
        font-size: 16px; /* Adjust percentage as needed */
    }

    /* Optional: You can also style the metric value */
    [data-testid="stMetricValue"] {
        font-size: 40px; /* Adjust size as needed */
    }
</style>
""", unsafe_allow_html=True)

############ OVERVIEW TAB ####################################################
with tab1:
    st.header('Overview of Energy and Emissions')
    st.markdown("Below are some key metrics on the community's adoption of key technologies to reduce energy consumption and emissions. \
                The percent of households with heat pumps is calculated from the number of accounts with a heat pump from the Mass Save \
                program (2024 data published in December 2025) divided by the number of households from the Census Bureau's American \
                Communities Survey (ACS) 5-year data (2024 data published in January 2026). The percent of electric vehicles is calculated \
                from the number of battery electric vehicles (BEVs) and plug-in hybrid electric vehicles (PHEVs) divided by the total \
                number of vehicles in the community. Vehicle data comes from the Massachusetts Vehicle Census (data published in January 2026).\
                The percent of households with solar is calculated from the number of residential projects in MassCEC's Production Tracking\
                System (data through Feb2025) divided by the number of households from the Census ACS data.\
                ")
    from utils.overview_graphs import m_graph1, my_graph1
    
    # metrics
    default_year = 2024
    base_year = 2020
    
    hh_w_hps = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==default_year),'HH with HPs'].item()
    top1_hp_adopters = dataset.loc[dataset['Year']==default_year,['Municipality','HH with HPs']].nlargest(4,columns='HH with HPs')
    top10_hp_adopters = dataset.loc[dataset['Year']==default_year,['Municipality','HH with HPs']].nlargest(35,columns='HH with HPs')
    
    hh_w_pvs = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==default_year),'HH with PVs'].item()
    top1_pv_adopters = dataset.loc[dataset['Year']==default_year,['Municipality','HH with PVs']].nlargest(4,columns='HH with PVs')
    top10_pv_adopters = dataset.loc[dataset['Year']==default_year,['Municipality','HH with PVs']].nlargest(35,columns='HH with PVs')
    
    pct_evs = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==default_year+1),'Percent Res EVs'].item()
    top1_ev_adopters = dataset.loc[dataset['Year']==default_year,['Municipality','Percent EVs']].nlargest(4,columns='Percent EVs')
    top10_ev_adopters = dataset.loc[dataset['Year']==default_year,['Municipality','Percent EVs']].nlargest(35,columns='Percent EVs')
    
    hh_energy = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==default_year),'Residential Energy per HH'].item()
    
    
    co2_year = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==default_year),'Total (MTCO2e)'].round(decimals=0).astype('int').item()
    co2_base = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==base_year),'Total (MTCO2e)'].round(decimals=0).astype('int').item()
    
    col1,col2,col3,col4 = st.columns([1,3,3,1])
    with col2:
        st.metric(label=f'{default_year} % Households with at least one heat pump for any end use.',
                  value=f'{hh_w_hps:,.2f}',
                  )
        if municipality in top1_hp_adopters['Municipality'].to_numpy():
            st.markdown(f'{municipality} is in the top 1% highest adoption rates for residential heat pumps in MA.')
        elif municipality in top10_hp_adopters['Municipality'].to_numpy():
            st.markdown(f'{municipality} is in the top 10% highest adoption rates for residential heat pumps in MA.')
        else:
            st.markdown(' ')
            st.markdown(' ')
            st.markdown(' ')
            st.markdown(' ')
        
        st.markdown(' ')
        
        st.metric(label=f'{default_year} % Households with solar panels installed.',
                  value=f'{hh_w_pvs:,.2f}',
                  )
        if municipality in top1_pv_adopters['Municipality'].to_numpy():
            st.markdown(f'{municipality} is in the top 1% highest adoption rates for residential solar in MA.')
        elif municipality in top10_pv_adopters['Municipality'].to_numpy():
            st.markdown(f'{municipality} is in the top 10% highest adoption rates for residential solar in MA.')
        else:
            st.markdown(' ')
            st.markdown(' ')
            st.markdown(' ')
            st.markdown(' ')
        
        st.markdown(' ')
        
        st.metric(label=f'{default_year} Total GHG emissions in MTCO2e.',
                    #label='Total 2022 GHGs in MTCO2e',
                  value=f'{co2_year:,.0f}',
                  #delta=round(100*(co2_year-co2_base)/co2_base,2),
                  #delta_color='normal'
                  )
    with col3:
        st.metric(label=f'{default_year} % Passenger vehicles that are electric vehicles (BEVs and PHEVs).',
                  value=f'{pct_evs:,.2f}',
                  )
        if municipality in top1_ev_adopters['Municipality'].to_numpy():
            st.markdown(f'{municipality} is in the top 1% highest adoption rates for residential solar in MA.')
        elif municipality in top10_ev_adopters['Municipality'].to_numpy():
            st.markdown(f'{municipality} is in the top 10% highest adoption rates for residential solar in MA.')
        else:
            st.markdown(' ')
            st.markdown(' ')
            st.markdown(' ')
            st.markdown(' ')
        
        st.markdown(' ')
            
        st.metric(label=f'{default_year} Average residential utility energy consumption in MMBTU.',
                  value=f'{hh_energy:,.2f}',
                  )
        st.markdown(' ')
        st.markdown(' ')
        st.markdown(' ')
        st.markdown(' ')
        
        st.markdown(' ')
        
        #st.markdown('% change from '+str(base_year)+'.')
        st.metric(label = f'% change in GHG emissions from {base_year}.',
                    #label='% change from 2020.',
                  value=round(100*(co2_year-co2_base)/co2_base,2))
    
    # annual emissions graph    
    subset1 = m_graph1(municipality,dataset,start_year,end_year)
    
    with st.expander('Data notes for GHG emissions',
                     expanded=True):
        st.markdown("""
                    - Where possible, the calculation of GHG emissions follows the methods in the MAPC Community \
                        Greenhouse Gas Inventory Tool. Off-road emissions are not included. \
                        Propane is included using the same methods as for fuel oil. \
                        Vehicle gasoline and diesel use is estimated based on the types of vehicles, vehicle miles traveled, \
                        and typical fuel efficiencies for each type of vehicle.
                    - Communities with more commercial and/or industrial activity will have higher total emissions \
                        per capita. Residential emissions per capita or per household are more comparable between communities.
                    """)
    
    st.markdown('**Which year would you like to look at?**')
    year1 = st.selectbox('**Choose a year from the drop down menu**',
                         range(end_year,2019,-1),
                         index=0,
                         key='year1',
                         on_change=track_selectbox,
                         kwargs={"widget_key": "year1", "widget_name": "overview_year", "page": "Home"}
                         )
    
    # emissions pie charts
    year_set1 = my_graph1(municipality,year1,dataset,colors_fuel)


############## DEMOGRAPHICS TAB #############################################
with tab2:
    st.header('Demographics')
    from utils.demographics import m_demog_graph
    st.markdown("Demographic data is from the U.S. Census Bureau's American Community Survey (ACS)\
                5-year data. The ACS does not report median household income data above \\$250,000. \
                Values of \\$250,000 should be interpreted as \\$250,000 or more.")
    
    col1, col2, col3 = st.columns([1,3,1])
    
    with col2:
        subset2 = m_demog_graph(municipality,dataset,start_year,end_year)


########## BUILDINGS TAB ####################################################
with tab3:
    st.header('Building Energy and Emissions')
    from utils.bldg_graphs import ms_hp_graph, bldg_graph0, bldg_graph1, bldg_graph2
    st.markdown("Below are some key metrics related to energy use in buildings.\
                The Mass Save particition rate is a cumulative measure of participation since 2013. \
                    More detail about Mass Save participation is provided in a graph below.\
                The number of heat pumps in the municipality is from the Mass Save program (2024 data published in December 2025). \
                    Data is not available for most MLP communities or communities with less than 100 accounts with heat pumps. \
                    (Mass Save's reporting threshold for privacy.)\
                The number of households is from the Census Bureau's ACS 5-year data for 2024 (published in January 2026).\
                The presence of a Community Electricity Aggregation (CEA) program is determined based on a list of approved programs \
                    from the MA DPU as of March 2026.")
    
    if municipality in ['Alford','Berkley','Blackstone','Bolton',
                           'Clarksburg','Dover','Leyden','Mendon',
                           'Millville','Montgomery','Monroe','Oxford',
                           'Rockport','Sterling','Sunderland','Whately']:
        st.markdown('Note: Some data may be missing from Mass Save Data due to a small number of customers.')
        
    # calc # of heat pumps or other metrics to show
    hps = pd.to_numeric(dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year),'Cumulative heat pumps all (accounts)'],errors='coerce')
    if hps.isna().item():
        hps = 'unknown'
    else: hps = hps.astype('int').item()
    households = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year),'Total Heating Fuel Households'].astype('int').item()
    ms_participation = (100*pd.to_numeric(dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year),'Cumulative location participation rate [%] (4)'],errors='coerce'))
    if ms_participation.isna().item():
        ms_participation = 'unknown'
    else: ms_participation = ms_participation.item()
    if dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year),'CEA Y/N'].item() == 'Yes':
        cea = 'Yes'
    else: cea = 'No'
    
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
            st.metric(label = 'Heat pumps*',
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
    
    st.markdown('*Note: In many communities, heat pump data is not available particularly those served by a Municipal Light Plant (MLP)\
                and communities that do not meet the 100 account reporting threshold for Mass Save.', unsafe_allow_html=True)
                
    st.markdown('Building emissions do not factor in renewable energy purchased through community aggregation programs. \
                This will be available in a future version.', unsafe_allow_html=True)
                
    st.markdown('This tab provides four different sets of graphs (as available). \
                The first shows annual building energy and emissions. \
                The second shows annual and cumulative participation in the Mass Save program. \
                The third shows monthly utility data from Mass Save. \
                The last set of graphs shows shares of fuel use.', unsafe_allow_html=True)
    
    subset3 = bldg_graph1(municipality,dataset,colors_fuel,start_year,end_year)
    with st.expander('Data notes for building energy and emissions:',
                     expanded=True):
        st.markdown("""
                    - Commercial includes industrial.
                    - Electricity and natural gas data come from the Mass Save program for participating communities. For MLP communities \
                        utility data is from MLP Annual Return reports published by the MA DPU.
                    - Fuel oil and propane use are estimated based on primary heating fuel and housing unit data from the Census Bureau's \
                        American Communities Survey (ACS) 5-year data in combination with average heating fuel use data from \
                            U.S. EIA's 2020 Resdiential Energy Consumption Survey (RECS).
                    - Utility-specific emissions factors are estimated based on Mass DEP's GHG Reporting Program data.
                    """)
    
    ms_hp_graph(municipality,dataset,start_year,end_year)
    with st.expander('Data notes for Mass Save participation and heat pumps:',
                     expanded=True):
        st.markdown(""" 
                    - Cumulative Mass Save participation counts each household or location only once even if they participated multiple times.
                    - Annual and cumulative heat pump adoption is provided for all types of heat pumps and for HVAC heat pumps.
                    - Households or accounts can have more than one type of heat pump, so the total number of accounts with heat pumps minus the number of HVAC heat pumps does not equal the number of hot water heat pumps.
                    - The Mass Save program does not publish data if the number of accounts is less than 100. * indicates suppressed data.
                    - Mass Save data for 2024 published in December of 2025.
                    """)
    
    bldg_graph0(municipality,dataset,start_year,end_year)
    with st.expander('Data notes for monthly utility data:',
                     expanded=True):
        st.markdown("""
                    -Monthly electric use can provide insights into use of air conditioning and adoption of electric heating. \
                        High summer peaks indicate use of air conditioning. High winter peaks indicate electric heating.\
                            If winter use of electricity is higher than summer use, your community may have high adoption of heat pumps.
                    """)
    
    st.text(' ')
    st.text(' ')
    st.markdown('**Which year would you like to look at?**')
    year3 = st.selectbox('**Choose a year from the drop down menu**',
                            range(end_year,start_year-1,-1),
                            index=0,
                            key='year3',
                            on_change=track_selectbox,
                            kwargs={"widget_key": "year3", "widget_name": "building_year", "page": "Home"}
                            )
    year_set3 = bldg_graph2(municipality,year3,dataset,colors_fuel)
    
    st.write('Notes: The Census uses a statistical model, not direct measurement, to estimate the number \
             of households using each type of heating fuel. Sometimes there will be a nonzero number \
            of households using natural gas for heat in communities that do not have any natural gas \
            infrastructure. The emissions calculations for natural gas rely on utility sales data and \
                so are not affected by this.\
                ')


############### SOLAR TAB ##################################################
with tab4:
    st.header('Solar Energy Adoption')
    from utils.solar_graphs import solar_graph
    st.text(' ')
    st.markdown('Note: Solar data is from the MassCEC PTS as of Feb 2024 and data for 2023 and 2024 are incomplete.')
    st.text(' ')
        
    # add widget w/ total capacity, n projects, avg project size?
    total_cap = solar.loc[(solar['City']==municipality)&(solar['Year']==end_year),'Capacity (kW DC) All Cumulative'].round(decimals=0).astype('int').item()
    total_num = solar.loc[(solar['City']==municipality)&(solar['Year']==end_year),'Project Count All Cumulative'].round(decimals=0).astype('int').item()
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


############# TRANSPORTATION TAB ############################################
with tab5:
    st.header('Transportation Energy and Emissions')
    from utils.transportation_graphs import trans_graph0, trans_graph
    st.markdown("Below are some key metrics related to transportation emissions. \
                 The number of battery electric vehicles (BEVs), plug-in hybrid electric vehicles (PHEVs), \
                    and gas hybrids are provided as of January 2026 (published by MassDOT January 2026). \
                The number of electric vehicle charging stations is from the Department of Energy's Alternative \
                    Fuels Data Center (AFDC) as of February 2026. \
                The share of commuters using public transit is from the Census Bureau's ACS 5-year data (2024 data \
                    published in January 2026).\
                ")
    
    evs_subset = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year+2),:] # taking Jan of the next year as year-end
    evs_subset['Percent BEVs'] = evs_subset['Count BEVs 01']/evs_subset['Count Total Vehicles 01']
    bevs = evs_subset.loc[:,'Count BEVs 01'].item()
    top1_ev_adopters = evs_subset.loc[:,['Municipality','Percent BEVs']].nlargest(4,columns='Percent BEVs')
    top10_ev_adopters = evs_subset.loc[:,['Municipality','Percent BEVs']].nlargest(35,columns='Percent BEVs')
    
    pct_bevs = 100*bevs/evs_subset.loc[:,'Count Total Vehicles 01'].item()
    phevs = evs_subset.loc[:,'Count PHEVs 01'].item()
    pct_phevs = 100*phevs/evs_subset.loc[:,'Count Total Vehicles 01'].item()
    ghyb = evs_subset.loc[:,'Count GHYs 01'].item()
    pct_ghyb = 100*ghyb/evs_subset.loc[:,'Count Total Vehicles 01'].item()
    pubtrans = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year),'pct public transit'].item()
    charge_stations = evs_subset.loc[:,'Total Level All Station Count'].item()
    
    col1,col2,col3,col4 = st.columns([1,3,3,1])
    with col2:
        st.metric(label='BEVs:',
                  value=f'{bevs:,.0f}')
        st.metric(label='PHEVs:',
                  value=f'{phevs:,.0f}')
        st.metric(label='Gas Hybrids:',
                  value=f'{ghyb:,.0f}')
        st.metric(label='Charging Stations:',
                  value=f'{charge_stations:,.0f}')
    with col3:
        st.metric(label='% BEVs:',
                  value=f'{pct_bevs:,.2f}')
        st.metric(label='% PHEVs:',
                  value=f'{pct_phevs:,.2f}')
        st.metric(label='% Gas Hybrids:',
                  value=f'{pct_ghyb:,.2f}')
        st.metric(label='% Public Transit Commuting:',
                  value=f'{pubtrans:,.0f}')
    
    st.text('')
    st.text('')
    set5 = trans_graph0(municipality,dataset,start_year,end_year,colors_vehicles,colors_fuel)
    
    st.text('')
    st.text('')
    st.markdown('**Which year would you like to look at?**')
    year5 = st.selectbox('**Choose a year from the drop down menu**',
                            range(end_year,2019,-1),
                            index=0,
                            key='year5',
                            on_change=track_selectbox,
                            kwargs={"widget_key": "year5", "widget_name": "transportation_year", "page": "Home"}
                            )
    
    year_set5 = trans_graph(municipality,year5,dataset)
    
    st.write('Data Sources: MA DOT Vehicle Census, MAPC MBTA data, FTA National Transit Database')


################ WASTE TAB ##################################################
with tab6:
    st.header('Waste Emissions')
    from utils.waste_graphs import waste_graph, waste_graph1
    
    st.markdown('What share (%) of trash in '+municipality+' is disposed in a landfill?')
    if dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year),'Incinerator'].item()=='Y':
        landfill = 0
        pct_msw = 0
        st.markdown(municipality+' sends all trash to an incinerator.')
    elif municipality == 'Massachusetts':
        landfill = 10
        pct_msw = 10
        st.markdown('Around 10% of trash is disposed in landfills, 90% is incinerated.')
    else:
        landfill = 100
        pct_msw = st.slider('Move the slider to adjust. 0 is all going to an incinerator, 100 is all going to a landfill.',
                             value=landfill,
                             min_value=0,max_value=100,key='landfill')
    
    if dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==end_year),'AD Community'].item()==1:
        mwra = 1
        st.markdown(municipality+' uses a waterwater treatment plant with anaerobic digestion and methane capture.')
    else: 
        mwra = 0
        if municipality != 'Massachusetts':
            st.markdown(municipality+' uses a municipal wastewater treatment plant and/or septic systems for wastewater.')
    
    st.markdown('What share (%) of '+municipality+' has septic systems?')
    septic = 46
    pct_septic = st.slider('Move the slider to adjust. 0 is all going to a municipal wastewater treatment plant, 100 is all septic.',
                             value=septic,
                             min_value=0,max_value=100,key='septic',
                             on_change=track_slider,
                             kwargs={"widget_key": "septic", "widget_name": "septic", "page": "Home"}
                             )
    
    # st.metric(label='Landfill slider',value=pct_msw)
    # l = (dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2022),'Landfill (MTCO2e)'].item())*(pct_msw/100)
    # st.metric(label='Landfill',
    #           value=l)
    # i = (dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2022),'Incineration (MTCO2e)'].item())*(100-pct_msw)/100
    # st.metric(label='Incinerator',
    #           value=i)
    # c = dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2022),'Compost (MTCO2e)'].item()
    # st.metric(label='Compost',
    #           value=c)
    # st.metric(label='MWRA Indicator',value=mwra)
    # ad = (dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2022),'MWRA AD (MTCO2e)'].item())*mwra
    # st.metric(label='WWT W/AD',
    #           value=ad)
    # st.metric(label='septic slider',value=pct_septic)
    # wwtp = (dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2022),'WWTP (MTCO2e)'].item())*(100-pct_septic)/100
    # st.metric(label='WWTP',
    #           value=wwtp)
    # s = (dataset.loc[(dataset['Municipality']==municipality)&(dataset['Year']==2022),'Septic (MTCO2e)'].item())*(septic/100)
    # st.metric(label='Septic',
    #           value=s)

    year_set6 = waste_graph(municipality,pct_msw,mwra,pct_septic,dataset,colors_waste)
    
    st.text('')
    st.text('')
    st.markdown('**Which year would you like to look at?**')
    year6 = st.selectbox('**Choose a year from the drop down menu**',
                            range(end_year,start_year-1,-1),
                            index=0,
                            key='year6',
                            on_change=track_selectbox,
                            kwargs={"widget_key": "year6", "widget_name": "waste_year", "page": "Home"}
                            )
    
    year_set6 = waste_graph1(municipality,year6,landfill,mwra,septic,dataset,colors_waste)
    
    
    st.write('Data Sources: MA DEP')


########## COMPARISON TAB ###################################################
with tab7:
    st.header('Comparison Tool')
    from utils.compare import compare_table, map_figure, scatter_explore
    st.text(' ')
    st.text(' ')
    
    st.markdown('**Choose communities to compare**')
    data0 = st.multiselect('Type a name or choose from the drop down menu',
                           municipalitiesList,
                           default=municipality,
                           key='data0',
                           )
    st.markdown('Scroll to the side to view more columns in the table. Additional table \
                controls available in the top right corner of the table including hiding \
                columns and downloading the data as a csv file.')
    table = compare_table(dataset,municipality,data0)
    
    column_config = {
    "Municipality": st.column_config.TextColumn(width="medium"),
    "Total GHG\n(2024)": st.column_config.NumberColumn(format="%,.0f"),
    "Population\n(2024)": st.column_config.NumberColumn(format="%d"),
    "Households\n(2024)": st.column_config.NumberColumn(format="%d"),
    "Median income\n(2024)": st.column_config.NumberColumn(format="$%d"),
    "% HPs\n(2024)": st.column_config.NumberColumn(format="%.2f"),
    "%Solar\n(2024)": st.column_config.NumberColumn(format="%.2f"),
    "% EVs\n(2025)": st.column_config.NumberColumn(format="%.2f"),
    }

    st.data_editor(table, use_container_width=True,hide_index=True,disabled=True,
                   column_config=column_config)
    
    st.markdown('**Which dataset would you like to map?**')
    data1 = st.selectbox('Choose from the drop down menu',
                         ['Total Emissions','Per Capita Emissions',
                          'Building Emissions','Transportation Emissions',
                          'Solar PV Capacity','Residential Solar PV Capacity',
                          'Percent EVs',
                          'Percent Households with Heat Pumps',
                          'Percent Households with Solar'],
                         index=1,
                         key='data1',
                         on_change=track_selectbox,
                         kwargs={"widget_key": "data1", "widget_name": "compare", "page": "Home"}
                         )
    st.markdown('**Which year would you like to look at?**')
    
    if data1 in ['Total Emissions','Per Capita Emissions','Transportation Emissions','Percent EVs','Percent Households with Heat Pumps']:
        start_year = 2020
    else: start_year = 2017
    year7 = st.selectbox('Choose from the drop down menu',
                         range(end_year,start_year-1,-1),
                         index=0,
                         key='year7',
                         on_change=track_selectbox,
                         kwargs={"widget_key": "year7", "widget_name": "compare_year", "page": "Home"}
                         )
    
    st.markdown('Hover over cities and towns on the map to see data values.')
    dataset_year = map_figure(dataset,solar,geo,year7,data1)
    
    st.markdown('Explore the dataset: choose variables to view on the graph.')
    data2 = st.selectbox('Choose a variable for the horizontal (x-) axis:',
                         ['Population', 'Households', 'Median household income',
                          'Households with <$50,000 income',
                          'Median age','Owner occupied housing', 'Renter occupied housing',
                          'Single family homes',
                          'Education','Limited English',
                          'Use of public transit', 'Working from home',
                          'Heating fuels: Natural gas', 'Heating fuels: Fuel oil',
                          'Heating fuels: Propane', 'Heating fuels: Wood',
                          'EJ block groups', 'Race: White', 'Race: Black or African American',
                          'Race: Asian','Race: Hispanic or Latinx'],
                         index=0,
                         key='data2',
                         on_change=track_selectbox,
                         kwargs={"widget_key": "data2", "widget_name": "compare_scatter", "page": "Home"}
                         )
    
    dataset_scatter = scatter_explore(dataset,data2,year7,data1,municipality,data0)
    

#streamlit_analytics.stop_tracking()

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
    




