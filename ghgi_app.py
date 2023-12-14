# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

st.title('Municipal Greenhouse Gas Inventory Tool')

#@st.cache_data
def load_data():
    # set file location
    os.chdir('C:/Users/acranmer/OneDrive - Bentley University/Municipal Emissions')
    df = pd.read_excel('municipal_emissions.xlsx')
    return df

data_load_state = st.text('Loading data...')
data = load_data
data_load_state.text('Loading data...done!')


st.write("""
# Total GHG emissions
""")

st.line_chart(data=data.loc[data['Municipality']=='Maynard',:],x='Year',y='Total (CO2e)')

