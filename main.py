import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

import urllib.request, urllib.parse, urllib.error
import unittest
import sqlite3
import requests
import json
import re
import csv

import matplotlib
import matplotlib.pyplot as plt
#import plotly.plotly as py
#from plotly.graph_objs import *
#import plotly.graph_objs as go




def get_avg_height():
    #print("HELLO")
    total = 0
    num = 0
    cur.execute('SELECT height FROM Pokemon')
    for item in cur:
        #print(item[0])
        total += int(item[0])
        num += 1
    return(total/num)
def get_avg_weight():
    #print("Hello")
    total = 0  
    num = 0
    cur.execute('SELECT weight FROM Pokemon')
    for item in cur:
        total += int(item[0])
        num += 1
    return(total/num)

def get_height_graph():
    height = {}
    cur.execute('SELECT height, type FROM Pokemon')
    for item in cur:
        #print(item)
        height[item[-1]] = height.get(item[-1], 0) + item[0]
    #print(avg_height)
    plt.bar(height.keys(), height.values(), color=['cyan', 'pink', 'magenta', 'lavender', 'gray'], edgecolor = "purple")
    plt.ylabel('In Decimetres')
    plt.xlabel('Types of the Pokemon')
    plt.title("Height of Pokemon vs. Types of Pokemon")
    plt.show()


def get_weight_graph():
    weight = {}
    cur.execute('SELECT weight, type FROM Pokemon')
    for item in cur:
        #print(item)
        weight[item[-1]] = weight.get(item[-1], 0) + item[0]
    #print(avg_weight)
    plt.bar(weight.keys(), weight.values(), color=['black', 'red', 'green', 'blue', 'cyan'], edgecolor = "gray")
    plt.ylabel('In Hectograms')
    plt.xlabel('Types of the Pokemon')
    plt.title("Weight of Pokemon vs. Types of Pokemon")
    plt.show()

def plotly_double():

    #py.sign_in('username', 'api_key')
    cur.execute('SELECT type FROM Pokemon')
    x = []
    for item in cur:
        if item[0] not in x:
            x.append(str(item[0]))
    #print(x)

    y = []
    height = {}
    height_w_num = {}
    cur.execute('SELECT height, type FROM Pokemon')
    for item in cur:
        #print(item)
        height[item[-1]] = height.get(item[-1], 0) + item[0]
        height_w_num[item[-1]] = height_w_num.get(item[-1], 0) + 1
    #print(height)
    #print(height_w_num)
    for item in height:
        for val in height_w_num:
            if item == val:
                #print(item)
                #print(height[item]/height_w_num[val])
                y.append(height[item]/height_w_num[val])
    #print(y)

    y2 = []
    weight = {}
    weight_w_num = {}
    cur.execute('SELECT weight, type FROM Pokemon')
    for item in cur:
        #print(item)
        weight[item[-1]] = weight.get(item[-1], 0) + item[0]
        weight_w_num[item[-1]] = height_w_num.get(item[-1], 0) + 1
    #print(weight)
    #print(weight_w_num)
    for item in weight:
        for val in weight_w_num:
            if item == val:
                #print(item)
                #print(height[item]/height_w_num[val])
                y2.append(weight[item]/weight_w_num[val])
    #print(y2)

    trace1 = {
    "x": x, 
    "y": y, 
    "marker": {
        "color": "rgb(44, 160, 44)", 
        "line": {"color": "rgb(44, 160, 44)"}
    }, 
    "name": "Average Height of Pokemon in Decimetres", 
    "opacity": 0.5, 
    "type": "bar", 
    "uid": "a76d02"
    }
    trace2 = {
    "x": x, 
    "y": y2, 
    "marker": {
        "color": "rgb(31, 119, 180)", 
        "line": {"color": "rgb(31, 119, 180)"}
    }, 
    "name": "Average Weight of Pokemon in Hectograms", 
    "opacity": 0.5, 
    "type": "bar", 
    "uid": "f37dc3", 
    "yaxis": "y2"
    }
    data = Data([trace1, trace2])
    layout = {
    "autosize": True, 
    "bargap": 0.31, 
    "height": 761, 
    "title": "Double Bar Chart of Average Height and Weight vs. Pokemon Type (left axis-Decimeters(height), right axis-Hectograms(weight))", 
    "width": 1345, 
    "xaxis": {
        "autorange": False, 
        "range": [-1.1864981382869304, 3.0283446334038695], 
        "type": "category"
    }, 
    "yaxis": {
        "autorange": False, 
        "range": [-5.895566463655328, 36.992307353549236], 
        "type": "linear"
    }, 
    "yaxis2": {
        "anchor": "x", 
        "autorange": False, 
        "exponentformat": "SI", 
        "overlaying": "y", 
        "range": [-4.675794091864562, 29.338726521780416], 
        "side": "right", 
        "type": "linear"
    }
    }
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig)


conn = sqlite3.connect('pokemon.sqlite')
cur = conn.cursor()
#cur.execute('''
#            CREATE TABLE IF NOT EXISTS Pokemon
#            (id INTEGER, name STRING, height INTEGER, weight INTEGER)''')

#cur.execute('DROP TABLE IF EXISTS Pokemon')
cur.execute('''CREATE TABLE IF NOT EXISTS Pokemon (id INTEGER PRIMARY KEY, name UNIQUE, height INTEGER, weight INTEGER, type STRING, moves STRING)''')

#put in range(1,100)
print("Welcome to the Pokemon API! To create a database of all the data we will be looking for each pokemon's id, name, height, weight, type, and moves. ")
print("*******************************")
#num_orig = input("Please input a number from 1 to 800 to set the range of how many pokemon you want to pull out: ")
#num_end = input("Plese input a number after the one you chose above to set the end of the range: ")
tuples = [(1, 21), (21, 41), (41, 61), (61, 81), (81, 101), (101, 121), (121, 141), (141, 161), (161, 181), (181, 201)]

for tup in tuples:
    for num in range(tup[0], tup[1]):
        string = 'http://pokeapi.co/api/v2/pokemon/'
        #print(num)
        #print(type(num))
        link = string + str(num) + '/'
        response = requests.get(link)
    #print(response.status_code)
    #print(response.content)
    #data = response.json()

        data = response.json()
        p_id = data["id"]
        #print(p_id)
        name = data["name"]
        #print(name)
        height = data["height"]
        #print(height)
        weight = data["weight"]
        #print(weight)
        types = data["types"][0]["type"]["name"]
        #print(types)
        moves = data["moves"][0]["move"]["name"]
        #print(moves)

        cur.execute('''INSERT OR IGNORE INTO Pokemon (id, name, height, weight, type, moves) VALUES (?, ?, ?, ?, ?, ?)''', (p_id, name, height, weight, types, moves))
    conn.commit()



print("*******************************")
#calculations - need to write it out to a json
print("Now we will be calculating a few things!")
calc_input = input("Please input which option you would like to output (1 for average height, 2 for average weight): ")

#data = str('The average height is: ' + str(get_avg_height()) + 'AND The average weight is: ' + str(get_avg_weight()))
if calc_input == '1':
    print("The average height for all the pokemon we pulled out is: " + str(get_avg_height()))
elif calc_input == '2':
    print("The average weight for all the pokemon we pulled out is: " + str(get_avg_weight()))

#actual json writing!!!
cur.execute('SELECT type FROM Pokemon')
cat = []
for item in cur:
    if item[0] not in cat:
        cat.append(str(item[0]))
#print(cat)

hei = []
height = {}
height_w_num = {}
cur.execute('SELECT height, type FROM Pokemon')
for item in cur:
        #print(item)
    height[item[-1]] = height.get(item[-1], 0) + item[0]
    height_w_num[item[-1]] = height_w_num.get(item[-1], 0) + 1
    #print(height)
    #print(height_w_num)
for item in height:
    for val in height_w_num:
        if item == val:
                #print(item)
                #print(height[item]/height_w_num[val])
            hei.append(height[item]/height_w_num[val])
#print(hei)


wei = []
weight = {}
weight_w_num = {}
cur.execute('SELECT weight, type FROM Pokemon')
for item in cur:
    weight[item[-1]] = weight.get(item[-1], 0) + item[0]
    weight_w_num[item[-1]] = height_w_num.get(item[-1], 0) + 1
for item in weight:
    for val in weight_w_num:
        if item == val:
            wei.append(weight[item]/weight_w_num[val])
#print(wei)

rows = zip(cat, hei, wei)

with open('pokemon_calc.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Pokemon Type', 'Average Height', 'Average Weight'])
    for row in rows:
        w.writerow(row)
f.close()


#visualizations
print("*******************************")
print("Now we will be making a visualizations!")
graph_input = input("Please input which option you would like to output (1 for a bar chart of Height of Pokemon vs. Types of Pokemon, 2 for a bar chart of Weight of Pokemon vs. Types of Pokemon, 3 for a Double Bar chart of the average Height and Weight vs. Pokemon Type): ")
if graph_input == '1':
    get_height_graph()

elif graph_input == '2':
    get_weight_graph()

elif graph_input == '3':
    plotly_double()


print("*******************************")
print("CONGRATS THE PROGRAM IS DONE RUNNING I HOPE YOU HAD FUN!!")

cur.close()    