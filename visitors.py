import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pydeck as pdk

st.title('Visitors to NI primary schools')

@st.cache_data
def load_su(dummy=8):
    data = pd.read_csv('./su.csv')
    return data

@st.cache_data
def load_cef(dummy=8):
    data = pd.read_csv('./cef.csv')
    return data

@st.cache_data
def load_cjm(dummy=8):
    data = pd.read_csv('./cjm.csv')
    return data

@st.cache_data
def load_hfy(dummy=8):
    data = pd.read_csv('./hfy.csv')
    return data

# Explain the source of the data and link to it
st.markdown("This site visualises our FOI results!")

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
su = load_su()
cef = load_cef()
cjm = load_cjm()
hfy = load_hfy()
data_load_state.text("Data Loaded!")

# Inspect the raw data.
view_cols = [
    'name',
    'pcd',
    'management',
    'pupils_total_2022_23',
    'protestant',
    'catholic',
    'other',
]

# Plot data on a map
st.subheader(f'Schools visited by Scripture Union')
st.markdown(('Schools are coloured by management type. Hover over to access pupil '
             'numbers by self-declared religion.'))

if st.checkbox('Show schools data', key='su'):
    st.subheader('Schools data')
    st.write(su[view_cols])

# Define the layer
sch_layer = pdk.Layer(
    'ScatterplotLayer',
    su,
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
tt_manag = '<b>Management:</b> {management}'
tt_num_pupils = '<b>Total pupils:</b> {pupils_total_2022_23}'
tt_num_protestant = '<b>Protestant:</b> {protestant}'
tt_num_catholic = '<b>Catholic:</b> {catholic}'
tt_num_other = '<b>Other:</b> {other}'
tt_source = '<b>Source:</b> Schools Plus NI'

# Define the tooltip
tooltip = {
    'html': '<br>'.join([tt_name, tt_manag, tt_num_pupils,
                         tt_num_protestant, tt_num_catholic, tt_num_other,
                         tt_source]),
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'fontSize': '12px',
        'padding': '5px',
        'border': '1px solid white',
    }
}

# Create the deck, and show it in Streamlit
view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)
r = pdk.Deck(layers=[sch_layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)


# Plot data on a map
st.subheader(f'Schools visited by Child Evangelism Fellowship')
st.markdown(('Schools are coloured by management type. Hover over to access pupil '
             'numbers by self-declared religion.'))

if st.checkbox('Show schools data', key='cef'):
    st.subheader('Schools data')
    st.write(cef[view_cols])

# Define the layer
sch_layer = pdk.Layer(
    'ScatterplotLayer',
    cef,
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
tt_manag = '<b>Management:</b> {management}'
tt_num_pupils = '<b>Total pupils:</b> {pupils_total_2022_23}'
tt_num_protestant = '<b>Protestant:</b> {protestant}'
tt_num_catholic = '<b>Catholic:</b> {catholic}'
tt_num_other = '<b>Other:</b> {other}'
tt_source = '<b>Source:</b> Schools Plus NI'

# Define the tooltip
tooltip = {
    'html': '<br>'.join([tt_name, tt_manag, tt_num_pupils,
                         tt_num_protestant, tt_num_catholic, tt_num_other,
                         tt_source]),
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'fontSize': '12px',
        'padding': '5px',
        'border': '1px solid white',
    }
}

# Create the deck, and show it in Streamlit
view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)
r = pdk.Deck(layers=[sch_layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)


# Plot data on a map
st.subheader(f'Schools visited by Crown Jesus Ministries')
st.markdown(('Schools are coloured by management type. Hover over to access pupil '
             'numbers by self-declared religion.'))

if st.checkbox('Show schools data', key='cjm'):
    st.subheader('Schools data')
    st.write(cjm[view_cols])

# Define the layer
sch_layer = pdk.Layer(
    'ScatterplotLayer',
    cjm,
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
tt_manag = '<b>Management:</b> {management}'
tt_num_pupils = '<b>Total pupils:</b> {pupils_total_2022_23}'
tt_num_protestant = '<b>Protestant:</b> {protestant}'
tt_num_catholic = '<b>Catholic:</b> {catholic}'
tt_num_other = '<b>Other:</b> {other}'
tt_source = '<b>Source:</b> Schools Plus NI'

# Define the tooltip
tooltip = {
    'html': '<br>'.join([tt_name, tt_manag, tt_num_pupils,
                         tt_num_protestant, tt_num_catholic, tt_num_other,
                         tt_source]),
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'fontSize': '12px',
        'padding': '5px',
        'border': '1px solid white',
    }
}

# Create the deck, and show it in Streamlit
view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)
r = pdk.Deck(layers=[sch_layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)


# Plot data on a map
st.subheader(f'Schools visited by Hope for Youth Ministries')
st.markdown(('Schools are coloured by management type. Hover over to access pupil '
             'numbers by self-declared religion.'))

if st.checkbox('Show schools data', key='hfy'):
    st.subheader('Schools data')
    st.write(hfy[view_cols])

# Define the layer
sch_layer = pdk.Layer(
    'ScatterplotLayer',
    hfy,
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
tt_manag = '<b>Management:</b> {management}'
tt_num_pupils = '<b>Total pupils:</b> {pupils_total_2022_23}'
tt_num_protestant = '<b>Protestant:</b> {protestant}'
tt_num_catholic = '<b>Catholic:</b> {catholic}'
tt_num_other = '<b>Other:</b> {other}'
tt_source = '<b>Source:</b> Schools Plus NI'

# Define the tooltip
tooltip = {
    'html': '<br>'.join([tt_name, tt_manag, tt_num_pupils,
                         tt_num_protestant, tt_num_catholic, tt_num_other,
                         tt_source]),
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'fontSize': '12px',
        'padding': '5px',
        'border': '1px solid white',
    }
}

# Create the deck, and show it in Streamlit
view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)
r = pdk.Deck(layers=[sch_layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)
