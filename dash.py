import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Aviation_Data.csv", encoding='latin1', low_memory=False)
    df['Event_Date'] = pd.to_datetime(df['Event_Date'], errors='coerce')
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
year_range = (int(df['Event_Date'].dt.year.min()), int(df['Event_Date'].dt.year.max()))
selected_year = st.sidebar.slider("Select Year", *year_range, year_range[1])
selected_aircraft = st.sidebar.selectbox("Select Aircraft Type", df['Aircraft_Category'].dropna().unique())

# Filtered Data
filtered_df = df[(df['Event_Date'].dt.year == selected_year) & (df['Aircraft_Category'] == selected_aircraft)]

# Dashboard Title
st.title("Aviation Accident Analysis Dashboard")

# Key Metrics
st.subheader("Key Statistics")
st.metric("Total Accidents", len(filtered_df))
st.metric("Total Fatal Injuries", filtered_df['Total_Fatal_Injuries'].sum())

# Visualizations
st.subheader("Accident Trends Over Time")
time_trend = df.groupby(df['Event_Date'].dt.year).size().reset_index(name='Accident Count')
fig1 = px.line(time_trend, x='Event_Date', y='Accident Count', title="Accidents Over Time")
st.plotly_chart(fig1)

st.subheader("Accidents by Aircraft Type")
aircraft_counts = df['Aircraft_Category'].value_counts().reset_index()
aircraft_counts.columns = ['Aircraft Category', 'Accident Count']
fig2 = px.bar(aircraft_counts, x='Aircraft Category', y='Accident Count', title="Accidents by Aircraft Type")
st.plotly_chart(fig2)

st.subheader("Accidents by Weather Condition")
weather_counts = df['Weather_Condition'].value_counts().reset_index()
weather_counts.columns = ['Weather Condition', 'Accident Count']
fig3 = px.pie(weather_counts, names='Weather Condition', values='Accident Count', title="Accidents by Weather Condition")
st.plotly_chart(fig3)

# Display Filtered Data
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)
