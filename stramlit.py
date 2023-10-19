import folium
import numpy as np
import pandas as pd
import streamlit as st
from folium import plugins
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from streamlit_option_menu import option_menu

import utils

df = utils.import_reports(filename='lat_lon_inspection_result_size', file_type='csv')
# df = pd.read_csv('~/Downloads/Datasets/Food_Establishment_Inspection_Data.csv')
# df.dropna(inplace=True)
# with st.container() as map_chart:
#     st.divider()
#     st.header('Map Chart')
#     df = pd.DataFrame({
#         "col1": df.latitude_bin,
#         "col2": df.longitude_bin,
#         "col3": df.inspection_result,
#         "col4": np.random.rand(1152, 4).tolist(),
#     })
#     st.map(df,
#            latitude='col1',
#            longitude='col2',
#            size='col3',
#            color='col4',
#            # zoom=5
#            )

st.dataframe(df)

# Convert latitude_bin to numerical values
df['latitude'] = df['latitude_bin'].str.extract(r'\((.*),.*\]').astype(float)
# print (df['latitude'])
df['longitude'] = df['longitude_bin'].str.extract(r'\((.*),.*\]').astype(float)

# Create a base map centered on a specific location
map_center = [(df['latitude'].mean()), (df['longitude'].mean())]
m = folium.Map(location=map_center, zoom_start=12)

# Iterate over the DataFrame and add circles to the map
for index, row in df.iterrows():
    lat = row['latitude']
    lon = (row['longitude'] + row['longitude']) / 2
    radius = abs(row['latitude'] - row['latitude']) * 111000

    result = row['inspection_result']
    size = row['_size']

    tooltip = f"Result: {result}, Size: {size}"
    folium.Circle(
        location=[lat, lon],
        radius=radius,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.4,
        popup=tooltip
    ).add_to(m)
#
# # Create a list of latitudes, longitudes, and sizes
# latitudes = df['latitude'].tolist()
# # longitudes = [print(row['longitude_bin']) for index, row in df.iterrows()]
# longitudes = df['longitude'].tolist()
# sizes = df['_size'].tolist()
# # (float(row['longitude_bin'][0])   + float(row['longitude_bin'][1])) / 2
# # Determine the maximum size for scaling the color gradients
# max_size = max(sizes)
#
# # Create a HeatMap with the frequencies and color gradients
# heat_data = [[lat, lon, size] for lat, lon, size in zip(latitudes, longitudes, sizes)]
#
# heat_map = plugins.HeatMap(heat_data, radius=25, blur=10, gradient={
#     0.2: 'blue',
#     0.4: 'green',
#     0.6: 'yellow',
#     1.0: 'red'
# }, max_val=max_size)
# m.add_child(heat_map)
#
# # Display the map using Streamlit
# st.markdown('<h1>Map Visualization</h1>', unsafe_allow_html=True)
# folium_static(m)


################################################################
#
data1 = [
    {'latitude_bin': '(47.821, 47.921]', "longitude_bin": "(-121.859, -121.759]",
     "inspection_result": 'Needs Assessment',
     '_size': 3},
    {'latitude_bin': '(47.821, 47.921]', "longitude_bin": "(-121.859, -121.759]",
     "inspection_result": 'No Longer At Location', '_size': 8},
]

df1 = pd.DataFrame(data1)

# Convert latitude_bin to numerical values
df1['latitude'] = df1['latitude_bin'].str.extract(r'\((.*),.*\]').astype(float)

# Extract longitude values from the string representation
df1['longitude'] = df1['longitude_bin'].str.extract(r'\((.*),.*\]').astype(float)

# Define the second dataset as a DataFrame
data2 = [
    {'latitude_bin': '(47.811, 47.911]', "longitude_bin": "(-121.849, -121.749]",
     "inspection_result": 'New Data',
     '_size': 5},
    {'latitude_bin': '(47.831, 47.931]', "longitude_bin": "(-121.869, -121.769]",
     "inspection_result": 'New Data',
     '_size': 2},
]

df2 = pd.DataFrame(data2)

# Convert latitude_bin to numerical values
df2['latitude'] = df2['latitude_bin'].str.extract(r'\((.*),.*\]').astype(float)

# Extract longitude values from the string representation
df2['longitude'] = df2['longitude_bin'].str.extract(r'\((.*),.*\]').astype(float)

# Create a base map centered on a specific location
map_center = [(df1['latitude'].mean() + df2['latitude'].mean()) / 2,
              (df1['longitude'].mean() + df2['longitude'].mean()) / 2]
m = folium.Map(location=map_center, zoom_start=12)

# # Iterate over the first DataFrame and add circles to the map
for index, row in df1.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    size = row['_size']

    result = row['inspection_result']
    print(result)
    tooltip = f"Result: {result}, Size: {size},latitude: {lat}, longitude: {lon}"
    folium.Circle(
        location=[lat, lon],
        radius=size * 1000,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.4,
        popup=tooltip
    ).add_to(m)

# Iterate over the second DataFrame and add circles to the map
for index, row in df2.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    size = row['_size']

    result = row['inspection_result']

    tooltip = f"Result: {result}, Size: {size}"
    folium.Circle(
        location=[lat, lon],
        radius=size * 1000,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.4,
        popup=tooltip
    ).add_to(m)

# Display the map using Streamlit
st.markdown('<h1>Map Visualization</h1>', unsafe_allow_html=True)
folium_static(m)

# with st.sidebar:
#     selected = option_menu("Main Menu", ["About", 'Data'],
#                            icons=['house', 'gear'], menu_icon="cast", default_index=1)
#     selected


# 2. horizontal menu
with st.sidebar:
    # selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
    #                         icons=['house', 'cloud-upload', "list-task", 'gear'],
    #                         menu_icon="cast", default_index=0, orientation="horizontal")
    # selected2

    # 3. CSS style definitions
    # selected3 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
    #                         icons=['house', 'cloud-upload', "list-task", 'gear'],
    #                         menu_icon="cast", default_index=0, orientation="horizontal",
    #                         styles={
    #                             "container": {"padding": "0!important", "background-color": "#fafafa"},
    #                             "icon": {"color": "orange", "font-size": "25px"},
    #                             "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
    #                                          "--hover-color": "#eee"},
    #                             "nav-link-selected": {"background-color": "green"},
    #                         }
    #                         )
    # selected3
    # 4. Manual Item Selection
    # if st.session_state.get('switch_button', False):
    #     st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
    #     manual_select = st.session_state['menu_option']
    # else:
    #     manual_select = None
    #
    # selected4 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
    #                         icons=['house', 'cloud-upload', "list-task", 'gear'],
    #                         orientation="horizontal", manual_select=manual_select, key='menu_4')
    # st.button(f"Move to Next {st.session_state.get('menu_option', 1)}", key='switch_button')
    # selected4


    # 5. Add on_change callback
    def on_change(key):
        selection = st.session_state[key]
        st.write(f"Selection changed to {selection}")


    selected5 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
                            icons=['house', 'cloud-upload', "list-task", 'gear'],
                            on_change=on_change, key='menu_5', orientation="vertical")
    selected5


# Define the dataset
# data = pd.DataFrame({
#     "latitude": [121.1, 121.2, 121.3, 121.4],
#     "longitude": [43, 43.1, 43.2, 43.3],
#     "A": [1, 2, 3, 2],
#     "City": ["a", "a", "c", "d"],
#     "Exam": [1.1, 1.2, 1.1, 2.3],
#     "F_T": [True, False, False, True],
# })
#
# # Create GeoDataFrame from the dataset
# gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude))
#
# # Define the grid size (25 km)
# grid_size = 25000  # meters
#
# # Create the grid polygons
# minx, miny, maxx, maxy = gdf.total_bounds
# x_grid = list(range(int(minx), int(maxx) + grid_size, grid_size))
# y_grid = list(range(int(miny), int(maxy) + grid_size, grid_size))
# polygons = []
# for x in range(len(x_grid) - 1):
#     for y in range(len(y_grid) - 1):
#         polygons.append(Polygon([(x_grid[x], y_grid[y]),
#                                 (x_grid[x + 1], y_grid[y]),
#                                 (x_grid[x + 1], y_grid[y + 1]),
#                                 (x_grid[x], y_grid[y + 1])]))
#
# # Create a GeoDataFrame for the grid
# grid_gdf = gpd.GeoDataFrame(geometry=polygons)
#
# # Perform group-by and aggregate operations
# grouped = gdf.groupby('City').agg({'A': 'sum', 'Exam': 'mean', 'F_T': 'sum'})
#
# # Merge the grid GeoDataFrame with the aggregated data
# merged = gpd.sjoin(grid_gdf, gdf, how='left', op='intersects')
#
# # Plot the square mosaic map
# fig, ax = plt.subplots(figsize=(8, 8))
# merged.plot(column='A', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
# ax.set_axis_off()
# plt.title('Square Mosaic Map')
# plt.show()
