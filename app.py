import streamlit as st
import pandas as pd
import random
from textblob import TextBlob

# Load dataset
df = pd.read_csv("tracks.csv")

# Keep only relevant columns
df = df[['track_name', 'artists', 'valence', 'energy', 'danceability', 'popularity', 'track_genre']]
df = df.dropna().drop_duplicates()

# Map valence to mood
def get_mood_from_valence(valence):
    if valence >= 0.7:
        return 'Happy'
    elif valence >= 0.4:
        return 'Neutral'
    else:
        return 'Sad'

df['mood'] = df['valence'].apply(get_mood_from_valence)

# Detect mood from user input using TextBlob
def detect_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "Happy"
    elif polarity < -0.3:
        return "Sad"
    else:
        return "Neutral"

# Recommend songs
def recommend_songs(user_mood, n=5):
    filtered = df[df['mood'] == user_mood]
    if len(filtered) < n:
        return filtered[['track_name', 'artists', 'track_genre']]
    return filtered[['track_name', 'artists', 'track_genre']].sample(n)

# Streamlit App
st.set_page_config(page_title="Mood Music Recommender", page_icon="🎧")
st.title("🎧 Mood-Based Music Recommender")
st.write("Describe how you're feeling, and get song recommendations based on your mood!")

# User input
user_input = st.text_input("How are you feeling today?")

if user_input:
    mood = detect_mood(user_input)
    st.success(f"Detected Mood: **{mood}**")

    if st.button("Recommend Songs"):
        songs = recommend_songs(mood)
        st.subheader("🎵 Recommended Songs:")
        for idx, row in songs.iterrows():
            st.markdown(f"**{row['track_name']}** — *{row['artists']}* ({row['track_genre']})")
