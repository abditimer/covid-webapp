from covidwebapp import app
from flask import render_template
from data_scripts import download_data, clean_data, return_figs
import plotly.graph_objs as go
import plotly, json
import pandas as pd

all_figures = return_figs.CovidFigures()

deaths_by_region_chart = all_figures.deaths_by_region_chart
ids = all_figures.ids
ids_p2 = all_figures.ids_p2
#home_page_charts = home
print(ids)
print(ids_p2)

figuresJSON = json.dumps(all_figures.figures, cls=plotly.utils.PlotlyJSONEncoder)
figuresJSON_p2 = json.dumps(all_figures.figures_p2, cls=plotly.utils.PlotlyJSONEncoder)
figures_home = json.dumps(deaths_by_region_chart, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
@app.route('/home')
def index():
    ##return render_template('home.html', ids=ids, figuresJSON=figuresJSON)
    return render_template('home.html', ids=ids, figuresJSON=figures_home)


@app.route('/nhs-trusts')
def sankey():
    return render_template('sankey.html', ids_p2=ids_p2, figuresJSON_p2=figuresJSON_p2)