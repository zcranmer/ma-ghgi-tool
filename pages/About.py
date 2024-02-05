# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:19:14 2023

@author: ACRANMER
"""

import streamlit as st

st.title('About this tool...')
st.header('The short version')
st.write('This tool takes data from the U.S. Census Bureau and MA state agencies related to \
         energy and calculates energy consumption in different sectors and the associated \
        emissions. The sectors include: Residential, Commercial (including Municipal), \
        and Industrial. The fuels and energy sources estimated include: electricity, \
        natural gas, fuel oil, propane, wood, gasoline, and diesel. The methods used are \
            very similar to those in the MAPC GHGI Spreadsheet tool.')

st.header('Buildings')
st.subheader('Residential')
st.write('The Mass Save program publishes monthly and annual totals of electricity and natural \
         gas purchases by municipality, separated by customer type (residential or commercial \
         & industrial). For communities served by a Municipal Light Plant for electricity \
        and/or natural gas, annual purchases by customer type are taken from the MLP Annual Reports.\
        To estimate fuel oil use, as in the MAPC Inventory Tool, the number of households by heating fuel \
         is taken from the U.S. Census Bureau Data (Table B25046). The site energy consumption by fuel \
         from the U.S. EIA Residential Energy Consumption Survey (RECS) is used to estimate the \
        heating fuel consumption by multiplying the number of households using fuel oil by the \
        site fuel oil consumption for the state of Massachusetts. The same method is applied to \
        calculate residential propane consumption.')

st.subheader('Commercial')
st.write('As for the residential buildings, the Mass Save and MLP Annual Reports provide information on\
         electricity and natural gas consumption in commercial and industrial buildings. ')

st.header('Transportation')
st.subheader('Residential')

st.subheader('Commercial')

st.header('Waste')
st.write('Tonnage of trash is collected from the Massachusetts DEP. An emissions factor is applied depending \
         on whether trash is primarily sent to a landfill or an incinerator.')

st.header('Data Sources')
st.write('Massachusetts Department of Energy Resources. Lists of Qualified Generation Units. \
             https://www.mass.gov/info-details/lists-of-qualified-generation-units\
         Massachusetts Department of Environmental Protection. Recycling & Solid Waste Data for\
             Massachusetts Cities & Towns. \
             https://www.mass.gov/lists/recycling-solid-waste-data-for-massachusetts-cities-towns \
         Massachusetts Department of Public Utilities. Find an MLP annual return. \
                 https://www.mass.gov/info-details/find-an-mlp-annual-return\
         Massachusetts Department of Transportation. Mass Vehicle Census. \
             https://geodot-homepage-massdot.hub.arcgis.com/pages/massvehiclecensus \
         Mass Save Data. \
             https://www.masssavedata.com/Public/GeographicSavings?view=C\
         Metropolitan Area Planning Council. Community Greenhouse Gas Inventories. \
             https://www.mapc.org/resource-library/community-ghg-inventory-resources/ \
         U.S. Census Bureau. \
             https://data.census.gov/ \
        U.S. EIA. Commercial Building Energy Consumption Survey. \
            https://www.eia.gov/consumption/commercial/data/2018/\
        U.S. EIA. Residential Building Energy Consumption Survey. \
            https://www.eia.gov/consumption/residential/data/2020/ \
            ')
