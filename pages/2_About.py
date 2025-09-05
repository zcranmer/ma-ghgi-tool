# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:19:14 2023

@author: ACRANMER
"""

import streamlit as st
import pandas as pd

st.title('About this tool...')
st.header('The short version')
st.write('This tool takes data from U.S. Federal government agencies and MA state agencies related to \
         energy and calculates energy consumption in different sectors and the associated \
        emissions. The sectors include: Residential, Commercial (including Municipal), \
        and Industrial. The fuels and energy sources estimated include: electricity, \
        natural gas, fuel oil, propane, wood, gasoline, and diesel. The methods used are \
            very similar to those in the MAPC GHGI Spreadsheet tool.')

#st.header('The Team')
#st.write('The development of this site is led by Dr. Zana Cranmer (acranmer@bentley.edu) of Bentley University in collaboration \
#         with the UMass Clean Energy Extension, Massachusetts Climate Action Network, Green Energy Consumers \
#        Alliance, and MassEnergize.')
#st.write('Bentley University: https://www.bentley.edu/')
#st.write('Green Energy Consumers Alliance, https://www.greenenergyconsumers.org/')
#st.write('Massachusetts Climate Action Network https://www.massclimateaction.org/')
#st.write('MassEnergize https://www.massenergize.org/')
#st.write('UMass Clean Energy Extension https://www.umass.edu/agriculture-food-environment/clean-energy')
            
st.header('About this database')
st.write('This database has been compiled in order to aggregate relevant data sources for energy \
         and greenhouse gases from across national and state agencies. This creates a single point \
        of reference for data needed to conduct community-wide greenhouse gas emissions analyses \
        and associated analysis such as energy use and production at the municipal level. Where \
        available, data are collected for the years 2017 through 2023. The database will be updated \
        as additional years of data become available. You can add your name to the mailing list for \
        updates through the form on the feedback page.\
            \
        Data is collected and cleaned from the original sources as described below and output into \
        a single file, municipal_data.xlsx. Due to differences in each dataset and analyses of interest, \
        different categories of data have been output to different sheets within the file. The \
        relevant datasets for any particular project can be pulled and condensed or combined as \
        appropriate to a project.')
        
st.header('Geographic Boundaries')
st.write('Geospatial data on the boundaries of municipalities are downloaded from the \
         Massachusetts Bureau of Geographic Information \
        (https://www.mass.gov/orgs/massgis-bureau-of-geographic-information).')
        
st.header('Demographic Data')
st.write('Demographic data including population, number of households, income and other \
         variables are collected from the U.S. Census Bureau’s American Communities Survey \
        (https://data.census.gov/). The 5-year data is used here and a table of data tables \
        and variables is given below.')
        
# add table here
census_tables = pd.DataFrame(data = {'Population':['B03002'],
                                     'Households':['B25002'],
                                     'Median Household Income':['B19013'],
                                     'Housing Units':['B25024'],
                                     'Heating Fuels':['B25040'],
                                     'Transportation to Work':['B08006'],
                                     'Travel Time to Work':['B08012']
                                     }, index=['Table'])
st.write(census_tables, unsafe_allow_html=True)

st.header('Utility Data')
st.write('Electric and natural gas utility data are collected from the Mass Save program \
         website (https://masssavedata.com/public/home) and from municipal light plant (MLP) \
        annual reports published by the Massachusetts Department of Public Utilities \
        (https://www.mass.gov/info-details/find-an-mlp-annual-return). \
        \
        Electric and gas data are published by municipality for the residential sectors and \
        the commercial and industrial sector for each year. Data collected from MLPs typically \
        disaggregate commercial and industrial use, but for consistency with the Mass Save data \
        they are combined. Where multiple municipalities are served by the same MLP, the usage \
        is distributed among the communities based on the number of meters in each municipality. \
        This may over- or under-estimate actual usage depending on the demographic differences \
        between communities and their relative shares of residential, commercial and industrial \
        activity. Future versions will develop improved methods to assign usage between communities.\
        \
        Data from EIA is used to estimate transmission and distribution losses for the state of \
        Massachusetts each year.\
        \
        Standard emission factor for natural gas is taken from the U.S. EIA list of carbon dioxide \
        emission factors. Emission factors for electricity are taken from the Mass DEP annual \
        reports on retail sellers of electricity.')

st.header('Buildings')
st.subheader('Residential')
st.write('In addition to the utility data described above, EIA’s RECS data is used to estimate \
         fuel oil, propane, and wood use for residential buildings. The 2020 RECS survey includes \
        data by state and thus the Massachusetts specific data is used to calculate fuel use by \
        home type, shown in the table below.')

# add table here
recs_data = pd.DataFrame(data = {'Housing Type': ['1, detached','1, attached','2-4 units','5+ units','mobile home'],
                                 'Average Oil Use (gallons/year)': [786,551,464,303,418],
                                 'Average Propane Use (gallons/year)': [503,362,153,144,332],
                                 #'Wood': []
                                 }
                         )
recs_data = recs_data.set_index('Housing Type')
st.write(recs_data, unsafe_allow_html=True)

st.write('As in the MAPC Inventory Tool, fuel oil and propane consumption are estimated from the number \
            of households using each heating fuel \
         as estimated by the U.S. Census Bureau (Table B25046) multiplied by the site energy consumption by fuel \
         from RECS. Emissions factors for fuel oil and \
            propane are taken from the U.S. EIA list of carbon dioxide emission factors.')
    
st.write('Emission factors for electricity are taken from the Mass DEP annual reports on retail sellers \
            of electricity. \
        As in the MAPC Inventory Tool, fuel oil and propane consumption are estimated from the number \
            of households using each heating fuel \
         as estimated by the U.S. Census Bureau (Table B25046). The site energy consumption by fuel \
         from the U.S. EIA Residential Energy Consumption Survey (RECS) is used to estimate the \
        heating fuel consumption by multiplying the number of households using fuel oil by the \
        site fuel oil consumption for the state of Massachusetts. Emissions factors for fuel oil and \
            propane are taken from the U.S. EIA list of carbon dioxide emission factors.')

st.subheader('Commercial & Industrial')
st.write('As for the residential buildings, the Mass Save and MLP Annual Reports provide information on\
         electricity and natural gas consumption in commercial and industrial buildings. Fuel oil consumption \
         in commercial and manufacturing operations are estimated using the average employment and/or number of \
          businesses in different sectors and estimates of site energy consumption by fuel from the U.S. EIA. \
            The Commercial Building Energy Consumption Survery (CBECS) and the Manufacturing Energy Consumption \
            Survey (MECS) provide estimates of energy consumption per site and per employee for different sectors. \
            In addition, direct emissions from industrial facilities from the U.S. EPA are included to capture \
                emissions from industrial processes.')

st.header('Solar and Renewables')
st.write("Data on solar installations is taken from the Massachusetts Clean Energy Center's Production Tracking \
         System (PTS). Data on other renewable energy installations is from MA DOER's lists of qualified generating \
            units.")

st.header('Transportation')
st.subheader('Residential')
st.write('The number of passenger vehicles and vehicle miles traveled is provided by the Massachusetts \
         Vehicle Census published by MassDOT. \
          These are combined with estimates of vehicle fleet efficiency to estimate the total number of \
          gallons of gasoline used each year and their associated emissions.')

st.subheader('Commercial')
st.write('Similar to the residential sector, the number of vehicles and vehicle miles traveled is taken \
          from the Massachusetts Vehicle Census and used to estimate gallons of gasoline and emissions. \
              Municipal vehicles are distinguished from other commercial vehicles in the dataset and thus are \
            shown separately in the tool as well.')

st.header('Waste')
st.write('Tonnage of trash is collected from the Massachusetts DEP. An emissions factor is applied depending \
         on whether trash is primarily sent to a landfill or an incinerator. Food and yard waste collection \
           reported is assumed to be composted.')
st.write('Wastewater emissions are based on state total wastewater emissions data applied per capita based on \
         the population in each municipality as well as their type of wastewater management system. ')

st.header('Data Sources')
st.markdown('''Massachusetts Department of Economic Research. Employment and Wages.  
            https://lmi.dua.eol.mass.gov/LMI/EmploymentAndWages?_ga=2.173362977.306818688.1722258458-2034122194.1708721447  
            Massachusetts Department of Energy Resources. Lists of Qualified Generation Units.  
             https://www.mass.gov/info-details/lists-of-qualified-generation-units  
         Massachusetts Department of Environmental Protection. Massachusetts Greenhouse Gas (GHG) Reporting Program Data  
             https://www.mass.gov/lists/massachusetts-greenhouse-gas-ghg-reporting-program-data  
         Massachusetts Department of Environmental Protection. Recycling & Solid Waste Data for
             Massachusetts Cities & Towns.  
             https://www.mass.gov/lists/recycling-solid-waste-data-for-massachusetts-cities-towns  
         Massachusetts Department of Public Utilities. Find an MLP annual return.  
                 https://www.mass.gov/info-details/find-an-mlp-annual-return  
         Massachusetts Department of Transportation. Massachusetts Vehicle Census.  
             https://geodot-homepage-massdot.hub.arcgis.com/pages/massvehiclecensus  
         Mass Save Data. \
             https://www.masssavedata.com/Public/GeographicSavings?view=C  
         Metropolitan Area Planning Council. Community Greenhouse Gas Inventories.  
             https://www.mapc.org/resource-library/community-ghg-inventory-resources/  
         U.S. Census Bureau. \
             https://data.census.gov/  
        U.S. EIA. Commercial Building Energy Consumption Survey. \
            https://www.eia.gov/consumption/commercial/data/2018/  
        U.S. EIA. Carbon Dioxide Emissions Coefficients.  
            https://www.eia.gov/environment/emissions/co2_vol_mass.php  
        U.S. EIA. Manufacturing Energy Consumption Survey. \ 
            https://www.eia.gov/consumption/manufacturing/data/2018/  
        U.S. EIA. Residential Building Energy Consumption Survey. \
            https://www.eia.gov/consumption/residential/data/2020/  
            ''')
