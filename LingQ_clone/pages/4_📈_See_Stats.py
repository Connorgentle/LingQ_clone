import streamlit as st
import pandas as pd
import numpy as np


st.title(":orange[Learning Progression]")

if "vb" in st.session_state:
    df = st.session_state["vb"]
    # gb = df.groupby("Fluency").apply(len)
    gb = df['Fluency'].value_counts().reindex(['0-Unknown','1-New','2-Recognized','3-Familiar','4-Learned','5-Known'], fill_value=0)
    st.subheader(':blue[Number of words by level of fluency]')
    st.bar_chart(gb)
else:
    st.markdown("Sorry, your vocabulary base is empty. Import a lesson to start growing your vocabulary base!")