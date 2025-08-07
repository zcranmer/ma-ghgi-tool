# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 09:32:22 2025

@author: ACRANMER
"""
import streamlit as st
import pandas as pd
import json

# Function for loading data
@st.cache_data
def load_data(start_year):
    df = pd.read_csv('datasets/municipal_emissions.csv',low_memory=False)
    gdf = json.load(open('datasets/municipalities.json'))
    
    dataset_ma = pd.concat([df.loc[df['Municipality']=='Massachusetts',:],df.loc[df['Municipality']!='Massachusetts',:]],axis=0)
    dataset = dataset_ma[dataset_ma['Year']>=start_year]
    
    if 'df' not in st.session_state:
        st.session_state.df = dataset
    if 'gdf' not in st.session_state:
        st.session_state.gdf = gdf
    
    df_solar = pd.read_csv('datasets/solar_data.csv')
    if 'df_solar' not in st.session_state:
        st.session_state.df_solar = df_solar
    
    df_stations = pd.read_csv('datasets/ev_stations.csv')
    if 'df_stations' not in st.session_state:
        st.session_state.df_stations = df_stations
        
    df_hp = pd.read_excel('datasets/masssave hp 2019-2023.xlsx')
    if 'df_hp' not in st.session_state:
        st.session_state.df_hp = df_hp
    
    return dataset,gdf,df_solar,df_stations,df_hp



