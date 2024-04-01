import simplestart as ss

"""
based on the project at
https://github.com/Data-Science-at-SWAST/handover_poc  (@author: Andi5)
"""

import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from easydict import EasyDict as edict


#this is the header
 

t1, t2 = ss.columns((0.09,1), design=False) 

t1.image('images/index.png', width = 120)
t2.title("South Western Ambulance Service - Hospital Handover Report")
t2.md(" **tel:** 01392 451192 **| website:** [https://www.swast.nhs.uk](https://www.swast.nhs.uk) **| email:** [data.science@swast.nhs.uk](mailto:data.science@swast.nhs.uk)")
    
## Data

#with st.spinner('Updating Report...'):
    
#Metrics setting and rendering

def calc(state = None, value = None):
    calc1()
    calc2()
    calc3()
    calc4()
    calc5()
    
def calc1(state = None, value = None):
    hosp = select1.value
    if hosp == "":
        return

    to = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Total Outstanding')]   
    if len(to) == 0:
        ss.message("data error")
        return
        
    ch = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Current Handover Average Mins')]   
    hl = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Hours Lost to Handovers Over 15 Mins')]
    

    metric1.update(label ='Total Outstanding Handovers',value = int(to['Value']), delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
    metric2.update(label ='Current Handover Average',value = str(int(ch['Value']))+" Mins", delta = str(int(ch['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
    metric3.update(label = 'Time Lost today (Above 15 mins)',value = str(int(hl['Value']))+" Hours", delta = str(int(hl['Previous']))+' Compared to yesterday')

    
hosp_df = pd.read_excel('DataforMock.xlsx',sheet_name = 'Hospitals')
select1 = ss.selectbox(hosp_df, label = 'Choose Hospital', help = 'Filter report to show only one hospital', onchange=calc)
hosp = "All"

m1, m2, m3, m4, m5 = ss.columns((1,1,1,1,1), design=False)
    
todf = pd.read_excel('DataforMock.xlsx',sheet_name = 'metrics')

m1.write('')

metric1 = m2.metric(label = "demo", value = 0, delta = 0)
metric2 = m3.metric()#也可以什么参数都不写，先占位，以后在事件函数里 用metric2.update更新数据
metric3 = m4.metric()

m5.write('')

calc1()


def calc2(state = None, value = None):
    hosp = select1.value
    
    # Number of Completed Handovers by Hour
    
    fgdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'Graph')

    fgdf = fgdf[fgdf['Hospital Attended']==hosp] 

    fig = px.bar(fgdf, x = 'Arrived Destination Resolved', y='Number of Handovers', template = 'seaborn')

    fig.update_traces(marker_color='#264653')

    fig.update_layout(title_text="Number of Completed Handovers by Hour",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    plotly_chart1.update(fig) 

    # Predicted Number of Arrivals

    fcst = pd.read_excel('DataforMock.xlsx',sheet_name = 'Forecast')

    fcst = fcst[fcst['Hospital Attended']==hosp]

    fig = px.bar(fcst, x = 'Arrived Destination Resolved', y='y', template = 'seaborn')

    fig.update_traces(marker_color='#7A9E9F')

    fig.update_layout(title_text="Predicted Number of Arrivals",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)

    plotly_chart2.update(fig, use_container_width=True)  
    
    # Average Completed Handover Duration by hour

    fig = px.bar(fgdf, x = 'Arrived Destination Resolved', y='Average Duration',color = "Average Duration", template = 'seaborn', color_continuous_scale=px.colors.diverging.Temps)

    fig.add_scatter(x=fgdf['Arrived Destination Resolved'], y=fgdf['Target'], mode='lines', line=dict(color="black"), name='Target')

    fig.update_layout(title_text="Average Completed Handover Duration by hour",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None, legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))

    plotly_chart3.update(fig, use_container_width=True) 
    

g1, g2, g3 = ss.columns((1,1,1), design = False)

plotly_chart1 = g1.plotly_chart() 
plotly_chart2 = g2.plotly_chart() 
plotly_chart3 = g3.plotly_chart()
calc2()


# Waiting Handovers table

cw1, cw2 = ss.columns((2.5, 1.7), design = False)

whdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'WaitingHandovers')

colourcode = []

for i in range(0,9):
    colourcode.append(whdf['c'+str(i)].tolist())   

whdf = whdf[['Hospital Attended ',	'Expected',	'Inbound ',	'Arrived ',	'Waiting',	'0 - 15 Mins',	'15 - 30 Mins ',	'30 - 60 Mins ',	'60 - 90 Mins',	'90 + Mins ',
]]


fig = go.Figure(
        data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9], columnwidth = [30,10,10,10,10,15,15,15,15,15],
            header = dict(
             values = list(whdf.columns),
             font=dict(size=12, color = 'white'),
             fill_color = '#264653',
             line_color = 'rgba(255,255,255,0.2)',
             align = ['left','center'],
             #text wrapping
             height=20
             )
          , cells = dict(
              values = [whdf[K].tolist() for K in whdf.columns], 
              font=dict(size=12),
              align = ['left','center'],
              fill_color = colourcode,
              line_color = 'rgba(255,255,255,0.2)',
              height=20))])

fig.update_layout(title_text="Current Waiting Handovers",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)                                                           
cw1.plotly_chart(fig, use_container_width=True)    

def calc3(state = None, value = None):
    hosp = select1.value
    
    # Current Waiting Table

    cwdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'CurrentWaitingCallsigns')

    if hosp == 'All':
        cwdf = cwdf
    elif hosp != 'All':
        cwdf = cwdf[cwdf['Hospital Attended']==hosp]


    fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3], columnwidth = [15,40,20,20],
                header = dict(
                 values = list(cwdf.columns),
                 font=dict(size=12, color = 'white'),
                 fill_color = '#264653',
                 align = 'left',
                 height=20
                 )
              , cells = dict(
                  values = [cwdf[K].tolist() for K in cwdf.columns], 
                  font=dict(size=12),
                  align = 'left',
                  fill_color='#F0F2F6',
                  height=20))]) 

    fig.update_layout(title_text="Current Waiting Callsigns",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)

    plotly_chart4.update(fig, use_container_width=True)

plotly_chart4 = cw2.plotly_chart()
calc3()

# Performance Section  

with ss.expander("Previous Performance"):

    hhc24 = pd.read_excel('DataforMock.xlsx',sheet_name = 'HospitalHandoversCompleted')  
    
    colourcode = []
                          
    for i in range(0,13):
        colourcode.append(hhc24['c'+str(i)].tolist())    
    
    hhc24 = hhc24[['Hospital Attended','Handovers','In Progress','Average','Hours Lost','0 to 15 mins','15 to 30 mins','30 to 60 mins','60 to 90 mins','90 to 120 mins','120 mins','% 15 Mins','% 30 Mins']]   
    
    fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9,10,11,12], columnwidth = [18,12],
                header = dict(
                 values = list(hhc24.columns),
                 font=dict(size=11, color = 'white'),
                 fill_color = '#264653',
                 line_color = 'rgba(255,255,255,0.2)',
                 align = ['left','center'],
                 #text wrapping
                 height=20
                 )
              , cells = dict(
                  values = [hhc24[K].tolist() for K in hhc24.columns], 
                  font=dict(size=10),
                  align = ['left','center'],
                  fill_color = colourcode,
                  line_color = 'rgba(255,255,255,0.2)', 
                  height=20))])
     
    fig.update_layout(title_text="Hospital Handovers Completed in the Past 24 Hours",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=400)                                                               
    ss.plotly_chart(fig, use_container_width=True) 

    ss.space()
    p1,p2 = ss.columns((3, 1.7))   

    def calc4(state = None, value = None):
        hosp = select1.value
        
        #  Current Waiting Handovers

        hhc = pd.read_excel('DataforMock.xlsx',sheet_name = 'HospitalHandoverCompletedByHour')  

        hhc = hhc[hhc['Hospital Attended']==hosp]

        colourcode = []

        for i in range(0,13):
            colourcode.append(hhc['c'+str(i)].tolist())    

        hhc = hhc[['dst','Handovers','In Progress','Average','Hours Lost','0 to 15 mins','15 to 30 mins','30 to 60 mins','60 to 90 mins','90 to 120 mins','120 mins','% 15 Mins','% 30 Mins']]

        fig = go.Figure(
                data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9,10,11,12], columnwidth = [18,12],
                    header = dict(
                     values = list(hhc.columns),
                     font=dict(size=11, color = 'white'),
                     fill_color = '#264653',
                     line_color = 'rgba(255,255,255,0.2)',
                     align = ['left','center'],
                     #text wrapping
                     height=20
                     )
                  , cells = dict(
                      values = [hhc[K].tolist() for K in hhc.columns], 
                      font=dict(size=10),
                      align = ['left','center'],
                      fill_color = colourcode,
                      line_color = 'rgba(255,255,255,0.2)',
                      height=20))])

        fig.update_layout(title_text="Hospital Handovers Completed by Hour",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=600)                                                               

        plotly_chart5.update(fig, use_container_width=True)  
    
    plotly_chart5 = p1.plotly_chart()  
    calc4()
    
    def calc5(state = None, value = None):
        hosp = select1.value
        
        #  Longest Completed Handovers    

        lch = pd.read_excel('DataforMock.xlsx',sheet_name = 'LongestCompletedHandover')

        if hosp == 'All':
                lch = lch
        elif hosp != 'All':
            lch = lch[lch['Hospital Attended']==hosp]

        fig = go.Figure(
                    data = [go.Table (columnorder = [0,1,2,3,4], columnwidth = [10,35,20,20,10],
                                      header = dict(
                                          values = list(lch.columns),
                                          font=dict(size=12, color = 'white'),
                                          fill_color = '#264653',
                                          align = 'left',
                                          height=20
                                              )
                  , cells = dict(
                      values = [lch[K].tolist() for K in lch.columns], 
                      font=dict(size=11),
                      align = 'left',
                      fill_color='#F0F2F6',
                      height=20))])

        fig.update_layout(title_text="Longest Completed Handovers",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=600)

        plotly_chart6.update(fig, use_container_width=True)
       
    plotly_chart6 = p2.plotly_chart()
    calc5()
    
# Contact Form

with ss.expander("Contact us"):
    #with ss.form(key='contact', clear_on_submit=True):
        
    email = ss.text_input("Contact Email")
    
    ss.text_area("Query","Please fill in all the information or we may not be able to process your request")  
        
    submit_button = ss.button('Send Information')
    
