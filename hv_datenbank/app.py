import streamlit as st
import pandas as pd
from db import get_connection

st.title("Adressverwaltung")

conn = get_connection()

query = """
SELECT 
    contacts.id,
    contacts.name,
    contacts.firma,
    contacts.email,
    contacts.ort,
    GROUP_CONCAT(tags.tag_name) AS tags
FROM contacts
LEFT JOIN contact_tags ON contacts.id = contact_tags.contact_id
LEFT JOIN tags ON tags.id = contact_tags.tag_id
GROUP BY contacts.id
"""

df = pd.read_sql(query, conn)

st.dataframe(df)