import streamlit as st
import pandas as pd
import os

# Title of the app
st.title("College Explorer: AP Courses and Accepting Colleges")

# Create data directory if it doesn't exist (for development; in production, assume it's there)
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    st.warning(f"Created '{data_dir}' folder. Please place your CSV files there, e.g., 'college_list_export_AP_Psychology.csv'.")

# Dynamically discover AP courses from CSV files in the data folder
# Assumes files are named like "college_list_export_AP_[Subject].csv"
subjects = []
for filename in os.listdir(data_dir):
    if filename.startswith("College_list_export_AP_") and filename.endswith(".csv"):
        # Extract subject name (e.g., "Psychology" from "college_list_export_AP_Psychology.csv")
        subject = filename.replace("college_list_export_AP_", "").replace(".csv", "")
        subjects.append(subject)

if not subjects:
    st.error("No AP course CSV files found in the 'data' folder. Please add files like 'college_list_export_AP_Psychology.csv'.")
    st.stop()

# User selects an AP course
selected_subject = st.selectbox("Select an AP Course:", subjects)

# Load the corresponding CSV file
csv_filename = f"college_list_export_AP_{selected_subject}.csv"
file_path = os.path.join(data_dir, csv_filename)

if not os.path.exists(file_path):
    st.error(f"File '{csv_filename}' not found in '{data_dir}'.")
    st.stop()

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

df = load_data(file_path)

# Display the data with columns: Name of the college, City, State, Minimum Score Required
st.subheader(f"Colleges Accepting AP {selected_subject}")
st.write("This table shows colleges that accept AP {selected_subject}, along with their location and minimum score required.")

# Optional: Add filters for interactivity
col1, col2 = st.columns(2)
with col1:
    selected_state = st.multiselect("Filter by State:", options=df['State'].unique(), default=df['State'].unique())
with col2:
    min_score = st.slider("Minimum Score Filter (>=):", min_value=int(df['Minimum Score Required'].min()), 
                          max_value=int(df['Minimum Score Required'].max()), 
                          value=int(df['Minimum Score Required'].min()))

# Filter the dataframe
filtered_df = df[
    (df['State'].isin(selected_state)) & 
    (df['Minimum Score Required'] >= min_score)
]

# Display the filtered table
st.dataframe(filtered_df, use_container_width=True)

# Optional: Show summary stats
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Colleges", len(df))
col2.metric("Filtered Colleges", len(filtered_df))
col3.metric("Avg Min Score", f"{df['Minimum Score Required'].mean():.1f}")

# Instructions for adding more courses
with st.expander("How to Add More AP Courses"):
    st.markdown("""
    1. Place CSV files in the `data` folder with the naming pattern: `college_list_export_AP_[Subject].csv` (e.g., `college_list_export_AP_Calculus.csv`).
    2. Ensure columns are: `Name of the college`, `City`, `State`, `Minimum Score Required`.
    3. Refresh the app to see the new course in the dropdown.
    """)
