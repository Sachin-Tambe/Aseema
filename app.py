import streamlit as st
import pandas as pd

st.set_page_config(page_title="Class-wise Attendance Summary", layout="wide")
st.title("📊 Class-wise Attendance Summary")

uploaded_file = st.file_uploader("📁 Upload attendance file (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Read file and skip first 5 rows
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, skiprows=5)
        else:
            df = pd.read_excel(uploaded_file, skiprows=5)

        # Clean column names: strip spaces and lowercase
        df.columns = df.columns.str.strip()

        st.success("✅ File uploaded successfully. Showing cleaned data.")
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Check required columns
        required_cols = ["Class", "Gender", "Student Name"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            st.error(f"❌ Missing required columns: {', '.join(missing)}")
            st.stop()

        # Attendance columns
        present_col = "Present"
        absent_cols = [
            "Absent", "Half-Day", "Leave", "Not responding", "Family Issue",
            "Not well", "Not interested", "Not understanding content",
            "Dot not know", "Village", "Other"
        ]

        for col in [present_col] + absent_cols:
            if col not in df.columns:
                df[col] = 0  # Create column if missing

        # Replace NaNs in attendance columns
        df[[present_col] + absent_cols] = df[[present_col] + absent_cols].fillna(0)

        # Logic: Present vs Absent
        df["Is_Present"] = df[present_col]
        df["Is_Absent"] = df[absent_cols].sum(axis=1)

        # Group by Class and Gender
        summary = df.groupby(["Class", "Gender"]).agg(
            Total_Students=("Student Name", "count"),
            Total_Present=("Is_Present", "sum"),
            Total_Absent=("Is_Absent", "sum")
        ).reset_index()

        st.subheader("📈 Class-wise Summary (Male/Female)")
        st.dataframe(summary, use_container_width=True)

        # Optional Pivot View
        st.subheader("📊 Pivot Table (Class × Gender)")
        pivot = summary.pivot(index="Class", columns="Gender", values=["Total_Students", "Total_Present", "Total_Absent"]).fillna(0)
        st.dataframe(pivot, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
