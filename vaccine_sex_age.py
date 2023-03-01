import altair as alt
import pandas as pd
import streamlit as st

#load data
df = pd.read_csv('vaccine_data_clean.csv'
    ).groupby(['vaccine', 'age', 'sex', 'seriousness'], as_index = False
    ).agg({'count' : 'sum'})

#create streamlit app
#add title
st.write('## Demographic distributions of vaccine adverse events from 1990 to 2022')

#add seriousness selector
seriousness = st.radio(label = 'Serious', options = ('serious', 'non-serious'))

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
subset = df[df.seriousness == seriousness]
subset = subset[subset.vaccine == vaccine]

#adverse event frequency chart
ae_freq = alt.Chart(subset).mark_bar().encode(
    alt.X('sex:N', axis = alt.Axis(title = None, labels = False)),
    alt.Y('count:Q', scale = alt.Scale(type = 'linear'), axis = alt.Axis(grid = False), title = 'Frequency of adverse events'),
    alt.Column('age:O', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
    alt.Color('sex:N')
    ).properties(title = f'Frequency of {vaccine} vaccine {seriousness} adverse events')

#adverse event proportion chart
ae_prop = alt.Chart(subset).mark_bar(
    ).transform_joinaggregate(
        sex_total = 'sum(count)',
        groupby = ['sex']
    ).transform_calculate(
        sex_percent = '100 * datum.count / datum.sex_total'
    ).encode(
        alt.X('sex:N', axis = alt.Axis(title = None, labels = False)),
        alt.Y('sex_percent:Q', scale = alt.Scale(type = 'linear'), axis = alt.Axis(grid = False), title = 'Percentage of adverse events'),
        alt.Column('age:O', header = alt.Header(titleOrient = 'bottom', labelOrient = 'bottom', labelColor = 'white'), title = ''),
        alt.Color('sex:N')
    ).properties(title = f'Age and sex distribution of {vaccine} vaccine {seriousness} adverse events')

combined_charts = ae_freq & ae_prop

st.altair_chart(combined_charts, use_container_width = False)
