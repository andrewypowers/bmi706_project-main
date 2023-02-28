import altair as alt
import pandas as pd
import streamlit as st

#load data
df = pd.read_csv('vaccine_data_clean.csv'
    ).groupby(['vaccine', 'event_type', 'serious'], as_index = False
    ).agg({'count' : 'sum'})

#create streamlit app
#add title
st.write('## Vaccination')

#add seriousness selector
serious = st.radio(label = 'Serious', options = ('Yes', 'No'))

#add vaccine list
vaccine_list = [
    'COVID',
    'DTaP',
    'Hepatitis B',
    'Influenza',
    'Meningococcal',
    'MMRV',
    'Pneumococcal',
]

vaccine = st.multiselect(label = 'Vaccine', options = vaccine_list, default = None)

#define subset
subset = df[df.serious == serious]
subset = subset[subset.vaccine.isin(vaccine)]

#adverse event frequency chart
ae_freq = alt.Chart(subset).mark_bar().encode(
    alt.X('vaccine:N', axis = alt.Axis(title = None, labels = False)),
    alt.Y('count:Q', scale = alt.Scale(type = 'log'), axis = alt.Axis(grid = False), title = 'Frequency (log scale)'),
    alt.Column('event_type:N', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
    alt.Color('vaccine:N')
    ).properties(title = 'Adverse event frequency, filtered by vaccine and seriousness, stratified by event type'
    ).configure_title(color = 'white')

st.altair_chart(ae_freq, use_container_width = False)

#adverse event proportion chart
ae_prop = alt.Chart(subset).mark_bar(
    ).transform_joinaggregate(
        total_event = 'sum(count)'
    ).transform_calculate(
        event_percent = ' datum.count / datum.total_event'
    ).encode(
        alt.X('vaccine:N', axis = alt.Axis(title = None, labels = False)),
        alt.Y('event_percent:Q', scale = alt.Scale(type = 'log'), axis = alt.Axis(grid = False), title = 'Proportion'),
        alt.Column('event_type:N', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
        alt.Color('vaccine:N')
        ).properties(title = 'Adverse event proportion, filtered by vaccine and seriousness, stratified by event type'
        ).configure_title(color = 'white')

st.altair_chart(ae_prop, use_container_width = False)