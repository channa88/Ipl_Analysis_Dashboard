import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up the page
st.set_page_config(page_title="IPL Dashboard", layout="wide")
st.title("🏏 IPL Case Study Dashboard")

# Load local CSV file
@st.cache_data
def load_data():
    return pd.read_csv("matches.csv")

df = load_data()

# Overview
st.subheader("📊 Dataset Overview")
st.write(df.head())
st.write(f"**Shape of dataset:** {df.shape}")

# Top Players
st.subheader("🏅 Top Players of the Match")
top_players = df['player_of_match'].value_counts().head(10)
st.bar_chart(top_players)

# Wins by Team
st.subheader("🏆 Matches Won by Teams")
team_wins = df['winner'].value_counts()
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(team_wins.index, team_wins.values, color='orange')
ax1.set_xlabel("Number of Wins")
ax1.set_ylabel("Team")
ax1.set_title("Total Wins by Team")
ax1.invert_yaxis()
st.pyplot(fig1)

# Matches per Season
st.subheader("📅 Matches Played Per Season")
matches_per_season = df['season'].value_counts().sort_index()
st.line_chart(matches_per_season)

# Toss Decision Analysis
st.subheader("🧠 Toss Decision Analysis")
toss_decision = df['toss_decision'].value_counts()
col1, col2 = st.columns(2)

with col1:
    st.write("### Toss Decision Count")
    st.bar_chart(toss_decision)

with col2:
    toss_win_match_win = df[df['toss_winner'] == df['winner']].shape[0]
    st.metric("Toss Winner = Match Winner", toss_win_match_win)

# Team Filter
st.sidebar.header("🔍 Filter by Team")
selected_team = st.sidebar.selectbox("Select a Team", sorted(df['winner'].dropna().unique()))

if selected_team:
    st.subheader(f"📈 Stats for {selected_team}")
    team_matches = df[(df['team1'] == selected_team) | (df['team2'] == selected_team)]
    st.write(f"Total Matches Played: {team_matches.shape[0]}")
    st.write(team_matches[['season', 'winner', 'player_of_match']].head(10))

    st.write("### Season-wise Wins")
    team_wins_by_season = team_matches[team_matches['winner'] == selected_team]['season'].value_counts().sort_index()
    st.bar_chart(team_wins_by_season)
