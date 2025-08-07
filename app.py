import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

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

if user_menu == "Country-Wise Analysis":
    st.sidebar.title("Country Wise Analysis")

    countries = data["region"].dropna().unique().tolist()
    countries.sort()
    selected_country = st.sidebar.selectbox("Select a country", countries)

    country_df = helper.yearwise_medal_tally(data, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the sports")
    pivot = helper.country_event_heatmap(data, selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pivot, annot=True)
    st.pyplot(fig)

    st.title(selected_country + "'s Top 10 successful athletes")
    table = helper.most_successful_athlete(data, selected_country)
    st.table(table)

if user_menu == "Athlete wise Analysis":
    athlete_df=data.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"]=="Gold"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"]=="Bronze"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"]=="Silver"]["Age"].dropna()
    fig=ff.create_distplot([x1, x2, x3, x4], ["Overall Age", "Gold","Silver", "Bronze"], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(data,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x='Weight',y='Height',hue='Medal',style='Sex',s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(data)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


