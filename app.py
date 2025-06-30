import streamlit as st
import pandas as pd

st.set_page_config(page_title="Class-wise Attendance Summary", layout="wide")
st.title("📊 Class-wise Attendance Summary")

# Upload attendance file
uploaded_file = st.file_uploader("📁 Upload attendance file (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, skiprows=5)
        else:
            df = pd.read_excel(uploaded_file, skiprows=5)

        st.success("✅ File uploaded and cleaned (first 5 rows removed).")
        st.subheader("🔍 Preview of Cleaned Data")
        st.dataframe(df.head(), use_container_width=True)

        # Normalize column names (remove extra spaces, lowercase)
        df.columns = df.columns.str.strip()

        # Expected attendance columns
        present_col = "Present"
        absent_cols = [
            "Absent", "Half-Day", "Leave", "Not responding", "Family Issue",
            "Not well", "Not interested", "Not understanding content",
            "Dot not know", "Village", "Other"
        ]

        # Ensure all columns exist
        for col in [present_col] + absent_cols:
            if col not in df.columns:
                df[col] = 0

        # Fill NaNs with 0s in attendance columns
        df[[present_col] + absent_cols] = df[[present_col] + absent_cols].fillna(0)

        # Attendance logic
        df["Is_Present"] = df[present_col]
        df["Is_Absent"] = df[absent_cols].sum(axis=1)

        # Group summary by Class & Gender
        summary = df.groupby(["Class", "Gender"]).agg(
            Total_Students=("Student Name", "count"),
            Total_Present=("Is_Present", "sum"),
            Total_Absent=("Is_Absent", "sum")
        ).reset_index()

        st.subheader("📈 Class-wise Summary (Male/Female)")
        st.dataframe(summary, use_container_width=True)

        # Pivot summary
        st.subheader("📊 Pivot Summary (Class × Gender)")
        pivot = summary.pivot(index="Class", columns="Gender", values=["Total_Students", "Total_Present", "Total_Absent"]).fillna(0)
        st.dataframe(pivot, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
