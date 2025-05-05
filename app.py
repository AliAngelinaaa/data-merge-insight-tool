import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Data Merge & Insight Tool")

st.sidebar.header("Upload Your Files")

file_a = st.sidebar.file_uploader("Upload Dataset A", type=["csv", "xlsx"])
file_b = st.sidebar.file_uploader("Upload Dataset B", type=["csv", "xlsx"])

common_column = st.sidebar.text_input("Enter the common column name to join on")

if file_a and file_b and common_column:
    df_a = pd.read_csv(file_a) if file_a.name.endswith('.csv') else pd.read_excel(file_a)
    df_b = pd.read_csv(file_b) if file_b.name.endswith('.csv') else pd.read_excel(file_b)

    if common_column in df_a.columns and common_column in df_b.columns:
        merged_df = pd.merge(df_b, df_a, on=common_column, how='left')

        page = st.sidebar.selectbox("Choose Page", ["Insights", "Data Explorer"])

        if page == "Insights":
            st.header("Summary Insights")
            st.write("Preview of Merged Data:")
            st.dataframe(merged_df.head())
            
            st.subheader("Top Values in Merge Column")
            st.bar_chart(df_a[common_column].value_counts().head(10))

            st.subheader("Missing Matches")
            st.write(merged_df[merged_df[common_column].isnull()])

        elif page == "Data Explorer":
            st.header("Explore Merged Dataset")
            selected_col = st.selectbox("Filter by column", merged_df.columns)
            if selected_col:
                unique_vals = merged_df[selected_col].dropna().unique()
                selected_val = st.selectbox("Choose a value", unique_vals)
                st.dataframe(merged_df[merged_df[selected_col] == selected_val])
    else:
        st.error("Common column not found in one or both files.")
