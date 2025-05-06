import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Merge & Insight Tool", layout="wide")
st.title("Data Merge & Insight Tool")

st.sidebar.header("Upload Your Files")
uploaded_files = st.sidebar.file_uploader(
    "Upload one or more datasets (CSV or Excel)", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)
common_column = st.sidebar.text_input("Enter the common column name to join on")

if uploaded_files and len(uploaded_files) >= 2 and common_column:
    file_names = [f.name for f in uploaded_files]
    file_a_name = st.sidebar.selectbox("Select Dataset A", file_names)
    file_b_name = st.sidebar.selectbox("Select Dataset B", file_names, index=1 if len(file_names) > 1 else 0)

    df_a = None
    df_b = None
    for f in uploaded_files:
        if f.name == file_a_name:
            df_a = pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f)
        if f.name == file_b_name:
            df_b = pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f)

    if common_column in df_a.columns and common_column in df_b.columns:
        merged_df = pd.merge(df_b, df_a, on=common_column, how='left')

        page = st.sidebar.radio("Choose Page", ["Insights", "Data Explorer", "Global Search"])

        if page == "Insights":
            st.header("Summary Insights")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records in A", len(df_a))
                st.metric("Unique Keys in A", df_a[common_column].nunique())
                st.metric("Duplicate Keys in A", df_a[common_column].duplicated().sum())
            with col2:
                st.metric("Total Records in B", len(df_b))
                st.metric("Unique Keys in B", df_b[common_column].nunique())
                st.metric("Duplicate Keys in B", df_b[common_column].duplicated().sum())
            with col3:
                matched_count = merged_df[merged_df[common_column].notnull()].shape[0]
                unmatched_count = merged_df[merged_df.isnull().any(axis=1)].shape[0]
                percent_matched = matched_count / len(df_b) * 100
                st.metric("Matched Rows in B", matched_count)
                st.metric("Unmatched Rows in B", unmatched_count)
                st.metric("Match Rate (%)", f"{percent_matched:.2f}")

            st.subheader("Preview of Merged Data")
            st.dataframe(merged_df.head(20), use_container_width=True)

            st.subheader(f"Top 10 Most Frequent `{common_column}` Values (in A)")
            top_values = df_a[common_column].value_counts().head(10)
            st.bar_chart(top_values)

            st.subheader("Rows in B with No Match in A")
            unmatched = merged_df[merged_df.isnull().any(axis=1)]
            st.dataframe(unmatched, use_container_width=True)

            numeric_cols = merged_df.select_dtypes(include='number').columns
            if len(numeric_cols) > 0:
                st.subheader("Distribution of Numeric Columns")
                selected_num_col = st.selectbox("Select numeric column", numeric_cols)
                st.bar_chart(merged_df[selected_num_col])

        elif page == "Data Explorer":
            st.header("Explore Merged Dataset")
            st.dataframe(merged_df, use_container_width=True)

            st.subheader("Filter By Column")
            selected_col = st.selectbox("Select column to filter", merged_df.columns)
            if selected_col:
                unique_vals = merged_df[selected_col].dropna().unique()
                selected_val = st.selectbox("Choose a value", sorted(unique_vals.astype(str)))
                filtered_df = merged_df[merged_df[selected_col].astype(str) == selected_val]
                st.write(f"Filtered rows: {len(filtered_df)}")
                st.dataframe(filtered_df, use_container_width=True)

        elif page == "Global Search":
            st.header("Global Search Across Merged Dataset")

            search_query = st.text_input("Search for any keyword, name, number, etc.")
            if search_query:
                mask = merged_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
                filtered = merged_df[mask]

                st.write(f"Found {len(filtered)} matching rows:")
                st.dataframe(filtered, use_container_width=True)

                if not filtered.empty:
                    st.subheader("Count by Group (Auto-detect)")
                    chart_col = None
                    for col in ['Assignment Group', 'Impacted CI', 'Change Owner']:
                        if col in filtered.columns:
                            chart_col = col
                            break
                    if chart_col:
                        st.bar_chart(filtered[chart_col].value_counts())
            else:
                st.info("Type something in the search bar to filter results.")

    else:
        st.error("Common column not found in one or both files.")
else:
    st.info("Upload both datasets and enter a column to join on to begin.")
