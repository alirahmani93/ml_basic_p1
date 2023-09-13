import numpy as np
import pandas as pd
import streamlit as st

df = pd.read_csv('~/Downloads/Datasets/Food_Establishment_Inspection_Data.csv')
df.dropna(inplace=True)
with st.container() as map_chart:
    st.divider()
    st.header('Map Chart')
    df = pd.DataFrame({
        "col1": df.Latitude,
        "col2": df.Longitude,
        "col3": df.Grade,
        "col4": np.random.rand(94087, 4).tolist(),
    })
    st.map(df,
           latitude='col1',
           longitude='col2',
           size='col3',
           color='col4',
           # zoom=5
           )
