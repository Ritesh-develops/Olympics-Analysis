import streamlit as st
import pandas as pd
import preprocessor, helper

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

data = preprocessor.preprocessor(df, region_df)

st.sidebar.header("Olympics Analysis")
user_menu = st.sidebar.radio(
    "Select an Option",
    {"Medal Tally", "Overall Analysis", "Country-Wise Analysis", "Athlete wise Analysis"}
)

if user_menu == "Medal Tally":
    st.sidebar.header("Medals Tally")
    years, country = helper.country_year_list(data)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Year", country)
    medal_tally=helper.fetch_medal_tally(data, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.header("Overall Medals Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.header("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == "Overall" and selected_country != "Overall":
        st.header("Medal Tally of " + selected_country)
    if selected_year != "Overall" and selected_country != "Overall":
        st.header("Medal Tally of "+ selected_country + " in the year "+ str(selected_year))

    st.table(medal_tally)