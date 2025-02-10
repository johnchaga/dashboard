import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Aviation Accident Analysis", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Aviation_Data.csv", low_memory=False)
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")
selected_year_range = st.sidebar.slider("Select Year Range", 1950, 2023, (1980, 2023))

# Convert 'Event_Date' to datetime
df["Event_Date"] = pd.to_datetime(df["Event_Date"], errors="coerce")
df = df.dropna(subset=["Event_Date"])
df["Year"] = df["Event_Date"].dt.year

# Filter data by selected years
df_filtered = df[(df["Year"] >= selected_year_range[0]) & (df["Year"] <= selected_year_range[1])]

# ---- TITLE ----
st.title("✈️ Aviation Accident Analysis Dashboard")
st.markdown("Analyze aviation accident trends, aircraft risks, and safety improvements.")

# ---- SECTION 1: Accident Trends Over Time ----
st.subheader("📊 Aviation Accident Trends Over Time")

accidents_over_time = df_filtered.groupby("Year").size()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(accidents_over_time.index, accidents_over_time.values, marker='o', color='b', linestyle='-')
ax.set_title("Aviation Accident Trends Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Accidents")
ax.grid(True)
st.pyplot(fig)

# ---- SECTION 2: Top 10 Aircraft Models with Most Accidents ----
st.subheader("✈️ Top 10 Aircraft Models with Most Accidents")

if "Aircraft_Model" in df_filtered.columns:
    top_models = df_filtered["Aircraft_Model"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_models.index, y=top_models.values, ax=ax, palette="Blues_r")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_title("Top 10 Aircraft Models with Most Accidents")
    ax.set_xlabel("Aircraft Model")
    ax.set_ylabel("Number of Accidents")
    st.pyplot(fig)
else:
    st.warning("Aircraft Model data is missing.")

# ---- SECTION 3: Weather Conditions vs. Aircraft Damage ----
st.subheader("🌦️ Impact of Weather Conditions on Aircraft Damage")

if "Weather_Condition" in df_filtered.columns and "Aircraft_Damage" in df_filtered.columns:
    weather_damage = df_filtered.groupby(["Weather_Condition", "Aircraft_Damage"]).size().unstack()

    fig, ax = plt.subplots(figsize=(10, 5))
    weather_damage.plot(kind="bar", stacked=True, ax=ax, colormap="coolwarm")
    ax.set_title("Impact of Weather Conditions on Aircraft Damage")
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Number of Accidents")
    st.pyplot(fig)
else:
    st.warning("Weather Condition or Aircraft Damage data is missing.")

# ---- SECTION 4: Business Insights & Recommendations ----
st.subheader("💡 Business Recommendations")

st.markdown("""
### **1. Aircraft Model Selection** 🚀
- Avoid high-risk aircraft like **Cessna 152 and 172** due to high accident counts.
- Prioritize **safer aircraft models** with better safety records.
- Implement **stricter maintenance & training** for high-risk models.

### **2. Weather-Related Safety Improvements** 🌦️
- Strengthen **pilot training** for IMC (poor visibility) conditions.
- Invest in **advanced avionics & weather radar** to reduce risk.
- Implement stricter **operational policies** for bad weather flights.

### **3. Operational Risk Management** ⚠️
- Focus on improving **takeoff & landing safety** (most accidents happen here).
- Enhance **maintenance & predictive analytics** to prevent failures.
- Review & improve **regulations for safety compliance**.
""")

# ---- Data Table ----
st.subheader("📜 Raw Data Preview")
st.dataframe(df_filtered.head(50))
