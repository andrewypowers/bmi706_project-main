import altair as alt
import pandas as pd
import streamlit as st

#load data
df = pd.read_csv('vaccine_data_clean.csv'
    ).groupby(['vaccine', 'event_type', 'seriousness'], as_index = False
    ).agg({'count' : 'sum'})

#create streamlit app
#add title
st.write('## Distribution of vaccine adverse events types')

#add seriousness selector
seriousness = st.radio(label = 'Seriousness', options = ('serious', 'non-serious'))

#add vaccine list
vaccine_list = [
    'COVID',
    'DTaP',
    'Hepatitis B',
    'Influenza',
    'Meningococcal',
    'MMRV',
    'Pneumococcal'
]

vaccine = st.multiselect(label = 'Vaccine', options = vaccine_list, default = None)

#define subset
subset = df[df.seriousness == seriousness]
subset = subset[subset.vaccine.isin(vaccine)]

#total adverse event per vaccine chart
ae_total = alt.Chart(subset
    ).transform_aggregate(
        total_count = 'sum(count)',
        groupby = ['vaccine']
    ).mark_bar().encode(
        alt.X('total_count:Q', scale = alt.Scale(type = 'linear'), axis = alt.Axis(grid = False), title = 'Adverse event frequency'),
        alt.Y('vaccine:N', title = ''),
        alt.Color('vaccine:N')
    ).properties(title = f'Total {seriousness} adverse event frequency, for the {vaccine} vaccine(s)')

st.altair_chart(ae_total, use_container_width = True)

#adverse event frequency chart
ae_freq = alt.Chart(subset).mark_bar().encode(
    alt.X('vaccine:N', axis = alt.Axis(title = None, labels = False)),
    alt.Y('count:Q', scale = alt.Scale(type = 'linear'), axis = alt.Axis(grid = False), title = 'Frequency of adverse events'),
    alt.Column('event_type:N', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
    alt.Color('vaccine:N', legend = None)
    ).properties(title = 'Adverse event frequency, filtered by vaccine and seriousness, stratified by event type')

st.altair_chart(ae_freq, use_container_width = False)

#adverse event proportion chart
ae_prop = alt.Chart(subset).mark_bar(
    ).transform_joinaggregate(
        total = 'sum(count)'
    ).transform_calculate(
        event_percent = '100 * datum.count / datum.total'
    ).encode(
        alt.X('vaccine:N', axis = alt.Axis(title = None, labels = False)),
        alt.Y('event_percent:Q', scale = alt.Scale(type = 'linear'), axis = alt.Axis(grid = False), title = 'Percentage of adverse events'),
        alt.Column('event_type:N', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
        alt.Color('vaccine:N', legend = None)
    ).properties(title = 'Adverse event percentage, filtered by vaccine and seriousness, stratified by event type')

st.altair_chart(ae_prop, use_container_width = False)
