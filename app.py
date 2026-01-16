# app.py
# Task 5: Interactive Business Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(
    page_title="Superstore Business Dashboard",
    layout="wide"
)

st.title("Superstore Sales & Profit Dashboard")

# Load Dataset
@st.cache_data
def load_data():
    df = df = pd.read_csv(r"D:\Internship 2\superstore.csv")
    # Clean column names: remove spaces, replace dots with underscores
    df.columns = df.columns.str.strip().str.replace('.', '_', regex=False)
    return df

df = load_data()

# Data Cleaning
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
df = df.dropna(subset=['Sales', 'Profit'])

# Sidebar Filters
st.sidebar.header("Filter Options")

region = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df['Sub_Category'].unique(),
    default=df['Sub_Category'].unique()
)

# Apply Filters
filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['Sub_Category'].isin(sub_category))
]

# KPI Metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")

# Sales by Category
st.subheader("Total Sales by Category")
fig, ax = plt.subplots()
sns.barplot(
    x='Category',
    y='Sales',
    data=filtered_df,
    estimator=sum,
    ax=ax
)
st.pyplot(fig)

# Profit by Region
st.subheader("Total Profit by Region")
fig, ax = plt.subplots()
sns.barplot(
    x='Region',
    y='Profit',
    data=filtered_df,
    estimator=sum,
    ax=ax
)
st.pyplot(fig)

# Top 5 Customers by Sales
st.subheader("Top 5 Customers by Sales")
top_customers = (
    filtered_df
    .groupby('Customer_Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)
st.table(top_customers)
