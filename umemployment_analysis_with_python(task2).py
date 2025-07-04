# -*- coding: utf-8 -*-
"""umemployment Analysis with python(task2).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qz-zqi5MmczgoAp8i7_uDO0sL7tsi2x3
"""

#TASK 2: Unemployment Analysis with Python
#● Analyze unemployment rate data representing unemployed people percentage.
#● Use Python for data cleaning, exploration, and visualization of unemployment trends.
#● Investigate the impact of Covid-19 on unemployment rates.
#● Identify key patterns or seasonal trends in the data.
#● Present insights that could inform economic or social policies.

import kagglehub

# Download latest version
path = kagglehub.dataset_download("gokulrajkmv/unemployment-in-india")

print("Path to dataset files:", path)

print(path)

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import calendar

import datetime as dt

import plotly.io as pio
pio.templates

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from IPython.display import HTML

import os

# Assuming the CSV file is directly inside the downloaded directory
csv_file_name = 'Unemployment_Rate_upto_11_2020.csv'
full_path = os.path.join(path, csv_file_name)

# Read the CSV file using the correct path
df = pd.read_csv(full_path)

df.head()

df.info()

df.isnull().sum()

df.columns =['States','Date','Frequency','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate','Region','longitude','latitude']

df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)

df['Frequency']= df['Frequency'].astype('category')

df['Month'] =  df['Date'].dt.month

df['Month_int'] = df['Month'].apply(lambda x : int(x))

df['Month_name'] =  df['Month_int'].apply(lambda x: calendar.month_abbr[x])

df['Region'] = df['Region'].astype('category')
df.drop(columns='Month',inplace=True)
df.head(3)

"""## **Statistics of Data Given**"""

df_stats = df[['Estimated Unemployment Rate',
       'Estimated Employed', 'Estimated Labour Participation Rate']]


round(df_stats.describe().T,2)

region_stats = df.groupby(['Region'])[['Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']].mean().reset_index()

region_stats = round(region_stats,2)


region_stats

heat_maps = df[['Estimated Unemployment Rate',
       'Estimated Employed', 'Estimated Labour Participation Rate',
       'longitude', 'latitude', 'Month_int']]

heat_maps = heat_maps.corr()

plt.figure(figsize=(10,6))
sns.set_context('notebook',font_scale=1)
sns.heatmap(heat_maps, annot=True,cmap='summer');

"""# **Data exploratory Analysis**"""

fig = px.box(df,x='States',y='Estimated Unemployment Rate',color='States',title='Unemployment rate',template='plotly')
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()

# The below box shows unemployement rate in each state in India

fig = px.scatter_matrix(df,template='plotly',
    dimensions=['Estimated Unemployment Rate','Estimated Employed',
                'Estimated Labour Participation Rate'],
    color='Region')
fig.show()

plot_ump = df[['Estimated Unemployment Rate','States']]

df_unemp = plot_ump.groupby('States').mean().reset_index()

df_unemp = df_unemp.sort_values('Estimated Unemployment Rate')

fig = px.bar(df_unemp, x='States',y='Estimated Unemployment Rate',color='States',
            title='Average Unemployment Rate in each state',template='plotly')

fig.show()

fig = px.bar(df, x='Region',y='Estimated Unemployment Rate',animation_frame = 'Month_name',color='States',
            title='Unemployment rate across region from Jan.2020 to Oct.2020', height=700,template='plotly')

fig.update_layout(xaxis={'categoryorder':'total descending'})

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig.show()

unemplo_df = df[['States','Region','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']]

unemplo = unemplo_df.groupby(['Region','States'])['Estimated Unemployment Rate'].mean().reset_index()
fig = px.sunburst(unemplo, path=['Region','States'], values='Estimated Unemployment Rate',
                  color_continuous_scale='Plasma',title= 'unemployment rate in each region and state',
                  height=650,template='ggplot2')

fig.show()

"""#** Impact of Lockdown on States Estimated Employed**

On 24 March 2020, the Government of India under Prime Minister Narendra Modi ordered a nationwide lockdown for 21 days
"""

fig = px.scatter_geo(df,'longitude', 'latitude', color="Region",
                     hover_name="States", size="Estimated Unemployment Rate",
                     animation_frame="Month_name",scope='asia',template='plotly',title='Impack of lockdown on employement across regions')

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig.update_geos(lataxis_range=[5,35], lonaxis_range=[65, 100],oceancolor="#6dd5ed",
    showocean=True)

fig.show()

lock = df[(df['Month_int'] >= 4) & (df['Month_int'] <=7)]

bf_lock = df[(df['Month_int'] >= 1) & (df['Month_int'] <=4)]
g_lock = lock.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()

g_bf_lock = bf_lock.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()


g_lock['Unemployment Rate before lockdown'] = g_bf_lock['Estimated Unemployment Rate']

g_lock.columns = ['States','Unemployment Rate after lockdown','Unemployment Rate before lockdown']

g_lock.head(2)

# percentage change in unemployment rate
g_lock['percentage change in unemployment'] = round(g_lock['Unemployment Rate after lockdown'] - g_lock['Unemployment Rate before lockdown']/g_lock['Unemployment Rate before lockdown'],2)

plot_per = g_lock.sort_values('percentage change in unemployment')

# percentage change in unemployment after lockdown

fig = px.bar(plot_per, x='States',y='percentage change in unemployment',color='percentage change in unemployment',
            title='percentage change in Unemployment in each state after lockdown',template='ggplot2')

fig.show()

"""# **most impacted states/UT**

Puducherry




Jharkhand

Bihar

Haryana

Tripura
"""

def sort_impact(x):
    if x <= 0:
        return 'Decreased'
    elif x > 0 and x < 10:
        return 'Increased Slightly'
    elif x >= 10 and x < 20:
        return 'Increased Moderately'
    else:
        return 'Increased Significantly'

plot_per['impact status'] = plot_per['percentage change in unemployment'].apply(lambda x:sort_impact(x))
fig = px.bar(plot_per, y='States',x='percentage change in unemployment',color='impact status',
            title='Impact of lockdown on employment across states',template='ggplot2',height=650)


fig.show()