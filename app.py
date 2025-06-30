# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Rural Loan Approval Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("EA.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("🔍 Filters")
gender = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())
marital = st.sidebar.multiselect("Select Marital Status", df["Marital Status"].unique(), default=df["Marital Status"].unique())
education = st.sidebar.multiselect("Select Education Level", df["Education Level"].unique(), default=df["Education Level"].unique())

filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Marital Status"].isin(marital)) &
    (df["Education Level"].isin(education))
]

# Tabs
overview, demographics, finance, tech = st.tabs([
    "📊 Overview", "👨‍👩‍👧‍👦 Demographics", "💰 Financial Behavior", "📱 Technology Access"
])

# --- OVERVIEW TAB ---
with overview:
    st.header("📊 Overview of Rural Loan Applicants")
    st.markdown("A snapshot of total applications and their approval status.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applicants", len(filtered_df))
    col2.metric("Approved", (filtered_df["Loan Approval"] == "Yes").sum())
    col3.metric("Rejected", (filtered_df["Loan Approval"] == "No").sum())

    st.subheader("Loan Approval Outcome")
    st.markdown("This chart shows how many customers were approved or rejected.")
    fig = px.histogram(filtered_df, x="Loan Approval", color="Loan Approval", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# --- DEMOGRAPHICS TAB ---
with demographics:
    st.header("👨‍👩‍👧‍👦 Demographics Analysis")
    st.markdown("Analyzing how demographic variables affect loan approval outcomes.")

    st.subheader("Gender-wise Loan Approval")
    fig = px.histogram(filtered_df, x="Gender", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Marital Status and Loan Approval")
    fig = px.histogram(filtered_df, x="Marital Status", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Education Level Distribution")
    fig = px.histogram(filtered_df, x="Education Level", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age Distribution by Loan Status")
    fig = px.box(filtered_df, x="Loan Approval", y="Age", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

# --- FINANCIAL BEHAVIOR TAB ---
with finance:
    st.header("💰 Financial Behavior Insights")
    st.markdown("Income, expenses, and savings patterns affecting loan decisions.")

    st.subheader("Monthly Income vs Loan Approval")
    fig = px.box(filtered_df, x="Loan Approval", y="Monthly Income", color="Loan Approval", points="outliers")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Household Expense Distribution")
    fig = px.histogram(filtered_df, x="Monthly Household Expense", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Savings in Bank vs Loan Outcome")
    fig = px.box(filtered_df, x="Loan Approval", y="Savings in bank", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Loan Approval Process Time (days)")
    fig = px.box(filtered_df, x="Loan Approval", y="Loan Approval Process (days)", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

# --- TECHNOLOGY ACCESS TAB ---
with tech:
    st.header("📱 Access to Technology")
    st.markdown("Technology access might influence ease of documentation and approval speed.")

    st.subheader("Smartphone Ownership vs Loan Approval")
    fig = px.histogram(filtered_df, x="Have smartphone", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Internet Access vs Loan Approval")
    fig = px.histogram(filtered_df, x="Access to internet", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.caption("Built for Director - Business Development | Rural Lending Insights | © 2025")
