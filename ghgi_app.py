# -*- coding: utf-8 -*-
"""
Main file in public dashboard tool
MA Greenhouse Gas Inventory Tool
"""

import streamlit as st
import pandas as pd
#import numpy as np
#import json
import plotly.express as px
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#import streamlit_analytics2 as streamlit_analytics

from utils.analytics import init_analytics

init_analytics()


pg = st.navigation([st.Page('pages/GHG_Inventory_Tool.py'),
                    st.Page('pages/2_About.py'),
                    st.Page('pages/3_Climate Goals Tracker.py'),
                    st.Page('pages/4_Feedback.py')
                    ])
pg.run()


st.set_page_config(layout='wide',
                   page_title='MA GHGI Tool'
                   )


