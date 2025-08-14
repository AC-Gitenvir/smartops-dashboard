import streamlit as st
import pandas as pd
from difflib import get_close_matches

# Load Indian law data
law_data = pd.read_csv('indian_laws.csv')

st.set_page_config(page_title="LegisLENS - Indian Law Recommender", page_icon="⚖️")
st.title("⚖️ LegisLENS – Indian Law & Legal Advice Recommender")

st.markdown("Type your legal concern or question in simple words and let LegisLENS find the matching law section for you.")

# User input
query = st.text_area("📝 Your Legal Concern:", placeholder="e.g., My tenant is not paying rent for 3 months...")

def find_relevant_laws(query):
    matched_rows = []
    for i, row in law_data.iterrows():
        keywords = row['Keyword'].lower().split(',')
        if any(word.strip() in query.lower() for word in keywords):
            matched_rows.append(row)
    if not matched_rows:
        close = get_close_matches(query.lower(), law_data['Keyword'].str.lower(), n=2, cutoff=0.4)
        for match in close:
            row = law_data[law_data['Keyword'].str.lower() == match]
            matched_rows.extend(row.to_dict('records'))
    return matched_rows

if st.button("🔍 Get Legal Insight"):
    if query.strip() == "":
        st.warning("Please enter a legal issue to analyze.")
    else:
        results = find_relevant_laws(query)
        if results:
            st.success(f"🔎 Found {len(results)} relevant legal section(s):")
            for law in results:
                st.markdown(f"""
                #### 📘 Section {law['Section']} – {law['Act']}
                - **Keyword**: {law['Keyword'].capitalize()}
                - **Explanation**: {law['Explanation']}
                """)
        else:
            st.error("❌ No matching law found. Try using different or simpler keywords.")
