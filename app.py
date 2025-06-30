import streamlit as st
import pandas as pd

st.set_page_config(page_title="Class-wise Attendance Summary", layout="wide")
st.title("📊 Class-wise Attendance Summary")

# Upload the attendance file
uploaded_file = st.file_uploader("📁 Upload attendance file (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, skiprows=5)
        else:
            df = pd.read_excel(uploaded_file, skiprows=5)

        # Show preview
        st.subheader("🔍 Raw Data Preview (after skipping first 5 rows)")
        st.dataframe(df.head(), use_container_width=True)

        # Check required columns
        required_cols = ["Student Name", "Class", "Gender", "Present"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
        else:
            # Absent-related columns
            absent_cols = [
                "Absent", "Half-Day", "Leave", "Not responding", "Family Issue",
                "Not well", "Not interested", "Not understanding content",
                "Dot not know", "Village", "Other"
            ]

            # Ensure all attendance columns exist and are numeric
            for col in absent_cols + ["Present"]:
                if col not in df.columns:
                    df[col] = 0
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            # Calculate Present and Absent values
            df["Is_Present"] = df["Present"]
            df["Is_Absent"] = df[absent_cols].sum(axis=1)

            # Group by Class and Gender
            summary = df.groupby(["Class", "Gender"]).agg(
                Total_Students=("Student Name", "count"),
                Total_Present=("Is_Present", "sum"),
                Total_Absent=("Is_Absent", "sum")
            ).reset_index()

            # Show summary table
            st.subheader("📈 Class-wise Attendance Summary")
            st.dataframe(summary, use_container_width=True)

            # Show pivot summary
            st.subheader("📊 Pivot Summary (Class x Gender)")
            pivot_table = summary.pivot(index="Class", columns="Gender", values=["Total_Students", "Total_Present", "Total_Absent"]).fillna(0)
            st.dataframe(pivot_table, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
