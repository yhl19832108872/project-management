import os
import dash_bio
from dash import Dash
import dash_html_components as html
from werkzeug.wsgi import DispatcherMiddleware
from app import app

path = os.path.join('/uploads', 'fastas.txt')
data = open(path, 'r').read()
print(data)
style = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
dash_app = Dash(__name__, server=app, url_base_pathname='/visual_fa/', external_stylesheets=style)
dash_app.layout = html.Div([
dash_bio.AlignmentChart(id="my_alignemnt", data=data),
    html.Div(id='alignment-Viewer-output')])
print(data)
#application = DispatcherMiddleware(app, {'/dash': dash_app.server})
