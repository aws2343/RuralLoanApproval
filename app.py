# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Page setup
st.set_page_config(page_title="Rural Loan Approval Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Rural Indonesia Loan Approval.csv")
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
overview, demographics, finance, tech, correlation = st.tabs([
    "📊 Overview", "👨‍👩‍👧‍👦 Demographics", "💰 Financial Behavior", "📱 Technology Access", "🔗 Correlation Analysis"
])

# --- OVERVIEW TAB ---
with overview:
    st.header("📊 Overview of Rural Loan Applicants")
    st.markdown("This section gives an executive-level summary of key metrics, helping stakeholders quickly grasp the scale and approval dynamics of rural loan applications.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applicants", len(filtered_df))
    col2.metric("Approved", (filtered_df["Loan Approval"] == "Yes").sum())
    col3.metric("Rejected", (filtered_df["Loan Approval"] == "No").sum())

    st.subheader("Loan Approval Outcome")
    st.markdown("Shows the breakdown of approved and rejected loan applications.")
    fig = px.histogram(filtered_df, x="Loan Approval", color="Loan Approval", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# --- DEMOGRAPHICS TAB ---
with demographics:
    st.header("👨‍👩‍👧‍👦 Demographics Analysis")
    st.markdown("This section allows stakeholders to identify patterns in approval decisions across different demographic groups.")

    st.subheader("Gender-wise Loan Approval")
    st.markdown("Understand gender-based differences in loan approvals.")
    fig = px.histogram(filtered_df, x="Gender", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Marital Status and Loan Approval")
    st.markdown("Explore how marital status may influence loan decisions.")
    fig = px.histogram(filtered_df, x="Marital Status", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Education Level Distribution")
    st.markdown("Analyze the educational background of applicants by approval outcome.")
    fig = px.histogram(filtered_df, x="Education Level", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age Distribution by Loan Status")
    st.markdown("View how age affects approval outcomes.")
    fig = px.box(filtered_df, x="Loan Approval", y="Age", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

# --- FINANCIAL BEHAVIOR TAB ---
with finance:
    st.header("💰 Financial Behavior Insights")
    st.markdown("Stakeholders can evaluate how applicants’ financial profiles impact loan decisions.")

    st.subheader("Monthly Income vs Loan Approval")
    st.markdown("Compare income levels between approved and rejected applicants.")
    fig = px.box(filtered_df, x="Loan Approval", y="Monthly Income", color="Loan Approval", points="outliers")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Household Expense Distribution")
    st.markdown("Understand spending behavior relative to loan decisions.")
    fig = px.histogram(filtered_df, x="Monthly Household Expense", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Savings in Bank vs Loan Outcome")
    st.markdown("Higher savings may increase approval chances. This chart explores that relation.")
    fig = px.box(filtered_df, x="Loan Approval", y="Savings in bank", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Loan Approval Process Time (days)")
    st.markdown("Check if quicker processing correlates with approvals.")
    fig = px.box(filtered_df, x="Loan Approval", y="Loan Approval Process (days)", color="Loan Approval")
    st.plotly_chart(fig, use_container_width=True)

# --- TECHNOLOGY ACCESS TAB ---
with tech:
    st.header("📱 Access to Technology")
    st.markdown("Stakeholders can assess whether digital access affects loan approval likelihood.")

    st.subheader("Smartphone Ownership vs Loan Approval")
    st.markdown("Evaluate the impact of smartphone access on approvals.")
    fig = px.histogram(filtered_df, x="Have smartphone", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Internet Access vs Loan Approval")
    st.markdown("Internet access may be an enabler of better documentation and credit scoring.")
    fig = px.histogram(filtered_df, x="Access to internet", color="Loan Approval", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# --- CORRELATION TAB ---
with correlation:
    st.header("🔗 Correlation Matrix")
    st.markdown("This heatmap reveals which financial and demographic variables are most associated with one another. Useful for identifying hidden patterns.")

    numeric_df = filtered_df.select_dtypes(include=[np.number]).dropna()
    corr_matrix = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Footer
st.caption("📌 Built for Director - Business Development | Insight-Driven Loan Decisions | © 2025")
