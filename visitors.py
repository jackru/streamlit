import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pydeck as pdk

st.title('Visitors to NI primary schools')

@st.cache_data
def load_su():
    data = pd.read_csv('./su.csv')
    return data

@st.cache_data
def load_cef():
    data = pd.read_csv('./cef.csv')
    return data

@st.cache_data
def load_cjm():
    data = pd.read_csv('./cjm.csv')
    return data

@st.cache_data
def load_hfy():
    data = pd.read_csv('./hfy.csv')
    return data

@st.cache_data
def load_visitor_strings():
    # data = pd.read_csv('./visitor_strings.csv')
    data = pd.read_csv('./visitor_strings_freq.csv')
    return data

# Explain the source of the data and link to it
st.markdown("This site visualises our FOI results.")

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
su = load_su()
cef = load_cef()
cjm = load_cjm()
hfy = load_hfy()
visitor_strings = load_visitor_strings()
data_load_state.text("Data Loaded.")

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
st.subheader(f'Visitors to NI primary schools')
st.markdown(('All visitors to schools between 6th Nov 2022 and 5th Nov 2023 '
             'can be viewed by hovering/clicking on the respective school in '
             'the map below. Frequency of visits to follow...'))

# Define the layer
sch_layer = pdk.Layer(
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

tt_name = '<b>Name:</b><br>{name}<br>'
tt_total = '<b>Total annual visits (est.): {estimated_total_visits}</b><br>'
tt_visitor_list = '<b>Visitors:</b><br>{display}'
# tt_manag = '<b>Management:</b> {management}'
# tt_num_pupils = '<b>Total pupils:</b> {pupils_total_2022_23}'
# tt_num_protestant = '<b>Protestant:</b> {protestant}'
# tt_num_catholic = '<b>Catholic:</b> {catholic}'
# tt_num_other = '<b>Other:</b> {other}'
# tt_source = '<b>Source:</b> Schools Plus NI'

# Define the tooltip
tooltip = {
    'html': '<br>'.join([tt_name, tt_total, tt_visitor_list]),
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
st.subheader(f'Scripture Union')
st.markdown(('Scripture Union is “an organisation determined to help people encounter God”. '
             'They visited at least 159 primary schools that we surveyed an estimated average '
             'of x times each during the period. SUNI are passionate about making God’s Good '
             'News known in primary, post primary and special schools through dedicated staff, '
             'training of local volunteers and resourcing the church.\n\n'
             'Their aims, beliefs and principles can be found [here]'
             '(https://www.suni.co.uk/who-we-are/aims-beliefs-principles).'))

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
st.subheader(f'Child Evangelism Fellowship')
st.markdown(('Child Evangelism Fellowship is a Bible-centred organisation, whose [purpose]'
             '(https://www.cefireland.com/what-we-do/) is to evangelise boys and girls with '
             'the Gospel of the Lord Jesus Christ, to edify (disciple) them in the Word of '
             'God and to establish them in a local church. They visited at least 121 primary '
             'schools in Northern Ireland an estimated average of x times each during the '
             'period.\n\n'
             'They specialise in training child evangelists, with a [series of courses]'
             '(https://www.cefonline.com/about/training/tce/) on effective methods of '
             'evangelism.\n\n'
             'Their statement of faith can be found [here]'
             '(https://www.cefonline.com/about/statementoffaith/).'))

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
st.subheader(f'Crown Jesus Ministries')
st.markdown(('Crown Jesus Ministries “do evangelism”. Their [KlassKids]'
             '(https://www.crownjesus.org/klasskids) programme uses '
             'puppetry to “invade assemblies with a production that encourages children '
             'to learn about a Bible story and the teachings of Jesus in a fun, creative '
             'and relevant way”.\n\nFor S.E.N.D. schools their team has developed specific '
             'assembly productions and R.E. classes that have been tailored to creatively '
             'share messages from the Bible using puppets, songs, visual aids, Makaton and '
             'additional sensory elements.\n\n'
             'Crown Jesus Ministries visited at least 51 primary schools in Northern '
             'Ireland an estimated average of x times each during the period. They also '
             'run [academy](https://www.crownjesus.org/academy) and [school of evangelism]'
             '(https://www.crownjesus.org/soe) programmes with a focus on youth and kids '
             'ministry.\n\nTheir statement of faith can be found [here]'
             '(https://www.crownjesus.org/statement-of-faith).'))

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
st.subheader(f'Hope for Youth Ministries')
st.markdown(('Hope for Youth Ministries claim to visit more than 250 schools across '
             'Northern Ireland. According to our survey, they visited at least 44 '
             'schools during the period in question. They deliver school assemblies, '
             '5-day Bible Clubs and Scripture Union meetings tailored to children, as '
             'well as producing several [devotional books]'
             '(https://hopeforyouthministries.org/product-category/devotional-books/), '
             '[tracts](https://hopeforyouthministries.org/product-category/tracts/) and '
             'a series of [videos](https://hopeforyouthministries.org/video/).\n\n'
             'Hope for Youth’s school ministry is explained by their founder in this '
             '[video](https://youtu.be/j9-Jl7O52kw).'))

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
