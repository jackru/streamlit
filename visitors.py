"""Map to display visitors to schools data from PfIE's FOI request"""
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title='Religious Visitors to Northern Irish Primary Schools',
                   page_icon='https://storage.mlcdn.com/account_image/293832/H3etpcTDIeoZhChu7cYp9RkbGecqwFM8aYZLhbWb.png')


st.header('Religious Visitors to Northern Irish Primary Schools')


@st.cache_data
def load_visitor_strings():
    data = pd.read_csv('./visitor_strings_freq_updated.csv') # changed 15.08.25
    data.loc[data['display'] == 'DID NOT RESPOND TO SURVEY', 'display'] = 'NO RESPONSE AS OF 2024-03-27'
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
             'the map below. Frequency of visits is estimated based on information '
             'provided by schools. School population data is from [Schools Plus NI]'
             '(https://www.education-ni.gov.uk/services/schools-plus) for the 2024/25 school year. '
             'Population ranges are explained in the notes below the map. '

            #  'Markers are coloured and sized according to a combination '
            #  'of visitor volume and the number of non-Christian pupils.'
            #  '\n\nNB: Data shown includes responses as of 2024-03-27 - this map will be updated shortly with the latest responses. '
            #  'Individual school responses can be viewed by visiting [WhatDoTheyKnow.com](https://www.whatdotheyknow.com/list/successful?utf8=%E2%9C%93&query=religious+practices+in+NI+primary+schools) '
            #  'and searching for your school.'
             ))

selected_school = st.selectbox('Select a school or navigate using the map:', sorted(visitor_strings['name'].unique()), index=None,
                               placeholder="Start typing to search...")    

if selected_school:
    lat, long = visitor_strings.loc[visitor_strings['name'] == selected_school, ['lat', 'lon']].values[0]
    url = visitor_strings.loc[visitor_strings['name'] == selected_school, 'url'].values[0]
    st.markdown(f"View {selected_school}'s response to our FOI request [here]({url}).")
else:
    lat, long = None, None


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
tt_pupils = '<b>Total pupils in 2024/2025:</b> {pupils_total_2024_25}' # changed 15.08.25
tt_num_other = '<b>Pupils designated "Other":</b> {other_string}' # changed 15.08.25
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

if selected_school:
    view_state = pdk.ViewState(latitude=lat - 0.03, longitude=long + 0.045, zoom=11, bearing=0, pitch=0)
    this_school_layer = pdk.Layer(
        'ScatterplotLayer',
        visitor_strings[visitor_strings['name'] == selected_school],
        opacity=0.6,
        stroked=True,
        filled=False,
        get_position='[lon, lat]',
        get_line_color='[255, 255, 255]',
        get_radius='radius_freq + 4',
        line_width_min_pixels=3,
        radius_min_pixels=2 + 2,
        radius_max_pixels=20 + 2,
        pickable=True
    )
    layers = [visitors_layer, this_school_layer]
else:
    view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)
    layers = [visitors_layer]

# Create the deck, and show it in Streamlit
visitors_deck = pdk.Deck(
    layers=layers,
    initial_view_state=view_state,
    tooltip=visitors_tooltip,
    height=800,
)

st.pydeck_chart(visitors_deck)

st.subheader("Population estimation methodology", divider="gray")

st.markdown("School population figures by granular religion categories are from a "
            "custom data request to the DE. This data can be downloaded using the "
            "button below. The DE redacts small populations for data protection - the "
            "population estimates presented here respect data privacy while giving "
            "insight into the relevant population ranges. Large ranges for the non-"
            "Christian populations are mostly due to schools having large numbers "
            "of 'unclassified' pupils within the 'Other' population: the lower ends "
            "of these ranges assume all these pupils are Christian, the upper ends "
            "assume that none of them are.")

with open("Granular Religion Statistics SUPPRESSED 2425.xlsx", "rb") as file:
    st.download_button(
        label="Download granular school population data",
        data=file,
        file_name="Granular Religion Statistics SUPPRESSED 2425.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
