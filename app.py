import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

if user_menu == "Overall Analysis":
    editions = data["Year"].unique().shape[0] -1
    cities = data["City"].unique().shape[0]
    sports = data["Sport"].unique().shape[0]
    events = data["Event"].unique().shape[0]
    athletes = data["Name"].unique().shape[0]
    nations = data["region"].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time = helper.participating_nations_over_time(data)
    fig = px.line(nations_over_time, x="Edition", y="No. of countries")
    st.title("Participating Nations over the year")
    st.plotly_chart(fig)

    events_over_time = helper.Events_over_time(data)
    fig = px.line(events_over_time, x="Edition", y="No. of Events")
    st.title("Total Events over the year")
    st.plotly_chart(fig)
 
    athletes_over_time = helper.Athletes_over_time(data)
    fig = px.line(athletes_over_time, x="Edition", y="No. of Athletes")
    st.title("Total Athletes over the year")
    st.plotly_chart(fig)


    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20,20))
    x = data.drop_duplicates(["Year", "Sport", "Event"])
    pivot = x.pivot_table(index="Sport", columns="Year",values="Event", aggfunc="count").fillna(0).astype("int")
    ax = sns.heatmap(pivot, annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = data["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(data, selected_sport)
    st.table(x)
