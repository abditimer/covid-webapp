from covidwebapp import app
from flask import render_template
from data_scripts import download_data, clean_data, return_figs
import plotly.graph_objs as go
import plotly, json
import pandas as pd

all_figures = return_figs.CovidFigures()
ids = all_figures.ids
ids_p2 = all_figures.ids_p2
print(ids)
print(ids_p2)

figuresJSON = json.dumps(all_figures.figures, cls=plotly.utils.PlotlyJSONEncoder)
figuresJSON_p2 = json.dumps(all_figures.figures_p2, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', ids=ids, figuresJSON=figuresJSON)


@app.route('/nhs-trusts')
def sankey():
    return render_template('sankey.html', ids_p2=ids_p2, figuresJSON_p2=figuresJSON_p2)