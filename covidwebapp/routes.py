from covidwebapp import app
from flask import render_template
from data_scripts import download_data, clean_data, return_figs
import plotly.graph_objs as go
import plotly, json
import pandas as pd
import logging

all_figures = return_figs.CovidFigures()

home_page_figure = all_figures.home_page_figure
data_page_figures = all_figures.data_page_figures

ids = all_figures.ids
ids_p2 = all_figures.ids_p2
home_page_names = all_figures.home_page_names
data_page_names = all_figures.data_page_names

# chart for home page
figuresJSON_home = json.dumps(home_page_figure, cls=plotly.utils.PlotlyJSONEncoder)
# charts for data page
figuresJSON_data = json.dumps(data_page_figures, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', ids=home_page_names, figuresJSON_home=figuresJSON_home)

@app.route('/data')
def data_page():
    return render_template('data.html', ids_2=data_page_names, figuresJSON_data=figuresJSON_data)

@app.route('/about')
def about():
    return render_template('about.html')