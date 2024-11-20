import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the dataset
skyscrapers_df = pd.read_csv('skyscrapers.csv')

# Clean and preprocess the data
skyscrapers_df = skyscrapers_df.dropna(subset=['location.latitude', 'location.longitude'])

# Title and description
st.title("Skyscraper Data Explorer")
st.write("""
This application provides an interactive exploration of skyscraper data. You can explore skyscrapers based on different attributes such as material, city, number of floors, and height.
""")

# Sidebar with widgets for user input
st.sidebar.header("Filters")

# Dropdown to select city
city = st.sidebar.selectbox("Select a City", skyscrapers_df['location.city'].unique())

# Dropdown to select material
material = st.sidebar.selectbox("Select Material", skyscrapers_df['material'].unique())

# Slider to filter by number of floors
min_floors = st.sidebar.slider("Minimum number of floors", 1, int(skyscrapers_df['statistics.floors above'].max()), 1)

# Filter data based on user input
filtered_df = skyscrapers_df[
    (skyscrapers_df['location.city'] == city) &
    (skyscrapers_df['material'] == material) &
    (skyscrapers_df['statistics.floors above'] >= min_floors)
]

# Display filtered data
st.subheader(f"Skyscrapers in {city} made of {material} with at least {min_floors} floor(s)")
if filtered_df.empty:
    st.write("No skyscrapers found that match your criteria.")
else:
    st.write(filtered_df[['Name', '# of Floors', 'Height (m)', 'City']])

    # Create a map of the filtered skyscrapers
    st.subheader("Skyscraper Locations on Map")
    map_data = filtered_df[['name', 'location.latitude', 'location.longitude']]

    # Check if there is any data to display on the map
    if not map_data.empty:
        # Create the map with individual location markers for each skyscraper
        layers = [
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[location.longitude, location.latitude]',
                get_radius=2000,
                get_fill_color=[255, 0, 0, 160],
                pickable=True,
                auto_highlight=True,
                get_tooltip='name'
            )
        ]

        # Set the map's initial view state based on the mean of the latitude and longitude
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=map_data['location.latitude'].mean(),
                longitude=map_data['location.longitude'].mean(),
                zoom=11
            ),
            layers=layers
        ))
    else:
        st.write("No data available to display on the map.")
