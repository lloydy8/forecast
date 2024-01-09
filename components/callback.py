from datetime import datetime
import pandas as pd
import plotly.graph_objs as go
from dash import html
import numpy as np
from statistics import mean

def update_dataframe(start_date, intervals_value, interval_value, demand_coef_slider, activity_coef_slider, initial_demand_value, initial_activity_value, wip_start_value,
                     demand_growth_slider, activity_growth_slider, weekend_demand_label, sat_activity_label, sund_activity_label,
                     check_update_1, update_date_value_1, update_demand_value_1, update_activity_value_1,
                     check_update_2, update_date_value_2, update_demand_value_2, update_activity_value_2,
                     check_update_3, update_date_value_3, update_demand_value_3, update_activity_value_3,
                     check_update_4, update_date_value_4, update_demand_value_4, update_activity_value_4,
                     check_update_5, update_date_value_5, update_demand_value_5, update_activity_value_5, n_clicks):

    activity_coef = activity_coef_slider / 100
    demand_coef = demand_coef_slider / 100
    demand_growth = demand_growth_slider / 100
    average_growth = activity_growth_slider / 100

    date_obj = datetime.strptime(start_date, '%d/%m/%Y')
    date_range_week = pd.date_range(start=date_obj, periods=int(intervals_value), freq='7D')
    date_range_day = pd.date_range(start=date_obj, periods=int(intervals_value), freq='1D')

    if interval_value == 1:
        df = pd.DataFrame({'Date': date_range_day[::int(intervals_value) // len(date_range_week)]})
        x = 365
    else:
        df = pd.DataFrame({'Date': date_range_week})
        x = 52

    df['Day'] = df['Date'].dt.day_name()
    df['Average Activity'] = initial_activity_value
    df['Average Demand'] = initial_demand_value



    date_update_1 = datetime.strptime(update_date_value_1, '%d/%m/%Y')
    date_update_2 = datetime.strptime(update_date_value_2, '%d/%m/%Y')
    date_update_3 = datetime.strptime(update_date_value_3, '%d/%m/%Y')
    date_update_4 = datetime.strptime(update_date_value_4, '%d/%m/%Y')
    date_update_5 = datetime.strptime(update_date_value_5, '%d/%m/%Y')




    # Method for updating the Average Demand

    #Update 1

    if check_update_1:
        df.loc[df['Date'] >= date_update_1, 'Average Demand'] = update_demand_value_1
        df.loc[df['Date'] >= date_update_1, 'Average Activity'] = update_activity_value_1

    #Update 2
        
    if check_update_2:
        df.loc[df['Date'] >= date_update_2, 'Average Demand'] = update_demand_value_2
        df.loc[df['Date'] >= date_update_2, 'Average Activity'] = update_activity_value_2



    #Update 3
    if check_update_3:
        df.loc[df['Date'] >= date_update_3, 'Average Demand'] = update_demand_value_3
        df.loc[df['Date'] >= date_update_3, 'Average Activity'] = update_activity_value_3

    

    #Update 4
        
    if check_update_4:
        df.loc[df['Date'] >= date_update_4, 'Average Demand'] = update_demand_value_4
        df.loc[df['Date'] >= date_update_4, 'Average Activity'] = update_activity_value_4



    #Update 5
        
    if check_update_5:
        df.loc[df['Date'] >= date_update_5, 'Average Demand'] = update_demand_value_5
        df.loc[df['Date'] >= date_update_5, 'Average Activity'] = update_activity_value_5


    #Formula for Growth over year

    average_demand = []
    for a in range(1, intervals_value + 1, 1):
        average_demand.append(1+(a/ x) * demand_growth)
        
    average_activity = []
    for b in range(1, intervals_value + 1, 1):
        average_activity.append(1+(b/ x) * average_growth)
    
    df['Average Demand'] = df['Average Demand'] * average_demand
    df['Average Activity'] = df['Average Activity'] * average_activity

    std_dev_demand = df['Average Demand'] * demand_coef 
    df['Approximate Demand'] = np.random.normal(df['Average Demand'], std_dev_demand)

    # Creating the Approximate Activity
    st_dev_activity = df['Average Activity'] * activity_coef
    df['Approximate Activity'] = np.random.normal(df['Average Activity'], st_dev_activity)


    # If Weekend Demand = No

    if not weekend_demand_label:
        if 'Saturday' in df['Day'].values:
            saturday_index = df[df['Day'] == 'Saturday'].index
            df.loc[saturday_index, 'Average Demand'] = 0
            df.loc[saturday_index, 'Approximate Demand'] = 0
        
        if 'Sunday' in df['Day'].values:
            sunday_index = df[df['Day'] == 'Sunday'].index
            df.loc[sunday_index, 'Average Demand'] = 0
            df.loc[sunday_index, 'Approximate Demand'] = 0

    if not  sat_activity_label:
        if 'Saturday' in df['Day'].values:
            saturday_index = df[df['Day']== 'Saturday'].index
            df.loc[saturday_index, 'Average Activity'] = 0
            df.loc[saturday_index, 'Approximate Activity'] = 0


    if not sund_activity_label:
        if 'Sunday' in df['Day'].values:
            sunday_index = df[df['Day']== 'Sunday'].index
            df.loc[sunday_index, 'Average Activity'] = 0
            df.loc[sunday_index, 'Approximate Activity'] = 0



    df['WIP'] = np.maximum(0, wip_start_value + df['Approximate Demand'] - df['Approximate Activity'])

    for i in range(1, len(df)):
        df.loc[i, 'WIP'] = np.maximum(0, df.loc[i - 1, 'WIP'] + df.loc[i, 'Approximate Demand'] - df.loc[i, 'Approximate Activity'])

    df['Average Waiting Time'] = 1
    df['Average Waiting Time'] = df['Average Waiting Time'].astype(np.float64)



    df.loc[0, 'Average Waiting Time'] = df['WIP'][0] / mean(df['Approximate Demand'][:5])
    df.loc[1, 'Average Waiting Time'] = df['WIP'][1] / mean(df['Approximate Demand'][:5])
    df.loc[2, 'Average Waiting Time'] = df['WIP'][2] / mean(df['Approximate Demand'][:5])
    df.loc[3, 'Average Waiting Time'] = df['WIP'][3] / mean(df['Approximate Demand'][:5])
    df.loc[4, 'Average Waiting Time'] = df['WIP'][4] / mean(df['Approximate Demand'][:5])
    df.loc[5, 'Average Waiting Time'] = df['WIP'][5] / mean(df['Approximate Demand'][:6])
    df.loc[6, 'Average Waiting Time'] = df['WIP'][6] / mean(df['Approximate Demand'][:7])

    # Assuming intervals and df are defined elsewhere
    a = 1

    for i in range(7, int(intervals_value)):
        df.loc[i, 'Average Waiting Time'] = df['WIP'][i] / df['Approximate Demand'].iloc[a:i+1].mean()
        a += 1

    df['Approximate Activity'] = df['Approximate Activity'].round(2)
    df['Approximate Demand'] = df['Approximate Demand'].round(2)
    df['WIP'] = df['WIP'].round(2)
    df['Average Waiting Time'] = df['Average Waiting Time'].round(2)

    # Create traces for 'Approximate Demand' and 'Approximate Activity'
    trace1 = go.Scatter(x=df['Date'], y=df['Approximate Demand'], mode='lines', name='Demand', line=dict(color='blue'))
    trace2 = go.Scatter(x=df['Date'], y=df['Approximate Activity'], mode='lines', name='Activity', line=dict(color='red'))

    # Create trace for 'WIP' on a secondary y-axis
    trace3 = go.Scatter(x=df['Date'], y=df['WIP'], mode='lines', name='WIP', line=dict(color='green'), yaxis='y2')

    # Define the layout with secondary y-axis and lower limits set to 0
    layout = go.Layout(
        xaxis=dict(
        title='Date',
        showgrid=True,
        tickangle=310,
        tickfont=dict(size=16, family='Arial', color='black'),  # Update tick font size here
        titlefont=dict(size=16, family='Arial', color='black'),  # Update title font size here
    ),
    yaxis=dict(
        title='<b>No. of Patients Demand & Activity per time interval</b>',
        showgrid=True,
        range=[0, df[['Approximate Demand', 'Approximate Activity']].values.max() + 20],
        showline=True,
        tickfont=dict(size=16, family='Arial', color='black'),  # Update tick font size here
        titlefont=dict(size=16, family='Arial', color='black'),  # Update title font size here
    ),
    yaxis2=dict(
        title='<b>No. of Patients WIP</b>',
        overlaying='y',
        side='right',
        showgrid=False,
        range=[0, df['WIP'].max() + 20],
        showline=True,
        tickfont=dict(size=16, family='Arial', color='green'),  # Update tick font size here
        titlefont=dict(size=16, family='Arial', color='green'),  # Update title font size here
    ),
        legend=dict(font=dict(size=12, family='Arial', color='black')),
        margin=dict(t=30, b=80, l=80, r=80),   # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)', 
    )

    # Create the figure with traces and layout
    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)

    # Create a second plot for Average Waiting Time
    trace_waiting_time = go.Scatter(x=df['Date'], y=df['Average Waiting Time'], mode='lines', name='Average Waiting Time', line=dict(color='orange'))

    # Define a new layout for the second plot underneath the first plot
    layout_waiting_time = go.Layout(
        xaxis=dict(title='Date', showgrid=True, tickangle=310, tickfont=dict(size=16, family='Arial', color='black'),
            titlefont=dict(size=16, family='Arial', color='black')),
        yaxis=dict(
            title='<b>Average Waiting Time</b>',
            showgrid=True,
            showline=True,
            range=[0, df['Average Waiting Time'].max()],
            tickfont=dict(size=16, family='Arial', color='black'),
            titlefont=dict(size=16, family='Arial', color='black')
        ),
        hovermode='closest',
        height=400,  # Adjust the height for the second plot as needed
        margin=dict(t=20, b=80, l=80, r=80),
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Create the figure with the trace for Average Waiting Time and its layout
    fig_waiting_time = go.Figure(data=[trace_waiting_time], layout=layout_waiting_time)


    return fig, fig_waiting_time
