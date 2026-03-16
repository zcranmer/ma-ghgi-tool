# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:31:35 2026

@author: ACRANMER
"""

import os
import streamlit as st
from streamlit_gtag import st_gtag

def get_ga_id():
    # Prefer secrets, fallback to None
    try:
        return st.secrets["GA_MEASUREMENT_ID"]
    except Exception:
        return None

def init_analytics():
    ga_id = get_ga_id()
    if not ga_id:
        return

    # Initialize GA tag; the package supports config like send_page_view. [1](https://discuss.streamlit.io/t/injecting-html-gtm-analytics-into-dockerized-streamlit-apps/116248)
    st_gtag(
        gtag_id=ga_id,
        config={"send_page_view": False}  # we'll emit our own page events
    )

def track_event(name: str, **params):
    """
    Send a GA4 event with parameters.
    """
    ga_id = get_ga_id()
    if not ga_id:
        return

    # The package supports sending custom events with parameters. [1](https://discuss.streamlit.io/t/injecting-html-gtm-analytics-into-dockerized-streamlit-apps/116248)
    st_gtag(
        event=name,
        parameters=params
    )

def track_page(page_name: str):
    """
    Track a 'virtual page' / screen view.
    """
    # GA4 event-based tracking is standard; event + params. [2](https://www.google.com/)
    track_event("screen_view", screen_name=page_name)