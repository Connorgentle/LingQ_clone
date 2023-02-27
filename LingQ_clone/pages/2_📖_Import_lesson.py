########################################
#     Importing libraries              #
########################################

from streamlit_player import st_player
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
from annotated_text import annotated_text
import requests
from st_aggrid import AgGrid
import pandas as pd
import numpy as np
from reverso_context_api import Client
from collections import namedtuple


########################################
#     Functions                        #
########################################

# function import lesson: given a youtube url, embed the youtube video, produce a script of the text, and update the vocabulary base

@st.cache_data
def import_lesson(youtube_url):
    #getting the transcript
    youtube_id = youtube_url[youtube_url.find("watch?v=")+len("watch?v="):]
    transcript = YouTubeTranscriptApi.get_transcript(youtube_id,languages=['fr'])
    if "transcript" not in st.session_state:
        st.session_state["transcript"]=transcript # save the transcript for later reference (NOW lets try to change this...)
    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            update_vocabulary(t)

# given a string of words, return a list of each word
def update_vocabulary(text):
    words = text.split()
    for word in words:
        if word.lower() not in st.session_state["vb"]['Word'].values:
            st.session_state["vb"].loc[len(st.session_state["vb"])] = [word.lower(),'','0-Unknown']

# define function to get translation
@st.cache_data
def get_tanslation(text):
    client = Client("fr", "en")
    return list(client.get_translations(text))

# Define function to add translations. This function updates the vocabulary base

def add_translations(text,translations=[],fluency='1-New'):
    if text.lower() not in st.session_state['vb']['Word'].values:
        #add text to the end of vocabulary base
        st.session_state['vb'].loc[len(st.session_state['vb'])] = [text.lower(),(", ").join(translations),fluency]
    else:
        #update row with translation and fluency
        st.session_state['vb'].loc[st.session_state['vb']['Word'] == text, ["Translation","Fluency"]] = [(", ").join(translations),fluency]

# @st.cache_data
# define function to return nicely colored text
def display_text(transcript):
    script =[] # list of tuples
    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            words = t.split()
            for word in words:
                script.append((word+" ", "", assign_color(word))) 
    return annotated_text(*script)

# Define function to assign colour based on fluency
def assign_color(text):
    colors = {'0-Unknown':"#87b2ff",'1-New':'#ffb93b','2-Recognized':"#ffdda1", '3-Familiar':'#c1c1c1','4-Learned':'dbdbdb','5-Known':'#0e1117'} 
    if text.lower() not in st.session_state["vb"]['Word'].values:
        return colors['0-Unknown']
        # return colors['1-New'] 
    else:
        #return appropriate color

        df = st.session_state["vb"].loc[st.session_state["vb"]['Word'] == text.lower(), 'Fluency'].iloc[0]
        return colors[df]


#function to check if video exists
def try_site(url):
    request = requests.get(url, allow_redirects=False)
    return request.status_code == 200

##########################
# SCRIPT TO RUN THE APP  #
##########################

# creating datafame of vocabulary base
# vb = pd.DataFrame(columns=['Word',"Definition","Fluency"])
if "vb" not in st.session_state:
        st.session_state["vb"] = pd.DataFrame(columns=['Word',"Translation","Fluency"])



st.title(':orange[Simple LingQ Clone]')
youtube_url = st.text_area('Enter a YouTube URL, then hit CTRL + ENTER. (The video must have available subtitles in your target-language)')


if youtube_url != '':
    if try_site(youtube_url) == True:
        import_lesson(youtube_url)
        st_player(youtube_url)
    else:
        st.text("Sorry, doesn't look like that link is working.")

with st.sidebar.form(key ='translations'):
    a = st.text_area('Search a translation:',key='my_search')  
    submitted1 = st.form_submit_button('Search Translation')
if a != '':
    with st.sidebar.form(key ='translations_2'):
        b = st.multiselect('Select the one or more translations:',get_tanslation(a),get_tanslation(a)[0:3],key='my_translations')
        c = st.radio('Select your level of fluency with the word: ',('1-New', '2-Recognized', '3-Familiar','4-Learned','5-Known'),key='my_fluency')
        submitted2 = st.form_submit_button('Accept Changes',on_click=add_translations(a,b,c))

if "transcript" in st.session_state:
    display_text(st.session_state["transcript"])