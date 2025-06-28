import streamlit as st
import pandas as pd

st.set_page_config(page_title="Class-wise Attendance Summary", layout="wide")
st.title("📊 Class-wise Attendance Summary")

# Upload the attendance file
uploaded_file = st.file_uploader("📁 Upload attendance file (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    # Read the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Raw Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Absent columns
    absent_cols = [
        "Absent", "Half-Day", "Leave", "Not responding", "Family Issue",
        "Not well", "Not interested", "Not understanding content",
        "Dot not know", "Village", "Other"
    ]

    # Ensure missing columns are handled
    for col in absent_cols + ["Present"]:
        if col not in df.columns:
            df[col] = 0

    # Calculate Present and Absent totals per student
    df["Is_Present"] = df["Present"]
    df["Is_Absent"] = df[absent_cols].sum(axis=1)

    # Summary by Class and Gender
    summary = df.groupby(["Class", "Gender"]).agg(
        Total_Students=("Student Name", "count"),
        Total_Present=("Is_Present", "sum"),
        Total_Absent=("Is_Absent", "sum")
    ).reset_index()

    st.subheader("📈 Class-wise Attendance Summary")
    st.dataframe(summary, use_container_width=True)

    # Optional pivot view
    st.subheader("📊 Pivot Summary (Class x Gender)")
    pivot_table = summary.pivot(index="Class", columns="Gender", values=["Total_Students", "Total_Present", "Total_Absent"]).fillna(0)
    st.dataframe(pivot_table, use_container_width=True)
