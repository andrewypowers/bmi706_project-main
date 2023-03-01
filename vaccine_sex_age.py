import altair as alt
import pandas as pd
import streamlit as st

#load data
df = pd.read_csv('vaccine_data_clean.csv'
    ).groupby(['vaccine', 'age', 'sex'], as_index = False
    ).agg({'count' : 'sum'})

#create streamlit app
#add title
st.write('## Demographic distributions of vaccine adverse events')

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
    'Pneumococcal'
]

vaccine = st.radio(label = 'Vaccine', options = vaccine_list)

#define subset
subset = df[df.serious == serious]
subset = subset[subset.vaccine == vaccine]

#adverse event frequency chart
ae_freq = alt.Chart(subset).mark_bar().encode(
    alt.X('sex:N', axis = alt.Axis(title = None, labels = False)),
    alt.Y('count:Q', scale = alt.Scale(type = 'log'), axis = alt.Axis(grid = False), title = 'Frequency of adverse events (log scale)'),
    alt.Column('age:O', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
    alt.Color('sex:N', legend = None)
    ).properties(title = 'Adverse event frequency, filtered by vaccine and seriousness, stratified by age and sex')

#adverse event proportion chart
ae_prop = alt.Chart(subset).mark_bar(
    ).transform_joinaggregate(
        total = 'sum(count)'
    ).transform_calculate(
        age_sex_percent = '100 * datum.count / datum.total'
    ).encode(
        alt.X('sex:N', axis = alt.Axis(title = None, labels = False)),
        alt.Y('age_sex_percent:Q', scale = alt.Scale(type = 'log'), axis = alt.Axis(grid = False), title = 'Percentage of adverse events (log scale)'),
        alt.Column('age:O', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
        alt.Color('sex:N', legend = None)
    ).properties(title = 'Adverse event percentage, filtered by vaccine and seriousness, stratified by age and sex')

combined_charts = ae_freq & ae_prop

st.altair_chart(combined_charts, use_container_width = False)
