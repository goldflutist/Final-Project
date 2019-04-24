import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import unittest
import sqlite3
import requests
import json
import re
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
from numpy import percentile
import statistics as stat
import csv


api_key = 'pG9YH1p3M1jDCQnsbWytiXoRCGMp4ltkaACoOxkNqqnkrSlHU2k8_hukdJRaHFIEtg3w6q16AjIBDNAPKoIKTGvs696pm5VGGZ3k3iwswLRb5zdv9xjJsEkBRha1XHYx'
headers = {'Authorization': 'Bearer %s' % api_key}

## Set up database
conn = sqlite3.connect('yelp.sqlite')
cur = conn.cursor()
cur.execute('''
			CREATE TABLE IF NOT EXISTS Yelp
			(name TEXT UNIQUE, rating INTEGER, latitude FLOAT, longitude FLOAT, category TEXT)''')

# Gathering the data 
for category in ['restaurants', 'bars', 'nightlife', 'active', 'fitness', 'shopping', 'arts']:
    for num in [0, 21, 41]: 
        url = 'https://api.yelp.com/v3/businesses/search'
        params = {'term': category, 'location':'Ann Arbor', 'offset': num}
        
        r = requests.get(url, params=params, headers=headers)
        parsed = json.loads(r.text)
    
        businesses = parsed["businesses"]
        
        #Saving the data in the database
        for business in businesses:
            name = business["name"]
            rating = business["rating"]
            latitude = business["coordinates"]["latitude"]
            longitude = business["coordinates"]["longitude"]
            bus_category = category
            cur.execute('''INSERT OR IGNORE INTO Yelp (name, rating, latitude, longitude, category) VALUES (?, ?, ?, ?, ?)''', (name, rating, latitude, longitude, bus_category))
    
        conn.commit()

# Calculating data 
x_data = ['Restaurants', 'Bars',
          'Nightlife', 'Active', 
          'Fitness', 'Shopping', 'Arts']

cur.execute('SELECT name, rating, latitude, longitude, category FROM Yelp')

#ratings 
rest_rate = list() 
bars_rate = list() 
night_rate = list() 
act_rate = list() 
fit_rate = list() 
shop_rate = list() 
arts_rate = list() 

#latitudes and longitudes 
rest_lat = list()
rest_lon = list()
bars_lat = list()
bars_lon = list()
night_lat = list()
night_lon = list()
act_lat = list()
act_lon = list()
fit_lat = list()
fit_lon = list()
shop_lat = list()
shop_lon = list()
arts_lat = list()
arts_lon = list()

#names
rest_name = list()
bars_name = list()
night_name = list()
act_name = list()
fit_name = list()
shop_name = list()
arts_name = list()

for row in cur: 
    if row[4] == 'restaurants': 
        rest_name.append(row[0])
        rest_rate.append(row[1])
        rest_lat.append(row[2])
        rest_lon.append(row[3])
    if row[4] == 'bars':
        bars_name.append(row[0])
        bars_rate.append(row[1])
        bars_lat.append(row[2])
        bars_lon.append(row[3])
    if row[4] == 'nightlife': 
        night_name.append(row[0])
        night_rate.append(row[1])
        night_lat.append(row[2])
        night_lon.append(row[3])
    if row[4] == 'active':
        act_name.append(row[0])
        act_rate.append(row[1])
        act_lat.append(row[2])
        act_lon.append(row[3])
    if row[4] == 'fitness': 
        fit_name.append(row[0])
        fit_rate.append(row[1])
        fit_lat.append(row[2])
        fit_lon.append(row[3])
    if row[4] == 'shopping':
        shop_name.append(row[0])
        shop_rate.append(row[1])
        shop_lat.append(row[2])
        shop_lon.append(row[3])
    if row[4] == 'arts': 
        arts_name.append(row[0])
        arts_rate.append(row[1])
        arts_lat.append(row[2])
        arts_lon.append(row[3])

# Write calculations to csv file 

categories = ['Restaurants', 'Bars', 'Nightlife', 'Active', 'Fitness', 'Shopping', 'Arts']

averages = list()
minimums = list()
q1s = list()
medians = list()
q3s = list()
maximums = list()

for lst in [rest_rate, bars_rate, night_rate, act_rate, fit_rate, shop_rate, arts_rate]: 
    averages.append(stat.mean(lst))
    minimums.append(min(lst))
    q1s.append(np.percentile(lst, 25))
    medians.append(np.percentile(lst, 50))
    q3s.append(np.percentile(lst, 75))
    maximums.append(max(lst))

rows = zip(categories, averages, minimums, q1s, medians, q3s, maximums)

with open('calculations.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Businesss Category','Average Rating', 'Minimum', 'Q1', 'Median', 'Q3', 'Maximum'])
    for row in rows:
        w.writerow(row)
f.close()

# Visualizations 
#Bar chart for average rating for each business category 
trace0 = go.Bar(
    x=['Restaurants', 'Bars',
          'Nightlife', 'Active', 
          'Fitness', 'Shopping', 'Arts'],
    y=[stat.mean(rest_rate), stat.mean(bars_rate), stat.mean(night_rate), stat.mean(act_rate), stat.mean(fit_rate), stat.mean(shop_rate), stat.mean(arts_rate)],
    marker=dict(
        color=['#A6C0FE', '#B8B1E2', '#C7A5CA', '#DA95AD', '#F28389', '#FCB9B4', '#FED7BE']),
)

data = [trace0]
layout = go.Layout(
    title='Average Rating for Each Business Category',
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Business Category') 
    ),
    yaxis = go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Average Rating')
    )
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig)

# Box plots of distribution of ratings for each business category 
y_data = [rest_rate, bars_rate, night_rate, act_rate, fit_rate, shop_rate, arts_rate]

colors = ['#A6C0FE', '#B8B1E2', '#C7A5CA', '#DA95AD', '#F28389', '#FCB9B4', '#FED7BE']

traces = []

for xd, yd, colors in zip(x_data, y_data, colors):
        traces.append(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=colors,
            marker=dict(
                size=2,
                color=colors
            ),
            line=dict(width=1),
        ))

layout = go.Layout(
    title='Distribution of Ratings for Categories of Businesses in Ann Arbor',
    yaxis=dict(
        autorange=True,
        showgrid=True,
        zeroline=True,
        dtick=1,
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=False
)

fig = go.Figure(data=traces, layout=layout)
py.plot(fig)

# Scatterplot on mapbox
mapbox_access_token = 'pk.eyJ1IjoiamV6emhhbmciLCJhIjoiY2p1bTZ5NDN1MmVtcTQ0cDMybjdpanF3YSJ9.zoUGoOCBJj53MyeT5gqAEQ'

data = [
    go.Scattermapbox(
        name = 'Restaurants',
        lat = rest_lat,
        lon = rest_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color = '#A6C0FE'
        ),
        text= rest_name,
    ),
    go.Scattermapbox(
        name = 'Bars',
        lat = bars_lat,
        lon = bars_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color = '#B8B1E2'
        ),
        text= bars_name,
    ), 
    go.Scattermapbox(
        name = 'Nightlife',
        lat = night_lat,
        lon = night_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color = '#C7A5CA'
        ),
        text= night_name,
    ), 
    go.Scattermapbox(
        name = 'Active',
        lat = act_lat,
        lon = act_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color = '#DA95AD'
        ),
        text= act_name,
    ),
    go.Scattermapbox(
        name = 'Fitness',
        lat = fit_lat,
        lon = fit_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color = '#F28389'
        ),
        text= fit_name,
    ), 
    go.Scattermapbox(
        name = 'Shopping',
        lat = shop_lat,
        lon = shop_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color = '#FCB9B4'
        ),
        text= shop_name,
    ),
    go.Scattermapbox(
        name = 'Arts',
        lat = arts_lat,
        lon = arts_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color = '#FED7BE'
        ),
        text= arts_name,
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=42.267571,
            lon=-83.7409894
        ),
        pitch=0,
        zoom=10
    ),
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig)

conn.close()
