import streamlit as st
import pandas as pd
import os
import re

# Title of the app
st.title("College Explorer: AP Courses and Accepting Colleges")

# Define the data directory
data_dir = "data"

# Check if data directory exists
if not os.path.exists(data_dir):
    st.error(f"The '{data_dir}' folder does not exist. Please create it in the same directory as this app and add your CSV files (e.g., 'College_list_export_AP Psychology.csv').")
    st.stop()

# Dynamically discover AP courses from CSV files in the data folder
subjects = []
for filename in os.listdir(data_dir):
    # Match files starting with 'College_list_export_AP ' and ending with '.csv'
    if filename.startswith("College_list_export_AP ") and filename.endswith(".csv"):
        # Extract subject name using regex to handle spaces and special characters
        match = re.match(r"College_list_export_AP (.*)\.csv$", filename)
        if match:
            subject = match.group(1)  # Extract the subject part (e.g., "Psychology", "Physics 2")
            subjects.append(subject)
        else:
            st.warning(f"File '{filename}' matches the pattern but could not extract subject name.")

if not subjects:
    st.error("No valid AP course CSV files found in the 'data' folder. Please ensure files are named like 'College_list_export_AP Psychology.csv' and are located in the 'data' folder.")
    st.write("**Expected file format:** Files must start with 'College_list_export_AP ' and end with '.csv'.")
    st.write("**Example:** 'College_list_export_AP Psychology.csv'")
    st.stop()

# User selects an AP course
selected_subject = st.selectbox("Select an AP Course:", sorted(subjects))

# Load the corresponding CSV file with explicit data folder prefix
csv_filename = f"College_list_export_AP {selected_subject}.csv"
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
        required_columns = ["Name of College", "City", "State", "Minimum Score Required"]
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

# Add filters for interactivity
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

# Show summary stats based on filtered data
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Colleges", len(df))
with col2:
    st.metric("Filtered Colleges", len(filtered_df))
with col3:
    st.metric("Avg Min Score", f"{filtered_df['Minimum Score Required'].mean():.1f}" if not filtered_df.empty else "N/A")
