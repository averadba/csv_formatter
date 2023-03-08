import pandas as pd
import streamlit as st
import base64

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

# function to clean the data
def clean_data(df):
    # replace accents and special characters in string columns
    for col in df.select_dtypes(include='object'):
        if df[col].dtype == "object":
            try:
                df[col] = df[col].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            except AttributeError:
                pass
    return df

# function to rename columns
def rename_columns(df, old_names, new_names):
    # create a dictionary with old and new column names
    rename_dict = {old: new for old, new in zip(old_names, new_names)}
    # rename the columns using the dictionary
    df = df.rename(columns=rename_dict)
    return df

# set the app title
st.title("CSV File Formatter")

st.write("*By:* A. Vera" )

st.write("This app allows you to upload a CSV file containing tabular data, select the columns you would like to rename, and clean the data from any special characters like accents. Once you have made your selections, click the \"Reformat your file\" button to see the reformatted data and download the new CSV file. Note that the column names must be unique after renaming, and the file size cannot exceed 200MB.")

# display a message to wait for file upload
st.write("Waiting for file upload...")

# create a file uploader
file = st.file_uploader("Choose a CSV file", type="csv")

if file is not None:
    # read the file as a dataframe
    df = pd.read_csv(file)

    # display the original data
    st.write("Original Data:")
    st.write(df)

    # select the columns to rename
    old_names = st.multiselect("Select the columns to rename", list(df.columns))

    if old_names:
        # get the new names for the selected columns
        new_names = []
        for old in old_names:
            new = st.text_input(f"New name for column '{old}'")
            new_names.append(new)

        # display the new names
        st.write("New column names:")
        for old, new in zip(old_names, new_names):
            st.write(f"{old} -> {new}")

        # display a button to reformat the data
        if st.button("Reformat your file"):
            # rename the selected columns
            df = rename_columns(df, old_names, new_names)

            # clean the data
            df = clean_data(df)

            # display the reformatted data
            st.write("Reformatted Data:")
            st.write(df)

            # create a download link for the reformatted data
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="formatted_data.csv">Download the reformatted data</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        # display a button to reformat the data
        if st.button("Reformat your file"):
            # clean the data
            df = clean_data(df)

            # display the reformatted data
            st.write("Reformatted Data:")
            st.write(df)

            # create a download link
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="formatted_data.csv">Download the reformatted data</a>'
            st.markdown(href, unsafe_allow_html=True)

