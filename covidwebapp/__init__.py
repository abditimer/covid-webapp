from flask import Flask
# __name__: (predefined variable) the name of the module in which it is used
app = Flask(__name__)

from covidwebapp import routes