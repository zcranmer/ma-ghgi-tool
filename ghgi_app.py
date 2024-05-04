import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt

start_year = 2019
end_year = 2021

st.set_page_config(
    page_title='MA GHGI Tool')

st.title('Municipal Greenhouse Gas Inventory Tool')

# Define df globally
df = pd.read_excel('datasets/info.xlsx')



def load_data():
    # Load municipal emissions data
    df = pd.read_excel('datasets/municipal_emissions.xlsx')
    df = df.drop(columns=['Unnamed: 0'])
    
    # Load municipalities geojson data
    with open('datasets/municipalities.json') as f:
        gdf = json.load(f)
    
    return df, gdf

# Call load_data() to get both dataset and geo
dataset, geo = load_data()

# You can now continue with your code using dataset and geo
dataset = dataset[dataset['Year'] > start_year - 1]
dataset['Per Capita (CO2e)'] = dataset['Total (CO2e)'] / dataset['Population'] + dataset['Commercial & Industrial Gas (CO2e)']

municipality = st.sidebar.selectbox(
    'Which city or town would you like to explore?',
    dataset['Municipality'].unique())



st.session_state.key = municipality
subset = dataset[dataset['Municipality']==municipality]

year = st.sidebar.slider('Choose a year',
                         min_value=start_year,max_value=end_year,
                         value=2021)

year_set = subset[subset['Year']==year]
dataset_year = dataset[dataset['Year']==year]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['Overview','Demographics',
                                        'Residential Buildings','Commercial Buildings',
                                        'Transportation','Waste','Massachusetts','Solar'])

with tab1:
    st.header('Overview of Emissions')
    
    # Line graph of total emissions and emission per capita
    # make the figure
    fig = make_subplots(specs=[[{'secondary_y':True}]])
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Total (CO2e)'].round(0),name='Total CO2e'),
        secondary_y=False)
    fig.add_trace(
        go.Scatter(x=subset.Year,y=subset['Per Capita (CO2e)'].round(2),name='Per Capita CO2e'),
        secondary_y=True)
    fig.update_layout(title_text='Emissions in '+municipality)
    fig.update_yaxes(title_text='Total CO2e',secondary_y=False)
    fig.update_yaxes(title_text='Per Capita CO2e',secondary_y=True)
    fig.update_xaxes(title_text='Year',tickvals=list(range(start_year,end_year+1)))
    fig.update_traces(mode='markers+lines',hovertemplate=None)
    fig.update_layout(hovermode='x')
    st.plotly_chart(fig)

    # emissions by fuel pie chart
    graph_cols = ['Total Electricity (CO2e)','Total Gas (CO2e)',
                  'Total Fuel Oil (CO2e)','Total Propane (CO2e)',
                  'Total Gasoline (CO2e)',
                  'Commercial & Industrial Gas (CO2e)']

    year_sub = year_set[graph_cols].T
    year_sub = year_sub.rename(columns={year_sub.columns[0]:'Emissions'},
                               index={'Total Electricity (CO2e)':'Electricity',
                                      'Total Gas (CO2e)':'Natural Gas',
                                         'Total Fuel Oil (CO2e)':'Fuel Oil',
                                         'Total Propane (CO2e)':'Propane',
                                         'Total Gasoline (CO2e)':'Gasoline',
                                         'Commercial & Industrial Gas (CO2e)':'Industrials'}
                               )
    year_sub = year_sub.reset_index()
    fig = px.pie(year_sub.round(0),values='Emissions',names='index',
                 title='Share of emissions by fuel in MTCO2e')
    fig.update_traces(textposition='outside',textinfo='percent+label+value')
    fig.layout.update(showlegend=False)
    st.plotly_chart(fig)

    graph_cols = ['Total Residential Buildings (CO2e)',
                  'Total Commercial & Industrial Buildings (CO2e)',
                  'Total Transportation (CO2e)',
                  'Commercial & Industrial Gas (CO2e)']

    year_sub = year_set[graph_cols].T
    year_sub = year_sub.rename(columns={year_sub.columns[0]:'Emissions'})
    year_sub = year_sub.rename(index={'Total Residential Buildings (CO2e)':'Residential',
                                  'Total Commercial & Industrial Buildings (CO2e)':'Commercial & Industrial',
                                  'Total Transportation (CO2e)':'Transportation',
                                  'Commercial & Industrial Gas (CO2e)':'Industrials'})
    year_sub = year_sub.reset_index()
    fig = px.pie(year_sub.round(0), values='Emissions', names='index',
             title='Share of emissions by sector in MTCO2e')
    fig.update_traces(textposition='outside', textinfo='percent+label+value')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig)


with tab2:
    st.header('Demographics')
    
   # Population    
    fig = px.line(subset,x='Year',y='Population',title='Population in '+municipality)
    fig.update_layout(yaxis_title='people')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    # Number of households
    fig = px.line(subset,x='Year',y='Total Heating Fuels Households',title='Households in '+municipality)
    fig.update_layout(yaxis_title='Occupied Households')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    # Median household income
    fig = px.line(subset,x='Year',y='Median household income',title='Median Household Income in '+municipality)
    fig.update_layout(yaxis_title='$')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    st.write('Data sources: U.S. Census Bureau')
    
with tab3:
    st.header('Residential Building Emissions')
    
    # Residential fuel emissions pie chart
    graph_cols = ['Residential Electricity (CO2e)','Residential Gas (CO2e)',
                  'Residential Fuel Oil (CO2e)','Residential Propane (CO2e)']

    rf_year_sub = year_set[graph_cols].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Electricity (CO2e)':'Electricity',
                                      'Residential Gas (CO2e)':'Natural Gas',
                                        'Residential Fuel Oil (CO2e)':'Fuel Oil',
                                        'Residential Propane (CO2e)':'Propane'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    fig = px.pie(rf_year_sub.round(0),values='Emissions',names='index',
                 title='Share of residential household emissions by fuel')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    
    # Residential heating fuels pie chart
    hh_graph_cols = ['pct electric','pct gas',
                     'pct fuel oil','pct propane',
                    'pct wood','pct other']

    hh_year_sub = year_set[hh_graph_cols].T*100
    hh_year_sub = hh_year_sub.rename(columns={hh_year_sub.columns[0]:'Fuels'},
                                     index={'pct electric':'Electricity',
                                      'pct gas':'Natural Gas',
                                         'pct fuel oil':'Fuel Oil',
                                         'pct propane':'Propane',
                                         'pct wood':'Wood',
                                         'pct other':'Other'}
                                     )
    hh_year_sub = hh_year_sub.reset_index()
    fig = px.pie(hh_year_sub.round(0),values='Fuels',names='index',
                 title='Share of household heating fuels')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    st.write('Note: Census figures shown here are not corrected in communities known \
             to have not natural gas infrastructure. The emissions calculations for natural gas \
            rely on utility sales data and so are not affected by this.')
            
    st.write('Data sources: Mass Save Data, MA DOER, MA DPU, U.S. Census Bureau, U.S. EIA')

with tab4:            
    st.header('Commercial and Industrial Buildings')

    # Commercial fuel emissions pie chart
    graph_cols = ['Commercial & Industrial Electricity (CO2e)','Commercial & Industrial Gas (CO2e)',
                'Commercial Fuel Oil (CO2e)']

    cf_year_sub = year_set[graph_cols].T
    cf_year_sub = cf_year_sub.rename(columns={cf_year_sub.columns[0]:'Emissions'},
                                    index={'Commercial & Industrial Electricity (CO2e)':'Electricity',
                                            'Commercial & Industrial Gas (CO2e)':'Natural Gas',
                                            'Commercial Fuel Oil (CO2e)':'Fuel Oil'}
                                    )
    cf_year_sub = cf_year_sub.reset_index()
    fig = px.pie(cf_year_sub.round(0), values='Emissions', names='index',
                title='Share of commercial building emissions by fuel')
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    # Add dropdown tab directly on the page
    option = st.selectbox('Select Option', ['All'] + df['City'].unique().tolist())

    if option == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['City'] == option]

    st.header('Pie Chart of Emissions by Type')

    if not filtered_df.empty:
        emission_counts = filtered_df['Latest Reported Industry Type (sectors)'].value_counts()
        if not emission_counts.empty:
            fig = px.pie(names=emission_counts.index, values=emission_counts,
                        title='Pie Chart of Emissions by Type', labels={'names': 'Type'})
            fig.update_traces(textposition='outside', textinfo='percent+label')
            fig.layout.update(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No emissions data available for the selected city.')
    else:
        st.write('No data available for the selected city.')

    st.write('Data sources: Mass Save Data, MA DOER, MA DPU, U.S. Census Bureau, U.S. EIA')

    @st.cache_data
    def load_data(file_path):
        return pd.read_excel(file_path)

    # Load the data
    file_path = "datasets/offroad.xlsx"  # Adjust the file path
    df = load_data(file_path)

    # Get unique years
    years = df['Data Year'].unique().tolist()
    min_year = min(years)
    max_year = max(years)

    # Ensure the min and max values for the year slider are valid
    if min_year == max_year:
        selected_year = min_year
    else:
        selected_year = st.slider('Select Year', min_value=min_year, max_value=max_year, value=min_year)

    # Filter data based on selected year
    filtered_df = df[df['Data Year'] == selected_year]

    if not filtered_df.empty:
        # Get unique county names
        county_names = filtered_df['County Name'].unique().tolist()
        
        # Dropdown menu for selecting county names
        selected_county = st.selectbox("Select County Name", county_names)

        # Filter data based on selected county
        filtered_df = filtered_df[filtered_df['County Name'] == selected_county]

        # Calculate total CO2 emissions
        total_co2 = filtered_df['Off-road CO2 (lbs)'].sum()

        # Calculate percentage of emissions for each source
        filtered_df['Percentage'] = filtered_df['Off-road CO2 (lbs)'] / total_co2 * 100

        # Group sources with percentage < 1% into "Miscellaneous"
        misc = filtered_df[filtered_df['Percentage'] < 1]
        misc_sum = misc['Off-road CO2 (lbs)'].sum()
        filtered_df.loc[filtered_df['Percentage'] < 1, 'Emissions Source'] = 'Miscellaneous'
        filtered_df.loc[filtered_df['Percentage'] < 1, 'Off-road CO2 (lbs)'] = 0

        # Summarize data for non-miscellaneous sources
        non_misc_df = filtered_df[filtered_df['Percentage'] >= 1]
        non_misc_df = non_misc_df.groupby('Emissions Source').sum().reset_index()

        # Combine non-miscellaneous and miscellaneous data
        combined_df = pd.concat([non_misc_df, pd.DataFrame({'Emissions Source': ['Miscellaneous'], 'Off-road CO2 (lbs)': [misc_sum]})])

        # Create a pie chart using Plotly Express
        fig = px.pie(combined_df, names='Emissions Source', values='Off-road CO2 (lbs)', title=f'Pie Chart of Emissions by Source for {selected_county} ({selected_year})')
        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f'No data available for the selected year.')

with tab5:
    st.header('Transportation Emissions')
    
    # Transportation emissions pie chart
    graph_cols = ['Residential Gasoline (CO2e)','Residential Vehicle Electricity (CO2e)',
                  'Commercial Gasoline (CO2e)','Commercial Vehicle Electricity (CO2e)',
                  'Municipal Gasoline (CO2e)','Municipal Vehicle Electricity (CO2e)']

    rf_year_sub = year_set[graph_cols].T
    rf_year_sub = rf_year_sub.rename(columns={rf_year_sub.columns[0]:'Emissions'},
                                     index={'Residential Gasoline (CO2e)':'Passenger Gasoline',
                                      'Residential Vehicle Electricity (CO2e)':'Passenger Electricity',
                                        'Commercial Gasoline (CO2e)':'Commercial Gasoline',
                                        'Commercial Vehicle Electricity (CO2e)':'Commercial Electricity',
                                        'Municipal Gasoline (CO2e)':'Municipal Gasoline',
                                        'Municipal Vehicle Electricity (CO2e)':'Municipal Electricity'}
                                     )
    rf_year_sub = rf_year_sub.reset_index()
    fig = px.pie(rf_year_sub.round(0),values='Emissions',names='index')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    
    # plot trends in VMT and # of vehicles
    
    st.write('Data Sources: MA DOT')

with tab6:
    st.header('Waste Emissions')
    # line chart
    fig = px.line(subset,x='Year',y='Trash Disposal Tonnage',
                  title='Waste in '+municipality)
    fig.update_layout(yaxis_title='tons')
    fig.update_xaxes(tickvals=list(range(start_year,end_year+1)))
    st.plotly_chart(fig)
    
    # pie chart
    graph_cols = ['trash','single stream recyc',
                  'other recyc','organics']

    msw_year_sub = year_set[graph_cols].T
    msw_year_sub = msw_year_sub.rename(columns={msw_year_sub.columns[0]:'Waste'},
                                     index={'trash':'Trash',
                                      'single stream recyc':'Single Stream Recycling',
                                        'other recyc':'Other Recycling',
                                        'organics':'Organics'}
                                     )
    msw_year_sub = msw_year_sub.reset_index()
    fig = px.pie(msw_year_sub.round(0),values='Waste',names='index',
                 title='Share of waste by type')
    fig.update_traces(textposition='outside',textinfo='percent+label')
    fig.layout.update(showlegend=False)

    st.plotly_chart(fig,use_container_width=True)
    
    st.write('Data Sources: MA DEP')
    
with tab7:
    st.header('Massachusetts')
    
    #geo should be a dictionary of geospatial data and df has the non-spatial data
    #then they are linked together via an id
    
    # total emissions
    st.write('Total emissions by municipality')
    fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                        featureidkey='properties.Name',color='Total (CO2e)')
    fig.update_geos(fitbounds='locations',visible=False)
    fig.update_layout(height=300,margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    
    # per capita emissions
    st.write('Per person emissions by municipality')
    fig = px.choropleth(dataset_year,geojson=geo,locations='TOWN',
                        featureidkey='properties.Name',color='Per Capita (CO2e)')
    fig.update_geos(fitbounds='locations',visible=False)
    fig.update_layout(height=300,margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

with tab8:
    st.header('Solar Energy Analysis by County')
    
    data = {
    'Barnstable County': {
        'New Solar Additions': [121, 121, 110, 176, 198],
        'Cost per Watt': [3.40, 3.20, 3.40, 3.60, 3.00],
        'Energy Consumption per Person': [2310, 2460, 3055, 2940, 2625],
        'Emissions per Person': [4.4, 4.3, 4.6, 4.7, 4.4],
        'Emissions per Municipality': [9500, 9025, 10450, 9500, 9025]
    },
    'Berkshire County': {
        'New Solar Additions': [110, 132, 77, 209, 242],
        'Cost per Watt': [3.50, 3.00, 3.80, 3.30, 2.70],
        'Energy Consumption per Person': [2258, 2467, 2887, 3202, 2782],
        'Emissions per Person': [4.2, 3.95, 4.37, 4.63, 4.2],
        'Emissions per Municipality': [9120, 8645, 10070, 9405, 8835]
    },
    'Bristol County': {
        'New Solar Additions': [105, 116, 95, 189, 200],
        'Cost per Watt': [3.70, 3.10, 3.60, 3.50, 2.80],
        'Energy Consumption per Person': [2226, 2456, 2856, 3171, 2753],
        'Emissions per Person': [3.9, 4.0, 3.8, 4.3, 3.9],
        'Emissions per Municipality': [8930, 8645, 9880, 9215, 8645]
    },
    'Dukes County': {
        'New Solar Additions': [121, 143, 165, 187, 209],
        'Cost per Watt': [3.40, 3.30, 3.20, 3.00, 2.80],
        'Energy Consumption per Person': [2310, 2460, 3055, 2940, 2625],
        'Emissions per Person': [4.5, 4.4, 4.3, 4.2, 4.1],
        'Emissions per Municipality': [9975, 9500, 9025, 8550, 8075]
    },
    'Essex County': {
        'New Solar Additions': [121, 110, 110, 176, 198],
        'Cost per Watt': [3.45, 3.35, 3.45, 3.65, 3.05],
        'Energy Consumption per Person': [2310, 2457, 3055, 2940, 2625],
        'Emissions per Person': [4.4, 4.3, 4.6, 4.7, 4.4],
        'Emissions per Municipality': [9500, 9025, 10450, 9500, 9025]
    },
    'Franklin County': {
        'New Solar Additions': [104.5, 115.5, 94.5, 189, 199.5],
        'Cost per Watt': [3.71, 3.14, 3.61, 3.52, 2.81],
        'Energy Consumption per Person': [2226, 2456, 2856, 3171, 2753],
        'Emissions per Person': [3.9, 4.0, 3.8, 4.3, 3.9],
        'Emissions per Municipality': [8930, 8645, 9880, 9215, 8645]
    },
    'Hampden County': {
        'New Solar Additions': [110, 132, 77, 209, 242],
        'Cost per Watt': [3.65, 3.05, 3.8, 3.35, 2.66],
        'Energy Consumption per Person': [2258, 2467, 2887, 3202, 2782],
        'Emissions per Person': [4.2, 3.95, 4.37, 4.63, 4.2],
        'Emissions per Municipality': [9120, 8645, 10070, 9405, 8835]
    },
     'Hampshire County': {
        'New Solar Additions': [110, 130, 150, 170, 190],
        'Cost per Watt': [3.6, 3.5, 3.4, 3.3, 3.2],
        'Energy Consumption per Person': [2200, 2340, 2910, 2800, 2500],
        'Emissions per Person': [4.6, 4.5, 4.4, 4.3, 4.2],
        'Emissions per Municipality': [10500, 10000, 9500, 9000, 8500]
    },
     'Middlesex County': {
        'New Solar Additions': [130, 155, 180, 205, 230],
        'Cost per Watt': [4.0, 3.9, 3.8, 3.7, 3.6],
        'Energy Consumption per Person': [2400, 2575, 2750, 2925, 3100],
        'Emissions per Person': [5.0, 4.9, 4.8, 4.7, 4.6],
        'Emissions per Municipality': [10900, 10650, 10400, 10150, 9900]
    },
     'Nantucket County': {
        'New Solar Additions': [43, 26, 31, 55, 68],
        'Cost per Watt': [3.9, 3.8, 3.7, 3.6, 3.5],
        'Energy Consumption per Person': [2350, 2525, 2700, 2875, 3050],
        'Emissions per Person': [3.9, 3.8, 3.7, 3.6, 3.5],
        'Emissions per Municipality': [9400, 10550, 10300, 10050, 9800]
    },
    'Norfolk County': {
        'New Solar Additions': [115, 135, 155, 175, 195],
        'Cost per Watt': [3.65, 3.55, 3.45, 3.35, 3.25],
        'Energy Consumption per Person': [2250, 2390, 2960, 2850, 2550],
        'Emissions per Person': [4.65, 4.55, 4.45, 4.35, 4.25],
        'Emissions per Municipality': [10750, 10250, 9750, 9250, 8750]
    },
    'Plymouth County': {
        'New Solar Additions': [110, 130, 150, 170, 190],
        'Cost per Watt': [3.6, 3.5, 3.4, 3.3, 3.2],
        'Energy Consumption per Person': [2200, 2340, 2910, 2800, 2500],
        'Emissions per Person': [4.6, 4.5, 4.4, 4.3, 4.2],
        'Emissions per Municipality': [10500, 10000, 9500, 9000, 8500]
    },
    'Suffolk County County': {
        'New Solar Additions': [125, 145, 165, 185, 205],
        'Cost per Watt': [3.7, 3.6, 3.5, 3.4, 3.3],
        'Energy Consumption per Person': [2350, 2490, 3060, 2950, 2650],
        'Emissions per Person': [4.7, 4.6, 4.5, 4.4, 4.3],
        'Emissions per Municipality': [11250, 10750, 10250, 9750, 9250]
    },
    'Worcester County': {
        'New Solar Additions': [120, 140, 160, 180, 200],
        'Cost per Watt': [3.8, 3.7, 3.6, 3.5, 3.4],
        'Energy Consumption per Person': [2300, 2440, 3010, 2900, 2600],
        'Emissions per Person': [4.8, 4.7, 4.6, 4.5, 4.4],
        'Emissions per Municipality': [11500, 11000, 10500, 10000, 9500]
    }

    
    }
    # Get the available years in the data
    available_years = np.arange(2017, 2022)

    
    # Slider for selecting year range
    start_year, end_year = st.slider('Select Year Range', 2017, 2021, (2017, 2021))

    # Ensure that the selected range is a full year range
    start_year = max(start_year, 2017)
    end_year = min(end_year, 2021)

    # County select dropdown
    county = st.selectbox('Select County', list(data.keys()))

# Filtered data based on selected county and year range
    filtered_data = pd.DataFrame({
    'Year': available_years[(available_years >= start_year) & (available_years <= end_year)],
    'New Solar Additions': data[county]['New Solar Additions'][start_year-2017:end_year-2017+1],
    'Cost per Watt': data[county]['Cost per Watt'][start_year-2017:end_year-2017+1],
    'Energy Consumption per Person': data[county]['Energy Consumption per Person'][start_year-2017:end_year-2017+1],
    'Emissions per Person': data[county]['Emissions per Person'][start_year-2017:end_year-2017+1],
    'Emissions per Municipality': data[county]['Emissions per Municipality'][start_year-2017:end_year-2017+1]
})
    # Convert years to integers
    filtered_data['Year'] = filtered_data['Year'].astype(int)

    # Display line charts for each data column
    for column in filtered_data.columns[1:]:
        st.subheader(column)
        fig, ax = plt.subplots()
        ax.plot(filtered_data['Year'], filtered_data[column])
        ax.set_xticks(filtered_data['Year'])  # Ensure ticks are at integer year values
        ax.set_xlabel('Year')
        ax.set_ylabel(column)
        st.pyplot(fig)
    
    allocated_capacities = {
        'Barnstable County': {'Commercial': 500000, 'Industrial': 250000, 'Residential': 589000},
        'Berkshire County': {'Commercial': 800000, 'Industrial': 700000, 'Residential': 900000},
        'Bristol County': {'Commercial': 900000, 'Industrial': 800000, 'Residential': 1000000},
        'Dukes County': {'Commercial': 300000, 'Industrial': 150000, 'Residential': 450000},
        'Essex County': {'Commercial': 950000, 'Industrial': 900000, 'Residential': 1100000},
        'Franklin County': {'Commercial': 400000, 'Industrial': 300000, 'Residential': 850000},
        'Hampden County': {'Commercial': 900000, 'Industrial': 800000, 'Residential': 1080000},
        'Hampshire County': {'Commercial': 450000, 'Industrial': 300000, 'Residential': 450000},
        'Middlesex County': {'Commercial': 1200000, 'Industrial': 1000000, 'Residential': 1300000},
        'Nantucket County': {'Commercial': 200000, 'Industrial': 100000, 'Residential': 2302000},
        'Norfolk County': {'Commercial': 1004800, 'Industrial': 900000, 'Residential': 1100000},
        'Plymouth County': {'Commercial': 850000, 'Industrial': 500000, 'Residential': 800000},
        'Suffolk County': {'Commercial': 1100000, 'Industrial': 1000000, 'Residential': 1200000},
        'Worcester County': {'Commercial': 1000000, 'Industrial': 600000, 'Residential': 140000}
    }

    # Generate data frame from allocated capacities
    data = []
    for municipality, capacities in allocated_capacities.items():
        for facility_type, capacity in capacities.items():
            data.append({'City/Town': municipality, 'Facility Type': facility_type, 'Capacity (MMBTU)': capacity})
    df = pd.DataFrame(data)

    # Function to aggregate capacity data based on facility type
    def aggregate_capacity(data):
        return data.groupby(['City/Town', 'Facility Type']).sum().reset_index()

    # Function to generate charts
    def generate_charts(data, city_town):
        # Filter data for selected city/town
        filtered_data = data[data['City/Town'] == city_town]

        # Create pie chart
        st.subheader('Pie Chart')
        pie_data = filtered_data.groupby('Facility Type')['Capacity (MMBTU)'].sum()
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        # Create bar chart
        st.subheader('Bar Chart')
        bar_data = filtered_data.groupby('Facility Type')['Capacity (MMBTU)'].sum()
        fig, ax = plt.subplots()
        bar_data.plot(kind='bar', ax=ax)
        ax.set_xlabel('Facility Type')
        ax.set_ylabel('Total Capacity (MMBTU)')
        ax.set_title('Total Capacity by Facility Type')
        st.pyplot(fig)

    # Function to analyze energy facility data and generate charts
    def analyze_energy_data():
        st.title('Energy Facility Data Analysis')

        # Get unique city/town names
        city_towns = df['City/Town'].unique()

        # Sidebar for selecting city/town
        city_town = st.selectbox('Select City/Town', city_towns)

        # Aggregate capacity data
        aggregated_data = aggregate_capacity(df)

        # Generate charts
        generate_charts(aggregated_data, city_town)

    if __name__ == "__main__":
        analyze_energy_data()