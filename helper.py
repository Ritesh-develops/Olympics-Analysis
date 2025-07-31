import pandas as pd

def Medal_tally(df):
    medal_tally = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally=medal_tally.groupby('region').sum()[['Gold', 'Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally["Total"] = medal_tally["Gold"]+medal_tally["Silver"]+medal_tally["Bronze"]

    medal_tally["Gold"] = medal_tally["Gold"].astype("int")
    medal_tally["Bronze"] = medal_tally["Bronze"].astype("int")
    medal_tally["Silver"] = medal_tally["Silver"].astype("int")
    return medal_tally