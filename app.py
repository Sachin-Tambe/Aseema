import streamlit as st
import pandas as pd

st.set_page_config(page_title="Class-wise Attendance Summary", layout="wide")
st.title("📊 Class-wise Attendance Summary")

# Upload the attendance file
uploaded_file = st.file_uploader("📁 Upload attendance file (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Read the file while skipping the first 5 rows
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, skiprows=5)
        else:
            df = pd.read_excel(uploaded_file, skiprows=5)

        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()

        st.subheader("🔍 Cleaned Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Attendance columns considered as ABSENT
        absent_cols = [
            "Absent", "Half-Day", "Leave", "Not responding", "Family Issue",
            "Not well", "Not interested", "Not understanding content",
            "Dot not know", "Village", "Other"
        ]

        # Ensure all columns are present and numeric
        for col in absent_cols + ["Present"]:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Drop rows with missing essential data
        df.dropna(subset=["Class", "Gender", "Student Name"], inplace=True)

        # Normalize case
        df["Class"] = df["Class"].astype(str).str.strip()
        df["Gender"] = df["Gender"].str.strip().str.capitalize()

        # Calculate attendance counts
        df["Is_Present"] = df["Present"]
        df["Is_Absent"] = df[absent_cols].sum(axis=1)

        # Group by Class and Gender
        summary = df.groupby(["Class", "Gender"]).agg(
            Total_Students=("Student Name", "count"),
            Total_Present=("Is_Present", "sum"),
            Total_Absent=("Is_Absent", "sum")
        ).reset_index()

        # Show the summary
        st.subheader("📈 Class-wise Attendance Summary")
        st.dataframe(summary, use_container_width=True)

        # Pivot summary (optional)
        st.subheader("📊 Pivot Summary (Class x Gender)")
        pivot_table = summary.pivot(index="Class", columns="Gender", values=["Total_Students", "Total_Present", "Total_Absent"]).fillna(0)
        st.dataframe(pivot_table, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error while processing the file: {e}")
