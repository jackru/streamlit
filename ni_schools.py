import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pydeck as pdk

st.title('NI primary school data')

DATA_LOC = './ni_schools.csv'
GEOJSON_PATH = './dea_data_simple.json'
INTEGR_PATH = './lgd_data_simple.geojson'

@st.cache_data
def load_data(dummy=8):
    data = pd.read_csv(DATA_LOC)
    return data

@st.cache_data
def load_geo_data(dummy=8):
    data = gpd.read_file(GEOJSON_PATH)
    return data

@st.cache_data
def load_integr_data(dummy=8):
    data = gpd.read_file(INTEGR_PATH)
    return data

# Explain the source of the data and link to it
survey_link=('https://view.publitas.com/integrated-education-fund/'
             'iefni-attitudinal-poll-may-summary-report-final/page/1')

st.markdown("This site visualises publicly available data from 2022/23 from the "
            "N.I. Department of Education's "
            "[Schools Plus](https://www.education-ni.gov.uk/services/schools-plus) website "
            f"and a LucidTalk [survey]({survey_link}) of parents in March 2023.")

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Data Loaded!")

# Inspect the raw data.
view_cols = [
    'name',
    'postcode',
    'management',
    'pupils_total_2022_23',
    'protestant',
    'catholic',
    'other',
]

# Plot data on a map
st.subheader(f'Map of all schools')
st.markdown(('Schools are coloured by management type. Hover over to access pupil '
             'numbers by self-declared religion.'))

if st.checkbox('Show schools data'):
    st.subheader('Schools data')
    st.write(data[view_cols])

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

# st.map(data,
#        color='color_string',
#        size='pupils_total_2022_23'
#        )

# Integrated places per LGD chloropleth
integr_places = load_integr_data()
display_cols = ['LGDNAME', 'Controlled', 'Maintained', 'Integrated',
                'Total', 'Integrated_Percent', 'integration_main_model_agree']

integr_places['Total'] = integr_places['Total'].apply(lambda x: f'{x:,}')
integr_places['Controlled'] = integr_places['Controlled'].apply(lambda x: f'{x:,}')
integr_places['Maintained'] = integr_places['Maintained'].apply(lambda x: f'{x:,}')
integr_places['Integrated'] = integr_places['Integrated'].apply(lambda x: f'{x:,}')
integr_places['Support'] = integr_places['integration_main_model_agree'].apply(lambda x: f'{x:.0%}')

lgd_layer = pdk.Layer(
    'GeoJsonLayer',
    integr_places,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=('[Integrated_Fraction * 600, '
                    'Integrated_Fraction * 900, '
                    'Integrated_Fraction * 2400]'),
    get_line_color=[200, 200, 200, 150],
    line_width_min_pixels=1,
    pickable=True,
)

tt_lgd = '<b>LGD:</b> {LGDNAME}'
tt_num_pupils = '<b>Total Places:</b> {Total}'
tt_num_contr = '<b>Controlled:</b> {Controlled}'
tt_num_maint = '<b>Maintained:</b> {Maintained}'
tt_num_integr = '<b>Integrated:</b> {Integrated}'
tt_perc_integr = '<b>Integrated Supply:</b> {Integrated_Percent}'
tt_integr_support = '<b>Integrated Demand:</b> {Support}'

tooltip0 = {
    'html': '<br>'.join([tt_lgd, tt_num_pupils, tt_num_contr,
                         tt_num_maint, tt_num_integr, tt_perc_integr, tt_integr_support]),
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'border': '1px solid white',
        'fontSize': '12px',
        'padding': '5px',
    }
}

view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)

r0 = pdk.Deck(layers=[lgd_layer], initial_view_state=view_state, tooltip=tooltip0)

st.subheader(f'Integrated Places per LGD')
st.markdown('Integrated Supply vs. Demand. Demand is from a LucidTalk [survey]'
            f'({survey_link}) of parents in March 2023 and indicates the percentage of '
            'parents agreeing that integrated education should be the main model. '
            'Supply is actual places in 2022/23.')

# Inspect the raw data.
if st.checkbox('Show LGD aggregate data'):
    st.subheader('LGD aggregate data')
    st.write(integr_places[display_cols])
    
# render the map
st.pydeck_chart(r0)

# DEA level Cloropleth maps
gdf = load_geo_data()
display_cols = ['FinalR_DEA', 'pupils_total_2022_23', 'pct_protestant', 'pct_catholic', 'pct_other']

rel_layer = pdk.Layer(
    'GeoJsonLayer',
    gdf,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=('[pct_protestant_num * 150 + 50, '
                    'pct_catholic_num * 150 + 50, '
                    'pct_other_num * 400]'),
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
        'border': '1px solid white',
        'fontSize': '12px',
        'padding': '5px',
    }
}

view_state = pdk.ViewState(latitude=54.7, longitude=-6.7, zoom=7, bearing=0, pitch=0)

r2 = pdk.Deck(layers=[rel_layer], initial_view_state=view_state, tooltip=tooltip2)

st.subheader(f'Religious mix per DEA')
st.markdown('Hover over to access aggregate pupil percentages by self-declared religion.')

# Inspect the raw data.
if st.checkbox('Show DEA aggregate data'):
    st.subheader('DEA aggregate data')
    st.write(gdf[display_cols])

# render the map
st.pydeck_chart(r2)