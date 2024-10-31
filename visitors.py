import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pydeck as pdk

st.set_page_config(page_title='Religious Visitors to Northern Irish Primary Schools',
                   page_icon='https://storage.mlcdn.com/account_image/293832/H3etpcTDIeoZhChu7cYp9RkbGecqwFM8aYZLhbWb.png')


st.header('Religious Visitors to Northern Irish Primary Schools')


@st.cache_data
def load_visitor_strings():
    data = pd.read_csv('./visitor_strings_freq.csv')
    return data

# Explain the source of the data and link to it
st.markdown("This site visualises the results of Parents for Inclusive Education's FOI request. "
            'Their report - [On A Mission](https://heyzine.com/flip-book/f1a10e8ea1.html) - '
            'containing the aggregated findings from this request can '
            'be found on their [website](https://www.parentsforinclusiveeducationni.org/).')


visitor_strings = load_visitor_strings()


# Plot data on a map
st.markdown(('All visitors to schools between 6th Nov 2022 and 5th Nov 2023 '
             'can be viewed by hovering/clicking on the respective school in '
             'the map below. School population data is from [Schools Plus NI](https://www.education-ni.gov.uk/services/schools-plus). '
             'Total frequency of visits is estimated based on information '
             'provided by schools. '
            #  'Markers are coloured and sized according to a combination '
            #  'of visitor volume and the number of non-Christian pupils.'
            #  '\n\nNB: Data shown includes responses as of 2024-03-27 - this map will be updated shortly with the latest responses. '
             'Individual school responses can be viewed by visiting [WhatDoTheyKnow.com](https://www.whatdotheyknow.com/list/successful?utf8=%E2%9C%93&query=religious+practices+in+NI+primary+schools) '
             'and searching for your school.'
             ))

# Define the layer
visitors_layer = pdk.Layer(
    'ScatterplotLayer',
    visitor_strings,
    opacity=0.6,
    stroked=False,
    get_position='[lon, lat]',
    get_fill_color='[red, green, blue]',
    get_radius='radius_freq',
    radius_min_pixels=2,
    radius_max_pixels=20,
    pickable=True
)

tt_name = '<b>Name:</b> {name}<br>'
tt_total = '<b>Total annual visits (est):</b> {estimated_total_visits}<br>'
tt_pupils = '<b>Total pupils in 2022/2023:</b> {pupils_total_2022_23}'
tt_num_other = '<b>Pupils designated "Other":</b> {other}'
tt_num_not_christian = '<b>...of which non-Christian:</b> {estimated_non_christian_string}'
tt_no_withdrawn = '<b># withdrawn from RE or CW:</b> {no_withdrawn}<br>'
tt_visitor_list = '<b>Visitors:</b><br>{display}'


# Define the tooltip
visitors_tooltip = {
    'html': '<br>'.join([tt_name, tt_total, tt_pupils, tt_num_other, tt_num_not_christian, tt_no_withdrawn, tt_visitor_list]),
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
visitors_deck = pdk.Deck(
    layers=[visitors_layer],
    initial_view_state=view_state,
    tooltip=visitors_tooltip,
    height=800,
)

st.pydeck_chart(visitors_deck)
