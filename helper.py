import numpy as np
import seaborn as sns

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        medals = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        medals = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    medals['Total'] = medals['Gold'] + medals['Silver'] + medals['Bronze']

    return medals

def medal_tally(df):

    medal_tally = df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()

    medal_tally['Total Medals'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year(df):
    # Year
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    # Country
    country = np.unique(df['region'].dropna().values).tolist()
    country.insert(0, 'Overall')

    return years, country

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates([col, 'Year'])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count' : col, 'Year' : 'Edition'}, inplace=True)


    return nations_over_time

# Most successful athletes in each sport
def most_successful(df, sport):
    temp_df = df.dropna(subset= ['Medal']) # We do not want the athletes with no medals..

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # return temp_df['Name'].value_counts().reset_index().merge(df)[['Name', 'count', 'Sport', 'region']].drop_duplicates() # Here it was unable to give for specific sports properly, showed for same athlete in different sports too!
    x = temp_df['Name'].value_counts().reset_index().merge(df, on = 'Name', how = 'left')[['Name', 'count', 'Sport', 'region']].drop_duplicates() # Getting the same problem as above here too! 2/2/25 - Will complete the project for now, then try to find the solution to this!
    x.rename(columns = {'count' : 'Medals'}, inplace = True)
    return x

# Year-wise Medal tally (Country-wise)
def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Sport', 'Event', 'City', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

# Country's each sports medal tally
def country_medal_sport(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Sport', 'Event', 'City', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    x = sns.heatmap(new_df.pivot_table(index = 'Sport', columns = 'Year', values = 'Medal', aggfunc = 'count').fillna(0), annot = True)


# Top 10 athletes for each country
def most_successful_athlete(df, country):
    temp_df = df.dropna(subset= ['Medal']) # We do not want the athletes with no medals..

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, on = 'Name', how = 'left')[['Name', 'count', 'Sport']].drop_duplicates()
    x.rename(columns = {'count' : 'Medals'}, inplace = True)
    return x

# Distribution comparison in regards with height and weight
def weight_vs_height(df, sport):
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace = True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


# Number of male athletes vs number of female athletes
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on = 'Year')
    final.rename(columns={'Name_x' : 'Male', 'Name_y' : 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final


