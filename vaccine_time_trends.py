import altair as alt
import pandas as pd
import streamlit as st

#load data
df = pd.read_csv('vaccine_data_clean.csv'
    ).groupby(['sex', 'year', 'vaccine', 'seriousness'], as_index = False
    ).agg({'count' : 'sum'})

#create streamlit app
#add title
st.write('## Vaccine adverse events over time between 1990 to 2022')

#add seriousness selector
seriousness = st.multiselect(label = 'Seriousness', options = ('serious', 'non-serious'),
                             default = ('serious', 'non-serious'))

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

# Add vaccine list selector
vaccine = st.multiselect(label = 'Vaccine', options = vaccine_list, default = None)

# Choose a group_by variable
grouping_variable = st.radio(label = "Grouping Variable",
                             options = ("vaccine", "seriousness", "sex"),
                             index = 0)

#define subset
subset = df[df.seriousness.isin(seriousness)]
subset = subset[subset.vaccine.isin(vaccine)]

# Group by grouping variable
    # Select columns and rename to grouping variable
subset = subset.loc[:, ("year", "count", grouping_variable)].rename(columns = {grouping_variable:"grouping_variable"})

subset_grouped = subset.groupby(["year", "grouping_variable"], as_index = False
    ).agg({'count' : 'sum'})

# Upper Chart: total adverse event per vaccine chart
ae_total = alt.Chart(subset
    ).transform_aggregate(
        count = 'sum(count)',
        groupby = ["year",'grouping_variable']
    ).mark_area().encode(
        alt.Y('sum(count):Q', scale = alt.Scale(type = 'linear'), axis = alt.Axis(grid = False), title = '# Adverse events'),
        alt.X('year:Q', title = '', axis=alt.Axis(format='.0f')),
        alt.Color('grouping_variable:N', title = grouping_variable, scale=alt.Scale(scheme='dark2'))
    ).properties(title = f'Total number of adverse events by year')


#Lower Chart adverse event frequency chart
ae_count = alt.Chart(subset
    ).transform_aggregate(
        count = 'sum(count)',
        groupby = ["year", 'grouping_variable']
    ).mark_line().encode(
        alt.Y('count:Q', scale = alt.Scale(type = 'linear'), axis = alt.Axis(grid = False), title = '# Adverse events'),
        alt.X('year:Q', title = '', axis=alt.Axis(format='.0f')),
        alt.Color('grouping_variable:N', title = grouping_variable, scale=alt.Scale(scheme='dark2'))
    ).properties(title = f'Count of adverse events per {grouping_variable} by year')


# Add Brush
########################
brush = alt.selection_interval(encodings=['x'])

chart_1 = ae_total
chart_2 = ae_count

# add your code here
lower = chart_2.add_selection(
    brush
).transform_filter(
    brush
)
lower = lower.properties(
    height=170
)


# add your code here
upper = chart_1.add_selection(
    brush
)
upper = upper.properties(
    height=170
)


chart = upper & lower
st.altair_chart(chart, use_container_width = True)
