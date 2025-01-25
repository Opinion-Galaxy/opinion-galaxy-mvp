import streamlit as st

firebaseConfig = {
  "apiKey": st.secrets["FIREBASE_API_KEY"],
  "authDomain": "opinion-galaxy.firebaseapp.com",
  # "projectId": "opinion-galaxy",
  "storageBucket": "opinion-galaxy.firebasestorage.app",
  # "messagingSenderId": "342245854279",
  # "appId": "1:342245854279:web:70ebb52e5198c9f9dcb562",
  # "measurementId": "G-MT555SLVLL",
  "databaseURL": "https://opinion-galaxy-default-rtdb.firebaseio.com"
}