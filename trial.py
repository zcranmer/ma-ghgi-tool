import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
@st.cache
def load_data(file_path):
    return pd.read_excel(file_path)

def main():
    st.title("Off-road CO2 Emissions by County")

    # Load the data
    file_path = "offroad.xlsx"
    df = load_data(file_path)

    # Group data by County Name and sum the Off-road CO2 emissions
    county_co2 = df.groupby('County Name')['Off-road CO2 (lbs)'].sum()

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(county_co2, labels=county_co2.index, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

if __name__ == "__main__":
    main()
