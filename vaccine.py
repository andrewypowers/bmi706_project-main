import altair as alt
import pandas as pd
import streamlit as st

#load data
df = pd.read_csv('vaccine_data_clean.csv')

#create streamlit app
#add title
st.write('## Vaccination')

#add seriousness selector
serious = st.radio(label = 'Serious', options = ('Yes', 'No'))
subset = df[df.serious == serious]

#add vaccine list
vaccine_list = [
    COVID,
    DTaP,
    Hepatitis B,
    Influenza,
    Meningococcal,
    MMRV,
    Pneumococcal,
]

vaccine = st.multiselect(label = 'Vaccine', options = vaccine_list, default = vaccine_list)
subset = subset[subset.vaccine.isin(vaccine)]

#

ae_freq = alt.Chart(subset
    ).mark_rect(
    ).encode(
        x = alt.X(event_type),
        y = alt.Y(count)
    ).properties(
        title = ''
    )