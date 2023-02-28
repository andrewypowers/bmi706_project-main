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
subset = df[df.serious == serious]

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
subset = subset[subset.vaccine.isin(vaccine)]

#

ae_freq = alt.Chart(subset).mark_bar().encode(
        x = alt.X('event_type:N', title = 'Event type'),
        y = alt.Y('count:Q', title = 'Frequency'),
        xOffset = 'vaccine',
        color = 'vaccine'
    ).properties(
        title = ''
    )

st.altair_chart(ae_freq, use_container_width = True)