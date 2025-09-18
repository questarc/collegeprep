import streamlit as st
import pandas as pd
import os

# Title of the app
st.title("College Explorer: AP Courses and Accepting Colleges")

# Define the data directory
data_dir = "data"

# Check if data directory exists
if not os.path.exists(data_dir):
    st.error(f"The '{data_dir}' folder does not exist. Please create it in the same directory as this app and add your CSV files (e.g., 'college_list_export_AP_Psychology.csv').")
    st.stop()

# List all files in the data directory for debugging
all_files = os.listdir(data_dir)
st.write("**Files found in 'data' folder for debugging:**")
if all_files:
    st.write(all_files)
else:
    st.warning(f"No files found in '{data_dir}' folder.")

# Dynamically discover AP courses from CSV files in the data folder
subjects = []
for filename in all_files:
    if filename.startswith("College_list_export_AP_") and filename.endswith(".csv"):
        # Extract subject name (e.g., "Psychology" from "college_list_export_AP_Psychology.csv")
        subject = filename.replace("College_list_export_AP_", "").replace(".csv", "")
        subjects.append(subject)

if not subjects:
    st.error("No AP course CSV files found in the 'data' folder. Please ensure files are named like 'college_list_export_AP_Psychology.csv' and are located in the 'data' folder.")
    st.write("**Expected file format:** Files must start with 'college_list_export_AP_' and end with '.csv'.")
    st.write("**Example:** 'college_list_export_AP_Psychology.csv'")
    st.stop()

# User selects an AP course
selected_subject = st.selectbox("Select an AP Course:", subjects)

# Load the corresponding CSV file
csv_filename = f"College_list_export_AP_{selected_subject}.csv"
file_path = os.path.join(data_dir, csv_filename)

# Verify file existence
if not os.path.exists(file_path):
    st.error(f"File '{csv_filename}' not found in '{data_dir}'. Please check the file name and path.")
    st.stop()

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Verify required columns
        required_columns = ["Name of the college", "City", "State", "Minimum Score Required"]
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            st.error(f"CSV file '{file_path}' is missing required columns: {missing}")
            st.stop()
        return df
    except Exception as e:
        st.error(f"Error reading CSV file '{file_path}': {str(e)}")
        st.stop()

df = load_data(file_path)

# Display the data
st.subheader(f"Colleges Accepting AP {selected_subject}")
st.write(f"This table shows colleges that accept AP {selected_subject}, along with their location and minimum score required.")

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
    2
