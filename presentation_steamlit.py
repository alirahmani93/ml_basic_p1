import folium
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
from folium import plugins
from streamlit_folium import folium_static
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from streamlit_option_menu import option_menu

import utils

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title(' _KingCounty Food_ :red[Inspection]')
st.markdown(':female-detective: :eyes: :male-detective: :hamburger: ')
st.divider()


@st.cache_data
def main_df():
    return pd.read_csv('../../../../../Downloads/Datasets/Food_Establishment_Inspection_Data.csv')


# df = utils.import_reports(filename='lat_lon_inspection_result_size', file_type='csv')
df = pd.read_csv('~/Downloads/Datasets/Food_Establishment_Inspection_Data.csv')
df.dropna(inplace=True)


# with st.container() as map_chart:
#     st.divider()
#     st.header('Map Chart')
#     df = pd.DataFrame({
#         "col1": df['Latitude'],
#         "col2": df['Longitude'],
#         "col3": df['Inspection Result'],
#         "col4": np.random.rand(94087, 4).tolist(),
#     })
#     st.map(df,
#            latitude='col1',
#            longitude='col2',
#            size='col3',
#            color='col4',
#            # zoom=5
#            )


@st.cache_data
def load_data(filename: str):
    return utils.import_reports(filename=filename, file_type='csv')


df_clean = load_data(filename='cleaned_data')
df = load_data(filename='lat_lon_inspection_result_size')

# Menu
with st.sidebar:
    def on_change(key):
        selection = st.session_state[key]
        st.write(f"Selection changed to {selection}")


    selected5 = option_menu(None, ["Home", ],
                            icons=['house', ],
                            on_change=on_change, key='menu_5', orientation="vertical",
                            menu_icon="cast", default_index=0,
                            styles={
                                "container": {"padding": "0!important", "background-color": "#fafafa"},
                                "icon": {"color": "orange", "font-size": "25px"},
                                "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                             "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "green"},
                            })

st.sidebar.header('User Input Features')
sector = df.groupby('_size')

###########
size_sorted_sector_unique = sorted(df['_size'].unique())
selected_sector = st.sidebar.multiselect('Sector', size_sorted_sector_unique, max_selections=5)

st.header('Population')
if st.button("Show Population"):
    with st.container():
        # st.dataframe(df_closed_score)
        # st.pyplot(df_closed_score.plot.bar('grade', 'inspection_closed_business').plot())
        # st.divider()
        # st.dataframe(df_mean_score)
        # st.pyplot(df_mean_score.plot.bar('inspection_closed_business', 'inspection_score').plot())
        st.image('./img/The Population Density.png')
        # st.image('./img/The Ratio of Inspection Frequency to Restuarant Number.png')
    if st.button("Close Population"):
        st.expander()
st.divider()

with st.container():
    st.header('Data Cleaning and Data Wrangling')
    st.markdown(
        '* Fix Lat and Long \n * Fill or remove null Values \n * Remove Useless Column for our Story like: '
        '( program_identifier, inspection_business_name, inspection_serial_num, violation_record_id,'
        ' business_id, phone_number)\n * Recalculate inspection score column by violation point \n '
        '* Modify the values of the cells in column violation description '  # @TODO: remove outside cities
        # Excluding cities outside the King County area
    )
st.divider()

# st.header('Display DataFrame')
# if st.button("Show DataFrame"):
#     with st.container():
#
#         # Filtering data
#         df_selected_sector = df[(df['_size'].isin(selected_sector))]
#         st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(
#             df_selected_sector.shape[1]) + ' columns.')
#         st.dataframe(df_selected_sector)
#     # st.map(data=df, latitude='latitude', longitude='longitude', size='_size',)
#     if st.button("Close", key='a'):
#         st.expander()
# st.divider()

# num_company = st.sidebar.slider('Number of grade', 1, 4)

# WeekDay
st.header('Time Interval Assessments')
if st.button("Show Intervals"):
    with st.container():
        weekday_df: pd.DataFrame = load_data('weekday')
        # st.dataframe(weekday_df)
        weekday_df_plot = weekday_df.plot.bar(
            x='weekday', y='count_weekday', legend=False,
            title='Inspection Weekday Count', color='red')

        st.pyplot(weekday_df_plot.plot())
        st.image('./img/Seasons_Inspection Number.png')
        st.image('./img/Inspection Number per Month.png')
        st.image('./img/Inspection Score Average per Month.png')
        st.image('./img/Impact of Covid-19 Pandemic on Handwashing Violation.png')

    if st.button("Close Intervals", key='a'):
        st.expander()
st.divider()

# Map
# grade_size_sorted_sector_unique = sorted(df_clean['grade'].unique())
# grade_selected_sector = st.sidebar.multiselect('Grade Sector', grade_size_sorted_sector_unique,
#                                                grade_size_sorted_sector_unique)
# st.header('Map')
# if st.button("Show Map"):
#     custom_grade = df_clean[df_clean.grade.isin(grade_selected_sector)]
#     z = custom_grade.dropna()
#
#     with st.container():
#         st.map(z,
#                latitude=z['latitude'], longitude=z['longitude'], color=z['grade'].tolist(),
#                size=z['grade']
#                )
#
#     if st.button("Close Closed Restaurant"):
#         st.expander()
#
# with st.container() as map_chart:
#     zz = pd.DataFrame({
#         "col1": z.latitude[:10],
#         "col2": z.longitude[:10],
#         "col3": z.inspection_result[:10],
#         "col4": np.random.rand(10, 4).tolist(),
#     })
#     st.map(zz,
#            latitude='col1',
#            longitude='col2',
#            size='col3',
#            color='col4',
#            # zoom=5
#            )
# if st.button("Close Closed Restaurant"):
#     st.expander()

grade_size_sorted_sector_unique = sorted(df_clean['grade'].unique())
grade_size_sorted_sector_unique.pop(2)
grade_selected_sector = st.sidebar.multiselect('Grade Sector', grade_size_sorted_sector_unique,
                                               grade_size_sorted_sector_unique)
st.header('Closed Restaurant')
if st.button("Show Closed Restaurant"):
    with st.container():
        custom_grade = df_clean[df_clean.grade.isin(grade_selected_sector)]
        p = sns.barplot(x=custom_grade['inspection_closed_business'], y=custom_grade['inspection_score'],
                        hue=custom_grade['grade'])
        st.pyplot(p.plot())
        st.image('./img/Average Inspection Score_grade.png')
        st.image('./img/Inspection Closed Business_Grade Average.png')
        st.image('./img/Inspection Closed Business_Inspection Score Average.png')
        # st.image('./img/map_number_close.png')
        # st.image('./img/The closed business number density.png')
        st.image('./img/The Ratio of Insp freq to restaurant number.jpg')

    insp_vio_freq_df: pd.DataFrame = load_data('insp_vio_freq')
    insp_vio_freq_sector_unique = insp_vio_freq_df.sort_values('violation_frequency', ascending=False)[
        'violation_description']
    insp_vio_freq_sector = st.sidebar.multiselect(
        'Violation Sector', insp_vio_freq_sector_unique, insp_vio_freq_sector_unique[:10])
    with st.container():
        custom_city = insp_vio_freq_df[insp_vio_freq_df.violation_description.isin(insp_vio_freq_sector)]
        city_count_df_plot = custom_city.plot.bar(
            x='code', y='violation_frequency', legend=False,
            title='Inspection Violation Descriptions', color='purple', rot=45)

        st.pyplot(city_count_df_plot.plot())
        st.dataframe(custom_city)
    if st.button("Close Closed Restaurant"):
        st.expander()
st.divider()

# st.header('Covid Affect')
# if st.button("Show Covid Affect"):
#     with st.container():
#         # st.image('./ShadiPlots/after Covid-19 pandemic (Seating Type).jpg')
#         # st.image('./ShadiPlots/after Covid-19 pandemic (Without Seating Type).jpg')
#         # st.image('./ShadiPlots/before Covid-19 pandemic (Seating Type).jpg')
#         # st.image('./ShadiPlots/before Covid-19 pandemic (Without Seating Type).jpg')
#     if st.button("Close Covid Affect"):
#         st.expander()
# st.divider()
