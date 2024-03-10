#120年奥运奖牌记录
#主要展示SimpleStart在大屏展示数据的能力

#本演示的主要代码除了app.py 其它都借鉴自Streamlit的演示程序
#https://github.com/udhavvvv-dev/Olympic-Data-Analysis

import simplestart as ss 
import pandas as pd
import preprocessor, helper

import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use("Agg") #很重要，否则在ss中会崩溃
import seaborn as sns
import plotly.figure_factory as ff

x = 1
func_options = ["Medal Tally", "Overall Analysis","Region Analysis","Athlete Analysis"]

df = pd.read_csv('./olympic-history/athlete_events.csv')
region_df = pd.read_csv('./olympic-history/noc_regions.csv')

df = preprocessor.preprocess(df, region_df)


years, regions = helper.region_year_list(df)


tabs_result = ss.tabs(func_options, show_tab_title = False)

def fresh_most_successful_atheletes():
    x = helper.best_athletes(df, selected_sport.value)
    table_most_succefull.data = x
    
#先占位
with tabs_result.tabs[0]:
    ss.md("# @medal_tally_title")
    table_medal = ss.table(region_df, show_border = True, style="color:#333")
    
with tabs_result.tabs[1]:
    ss.write("# Statistics")
    
    col1, col2, col3 = ss.columns(3, design = False)
    with col1:
        ss.write("### Editions")
        ss.write("@editions")
    with col2:
        ss.write("### Cities")
        ss.write("@cities")
    with col3:
        ss.write("### Events")
        ss.write("@events")
        
    col1, col2, col3 = ss.columns(3, design = False)
    with col1:
        ss.write("### Sports")
        ss.write("@sports")
    with col2:
        ss.write("### Nations")
        ss.write("@nations")
    with col3:
        ss.write("### Athletes")
        ss.write("@athletes")
        
    ss.space()
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time,x ='Editions', y='region')
    ss.write("## Nations in Olympics over Time")
    ss.plotly_chart(fig)
    
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time,x ='Editions', y='Event')
    ss.write("## Events over Time")
    ss.plotly_chart(fig)
    
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x ='Editions', y='Name')
    ss.write("## Athletes over Time")
    ss.plotly_chart(fig)
    
    ss.write("## Number of Events over Time")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns="Year", values="Event", aggfunc="count").fillna(0).astype('int'), annot=True)
    ss.pyplot(fig)

    ss.write("## Most Successful Atheletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    
    ss.write("Select a Sport")
    selected_sport = ss.selectbox(sport_list, value="Overall", onchange=fresh_most_successful_atheletes)

    table_most_succefull = ss.table(None)
    fresh_most_successful_atheletes()
    
with tabs_result.tabs[2]:
    ss.md("# @selected_region Medals Over the Years")
    plotly1 = ss.plotly_chart(style="height:1600px")
    
    ss.md("# @selected_region in various sports")
    plot2 = ss.pyplot()
    
    ss.md("# Best athletes of @selected_region")
    table_best_athletes = ss.table(None)
    
sidebar = ss.sidebar()

def fresh_medal_tally():
    selected_year = sel_year.value
    selected_region = sel_region.value
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_region)
    
    if selected_year == 'Overall' and selected_region == 'Overall':
        ss.session.state["medal_tally_title"] = "Overall Tally"
    else:
        ss.session.state["medal_tally_title"] = f"{selected_region} in {selected_year} olympics!"
        
    table_medal.data = medal_tally
    
    
def fresh_overall_analysis():
    ss.session.state["editions"] = df['Year'].unique().shape[0]
    ss.session.state["cities"] = df['City'].unique().shape[0]
    ss.session.state["sports"] = df['Sport'].unique().shape[0]
    ss.session.state["events"] = df['Event'].unique().shape[0]
    ss.session.state["athletes"] = df['Name'].unique().shape[0]
    ss.session.state["nations"] = df['region'].unique().shape[0]

def fresh_region_analysis():
    selected_region  = sel_region2.value

    region_df = helper.yearwise_medal_tally(df, selected_region )
    fig = px.line(region_df, x='Year', y='Medal')
    ss.session.state["selected_region"] = sel_region2.value

    plotly1.plot(fig)


    pt = helper.country_event_heatmap(df, selected_region)
    if len(pt) > 0:
        fig, ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(pt, annot=True )
        plot2.plot(fig)
    else:
        plot2.plot("")

    athlete_df = helper.country_athlete_analysis(df, selected_region)
    table_best_athletes.data = athlete_df
    
def fresh_athlete_analysis():
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist','Silver Medalist', ' Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    ss.write("## Athletes - Distribution by Age")

    ss.plotly_chart(fig)
    
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
    ss.write("## Sports - Distribution by Age for Gold Medalist")
    ss.plotly_chart(fig)
    
    ss.write("## Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    ss.plotly_chart(fig)
    
def radio_change(state, value):
    mytabs.activeTab = value
    tabs_result.activeTab = value

    if value == "Medal Tally":
        fresh_medal_tally()
    elif value == "Overall Analysis":
        fresh_overall_analysis()
    elif value == "Region Analysis":
        fresh_region_analysis()
    else:
        if ss.session.state["athlete_analysis_loaded"] == False:
            with tabs_result.tabs[3]:
                fresh_athlete_analysis()
            ss.session.state["athlete_analysis_loaded"] = True # load only once

with sidebar:
    ss.write("#### Olympic Data Analysis")
    ss.image("./media/images/olympics1.png")

    ##
    ss.write("### Select An Option")
    ss.radio(func_options, value="Medal Tally", inline = False, onchange=radio_change)
    ss.space()

    mytabs = ss.tabs(func_options, show_tab_title = False, tab_position = "left")
    with mytabs.tabs[0]:
        ##
        ss.write("Select Years")
        sel_year =ss.selectbox(years, value="Overall", onchange = fresh_medal_tally)

        ##
        ss.write("Select Region")
        sel_region = ss.selectbox(regions, value="Overall", onchange = fresh_medal_tally)
        
    with mytabs.tabs[1]:
        pass #nothing
    
    with mytabs.tabs[2]:
        ##
        ss.write("Select Region")
        region_list = df['region'].dropna().unique().tolist()
        region_list.sort()
        sel_region2 = ss.selectbox(region_list, value="China", onchange = fresh_region_analysis)
        
    with mytabs.tabs[3]:
        pass #nothing
    
#initially
fresh_medal_tally()

def onPageLoad():
    ss.experimental_js('''
document.title = "120 years of Olympic games"
''')
    ss.session.state["medal_tally_title"] = "Overall Tally"
    
def onPageLoad():
    ss.session.state["medal_tally_title"] = "Overall Tally"
    ss.session.state["athlete_analysis_loaded"] = False