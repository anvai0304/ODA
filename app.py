import pandas as pd
import streamlit as st
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

# Load the data
df = pd.read_csv('athlete_events.csv')
regions_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, regions_df)

st.sidebar.header('Olympics Analysis')
st.sidebar.image('olympics.jpeg')

user = st.sidebar.radio('Select an option', ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis'))

# st.dataframe(df)

if user == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+"'s" + ' Overall Performance')
    if selected_year !='Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+"'s" + ' Performance in ' + str(selected_year) + ' Olympics')
    
    # st.dataframe(medal_tally)
    st.table(medal_tally) # Looks better

if user == 'Overall Analysis':
    num = df['Year'].nunique()
    num_of_editions = num - 1

    num_of_cities = df['City'].nunique()
    num_of_events = df['Event'].nunique()
    num_of_sports = df['Games'].nunique()
    num_of_athletes = df['Name'].nunique()
    num_of_nations = df['region'].nunique()

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(num_of_editions)

    with col2:
        st.header('Hosts')
        st.title(num_of_cities)

    with col3:
        st.header('Sports')
        st.title(num_of_sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(num_of_events)

    with col2:
        st.header('Athletes')
        st.title(num_of_athletes)

    with col3:
        st.header('Nations')
        st.title(num_of_nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x = 'Edition', y = 'region')
    fig.show()
    st.header('Participating Nations Over the Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x = 'Edition', y = 'Event')
    fig.show()
    st.header('Number of Events Over the Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x = 'Edition', y = 'Name')
    fig.show()
    st.header('Number of Athletes Over the Years')
    st.plotly_chart(fig) # Line chart

    st.header('Number of Events Over the Years (Every Sports)')
    fig, ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index = 'Sport', columns = 'Year', values = 'Event', aggfunc = 'count').fillna(0).astype('int'), annot = True)
    st.pyplot(fig) # Heatmap

    st.header('Most Successful Athletes')
    # Need a dropdown to select a specific sport, and get the successful athletes in that sport
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sports_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)


if user == 'Country-wise Analysis':
    st.sidebar.header('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country', country_list)

    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x = 'Year', y = 'Medal')
    st.header(selected_country + "'s" + ' Medal Tally over the years')
    st.plotly_chart(fig)

    # Country's medals in each sport
    
    fig, ax = plt.subplots(figsize = (15,10))
    ax = helper.country_medal_sport(df, selected_country)
    st.header(selected_country + "'s" + ' Medal Tally (Sports-wise)')
    st.pyplot(fig)

    # Top 10 athletes country-wise
    st.header('Top Athletes of ' + selected_country)
    top_10_athletes = helper.most_successful_athlete(df, selected_country)
    st.table(top_10_athletes)


# Athlete-wise Analysis
if user == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Nedalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize = False, width = 1200, height = 600)
    st.header('Distribution of Age')
    st.plotly_chart(fig)

    # Comparison of height and weight with regards to medals won
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    st.header('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sports_list)
    temp_df = helper.weight_vs_height(df, selected_sport)
    fig,ax = plt.subplots() 
    ax = sns.scatterplot(x = 'Weight', y = 'Height', hue = 'Medal', data = temp_df)
    st.pyplot(fig) # Scatterplot

    # Number of male vs number of female athletes participation
    st.header('Men vs Women Participation over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x = 'Year', y = ['Male', 'Female'])
    st.plotly_chart(fig)
    