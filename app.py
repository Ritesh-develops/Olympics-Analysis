import streamlit as st
import pandas as pd
import preprocessor, helper

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

data = preprocessor.preprocessor(df, region_df)
medal_tally=helper.Medal_tally(data)

user_menu = st.sidebar.radio(
    "Select an Option",
    {"Medal Tally", "Overall Analysis", "Country-Wise Analysis", "Athlete wise Analysis"}
)

if user_menu == "Medal Tally":
    st.dataframe(medal_tally)