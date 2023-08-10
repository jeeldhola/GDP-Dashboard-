# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Load the world map (outside the main app loop)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Correct file path
file_path = 'Global Dataset of Inflation.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Drop unnecessary columns
data.drop(columns=[col for col in data.columns if 'Unnamed' in col], inplace=True)

# Streamlit App
st.title('Global Inflation Dashboard')
st.sidebar.header('Filters')

# Year Selector for Map
selected_year = st.sidebar.slider('Select a Year for Global Map:', min_value=1970, max_value=2022, value=2022)

# Global Inflation Map (place this where you want the map to appear)
st.header(f'Global Inflation Map for {selected_year}')
# Select the inflation data for the chosen year
inflation_data = data[['Country', str(selected_year)]].copy()
world_inflation = world.merge(inflation_data, left_on='name', right_on='Country')
fig, ax = plt.subplots(figsize=(12, 6))
world_inflation.plot(column=str(selected_year), cmap='OrRd', legend=True,
                     legend_kwds={'label': "Inflation Rate by Country"}, ax=ax)
plt.title(f'Global Inflation Rates in {selected_year}')
plt.axis('off')  # Turn off the axis
st.pyplot(fig)


# Country Selector For Inflation
selected_country = st.sidebar.selectbox('Select a Country:', data['Country'].unique(), key='country_selector')

# Series Selector (if different types of inflation series are available)
if 'Series Name' in data.columns:
    selected_series = st.sidebar.selectbox('Select an Inflation Series:', data['Series Name'].unique(), key='series_selector')
else:
    selected_series = 'Headline Consumer Price Inflation'  # Default series

# Select data for the chosen country and series
country_data = data[(data['Country'] == selected_country) & (data['Series Name'] == selected_series)]
headline_inflation_series = country_data.iloc[:, 4:-1].T

# Country Selector
# selected_country = st.sidebar.selectbox('Select a Country:', data['Country'].unique())

# Select data for the chosen country
country_data = data[data['Country'] == selected_country]
headline_inflation_series = country_data[country_data['Series Name'] == 'Headline Consumer Price Inflation'].iloc[:, 4:-1].T

# Reset the index
headline_inflation_series.reset_index(inplace=True)

# Drop the row with 'Series Name'
headline_inflation_series = headline_inflation_series[headline_inflation_series['index'] != 'Series Name']

# Rename the columns
headline_inflation_series.columns = ['Year', 'Inflation']

# Convert 'Year' to integers
headline_inflation_series['Year'] = headline_inflation_series['Year'].astype(int)

# Update the variable name
country_data = headline_inflation_series

# Year Range Slider
year_range = st.sidebar.slider('Select a Year Range:', min_value=1970, max_value=2022, value=(1970, 2022))
country_data = country_data[(country_data['Year'] >= year_range[0]) & (country_data['Year'] <= year_range[1])]



# Line Chart
st.header(f'{selected_country} Inflation Trend')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='Year', y='Inflation', data=country_data, ax=ax)
plt.title(f'{selected_country} Inflation Rate Over Time')
plt.ylabel('Inflation Rate (%)')
plt.xlabel('Year')
st.pyplot(fig)

# Histogram for Inflation Distribution
st.header(f'{selected_country} Inflation Distribution')
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(country_data['Inflation'], kde=True, ax=ax)
plt.title(f'{selected_country} Inflation Distribution')
plt.xlabel('Inflation Rate (%)')
st.pyplot(fig)

selected_countries = st.sidebar.multiselect('Select Countries for Comparison:', data['Country'].unique(), key='country_comparison')

# ...

# Comparative Analysis (place this where you want the comparative analysis to appear)
if selected_countries:
    st.header('Comparative Analysis of Inflation Trends')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for country in selected_countries:
        country_data = data[(data['Country'] == country) & (data['Series Name'] == selected_series)].iloc[:, 4:-1].T
        country_data.reset_index(inplace=True)
        country_data.columns = ['Year', 'Inflation']
        country_data['Year'] = country_data['Year'].astype(int)
        sns.lineplot(x='Year', y='Inflation', data=country_data, ax=ax, label=country)
    
    plt.title('Comparative Inflation Rate Over Time')
    plt.ylabel('Inflation Rate (%)')
    plt.xlabel('Year')
    plt.legend(title='Country')
    st.pyplot(fig)


# Summary Statistics
st.header(f'{selected_country} Summary Statistics')
st.write(country_data['Inflation'].describe())

# Data Table (Optional)
if st.checkbox('Show Raw Data'):
    st.dataframe(country_data)

# Additional components like global maps can be added as needed

st.markdown('Data Source: Global Dataset of Inflation')