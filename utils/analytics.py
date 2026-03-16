# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:31:35 2026

@author: ACRANMER
"""

import streamlit as st
from streamlit_gtag import st_gtag

def get_ga_id():
    if "GA_MEASUREMENT_ID" not in st.secrets:
        #st.warning(f"GA_MEASUREMENT_ID not found in secrets. Available keys: {list(st.secrets.keys())}")
        return None
    return st.secrets["GA_MEASUREMENT_ID"]

def init_analytics():
    ga_id = get_ga_id()
    if not ga_id:
        return
    
    if st.session_state.get('_ga_initialized'):
        return

    st_gtag(
        gtag_id=ga_id,
        id=ga_id,
        config={"send_page_view": False},
        key='ga_init'
    )
    st.session_state['_ga_initialized'] = True

def track_event(name: str, **params):
    init_analytics()
    
    ga_id = get_ga_id()
    if not ga_id:
        return

    st_gtag(
        event=name,
        parameters=params,
        gtag_id=ga_id,
        id=ga_id,
        key=f"ga_evt_{name}",
    )

def track_page(page_name: str):
    track_event("screen_view", screen_name=page_name)