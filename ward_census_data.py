"""Map to display census data"""
import geopandas as gpd
import pydeck as pdk
import streamlit as st

GEOJSON_PATH = 'ward_data_strings.geojson'
DELTAS_PATH = 'ward_delta_strings.geojson'

st.set_page_config(page_title='Census data by ward 2021',
                   page_icon='https://storage.mlcdn.com/account_image/293832/H3etpcTDIeoZhChu7cYp9RkbGecqwFM8aYZLhbWb.png')


st.header('Northern Ireland Census 2021: Religious mix by ward')


@st.cache_data
def load_ward_data():
    data = gpd.read_file(GEOJSON_PATH)
    return data

@st.cache_data
def load_ward_deltas():
    data = gpd.read_file(DELTAS_PATH)
    return data

# Explain the source of the data and link to it
st.markdown("This map visualises the religious mix of Northern Ireland's population by age and ward. "
            "Wards are coloured by the percentage of the population in each age band who self-declared as "
            "having no religion."
            )

gdf = load_ward_data()
age_band = st.selectbox(
    "Select an age band",
    gdf['AgeBand'].unique(),
)

rel_layer = pdk.Layer(
    'GeoJsonLayer',
    gdf[gdf['AgeBand'] == age_band],
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=('[red, green, blue]'),
    get_line_color=[200, 200, 200, 150],
    line_width_min_pixels=1,
    pickable=True,
)

tooltip1 = {
    'html': '{tooltip}',
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'border': '1px solid white',
        'fontSize': '12px',
        'padding': '5px',
    }
}

view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)

r = pdk.Deck(layers=[rel_layer], initial_view_state=view_state, tooltip=tooltip1)

# st.subheader('Religious mix per DEA')
# st.markdown('Hover over to access aggregate pupil percentages by self-declared religion.')

# render the map
st.pydeck_chart(r)


# Explain the source of the data and link to it
st.markdown("The bottom map visualises the change in religious categories between the 2011 and 2021 censuses. "
            "This data is for all age bands. Wards are coloured by the increase in the percentage of "
            "the population identifying as having no religion."
            )

ddf = load_ward_deltas()

rel_layer = pdk.Layer(
    'GeoJsonLayer',
    ddf,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=('[red, green, blue]'),
    get_line_color=[200, 200, 200, 150],
    line_width_min_pixels=1,
    pickable=True,
)

tooltip2 = {
    'html': '{tooltip}',
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'border': '1px solid white',
        'fontSize': '12px',
        'padding': '5px',
    }
}

view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)

r = pdk.Deck(layers=[rel_layer], initial_view_state=view_state, tooltip=tooltip2)

# st.subheader('Religious mix per DEA')
# st.markdown('Hover over to access aggregate pupil percentages by self-declared religion.')

# render the map
st.pydeck_chart(r)
