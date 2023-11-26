import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pydeck as pdk

st.title('NI primary school data')

DATA_LOC = './ni_schools.csv'
GEOJSON_PATH = './dea_data_simple.json'

@st.cache_data
def load_data(nrows=None):
    data = pd.read_csv(DATA_LOC, nrows=nrows)
    return data

@st.cache_data
def load_geo_data(dummy=7):
    data = gpd.read_file(GEOJSON_PATH)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Data Loaded!")

# Inspect the raw data.
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Plot data on a map
st.subheader(f'Map of all schools')

# Define the layer
sch_layer = pdk.Layer(
    'ScatterplotLayer',
    data,
    opacity=0.6,
    stroked=False,
    get_position='[lon, lat]',
    get_fill_color='[red, green, blue]',
    get_radius='radius',
    radius_min_pixels=2,
    radius_max_pixels=20,
    pickable=True
)

tt_name = '<b>Name:</b> {name}'
tt_num_pupils = '<b>Total pupils:</b> {pupils_total_2022_23}'
tt_num_protestant = '<b>Protestant:</b> {religion_protestant_est_mid_2022_23}'
tt_num_catholic = '<b>Catholic:</b> {religion_catholic_est_mid_2022_23}'
tt_num_other = '<b>Other:</b> {religion_other_est_mid_2022_23}'

# Define the tooltip
tooltip = {
    'html': '<br>'.join([tt_name, tt_num_pupils, tt_num_protestant, tt_num_catholic, tt_num_other]),
    'style': {
        'backgroundColor': 'beige',
        'color': 'maroon',
        'fontSize': '12px',
        'padding': '5px',
        'border': '1px solid maroon'
    }
}

# Create the deck, and show it in Streamlit
view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)
r = pdk.Deck(layers=[sch_layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)

# st.map(data,
#        color='color_string',
#        size='pupils_total_2022_23'
#        )

# Cloropleth map
gdf = load_geo_data()

# Inspect the raw data.
if st.checkbox('Show raw geo data'):
    st.subheader('Raw geo data')
    st.write(gdf[['FinalR_DEA', 'pupils_formatted']])

layer = pdk.Layer(
    'GeoJsonLayer',
    gdf,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color='[100, (pupils_total_2022_23 / 5000) * 255, (pupils_total_2022_23 / 5000) * 200]',
    get_line_color=[200, 200, 200, 150],
    line_width_min_pixels=1,
    pickable=True,
)

tooltip1 = {
    'html': '<b>DEA:</b> {FinalR_DEA}<br><b>Total pupils:</b> {pupils_formatted}',
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'border': '1px solid white'
    }
}

view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)

r1 = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip1)

st.subheader(f'Total pupils per DEA')
st.pydeck_chart(r1)

rel_layer = pdk.Layer(
    'GeoJsonLayer',
    gdf,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color='[pct_protestant_num * 255, pct_catholic_num * 255, pct_other_num * 255]',
    get_line_color=[200, 200, 200, 150],
    line_width_min_pixels=1,
    pickable=True,
)

tt_dea = '<b>DEA:</b> {FinalR_DEA}'
tt_num = '<b>Total pupils:</b> {pupils_formatted}'
tt_protestant = '<b>Protestant:</b> {pct_protestant}'
tt_catholic = '<b>Catholic:</b> {pct_catholic}'
tt_other = '<b>Other:</b> {pct_other}'

tooltip2 = {
    'html': '<br>'.join([tt_dea, tt_num, tt_protestant, tt_catholic, tt_other]),
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'border': '1px solid white'
    }
}

view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)

r2 = pdk.Deck(layers=[rel_layer], initial_view_state=view_state, tooltip=tooltip2)

st.subheader(f'Self-designated religious mix per DEA')
st.pydeck_chart(r2)