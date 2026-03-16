# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:22:48 2023

@author: ACRANMER
"""

import streamlit as st
from utils.analytics import init_analytics, track_page, track_event

init_analytics()
track_page('Feedback')

st.title('Have feedback?')
st.write('Please provide us with some feedback on this tool, it will help us to make it better!\
         This tool is actively under development, use the form available here to \
            provide comments and suggestions: https://bit.ly/ghgi-app. \
            If you have any questions about what you are seeing in this tool, \
            you can email Zana Cranmer, acranmer@bentley.edu.')
