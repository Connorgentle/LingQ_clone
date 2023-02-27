from streamlit_player import st_player
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
from annotated_text import annotated_text
import requests
from st_aggrid import AgGrid
import pandas as pd
import numpy as np

######################
#     Functions      #
######################

#write a function to setup the study session
def study(num,f):
    if "vb" in st.session_state:
        df = st.session_state["vb"]
        df = df[df.Fluency == f].sample(n=num)
        return AgGrid(df)
    else:
        return st.markdown("Sorry, your vocabulary base is empty. Import a lesson to start growing your vocabulary base!")


st.title(":orange[Study Vocabulary]")


num_cards = st.number_input("Select the number of words you want to review: ", min_value=0,max_value=50,value=10,step=10)
fluency_level = st.radio("Which words would you like to review?",('1-New', '2-Recognized', '3-Familiar','4-Learned','5-Known'))

study(num_cards,fluency_level)
# study(10,'1-New')



