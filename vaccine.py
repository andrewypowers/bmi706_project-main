import altair as alt
import pandas as pd
import streamlit as st

#load data
df = pd.read_csv('vaccine_data_clean.csv'
    ).groupby(['vaccine', 'event_type', 'serious'], as_index = False
    ).agg({'count' : 'sum'})
print(df)

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

#plot chart

ae_freq = alt.Chart(subset).mark_bar().encode(
    alt.X('vaccine:N', axis = alt.Axis(title = None, labels = False)),
    alt.Y('count:Q', scale = alt.Scale(type = 'log'), axis = alt.Axis(grid = False), title = 'Frequency'),
    alt.Column('event_type:N', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = 'Event type'),
    alt.Color('vaccine:N')
    ).configure_header(
    titleColor = 'green',
    titleFontSize = 14,
    labelColor = 'red',
    labelFontSize = 14
    ).properties(
        title = 'Adverse event frequency, filtered by vaccine and seriousness, stratified by event type'
    )

st.altair_chart(ae_freq, use_container_width = False)